from pathlib import Path

from stressrnn import StressRNN

from .sounds import ru_vowel_symbols

ROOT_DIR = Path(__file__).resolve().parent

error_words_path = ROOT_DIR / '../data/error_words_stresses_default.txt'
with error_words_path.open(encoding='utf-8') as file:
    error_words_stresses = file.readlines()

stress_default_dict = {}
for word in error_words_stresses:
    stress_default_dict[word.replace('+', '').replace('\n', '')] = word.replace('\n', '')

stress_rnn = StressRNN()


def place_stress(token: str, stress_accuracy_threshold: float) -> str:
    """
    Place an accent (stress) in a Russian word.

    param token: Token without an accent.
    param stress_accuracy_threshold: Threshold for stress prediction accuracy.
    return: Word with an accent placed.
    """
    if token in stress_default_dict:
        return stress_default_dict[token]

    token_list = list(token)

    if 'ё' in token:
        # ё всегда ударная
        token_list.insert(token.index('ё') + 1, '+')
        return ''.join(token_list)

    # count vowels
    vowels_count = sum(1 for let in token if let in ru_vowel_symbols)

    if vowels_count == 1:
        # only one vowel, stress on it
        for i, let in enumerate(token):
            if let in ru_vowel_symbols:
                token_list.insert(i + 1, '+')
                break
        return ''.join(token_list)

    if vowels_count == 0:
        # no vowels, return as is
        return ''.join(token_list)

    # raise ValueError("Unfortunately, the automatic stress placement function is not yet available. "
    # f"Add stresses yourselves.\nThere is no stress for the word {token}")
    return stress_rnn.put_stress(token, accuracy_threshold=stress_accuracy_threshold)


def replace_stress(token: str) -> str:
    """
    Replace an accent so that it follows a stressed vowel instead of preceding it.

    param token: Token which needs to be refactored.
    return: Token with the accent moved after the stressed vowel.
    """
    plus_index = token.find('+')
    new_token_split = list(token)
    new_token_split.remove('+')  # remove the old accent
    new_token_split.insert(plus_index + 1, '+')  # insert it after the vowel

    return ''.join(new_token_split)


def remove_extra_stresses(string: str) -> str:
    """
    Keep only the first accent in the token and remove any additional accents.

    param string: Token that may contain multiple accents.
    return: Token with only the first accent retained.
    """
    first_plus_index = string.find('+')
    return string[: first_plus_index + 1] + string[first_plus_index + 1 :].replace('+', '')


def replace_stress_before(text: str | list[str]) -> list[str]:
    """
    Move the accent to the position before the stressed vowel.

    param text: Input text as a string or a list of characters.
    return: List of characters with the accent moved before the stressed vowel.
    """
    if isinstance(text, str):
        text = list(text)

    text_copy = text.copy()
    for i, char in enumerate(text):
        if char == '+':
            text_copy.pop(i)  # remove the old accent
            text_copy.insert(i - 1, '+')  # insert it before the vowel
    return text_copy


def put_stresses(
    tokens_list: list[str], stress_place: str = 'after', stress_accuracy_threshold: float = 0.86
) -> list[str]:
    """
    Put or replaces stresses in tokens.

    param tokens_list: List of tokens.
    param stress_place: 'after' - to place the stress symbol after the stressed vowel,
        'before' - to place the stress symbol before the stressed vowel.
    param stress_accuracy_threshold: Threshold for StressRNN accuracy when placing stress automatically.
    return: List of tokens with stress symbols applied or adjusted.
    """
    res = []
    for token in tokens_list:
        if ('+' in token) and (stress_place == 'before'):  # need to replace stress position
            res.append(replace_stress(token))
        elif '+' not in token:  # use StressRNN to place stress
            res.append(place_stress(token, stress_accuracy_threshold))
        else:
            res.append(token)  # stress is already correctly placed

    return res


"""
[
replace_stress(token) if ('+' in token) and (stress_place == 'before')  # need to replace
else place_stress(token, stress_accuracy_threshold) if ('+' not in token)  # use StressRNN
else token
for token in tokens_list
]
"""
