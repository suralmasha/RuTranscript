import pandas as pd

import spacy
import epitran
from nltk.stem.snowball import SnowballStemmer

from .main_tools import TextNormalizationTokenization, Stresses, find_clitics, extract_phrasal_words
from .sounds import epi_starterpack, allophones
from .allophones_tools import nasal_m_n, silent_r, voiced_ts, shch, long_ge, fix_jotised, assimilative_palatalization, \
    long_consonants, vowels, labia_velar

snowball = SnowballStemmer('russian')
nlp = spacy.load('ru_core_news_sm')

irregular_exceptions_df = pd.read_excel(r'C:\Users\Саша\PycharmProjects\RuTranscript\RuTranscript\src\irregular_exceptions.xlsx', engine='openpyxl', usecols=[0, 1])
irregular_exceptions = {row['original word']: row['pronunciation'] for _, row in irregular_exceptions_df.iterrows()}
irregular_exceptions_stems = dict(zip([snowball.stem(ex) for ex in irregular_exceptions],
                                      irregular_exceptions.values()))


class RuTranscript:
    def __init__(self, text, a_text=None, accent_place='after'):
        if a_text is not None:
            self.a_text = a_text
        else:
            self.a_text = text

        self.text = text
        self.accent_place = accent_place

        norm_tok = TextNormalizationTokenization(self.text, self.a_text)
        norm_tok.section_split()
        norm_tok.tokenize()
        norm_tok.my_num2text()

        self.sections_len = norm_tok.sections_len
        self.pause_dict = norm_tok.pause_dict
        self.a_tokens = norm_tok.a_tokens_normal
        self.tokens = norm_tok.tokens_normal
        self.phrasal_words_indexes = []
        self.transliterated_tokens = [[]] * self.sections_len
        self.phonemes_list = []
        self.letters_list = []
        self.phrasal_words = [[]] * self.sections_len
        self.allophones = [[]] * self.sections_len
        self.transcription = []

    def transcribe(self):
        second_silent = 'стн стл здн рдн нтск ндск лвств'.split()
        first_silent = 'лнц дц вств'.split()
        hissing_rd = {'сш': 'шш', 'зш': 'шш', 'сж': 'жж', 'сч': 'щ'}
        epi = epitran.Epitran('rus-Cyrl')
        non_ipa_symbols = {'t͡ɕʲ': 't͡ɕ', 'ʂʲː': 'ʂ', 'ɕːʲ': 'ɕː'}

        # ---- Accenting ----
        stress = Stresses()
        for section_num in range(self.sections_len):
            for token_i, token in enumerate(self.a_tokens[section_num]):
                if ('+' in token) and (self.accent_place == 'before'):  # need to replace
                    self.a_tokens[section_num][token_i] = stress.replace_accent(token)
                elif '+' not in token:  # use StressRNN
                    self.a_tokens[section_num][token_i] = stress.place_accent(token)

            # ---- Phrasal words extraction ----
            dep = stress.make_dependency_tree(' '.join(self.tokens[section_num]))
            self.phrasal_words_indexes.append(find_clitics(dep, self.tokens[section_num]))

            # ---- LPC-1. Irregular exceptions ----
            for i, token in enumerate(self.tokens[section_num]):
                stem = snowball.stem(token)
                if stem in irregular_exceptions_stems:
                    try:
                        new_token = irregular_exceptions[token]
                    except KeyError:
                        ending = token[len(stem):]
                        dif = - (len(token) - len(stem))
                        new_token = irregular_exceptions_stems[stem][:dif] + ending

                    self.tokens[section_num][i] = new_token
                    accent_index = self.a_tokens[section_num][i].index('+')
                    new_token_split = list(new_token)
                    new_token_split.insert(accent_index, '+')
                    self.a_tokens[section_num][i] = ''.join(new_token_split)

            # ---- LPC-2. Regular exceptions ----
            for i, token in enumerate(self.a_tokens[section_num]):
                # adjective endings 'ого его'
                if token.replace('+', '')[-3:] in 'ого его'.split() and token != 'ого+':
                    accent_index = token.index('+')
                    token = token.replace('+', '')[:-2] + 'во'
                    self.a_tokens[section_num][i] = token[:accent_index] + '+' + token[accent_index:]

                # 'что' --> 'што'
                while 'что' in self.a_tokens[section_num][i]:
                    self.a_tokens[section_num][i] = token.replace('что', 'што')

                # verb endings 'тся ться'
                if token not in 'заботься отметься'.split():
                    if token[-3:] == 'тся':
                        self.a_tokens[section_num][i] = token[:-3] + 'ца'
                    elif token[-4:] == 'ться':
                        self.a_tokens[section_num][i] = token[:-4] + 'ца'

                # unpronounceable consonants
                for sub in second_silent:
                    if sub in token:
                        self.a_tokens[section_num][i] = token.replace(sub, sub.replace(sub[1], '', 1))

                for sub in first_silent:
                    if sub in token:
                        self.a_tokens[section_num][i] = token.replace(sub, sub.replace(sub[0], '', 1))

                # combinations with hissing consonants
                stem = snowball.stem(token)
                for key, value in hissing_rd.items():
                    if key in token:
                        self.a_tokens[section_num][i] = token.replace(key, value)

                if ('зч' in token) and (stem[-3:] == 'чик' or stem[-3:] == 'чиц'):
                    self.a_tokens[section_num][i] = token.replace('зч', 'щ')
                elif ('тч' in token) and (stem[-3:] == 'чик' or stem[-3:] == 'чиц'):
                    self.a_tokens[section_num][i] = token.replace('тч', 'ч')
                elif ('дч' in token) and (stem[-3:] == 'чик' or stem[-3:] == 'чиц'):
                    self.a_tokens[section_num][i] = token.replace('дч', 'ч')

            # ---- LPC-3. Transliteration ----
            self.transliterated_tokens[section_num] = self.a_tokens[section_num][:]

            for i, token in enumerate(self.a_tokens[section_num]):
                transliterated_token = epi.transliterate(token)
                for key, value in non_ipa_symbols.items():
                    if key in token:
                        transliterated_token = transliterated_token.replace(key, value)

                self.transliterated_tokens[section_num][i] = transliterated_token

            # ---- LPC-4. Common rules ----
            # fricative g
            for i, token in enumerate(self.transliterated_tokens[section_num]):
                try:
                    next_token = self.transliterated_tokens[section_num][i + 1]
                except IndexError:
                    next_token = ''

                token_let = self.tokens[section_num][i]
                nlp_token = nlp(token_let)[0]
                lemma = nlp_token.lemma_
                if lemma in 'ага ого угу господь господи бог'.split(' '):
                    self.transliterated_tokens[section_num][i] = token.replace('ɡ', 'γ', 1)
                elif (token_let in 'ах эх ох ух'.split(' ')) \
                        and (allophones[next_token[0]]['phon'] == 'C') \
                        and (allophones[next_token[0]]['voice'] == 'voiced'):
                    self.transliterated_tokens[section_num][i] = token.replace('x', 'γ', 1)

            # ---- Join phonemes ----
            section_phonemes_list = []
            transliterated_tokens_joined = '_'.join(self.transliterated_tokens[section_num])
            for i, symb in enumerate(transliterated_tokens_joined):
                if symb not in ['+', '-']:
                    n = 4
                    if i != len(transliterated_tokens_joined) - 1:
                        while (transliterated_tokens_joined[i:i + n] not in epi_starterpack + ['_', '|', '||', 'γ']) \
                                and (n > 0):
                            n -= 1
                    section_phonemes_list.append(transliterated_tokens_joined[i:i + n])
                else:
                    section_phonemes_list.append(symb)

            section_phonemes_list[:] = [x for x in section_phonemes_list if x not in ['', 'ʲ']]
            self.phonemes_list.append(section_phonemes_list)

            for allophone_index, allophone in enumerate(self.phonemes_list[section_num]):
                if ((allophone == 't͡s') and self.phonemes_list[section_num][allophone_index + 1] == 's') \
                        or ((allophone == 'd͡ʒ') and self.phonemes_list[section_num][allophone_index + 1] == 'ʒ'):
                    del self.phonemes_list[section_num][allophone_index + 1]

            # ---- Join letters ----
            self.letters_list.append(list('_'.join(self.a_tokens[section_num])))

            # ---- Continue LPC-4. Common rules ----

            self.phonemes_list[section_num] = fix_jotised(self.phonemes_list[section_num],
                                                          self.letters_list[section_num])
            self.phonemes_list[section_num] = shch(self.phonemes_list[section_num])
            self.phonemes_list[section_num] = long_ge(self.phonemes_list[section_num])
            self.phonemes_list[section_num] = assimilative_palatalization(self.tokens[section_num],
                                                                          self.phonemes_list[section_num])
            self.phonemes_list[section_num] = long_consonants(self.phonemes_list[section_num])

            # ---- Allophones ----
            self.allophones[section_num] = nasal_m_n(self.phonemes_list[section_num])
            self.allophones[section_num] = silent_r(self.allophones[section_num])
            self.allophones[section_num] = voiced_ts(self.allophones[section_num])

            # ---- Extract phrasal words ----
            self.phrasal_words[section_num] = extract_phrasal_words(self.allophones[section_num],
                                                                    self.phrasal_words_indexes[section_num])
            # ---- Prestressed syllable ----
            section = self.phrasal_words[section_num][:]
            n = 0
            for symb_i, symb in enumerate(section):
                if symb == '+':
                    preavi = []  # pre accented vowel indexes
                    for phon_i, phon in enumerate(section[:symb_i - 1]):
                        if (allophones[phon]['phon'] == 'V') and ('_' not in section[phon_i + n:symb_i]):
                            preavi.append(phon_i)
                    if preavi:
                        self.phrasal_words[section_num].insert(preavi[-1] + n + 1, '-')
                        n += 1

            #  ---- Vowels ----
            self.allophones[section_num] = vowels(self.phrasal_words[section_num])

            # ---- Labialization and velarization ----
            self.allophones[section_num] = labia_velar(self.allophones[section_num])

        # ---- Result transcription (with pauses) ----
        if len(self.pause_dict) == self.sections_len:
            for section_num in range(self.sections_len):
                self.transcription.extend(self.allophones[section_num] + [self.pause_dict[section_num]])

        elif len(self.pause_dict) == self.sections_len - 1:  # no punctuation in the end
            for section_num in range(self.sections_len - 1):
                self.transcription.extend(self.allophones[section_num] + [self.pause_dict[section_num]])
            self.transcription.extend(self.allophones[-1])

        elif not self.pause_dict:  # no punctuation at all
            self.transcription = self.allophones[0]

        self.transcription = ' '.join([x for x in self.transcription if x not in ['+', '-', '_']])

        # ---- Result allophones ----
        allophones_joined = []
        for section in self.allophones:
            allophones_joined.extend(section)

        self.allophones = [x for x in allophones_joined if x not in ['+', '-', '_']]
