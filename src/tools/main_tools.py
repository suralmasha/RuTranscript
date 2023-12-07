import re

import nltk
from num2t4ru import num2text

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_ru')


def apply_differences(words):
    differences = {}
    for i, (char1, char2) in enumerate(zip(words[0], words[1].replace('+', ''))):
        if char1 != char2:
            differences[i + 1] = char2

    original_word, changed_word = words
    new_word = []
    n = 0
    for i, char in enumerate(changed_word):
        if char == '+':
            n += 1
            continue
        elif i + n + 1 in differences:
            new_word.append(differences[i + n + 1])
        else:
            new_word.append(char)

    return ''.join(new_word)


def get_punctuation_dict(text):
    """
    Returns a dictionary with the indices of punctuation marks as keys and the corresponding
    punctuation symbol (either '|' or '||') as values.
    """
    punctuation = r'.,:;()\—\|\?\!…'
    pause_dict = {}

    i = 1
    for char in text:
        if char in punctuation:
            pause_type = '||' if char in '.?!…' else '|'
            pause_dict[i] = pause_type
            i += 1

    return pause_dict


def custom_num2text(tokens: list):
    """
    Turns digits to words.
    """
    tokens_normal = []
    cache = {}

    for section_tokens in tokens:
        section_normal = []
        for word in section_tokens:
            if word.isnumeric():
                if word not in cache:
                    cache[word] = num2text(int(word))
                word_normal = cache[word]
                section_normal.extend(word_normal.split(' '))
            else:
                section_normal.append(word)
        tokens_normal.append(section_normal)

    return tokens_normal


def text_norm_tok(text: str):
    """
    Splits text by punctuation (not including ' and ") and than tokenize it.
    """
    sections = re.split(r'[.?!,:;()—…]', text)
    sections = [re.sub(r'\s+', ' ', w) for w in sections if w != '']
    sections = [re.sub(r'\s$', '', w) for w in sections if w != '']
    sections = [re.sub(r'^\s', '', w) for w in sections if w != '']

    tokens = [[re.sub(r"[,.\\|/;:()*&^%$#@?!\[\]{}\"—…«»]", '', word) for word in section.split()]
              for section in sections]

    return custom_num2text(tokens)


adverb_adp = {'после', 'кругом', 'мимо', 'около', 'вокруг', 'напротив', 'поперёк'}


def find_clitics(dep, text, indexes=None):
    """
    Finds proclitics and enclitics in text by using dependency trees.
    Args:
      dep (class 'nltk.tree.tree.Tree'): dependency tree
      text (list): list of tokens in the text
      indexes (list[tuple]): list of tuples with indexes of a main and a dependent words.
    """
    if indexes is None:
        indexes = set()
    functors_pos = {'CCONJ', 'PART', 'ADP'}
    str_dep = str(dep)

    if len(str_dep.split(' ')) > 1:
        for token in dep:
            if isinstance(token, nltk.tree.Tree):
                indexes = find_clitics(token, text, indexes)

            elif (token.pos_ in functors_pos) and (token.text not in adverb_adp):
                clitic_index = token.i
                main_word_index = None

                if (token.i < len(text) - 1) and (text[token.i + 1] in str_dep) \
                        and (text[token.i + 1][0] not in 'еёюяи'):  # proclitic
                    main_word_index = token.i + 1

                elif (token.i > 0) and (text[token.i - 1] in str_dep):  # enclitic
                    main_word_index = token.i - 1

                if main_word_index is not None:
                    indexes.add((main_word_index, clitic_index))

    return indexes


def extract_phrasal_words(phonemes, indexes):
    """
    Joins clitics with main words.
    Args:
        phonemes (list): list of phonemes with '_' for spaces;
        indexes (set[tuple]): set of tuples with indexes of a main and a dependent words.
    """
    tokens_list = []
    start_token_index = 0

    for i, current_phon in enumerate(phonemes):
        if current_phon == '_':
            tokens_list.append(phonemes[start_token_index:i])
            start_token_index = i + 1

    tokens_list.append(phonemes[start_token_index:])

    phrasal_words = tokens_list[:]
    n = 0
    main_word_cache = []
    enclitic_cache = []

    for tuple_indexes in indexes:
        try:
            main_word_index = tuple_indexes[0]

            if tuple_indexes[1] > main_word_index:  # проклитика
                main_word = phrasal_words[main_word_index + n] if main_word_index in main_word_cache\
                    else tokens_list[main_word_index]
                main_word_cache.append(main_word_index)
                proclitic_index = tuple_indexes[1]

                proclitic = [x for x in tokens_list[proclitic_index] if x != '+']
                phrasal_words.remove(tokens_list[proclitic_index])
                phrasal_words.remove(main_word)
                if proclitic_index == 1:
                    phrasal_words.insert(0, main_word + proclitic)
                else:
                    phrasal_words.insert(proclitic_index - main_word_cache.count(main_word_index),
                                         main_word + proclitic)
                n -= 1

            else:  # энклитика
                main_word = phrasal_words[main_word_index - enclitic_cache.count(main_word_index)] \
                    if main_word_index in enclitic_cache \
                    else tokens_list[main_word_index]
                main_word_cache.append(main_word_index)
                enclitic_index = tuple_indexes[1]
                enclitic_cache.append(enclitic_index)

                enclitic = [x for x in tokens_list[enclitic_index] if x != '+']
                phrasal_words.remove(tokens_list[enclitic_index])
                phrasal_words.remove(main_word)
                phrasal_words.insert(enclitic_index + n + enclitic_cache.count(main_word_index), enclitic + main_word)
                n -= 1

        except:
            continue

    phrasal_words_result = []
    for token in phrasal_words:
        phrasal_words_result.extend(token + ['_'])
    del phrasal_words_result[-1]

    return phrasal_words_result
