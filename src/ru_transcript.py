import nltk
import re
import csv
import spacy
from nltk import Tree
from stressrnn import StressRNN
import epitran
from RuTranscript.src.sounds_m import Sounds

with open('RuTranscript/alphabet.txt', 'r') as f:
    alphabet = f.read()

with open('RuTranscript/sorted_allophones.txt', 'r') as f:
    sorted_allophones = f.read()

with open('RuTranscript/paired_consonants.txt', 'r') as f:
    paired_consonants = f.read()

nltk.download('averaged_perceptron_tagger_ru')
nlp = spacy.load('ru_core_news_sm')
stress_rnn = StressRNN()
epi = epitran.Epitran('rus-Cyrl')

sor_list = []
for x in sorted_allophones.split('\n'):
    sor_list.append(x.split(', '))

sorted_phon = {}
for x in sor_list:
    for y in x:
        if '=' in y:
            index = y.index('=')
            sorted_phon[y[:index - 1]] = [y[index + 2:]] + x[1:]

paired_c_new = paired_consonants.split(', ')
paired = {}
for i, x in enumerate(paired_c_new):
    if '(' in x:
        paired[x[1:]] = paired_c_new[i + 1][:-1]

starterpack = 'a b bʲ v vʲ ɡ ɡʲ d dʲ e ʒ z zʲ i j k kʲ l lʲ m mʲ n nʲ o p pʲ r rʲ s sʲ t tʲ u f fʲ x xʲ t͡s t͡ɕ ʂ ɕː ɨ d͡ʒ'.split(
    ' ')  # epi phonemes

rus_v = 'а е ё и о у э ю я ы'.split(' ')  # russian vowels


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node, [to_nltk_tree(child) for child in node.children])
    else:
        return node


def make_dependency_tree(text):
    doc = nlp(text)
    for sent in doc.sents:
        dependency_tree = to_nltk_tree(sent.root)
        return dependency_tree


class RuTranscript:
    def __init__(self, data):
        self.tokens = data.tokens
        self.accented_tokens = data.accented_tokens
        self.tokens_len = data.tokens_len
        self.stems = data.stems
        self.lemmas = data.lemmas
        self.tags = data.tags
        self.phrasal_words = []
        self.transcription = []
        self.word = ''
        self.orig_word = ''
        self.translited_word = []
        self.lpc_unr_ex = {'кафе': 'кафэ', 'шоссе': 'шоссэ', 'сегодня': 'севодня',
                           'бог': 'бох', 'отель': 'отэль', 'купе': 'купэ',
                           'россия': 'росия', 'одиннадцать': 'одинацать',
                           'пятьдесят': 'пядесят', 'коммуналка': 'комуналка',
                           'грипп': 'грип'}

    def _accent_placing(self, word):
        new_word = stress_rnn.put_stress(word, stress_symbol='+', accuracy_threshold=0.75, replace_similar_symbols=True)
        return new_word

    def _accent_replacing(self, sova=False):
        new_text = []
        for i, word in enumerate(self.accented_tokens):
            new_word = ''
            if '+' in word:
                if sova:
                    new_word = word[:word.index('+')] + word[word.index('+') + 1: word.index('+') + 2] + '+' \
                               + word[word.index('+') + 2:]
                else:
                    new_word = word
            else:
                new_word = self._accent_placing(word)

            if '+' in new_word and len(new_word) > 2:
                preavi = []  # pre acented vowel indexes
                for i, phon in enumerate(new_word[:new_word.index('+') - 1]):
                    if phon in rus_v:
                        preavi.append(i)
                if preavi:
                    new_word = new_word[:preavi[-1] + 1] + '-' + new_word[preavi[-1] + 1:]

            new_text += [new_word]
            self.accented_tokens = new_text

    def _clitics(self, dep, n=0):
        functors_pos = {'CCONJ', 'PART', 'ADP'}
        adverb_adp = ['после', 'кругом', 'мимо', 'около', 'вокруг', 'напротив', 'поперёк']
        if not self.phrasal_words:
            self.phrasal_words = self.accented_tokens

        a_text = self.phrasal_words

        if len(str(dep).split(' ')) > 1:
            for token in dep:
                if isinstance(token, nltk.tree.Tree):
                    self._clitics(token, n)
                else:
                    if token.pos_ in functors_pos and token.text not in adverb_adp:
                        if '+' in a_text[token.i + n]:
                            clitic = a_text[token.i + n].replace('+', '')
                        else:
                            clitic = a_text[token.i + n]

                        if token.i < len(self.tokens) - 1:
                            if self.tokens[token.i + n + 1] in str(dep) and self.tokens[token.i + n + 1][
                                0] not in 'еёюяи':
                                a_text = a_text[:token.i + n] + [clitic + a_text[token.i + n + 1]] + a_text[
                                                                                                     token.i + n + 2:]
                                n -= 1
                        elif token.i > 0:
                            if self.tokens[token.i + n - 1] in str(dep):  # enclitics
                                a_text = a_text[:token.i + n - 1] + [a_text[token.i + n - 1] + clitic] + a_text[
                                                                                                         token.i + n + 1:]
                                n -= 1

        self.phrasal_words = a_text

    def _ogoego(self):
        if self.orig_word[-3:] in 'ого его'.split() \
                and self.word != 'ого+':
            accent_i = self.word.index('+')
            self.word = self.orig_word[:-2] + 'во'
            self.word = self.word[:accent_i] + '+' + self.word[accent_i:]

    def _sto(self):
        if 'что' in self.word:
            self.word = self.word.replace('что', 'што')

    def _tsa(self):
        if self.word not in 'заботься отметься'.split():
            if self.word[-3:] == 'тся':
                self.word = self.word[:-3] + 'ца'
            elif self.word[-4:] == 'ться':
                self.word = self.word[:-4] + 'ца'

    def _unpron(self):
        for i in range(len(self.word[:-2])):
            if self.word[i:i + 3] in 'стн стл здн рдн'.split() \
                    or self.word[i:i + 4] in 'нтск ндск'.split() or self.word[i:i + 5] == 'лвств':
                self.word = self.word[:i + 1] + self.word[i + 2:]
            elif self.word[i:i + 3] == 'лнц' or self.word[i:i + 2] == 'дц' \
                    or self.word[i:i + 4] == 'вств':
                self.word = self.word[:i] + self.word[i + 1:]

    def _hissing(self):
        for i in range(len(self.word) - 2):  # hissing consonants
            if 'сш' in self.word:
                self.word.replace('сш', 'шш')
            elif 'зш' in self.word:
                self.word.replace('зш', 'шш')
            elif 'сж' in self.word:
                self.word.replace('сж', 'жж')
            elif 'зж' in self.word:
                self.word.replace('зж', 'жж')
            elif 'сч' in self.word:
                self.word.replace('сч', 'щ')
            elif 'зч' in self.word:
                if self.stems[self.word][-3:] == 'чик' or self.stems[self.word][-3:] == 'чиц':
                    self.word.replace('зч', 'щ')
            elif 'тч' in self.word:
                if self.stems[self.word][-3:] == 'чик' or self.stems[self.word][-3:] == 'чиц':
                    self.word.replace('тч', 'ч')
            elif 'дч' in self.word:
                if self.stems[self.word][-3:] == 'чик' or self.stems[self.word][-3:] == 'чиц':
                    self.word.replace('дч', 'ч')

    def _lpc_ex(self, word: str):
        orig_word = word
        if '+' in orig_word:
            orig_word = orig_word.replace('+', '')
            if '-' in orig_word:
                orig_word = orig_word.replace('-', '')

        self.orig_word = orig_word
        if self.lemmas[self.orig_word] in self.lpc_unr_ex:
            word = self.lpc_unr_ex[self.orig_word]
            word = data.word_form(word, self.orig_word)
            word = self._accent_placing(word)

        self.word = word
        self._ogoego()
        self._sto()
        self._tsa()
        self._unpron()
        self._hissing()

    def _transliterate(self, word: str):
        self._lpc_ex(word)
        self.translited_word = epi.transliterate(self.word)
        res = []
        del_idx = []

        if 't͡ɕʲ' in self.translited_word:
            self.translited_word = self.translited_word.replace('t͡ɕʲ', 't͡ɕ')
        if 'ʂʲː' in self.translited_word:
            self.translited_word = self.translited_word.replace('ʂʲː', 'ʂ')
        if 'ɕːʲ' in self.translited_word:
            self.translited_word = self.translited_word.replace('ɕːʲ', 'ɕː')

        for i, symb in enumerate(self.translited_word):
            if symb != '+' and symb != '-':
                n = 4
                if i != len(self.translited_word) - 1:
                    while self.translited_word[i:i + n] not in starterpack and n > 0:
                        n -= 1
                    if n > 1:
                        for n_i in range(1, n):
                            del_idx.append(i + n_i)
                res.append(self.translited_word[i:i + n])
            else:
                res.append(symb)

        res[:] = [x for i, x in enumerate(res) if i not in del_idx]

        self.translited_word = res

    def _palatalization(self):
        if self.lemmas[self.orig_word] not in 'сосиска злить после'.split(' '):
            for i in range(len(self.translited_word) - 1):
                if ['i', '+', 'z', 'm'] not in self.translited_word \
                        and 'ʲ' not in self.translited_word[i]:
                    sound_0 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i])
                    sound_0.analize()
                    sound_1 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 1])
                    sound_1.analize()
                    if sound_1.palatalization == 'soft' and 'lab' not in sound_1.place \
                            and sound_0.palatalization[0] != 'a' and sound_0.phon == 'C':
                        self.translited_word[i] = self.translited_word[i] + 'ʲ'

    def _voicing(self):
        sound_last = Sounds(alphabet, sorted_phon, paired, self.translited_word[-1])
        sound_last.analize()
        if sound_last.voice == 'voiced' and sound_last.pair:
            self.translited_word[-1] = sound_last.pair
        for i in range(len(self.translited_word) - 2):
            sound_0 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i])
            sound_0.analize()
            sound_1 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 1])
            sound_1.analize()
            if sound_1.voice == 'voiced' and self.translited_word[i + 1] != 'j' \
                    and 'son' not in sound_1.manner and 'v' not in self.translited_word[i + 1] and sound_0.pair:
                self.translited_word[i] = sound_0.pair

    def _jot(self):
        n = 0
        if self.translited_word[0] == 'j' and self.word[0] != 'й':
            n += 1
        for el in 'd͡ʒ ь ъ'.split(' '):
            if el in self.translited_word:
                n -= 1
        for i, let in enumerate(self.word):
            sound_n = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + n - 1])
            sound_n.analize()
            if let == 'е' or let == 'ё' or let == 'ю' or let == 'я':
                if i != 0:
                    if self.word[i - 1] in 'ьъ':
                        n += 1
                        if self.translited_word[i + n] != 'j':
                            self.translited_word = self.translited_word[:i + n - 1] + ['j'] + self.translited_word[
                                                                                              i + n - 1:]
                    elif self.word[i - 1] in rus_v:
                        if self.translited_word[i + n - 1] != 'j':
                            self.translited_word = self.translited_word[:i + n] + ['j'] + self.translited_word[i + n:]
                            n += 1
                        else:
                            n += 1
                    elif 'ʲ' not in self.translited_word[i + n - 1] and self.translited_word[i + n] != 'э' \
                            and sound_n.palatalization[0] != 'a':
                        self.translited_word[i + n - 1] = self.translited_word[i + n - 1] + 'ʲ'
                elif i < len(self.word) - 2:
                    if self.word[i + 2] == '+':
                        if self.translited_word[i + n - 1] != 'j':
                            self.translited_word = self.translited_word[:i + n] + ['j'] + self.translited_word[i + n:]
                            n += 1
                        elif i + n - 1 != 0:
                            n += 1
            elif let == 'и' and i != 0:
                if self.word[i - 1] == 'ь':
                    if self.translited_word[i + n - 1] != 'j':
                        self.translited_word = self.translited_word[:i + n] + ['j'] + self.translited_word[i + n:]
                        n += 1
                    else:
                        n += 1
                elif 'ʲ' not in self.translited_word[i + n - 1] and sound_n.palatalization[0] != 'a':
                    self.translited_word[i + n - 1] = self.translited_word[i + n - 1] + 'ʲ'

    def _long_cons(self):
        n = 0
        for i, phon in enumerate(self.translited_word):
            if i < len(self.translited_word) - 2:
                if phon == self.translited_word[i + n + 1] and phon in 'bpfkstrlmngdz':
                    self.translited_word = self.translited_word[:i + n] + [phon + 'ː'] + self.translited_word[i + 2:]
                    n -= 1

    def _lpc_full(self, word: str):
        self._transliterate(word)
        self._palatalization()
        self._voicing()
        self._jot()
        self._long_cons()

    def _nasal_m(self):
        for i, phon in enumerate(self.translited_word[:-1]):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 1])
            sound.analize()
            if phon == 'm' and sound.place == 'labial, labiodental':
                self.translited_word[i] = 'ɱ'
            elif phon == 'mʲ' and sound.place == 'labial, labiodental':
                self.translited_word[i] = 'ɱʲ'

    def _silent_r(self):
        for i, phon in enumerate(self.translited_word):
            if phon == 'r':
                if i == len(self.translited_word) - 1:
                    self.translited_word[i] = 'r̥'
                else:
                    sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 1])
                    sound.analize()
                    if sound.voice == 'voiceless':
                        self.translited_word[i] = 'r̥'
            elif phon == 'rʲ':
                if i == len(self.translited_word) - 1:
                    self.translited_word[i] = 'r̥ʲ'

    def _vosed_ts(self):
        for i, phon in enumerate(self.translited_word[:-1]):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 1])
            sound.analize()
            if phon == 't͡s' and sound.voice == 'voiced':
                self.translited_word[i] = 'd̻͡z̪'

    def _fricative_g(self):
        if self.lemmas[self.orig_word] in 'ага ого господь господи'.split(' '):
            for i, phon in enumerate(self.translited_word):
                if phon == 'ɡ':
                    self.translited_word[i] = 'γ'

    def _vowel_a(self):
        for i, phon in enumerate(self.translited_word):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound.analize()
            if phon == 'a':
                if i != len(self.translited_word) - 1 and i != 0:

                    if self.translited_word[i + 1] == '+':  # ударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ɐ.'
                        elif 'soft' in sound.palatalization:
                            self.translited_word[i] = 'æ'
                        elif i != len(self.translited_word) - 2:
                            if 'hard' in sound.palatalization and self.translited_word[i + 2] == 'l':
                                self.translited_word[i] = 'ɑ'
                        else:
                            self.translited_word[i] = 'æ'

                    elif self.translited_word[i + 1] == '-':  # первый предударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ᵻ'
                        elif 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ɐ'
                        else:
                            self.translited_word[i] = 'ɪ'

                    else:  # заударные/второй предударный (not last, not first)
                        if sound.hissing == 'hissing' or 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ə'
                        else:
                            self.translited_word[i] = 'ɪ.'

                elif i == len(self.translited_word) - 1:  # заударные (last)
                    if sound.hissing == 'hissing':
                        self.translited_word[i] = 'ə'
                    elif 'hard' in sound.palatalization:
                        self.translited_word[i] = 'ʌ'
                    else:
                        self.translited_word[i] = 'æ.'

                else:
                    if self.translited_word[i + 1] == '-':  # первый предударный (first)
                        self.translited_word[i] = 'ɐ'
                    elif self.translited_word[i + 1] != '+':  # заударные/второй предударный (first)
                        self.translited_word[i] = 'ə'

    def _vowel_o(self):
        for i, phon in enumerate(self.translited_word):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound.analize()
            if phon == 'o':
                if i != len(self.translited_word) - 1 and i != 0:

                    if self.translited_word[i + 1] == '+':  # ударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ɐ.'
                        elif 'soft' in sound.palatalization:
                            self.translited_word[i] = 'ɵ'
                        else:
                            self.translited_word[i] = 'ɵ'

                    elif self.translited_word[i + 1] == '-':  # первый предударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ᵻ'
                        elif 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ɐ'
                        else:
                            self.translited_word[i] = 'ɪ'

                    else:  # заударные/второй предударный (not last, not first)
                        if sound.hissing == 'hissing' or 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ə'
                        else:
                            self.translited_word[i] = 'ɪ.'

                elif i == len(self.translited_word) - 1:  # заударные (last)
                    if sound.hissing == 'hissing':
                        self.translited_word[i] = 'ə'
                    elif 'hard' in sound.palatalization:
                        self.translited_word[i] = 'ʌ'
                    else:
                        self.translited_word[i] = 'æ.'

                else:
                    if self.translited_word[i + 1] == '-':  # первый предударный (first)
                        self.translited_word[i] = 'ɐ'
                    elif self.translited_word[i + 1] != '+':  # заударные/второй предударный (first)
                        self.translited_word[i] = 'ə'

    def _vowel_e(self):
        for i, phon in enumerate(self.translited_word):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound.analize()
            if phon == 'e':
                if i < len(self.translited_word) - 1 and i != 0:

                    if self.translited_word[
                        i + 1] == '+' and sound.hissing == 'hissing':  # ударный (not last, not first)
                        self.translited_word[i] = 'ᵻ'
                    elif 'hard' in sound.palatalization:
                        self.translited_word[i] = 'ɛ'

                    elif self.translited_word[i + 1] == '-':  # первый предударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ə'
                        elif 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ᵻ'
                        else:
                            self.translited_word[i] = 'ɪ'

                    else:  # заударные/второй предударный (not last, not first)
                        if sound.hissing == 'hissing':
                            self.translited_word[i] = 'ə'
                        elif 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ᵻ'
                        else:
                            self.translited_word[i] = 'ɪ.'

                elif i == len(self.translited_word) - 1:  # заударные (last)
                    if sound.hissing == 'hissing':
                        self.translited_word[i] = 'ə'
                    elif 'hard' in sound.palatalization:
                        self.translited_word[i] = 'ᵻ'
                    else:
                        self.translited_word[i] = 'æ.'

                else:
                    if self.translited_word[i + 1] == '+':  # ударный (first)
                        self.translited_word[i] = 'ɛ'
                    elif self.translited_word[i + 1] == '-':  # первый предударный (first)
                        self.translited_word[i] = 'ᵻ'
                    else:  # заударные/второй предударный (first)
                        self.translited_word[i] = 'ɪ.'

    def _vowel_u(self):
        for i, phon in enumerate(self.translited_word):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound.analize()
            if phon == 'u':
                if i != len(self.translited_word) - 1:

                    if self.translited_word[i + 1] == '+':  # ударный
                        if 'soft' in sound.palatalization:
                            self.translited_word[i] = 'ʉ'

                    else:  # первый/второй предударный/заударные не посл.
                        if 'hard' in sound.palatalization:
                            self.translited_word[i] = 'ʊ'
                        else:
                            self.translited_word[i] = 'ᵿ'

                else:  # первый/второй предударный/заударные посл.
                    if 'hard' in sound.palatalization:
                        self.translited_word[i] = 'ʊ'
                    else:
                        self.translited_word[i] = 'ᵿ'

    def _vowel_i(self):
        for i, phon in enumerate(self.translited_word):
            sound = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound.analize()
            if phon == 'i':
                if i == 0 and self.translited_word[i + 1] != '+':
                    self.translited_word[i] = 'ɪ'
                elif i == len(self.translited_word) - 1:  # и последний (не может быть ударным)
                    if sound.hissing == 'hissing' and self.translited_word[i - 1] != 't͡ɕ':
                        self.translited_word[i] = 'ɨ'
                    else:
                        self.translited_word[i] = 'ɪ'
                else:
                    if sound.hissing == 'hissing' and self.translited_word[i - 1] != 't͡ɕ':
                        self.translited_word[i] = 'ɨ'
                    elif self.translited_word[i + 1] != '+':
                        self.translited_word[i] = 'ɪ'

    def _vowel_ii(self):
        for i, phon in enumerate(self.translited_word):
            sound_1 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound_1.analize()
            if phon == 'ɨ':
                if i < len(self.translited_word) - 1:
                    if self.translited_word[i + 1] == '+':  # ударный
                        if len(self.translited_word) > 4:
                            sound_2 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 2])
                            sound_2.analize()
                            if self.translited_word[i - 1] == 'l' 'lab' in sound_2.place:
                                self.translited_word[i] = 'ɯ̟ɨ̟'
                        if i < len(self.translited_word) - 2:
                            sound_3 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i + 2])
                            sound_3.analize()
                            if sound_1.place == 'lingual, dental' \
                                    and sound_3.place == 'lingual, velar' \
                                    or sound_1.place == 'lingual, palatinоdental' \
                                    and sound_3.place == 'lingual, velar':
                                self.translited_word[i] = 'ɨ̟'

                    else:  # предударный / заударный (not last)
                        if sound_1.hissing == 'hissing':
                            self.translited_word[i] = 'ə'
                        else:
                            self.translited_word[i] = 'ᵻ'

                else:  # заударный (last)
                    if sound_1.hissing == 'hissing':
                        self.translited_word[i] = 'ə'
                    else:
                        self.translited_word[i] = 'ᵻ'

    def _labia_velar(self):
        for i, phon in enumerate(self.translited_word):
            sound_0 = Sounds(alphabet, sorted_phon, paired, phon)
            sound_0.analize()
            sound_1 = Sounds(alphabet, sorted_phon, paired, self.translited_word[i - 1])
            sound_1.analize()
            if sound_0.round == 'round' and i != 0:
                if sound_1.phon == 'C' and 'ʷ' not in self.translited_word[i - 1]:
                    self.translited_word[i - 1] = self.translited_word[i - 1] + 'ʷ'
                    if i != len(self.translited_word) - 2:
                        self._labia_velar()
                        break

                    elif sound_0.round == 'velarize' \
                            and 'soft' not in sound_1.palatalization and 'ˠ' not in self.translited_word[i - 1]:
                        self.translited_word[i - 1] = self.translited_word[i - 1] + 'ˠ'
                        if i != len(self.translited_word) - 2:
                            self._labia_velar()
                            break

    def _add_allophones(self, word: str):
        self._lpc_full(word)
        self._nasal_m()
        self._silent_r()
        self._vosed_ts()
        self._fricative_g()
        self._vowel_a()
        self._vowel_o()
        self._vowel_e()
        self._vowel_u()
        self._vowel_i()
        self._vowel_ii()
        self._labia_velar()

    def full_transcription(self):
        dep = make_dependency_tree(' '.join(self.tokens))
        self._accent_replacing()
        self._clitics(dep)
        for word in self.phrasal_words:
            self._add_allophones(word)
            self.transcription += self.translited_word

        while '+' in self.transcription:
            self.transcription.pop(self.transcription.index('+'))
            while '-' in self.transcription:
                self.transcription.pop(self.transcription.index('-'))
