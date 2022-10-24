import re

import spacy
import nltk
from nltk import Tree

from .ru_number_to_text.num2t4ru import num2text
from .StressRNN.stressrnn.stressrnn import StressRNN

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_ru')


class TextNormalizationTokenization:
    def __init__(self, text, a_text):
        self.text = text
        self.a_text = a_text
        self.pause_dict = {}  # {section_index: pause_type}
        self.sections = []
        self.a_sections = []
        self.sections_len = 0
        self.tokens = []
        self.a_tokens = []
        self.tokens_normal = []
        self.a_tokens_normal = []

    def section_split(self):
        """
        Splits text by punctuation (not including ' and ").
        """
        long_pause = ['.', '?', '!', '…']
        short_pause = [',', ':', ';', '(', ')']

        index = 0
        for word in self.text.split():
            if any(symbol in long_pause for symbol in word):
                self.pause_dict[index] = '||'
                index += 1
            elif any(symbol in short_pause for symbol in word):
                self.pause_dict[index] = '|'
                index += 1

        sections = re.split(r'[.?!,:;()…]', self.text)
        sections = [re.sub(r'\s+', ' ', w) for w in sections if w != '']
        sections = [re.sub(r'\s$', '', w) for w in sections if w != '']
        self.sections = [re.sub(r'^\s', '', w) for w in sections if w != '']

        a_sections = re.split(r'[.?!,:;()…]', self.a_text)
        a_sections = [re.sub(r'\s+', ' ', w) for w in a_sections if w != '']
        a_sections = [re.sub(r'\s$', '', w) for w in a_sections if w != '']
        self.a_sections = [re.sub(r'^\s', '', w) for w in a_sections if w != '']

        self.sections_len = len(self.sections)

    def tokenize(self):
        """
        Splits text into tokens.
        """
        for section_num in range(self.sections_len):
            tokens = [w.lower() for w in self.sections[section_num].split()]
            tokens = [re.sub(r"[^\wу́\-\+\|]", '', w) for w in tokens if w != '']
            tokens = [re.sub(r"у́", 'у', w) for w in tokens if w != '']
            self.tokens.append(tokens)

            a_tokens = [w.lower() for w in self.sections[section_num].split()]
            a_tokens = [re.sub(r"[^\wу́\-\+\|]", '', w) for w in a_tokens if w != '']
            a_tokens = [re.sub(r"у́", 'у', w) for w in a_tokens if w != '']
            self.a_tokens.append(a_tokens)

    def my_num2text(self):
        """
        Turns digits to words.
        """
        self.tokens_normal = self.tokens
        self.a_tokens_normal = self.a_tokens

        for section_num in range(self.sections_len):
            n = 0
            for i, word in enumerate(self.tokens[section_num]):
                if word.isnumeric():
                    if len(word) == 1:
                        self.tokens_normal[section_num][i + n] = num2text(int(word))
                        self.a_tokens_normal[section_num][i + n] = num2text(int(self.a_tokens[section_num][i]))
                    else:
                        add = num2text(int(word)).split(' ')
                        self.tokens_normal[section_num] = self.tokens[section_num][:i + n] + add + self.tokens[
                                                                                                       section_num][
                                                                                                   i + n + 1:]
                        self.a_tokens_normal[section_num] = self.a_tokens[section_num][:i + n] + add + self.a_tokens[
                                                                                                           section_num][
                                                                                                       i + n + 1:]
                        n += len(add) - 1


class Stresses:
    def __init__(self):
        self.dependency_tree = None

        self.nlp = spacy.load('ru_core_news_sm')
        self.stress_rnn = StressRNN()

    def place_accent(self, token):
        """
        Places an accent.
        Args:
          token (str): token without an accent.
        """
        return self.stress_rnn.put_stress(token, accuracy_threshold=0.75)

    @staticmethod
    def replace_accent(token):
        """
        Replaces an accent from a place before a stressed vowel to a place after it.
        Args:
          token (str): token which needs to be refactored.
        """
        token_split = list(token)
        plus_index = token_split.index('+')

        new_token_split = token_split[:]
        new_token_split.remove('+')
        new_token_split.insert(plus_index + 1, token_split.pop(plus_index))

        return ''.join(new_token_split)

    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node, [self.to_nltk_tree(child) for child in node.children])

        return node

    def make_dependency_tree(self, text):
        """
        Makes a dependency tree.
        Args:
          text (str): original text
        """
        doc = self.nlp(text)
        for sent in doc.sents:
            self.dependency_tree = self.to_nltk_tree(sent.root)

        return self.dependency_tree


def find_clitics(dep, text, indexes=None):
    """
    Finds proclitics and enclitics in text by using dependency trees.
    Args:
      dep (class 'nltk.tree.tree.Tree'): dependency tree
      text (list): list of tokens in the text
      indexes (list[tuple]): list of tuples with indexes of a main and a dependent words.
    """
    if indexes is None:
        indexes = []
    functors_pos = {'CCONJ', 'PART', 'ADP'}
    adverb_adp = ['после', 'кругом', 'мимо', 'около',
                  'вокруг', 'напротив', 'поперёк']

    if len(str(dep).split(' ')) > 1:
        for token in dep:
            if isinstance(token, nltk.tree.Tree):
                indexes = find_clitics(token, text, indexes)

            elif (token.pos_ in functors_pos) and (token.text not in adverb_adp):
                clitic_index = token.i
                main_word_index = None

                if (token.i < len(text) - 1) and (text[token.i + 1] in str(dep)) \
                        and (text[token.i + 1][0] not in 'еёюяи'):  # proclitic
                    main_word_index = token.i + 1

                elif (token.i > 0) and (text[token.i - 1] in str(dep)):  # enclitic
                    main_word_index = token.i - 1

                tuple_indexes = tuple([main_word_index, clitic_index])
                if tuple_indexes not in indexes:
                    indexes.append(tuple_indexes)

    return indexes


def extract_phrasal_words(phonemes, indexes):
    """
    Joins clitics with main words.
    Args:
        phonemes (list): list of phonemes with '_' for spaces;
        indexes (list[tuple]): list of tuples with indexes of a main and a dependent words.
    """
    tokens_list = []
    start_token_index = 0

    for i, current_phon in enumerate(phonemes):
        if current_phon == '_':
            tokens_list.append(phonemes[start_token_index:i])
            start_token_index = i + 1

    tokens_list.append(phonemes[start_token_index:])

    phrasal_words = tokens_list[:]
    proclitic_index = None
    enclitic_index = None
    n = 0

    for tuple_indexes in indexes:
        main_word_index = tuple_indexes[0]
        main_word = tokens_list[main_word_index]

        if tuple_indexes[1] > main_word_index:
            proclitic_index = tuple_indexes[1]
        else:
            enclitic_index = tuple_indexes[1]

        if proclitic_index is not None:
            proclitic = [x for x in tokens_list[proclitic_index] if x != '+']
            phrasal_words.remove(tokens_list[proclitic_index])
            phrasal_words.remove(main_word)
            phrasal_words.insert(proclitic_index + n, main_word + proclitic)
            n -= 1

        if enclitic_index is not None:
            enclitic = [x for x in tokens_list[enclitic_index] if x != '+']
            phrasal_words.remove(tokens_list[enclitic_index])
            phrasal_words.remove(main_word)
            phrasal_words.insert(enclitic_index + n, enclitic + main_word)
            n -= 1

    phrasal_words_result = []
    for token in phrasal_words:
        phrasal_words_result.extend(token + ['_'])
    del phrasal_words_result[-1]

    return phrasal_words_result
