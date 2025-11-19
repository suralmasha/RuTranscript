import re

import nltk
from num2t4ru import num2text

from ru_transcript.consts import JOTISED_LETTERS

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_ru')


def apply_differences(words: list[str]) -> str:
    """
    Apply character-level differences from the second word to the first word.

    param words: A list containing two strings: [original_word, changed_word].
                  The changed_word may contain '+' symbols to ignore.
    return: A new string where differences from changed_word are applied to original_word.
    """
    original, changed = words
    # Remove '+' for comparison
    clean_changed = changed.replace('+', '')

    # Record positions where characters differ
    differences = {i: c2 for i, (c1, c2) in enumerate(zip(original, clean_changed, strict=True)) if c1 != c2}

    # Apply differences while skipping '+' symbols
    new_word = []
    skip_count = 0
    for i, c in enumerate(changed):
        if c == '+':
            skip_count += 1
            continue
        index = i - skip_count
        new_word.append(differences.get(index, c))

    return ''.join(new_word)


def get_punctuation_dict(text: str) -> dict[int, str]:
    """
    Return a dictionary mapping positions of punctuation marks to pause types.

    param text: Input text string.
    return: Dictionary where keys are 1-based indices of punctuation marks,
            and values are '||' for sentence-ending punctuation or '|' for minor pauses.
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


def custom_num2text(tokens: list[list[str]]) -> list[list[str]]:
    """
    Convert numeric tokens to their word representations.

    param tokens: A list of token lists (sections), each containing words or digits.
    return: A new list of token lists where numeric strings are replaced by words.
    """
    tokens_normal = []
    cache = {}

    for section_tokens in tokens:
        section_normal = []
        for word in section_tokens:
            if word.isnumeric():
                # Use cached conversion if available
                if word not in cache:
                    cache[word] = num2text(int(word))
                section_normal.extend(cache[word].split())
            else:
                section_normal.append(word)
        tokens_normal.append(section_normal)

    return tokens_normal


def text_norm_tok(text: str) -> list[list[str]]:
    """
    Normalize text by splitting, tokenizing, and converting numeric tokens to words.

    param text: Input text string.
    return: A list of token lists (sections), with numbers converted to words.
    """
    sections = re.split(r'[.?!,:;()—…]', text)
    sections = [re.sub(r'\s+', ' ', w) for w in sections if w != '']
    sections = [re.sub(r'\s$', '', w) for w in sections if w != '']
    sections = [re.sub(r'^\s', '', w) for w in sections if w != '']

    tokens = [
        [re.sub(r'[,.\\|/;:()*&^%$#@?!\[\]{}\"—…«»]', '', word) for word in section.split()] for section in sections
    ]

    return custom_num2text(tokens)


adverb_adp = {'после', 'кругом', 'мимо', 'около', 'вокруг', 'напротив', 'поперёк'}


def find_clitics(
    dep: 'nltk.tree.Tree', text: list[str], indexes: set[tuple[int, int]] | None = None
) -> set[tuple[int, int]]:
    """
    Find proclitics and enclitics in a text using a dependency tree.

    param dep: An NLTK dependency tree node.
    param text: List of tokens in the text.
    param indexes: A set to store tuples of (main_word_index, clitic_index).
                    If None, a new set is created.
    return: Set of tuples representing clitic relationships.
    """
    if indexes is None:
        indexes = set()

    functors_pos = {'CCONJ', 'PART', 'ADP'}
    str_dep = str(dep)

    # Only process nodes with more than one token
    if len(str_dep.split()) > 1:
        for token in dep:
            if isinstance(token, nltk.tree.Tree):
                # Recurse into subtrees
                indexes = find_clitics(token, text, indexes)
            elif token.pos_ in functors_pos and token.text not in adverb_adp:
                clitic_index = token.i
                main_word_index = None

                # Proclitic: functor before main word (excluding some vowels)
                if (
                    token.i < len(text) - 1
                    and text[token.i + 1] in str_dep
                    and text[token.i + 1][0] not in JOTISED_LETTERS
                ):
                    main_word_index = token.i + 1
                # Enclitic: functor after main word
                elif token.i > 0 and text[token.i - 1] in str_dep:
                    main_word_index = token.i - 1

                if main_word_index is not None:
                    indexes.add((main_word_index, clitic_index))

    return indexes


def merge_phrasal_words(phonemes: list[str], indexes: set[tuple[int, int]]) -> list[str]:
    """
    Merge clitics with their main words in a phoneme list.

    param phonemes: List of phonemes with '_' representing spaces.
    param indexes: Set of tuples (main_word_index, clitic_index) indicating clitic relationships.
    return: A new phoneme list where clitics are joined with their main words.
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
                main_word = (
                    phrasal_words[main_word_index + n]
                    if main_word_index in main_word_cache
                    else tokens_list[main_word_index]
                )
                main_word_cache.append(main_word_index)
                proclitic_index = tuple_indexes[1]

                proclitic = [x for x in tokens_list[proclitic_index] if x != '+']
                phrasal_words.remove(tokens_list[proclitic_index])
                phrasal_words.remove(main_word)
                if proclitic_index == 1:
                    phrasal_words.insert(0, main_word + proclitic)
                else:
                    phrasal_words.insert(
                        proclitic_index - main_word_cache.count(main_word_index), main_word + proclitic
                    )
                n -= 1

            else:  # энклитика
                main_word = (
                    phrasal_words[main_word_index - enclitic_cache.count(main_word_index)]
                    if main_word_index in enclitic_cache
                    else tokens_list[main_word_index]
                )
                main_word_cache.append(main_word_index)
                enclitic_index = tuple_indexes[1]
                enclitic_cache.append(enclitic_index)

                enclitic = [x for x in tokens_list[enclitic_index] if x != '+']
                phrasal_words.remove(tokens_list[enclitic_index])
                phrasal_words.remove(main_word)
                phrasal_words.insert(enclitic_index + n + enclitic_cache.count(main_word_index), enclitic + main_word)
                n -= 1

        except Exception:  # noqa: PERF203, S112
            continue

    phrasal_words_result = []
    for token in phrasal_words:
        phrasal_words_result.extend([*token, '_'])
    del phrasal_words_result[-1]

    return phrasal_words_result
