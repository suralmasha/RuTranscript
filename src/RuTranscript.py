from os.path import join, dirname, abspath
from tqdm import tqdm

import spacy
import epitran
from openpyxl import load_workbook
from nltk.stem.snowball import SnowballStemmer
from tps import find, download
from tps import modules as md

from ru_transcript.src.utils.main_tools import get_punctuation_dict, text_norm_tok, Stresses, find_clitics, \
    extract_phrasal_words, apply_differences
from ru_transcript.src.utils.sounds import epi_starterpack, allophones
from ru_transcript.src.utils.allophones_tools import nasal_m_n, silent_r, voiced_ts, shch, long_ge, fix_jotised,\
    assimilative_palatalization, long_consonants, vowels, labia_velar

snowball = SnowballStemmer('russian')
nlp = spacy.load('ru_core_news_sm', disable=["tagger", "morphologizer", "attribute_ruler"])

ROOT_DIR = dirname(abspath(__file__))
wb = load_workbook(join(ROOT_DIR, 'data/irregular_exceptions.xlsx'))
sheet = wb.active
irregular_exceptions = {sheet[f'A{i}'].value: sheet[f'B{i}'].value for i in range(2, sheet.max_row + 1)}
irregular_exceptions_stems = {snowball.stem(ex): pron for ex, pron in irregular_exceptions.items()}

epi = epitran.Epitran('rus-Cyrl')
second_silent = 'стн стл здн рдн нтск ндск лвств'.split()
first_silent = 'лнц дц вств'.split()
hissing_rd = {'сш': 'шш', 'зш': 'шш', 'сж': 'жж', 'сч': 'щ'}
non_ipa_symbols = {'t͡ɕʲ': 't͡ɕ', 'ʂʲː': 'ʂ', 'ɕːʲ': 'ɕː'}

try:
    yo_dict = find("yo.dict", raise_exception=True)
except FileNotFoundError:
    yo_dict = download("yo.dict")

try:
    e_dict = find("e.dict", raise_exception=True)
except FileNotFoundError:
    e_dict = download("e.dict")

e_replacer = md.Replacer([e_dict, "plane"])
yo_replacer = md.Replacer([yo_dict, "plane"])
stress = Stresses()


def remove_extra_accents(string):
    first_plus_index = string.find('+')
    return string[:first_plus_index + 1] + string[first_plus_index + 1:].replace('+', '')


class RuTranscript:
    def __init__(
            self,
            text: str,
            a_text: str = None,
            accent_place: str = 'after',
            save_spaces: bool = False,
            replacement_dict: dict = None
    ):
        text = ' '.join(['—' if word == '-' else word for word in text.replace('\n', ' ').lower().split()])
        a_text = ' '.join(['—' if word == '-' else word for word in a_text.replace('\n', ' ').lower().split()]) \
            if a_text is not None else text

        if replacement_dict is not None:
            user_replacer = md.Replacer([replacement_dict, "plane"])
            text = user_replacer(text)
            a_text = user_replacer(a_text)

        self._save_spaces = save_spaces
        self._tokens = text_norm_tok(text)
        self._a_tokens = text_norm_tok(a_text)
        self._sections_len = len(self._tokens)
        self._accent_place = accent_place
        self._pause_dict = get_punctuation_dict(text)

        self._phrasal_words_indexes = []
        self._transliterated_tokens = [[]] * self._sections_len
        self._phonemes_list = []
        self._letters_list = []
        self._phrasal_words = [[]] * self._sections_len
        self.allophones = [[]] * self._sections_len
        self.transcription = []
        self.phonemes = []
        self.accented_text = [[]] * self._sections_len

    def transcribe(self):
        # ---- TPS ----
        for section_num in tqdm(range(self._sections_len)):
            default_section = self._tokens[section_num]
            self._tokens[section_num] = [e_replacer(token).replace('+', '') for token in self._tokens[section_num]]
            self._tokens[section_num] = [yo_replacer(token).replace('+', '') for token in self._tokens[section_num]]

            if self._tokens[section_num] != default_section:
                self._a_tokens[section_num] = [
                    apply_differences([default_section[i], self._tokens[section_num][i]])
                    for i in range(len(default_section))
                ]

            # ---- Accenting ----
            self._a_tokens[section_num] = [
                stress.replace_accent(token) if ('+' in token) and (self._accent_place == 'before')  # need to replace
                else stress.place_accent(token) if ('+' not in token)  # use StressRNN
                else token
                for token in self._a_tokens[section_num]]

            self.accented_text[section_num] = self._a_tokens[section_num]

            # ---- Removing dashes ----
            section = self._tokens[section_num]
            a_section = self._a_tokens[section_num]
            self._tokens[section_num] = [token.replace('-', '') for token in section]
            self._a_tokens[section_num] = [token.replace('-', '') if token.count('+') == 1
                                           else remove_extra_accents(token).replace('-', '')
                                           for token in a_section]

            # ---- Phrasal words extraction ----
            dep = stress.make_dependency_tree(' '.join(self._tokens[section_num]))
            self._phrasal_words_indexes.append(find_clitics(dep, self._tokens[section_num]))

            # ---- LPC-1. Irregular exceptions ----
            for i, token in enumerate(self._tokens[section_num]):
                stem = snowball.stem(token)
                if stem in irregular_exceptions_stems:
                    try:
                        new_token = irregular_exceptions[token]
                    except KeyError:
                        ending = token[len(stem):]
                        dif = - (len(token) - len(stem))
                        new_token = irregular_exceptions_stems[stem][:dif] + ending

                    self._tokens[section_num][i] = new_token
                    accent_index = self._a_tokens[section_num][i].index('+')
                    self._a_tokens[section_num][i] = new_token[:accent_index] + '+' + new_token[accent_index:]

            # ---- LPC-2. Regular exceptions ----
            for i, token in enumerate(self._a_tokens[section_num]):
                # adjective endings 'ого его'
                if token != 'ого+' and (token.replace('+', '').startswith('какого')
                                        or token.replace('+', '').endswith('ого')
                                        or token.replace('+', '').endswith('его')):
                    accent_index = token.index('+')
                    token = token.replace('+', '').replace('ого', 'ово').replace('его', 'ево')
                    self._a_tokens[section_num][i] = token[:accent_index] + '+' + token[accent_index:]

                # 'что' --> 'што'
                if 'что' in self._a_tokens[section_num][i]:
                    self._a_tokens[section_num][i] = token.replace('что', 'што')

                # verb endings 'тся ться'
                if token not in {'заботься', 'отметься'}:
                    if token[-3:] == 'тся':
                        self._a_tokens[section_num][i] = token[:-3] + 'ца'
                    elif token[-4:] == 'ться':
                        self._a_tokens[section_num][i] = token[:-4] + 'ца'

                # noun endings 'ия ие ию'
                if (token[-2:] in {'ия', 'ие', 'ию'}) and (token[-3] not in {'ц', 'щ'}):
                    if token[-3] not in {'ж', 'ш'}:
                        self._a_tokens[section_num][i] = token[:-2] + 'ь' + token[-1]
                    else:
                        self._a_tokens[section_num][i] = token[:-2] + 'й' + token[-1]

                # unpronounceable consonants
                for sub in first_silent + second_silent:
                    if sub in token:
                        new_sub = sub.translate(str.maketrans('', '', 'ьъ'))
                        self._a_tokens[section_num][i] = token.translate(str.maketrans(sub, new_sub))

                # combinations with hissing consonants
                stem = snowball.stem(token)
                if ('зч' in token or 'тч' in token or 'дч' in token) and (stem[-3:] == 'чик' or stem[-3:] == 'чиц'):
                    self._a_tokens[section_num][i] = token.replace('зч', 'щ').replace('тч', 'ч').replace('дч', 'ч')
                for key, value in hissing_rd.items():
                    if key in token:
                        self._a_tokens[section_num][i] = token.replace(key, value)

            # ---- LPC-3. Transliteration ----
            self._transliterated_tokens[section_num] = [epi.transliterate(token).replace('6', '').replace('4', '')
                                                        for token in self._a_tokens[section_num]]
            for i, token in enumerate(self._transliterated_tokens[section_num]):
                for key, value in non_ipa_symbols.items():
                    if key in token:
                        token = token.replace(key, value)
                        self._transliterated_tokens[section_num][i] = token

            # ---- LPC-4. Common rules ----
            # fricative g
            for i, token in enumerate(self._transliterated_tokens[section_num]):
                try:
                    next_token = self._transliterated_tokens[section_num][i + 1]
                except IndexError:
                    next_token = ' '

                token_let = self._tokens[section_num][i]
                nlp_token = nlp(token_let)[0]
                lemma = nlp_token.lemma_

                if lemma in {'ага', 'ого', 'угу', 'господь', 'господи', 'бог'}:
                    self._transliterated_tokens[section_num][i] = token.replace('ɡ', 'γ', 1)
                elif token_let in {'ах', 'эх', 'ох', 'ух'}:
                    next_token_allophone = allophones.get(next_token[0], {})
                    if next_token_allophone.get('voice', '') == 'voiced':
                        self._transliterated_tokens[section_num][i] = token.replace('x', 'γ', 1)

            # ---- Join phonemes ----
            section_phonemes_list = []
            joined_tokens = '_'.join(self._transliterated_tokens[section_num])
            i = 0
            default_len = len(joined_tokens)
            while i < default_len:
                if joined_tokens[i] not in ['+', '-']:
                    n = 4
                    if i != default_len - 1:
                        while (joined_tokens[i:i + n] not in epi_starterpack + ['_', '|', '||', 'γ']) and (n > 0):
                            n -= 1
                        section_phonemes_list.append(joined_tokens[i:i + n])
                    elif joined_tokens[i] in epi_starterpack + ['||', 'γ']:
                        section_phonemes_list.append(joined_tokens[i])
                    i += n
                else:
                    section_phonemes_list.append(joined_tokens[i])
                    i += 1

            section_phonemes_list = [x for x in section_phonemes_list if x not in ['', 'ʲ']]
            self._phonemes_list.append(section_phonemes_list)

            for allophone_index in range(len(self._phonemes_list[section_num]) - 1):
                allophone = self._phonemes_list[section_num][allophone_index]
                next_allophone = self._phonemes_list[section_num][allophone_index + 1]
                if (allophone == 't͡s' and next_allophone == 's') or (allophone == 'd͡ʒ' and next_allophone == 'ʒ'):
                    del self._phonemes_list[section_num][allophone_index + 1]

            # ---- Join letters ----
            self._letters_list.append(list('_'.join(self._a_tokens[section_num])))

            # ---- Continue LPC-4. Common rules ----
            self._phonemes_list[section_num] = fix_jotised(self._phonemes_list[section_num],
                                                           self._letters_list[section_num])
            self._phonemes_list[section_num] = shch(self._phonemes_list[section_num])
            self._phonemes_list[section_num] = long_ge(self._phonemes_list[section_num])
            self._phonemes_list[section_num] = assimilative_palatalization(self._tokens[section_num],
                                                                           self._phonemes_list[section_num])
            self._phonemes_list[section_num] = long_consonants(self._phonemes_list[section_num])

            # ---- Allophones ----
            self.allophones[section_num] = nasal_m_n(self._phonemes_list[section_num])
            self.allophones[section_num] = silent_r(self.allophones[section_num])
            self.allophones[section_num] = voiced_ts(self.allophones[section_num])

            # ---- Extract phrasal words ----
            self._phrasal_words[section_num] = extract_phrasal_words(self.allophones[section_num],
                                                                     self._phrasal_words_indexes[section_num])
            # ---- Prestressed syllable ----
            section = self._phrasal_words[section_num][:]
            n = 0
            for symb_i, symb in enumerate(section):
                if symb == '+':
                    preavi = [phon_i for phon_i, phon in enumerate(section[:symb_i - 1]) if
                              allophones[phon]['phon'] == 'V' and '_' not in section[phon_i + n:symb_i]]
                    if preavi:
                        self._phrasal_words[section_num].insert(preavi[-1] + n + 1, '-')
                        n += 1

            #  ---- Vowels ----
            self.allophones[section_num] = vowels(self._phrasal_words[section_num])

            # ---- Labialization and velarization ----
            self.allophones[section_num] = labia_velar(self.allophones[section_num])

        # ---- Result transcription (with pauses) ----
        allophones_working = self.allophones.copy()
        for i, key in enumerate(self._pause_dict):
            allophones_working.insert(i + key, self._pause_dict[key])

        self.transcription = ' '.join(
            [' '.join(
                [x for x in section if x not in ['+', '-', '_']])
             if section != '||'
             else section
             for section in allophones_working]
        )

        # ---- Result accented text ----
        self.accented_text = ' '.join([' '.join(section) for section in self.accented_text])

        # ---- Result allophones ----
        escape_symbols = ['+', '-', '_'] if not self._save_spaces else ['+', '-']

        allophones_joined = []
        for section in self.allophones:
            allophones_joined.extend(section)
        self.allophones = [x for x in allophones_joined if x not in escape_symbols]

        # ---- Result phonemes ----
        phonemes_joined = []
        for section in self._phonemes_list:
            phonemes_joined.extend(section)
        self.phonemes = [x for x in phonemes_joined if x not in escape_symbols]
