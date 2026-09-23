import re
from functools import lru_cache

import nltk
from num2t4ru import num2text

from ru_transcript.data_constants import JOTISED_LETTERS

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_ru')

PUNCTUATION = frozenset('.,:;()—|?!…')
LONG_PAUSE_PUNCTUATION = frozenset('.?!…')
SECTION_SPLIT_RE = re.compile(r'[.?!,:;()—…]')
SPACE_RE = re.compile(r'\s+')
TOKEN_CLEANUP_TABLE = str.maketrans('', '', r'.,\|/;:()*&^%$#@?![]{}"—…«»')
ADVERB_ADP = frozenset({'после', 'кругом', 'мимо', 'около', 'вокруг', 'напротив', 'поперёк'})
FUNCTORS_POS = frozenset({'CCONJ', 'PART', 'ADP'})


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
    return {
        punctuation_index: '||' if char in LONG_PAUSE_PUNCTUATION else '|'
        for punctuation_index, char in enumerate((char for char in text if char in PUNCTUATION), start=1)
    }


@lru_cache(maxsize=512)
def _num2text_words(word: str) -> tuple[str, ...]:
    return tuple(num2text(int(word)).split())


def custom_num2text(tokens: list[list[str]]) -> list[list[str]]:
    """
    Convert numeric tokens to their word representations.

    param tokens: A list of token lists (sections), each containing words or digits.
    return: A new list of token lists where numeric strings are replaced by words.
    """
    tokens_normal = []
    for section_tokens in tokens:
        section_normal: list[str] = []
        for word in section_tokens:
            if word.isnumeric():
                section_normal.extend(_num2text_words(word))
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
    sections = [SPACE_RE.sub(' ', section).strip() for section in SECTION_SPLIT_RE.split(text)]
    sections = [section for section in sections if section]

    tokens = [[word.translate(TOKEN_CLEANUP_TABLE) for word in section.split()] for section in sections]

    return custom_num2text(tokens)


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
    result = set() if indexes is None else indexes

    str_dep = str(dep)

    # Only process nodes with more than one token
    if len(str_dep.split()) > 1:
        for token in dep:
            if isinstance(token, nltk.tree.Tree):
                # Recurse into subtrees
                result = find_clitics(token, text, result)
            elif token.pos_ in FUNCTORS_POS and token.text not in ADVERB_ADP:
                clitic_index = token.i
                main_word_index = None

                # Proclitic: functor before main word (excluding some vowels)
                if (
                    (token.i < len(text) - 1)
                    and (text[token.i + 1] in str_dep)
                    and (text[token.i + 1][0] not in JOTISED_LETTERS)
                ):
                    main_word_index = token.i + 1
                # Enclitic: functor after main word
                elif token.i > 0 and text[token.i - 1] in str_dep:
                    main_word_index = token.i - 1

                if main_word_index is not None:
                    result.add((main_word_index, clitic_index))

    return result


def split_token_by_words(token: str, words: list[str]) -> list[str]:
    """
    Split a stressed token by word lengths while preserving stress marks.

    param token: Stressed token that may contain '+' marks.
    param words: Text words matching the token without stress marks.
    return: Stressed token parts aligned to the given words.
    """
    result = []
    token_index = 0

    for word in words:
        part = []
        letters_seen = 0
        while token_index < len(token) and (letters_seen < len(word) or token[token_index] == '+'):
            char = token[token_index]
            part.append(char)
            token_index += 1
            if char != '+':
                letters_seen += 1
        result.append(''.join(part))

    return result


def align_stressed_tokens_with_text(
    tokens: list[str], stressed_tokens: list[str], clitic_indexes: set[int]
) -> tuple[list[str], set[int]]:
    """
    Expand stressed tokens that join a clitic and its host into separate text tokens.

    param tokens: Normalized text tokens.
    param stressed_tokens: Normalized stressed text tokens.
    param clitic_indexes: Token indexes detected as clitics.
    return: Aligned stressed tokens and indexes of clitics explicitly stressed in fused spelling.
    """
    aligned = []
    fused_stressed_clitic_indexes = set()
    token_index = 0
    stressed_index = 0

    while token_index < len(tokens) and stressed_index < len(stressed_tokens):
        stressed_token = stressed_tokens[stressed_index]
        clean_stressed_token = stressed_token.replace('+', '')

        if clean_stressed_token == tokens[token_index]:
            aligned.append(stressed_token)
            token_index += 1
            stressed_index += 1
            continue

        words = []
        clean_words = ''
        split_end = token_index
        while split_end < len(tokens) and len(clean_words) < len(clean_stressed_token):
            words.append(tokens[split_end])
            clean_words += tokens[split_end]
            split_end += 1
            if clean_words == clean_stressed_token:
                parts = split_token_by_words(stressed_token, words)
                aligned.extend(parts)
                has_non_clitic_stress = any(
                    '+' in part and part_index not in clitic_indexes
                    for part_index, part in enumerate(parts, start=token_index)
                )
                for part_index, part in enumerate(parts, start=token_index):
                    if part_index in clitic_indexes and '+' in part and not has_non_clitic_stress:
                        fused_stressed_clitic_indexes.add(part_index)
                token_index = split_end
                stressed_index += 1
                break
        else:
            aligned.append(stressed_token)
            token_index += 1
            stressed_index += 1

    aligned.extend(stressed_tokens[stressed_index:])
    return aligned, fused_stressed_clitic_indexes


def merge_phrasal_words(
    phonemes: list[str], indexes: set[tuple[int, int]], stressed_clitic_indexes: set[int] | None = None
) -> list[str]:
    """
    Merge clitics with their main words in a phoneme list.

    param phonemes: List of phonemes with '_' representing spaces.
    param indexes: Set of tuples (main_word_index, clitic_index) indicating clitic relationships.
    param stressed_clitic_indexes: Token indexes of clitics whose stress should be preserved.
    return: A new phoneme list where clitics are joined with their main words.
    """
    if stressed_clitic_indexes is None:
        stressed_clitic_indexes = set()

    tokens_list: list[list[str]] = []
    start_token_index = 0
    for index, current_phon in enumerate(phonemes):
        if current_phon == '_':
            tokens_list.append(phonemes[start_token_index:index])
            start_token_index = index + 1
    tokens_list.append(phonemes[start_token_index:])

    phrasal_words = tokens_list[:]
    offset = 0
    main_word_cache: list[int] = []
    enclitic_cache: list[int] = []

    for main_word_index, clitic_index in sorted(indexes, key=lambda relation: relation[1]):
        try:
            if clitic_index > main_word_index:  # проклитика
                main_word = (
                    phrasal_words[main_word_index + offset]
                    if main_word_index in main_word_cache
                    else tokens_list[main_word_index]
                )
                main_word_cache.append(main_word_index)
                clitic = tokens_list[clitic_index]
                if clitic_index not in stressed_clitic_indexes:
                    clitic = [phoneme for phoneme in clitic if phoneme != '+']
                phrasal_words.remove(tokens_list[clitic_index])
                phrasal_words.remove(main_word)
                if clitic_index == 1:
                    phrasal_words.insert(0, main_word + clitic)
                else:
                    phrasal_words.insert(
                        clitic_index - main_word_cache.count(main_word_index),
                        main_word + clitic,
                    )
                offset -= 1
            else:  # энклитика
                main_word = (
                    phrasal_words[main_word_index - enclitic_cache.count(main_word_index)]
                    if main_word_index in enclitic_cache
                    else tokens_list[main_word_index]
                )
                main_word_cache.append(main_word_index)
                enclitic_cache.append(clitic_index)
                clitic = tokens_list[clitic_index]
                if clitic_index not in stressed_clitic_indexes:
                    clitic = [phoneme for phoneme in clitic if phoneme != '+']
                phrasal_words.remove(tokens_list[clitic_index])
                phrasal_words.remove(main_word)
                phrasal_words.insert(
                    clitic_index + offset + enclitic_cache.count(main_word_index),
                    clitic + main_word,
                )
                offset -= 1
        except (IndexError, ValueError):
            continue

    phrasal_words_result: list[str] = []
    for token in phrasal_words:
        phrasal_words_result.extend([*token, '_'])

    return phrasal_words_result[:-1]
