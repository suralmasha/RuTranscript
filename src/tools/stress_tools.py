from os.path import join, dirname, abspath

from stressrnn import StressRNN

from .sounds import rus_v

ROOT_DIR = dirname(abspath(__file__))

with open(join(ROOT_DIR, '../data/error_words_stresses_default.txt'), encoding='utf-8') as file:
    error_words_stresses = file.readlines()
stress_default_dict = {}
for word in error_words_stresses:
    stress_default_dict[word.replace('+', '').replace('\n', '')] = word.replace('\n', '')

stress_rnn = StressRNN()


def place_stress(token: str, stress_accuracy_threshold: float):
    """
    Places an accent.
    Args:
      :param token: token without an accent.
      :param stress_accuracy_threshold:
    """
    if token in stress_default_dict.keys():
        return stress_default_dict[token]

    token_list = list(token)

    if 'ё' in token:
        token_list.insert(token.index('ё') + 1, '+')
        return ''.join(token_list)

    vowels_count = sum(token.count(let) for let in token if let in rus_v)

    if vowels_count == 1:
        for i, let in enumerate(token):
            if let in rus_v:
                token_list.insert(i + 1, '+')
        return ''.join(token_list)

    if vowels_count == 0:
        return ''.join(token_list)

    # raise ValueError("Unfortunately, the automatic stress placement function is not yet available. "
    # f"Add stresses yourselves.\nThere is no stress for the word {token}")
    return stress_rnn.put_stress(token, accuracy_threshold=stress_accuracy_threshold)


def replace_stress(token):
    """
    Replaces an accent from a place before a stressed vowel to a place after it.
    Args:
      token (str): token which needs to be refactored.
    """
    plus_index = token.find('+')
    new_token_split = list(token)
    new_token_split.remove('+')
    new_token_split.insert(plus_index + 1, '+')
    return ''.join(new_token_split)


def remove_extra_stresses(string: str):
    first_plus_index = string.find('+')
    return string[:first_plus_index + 1] + string[first_plus_index + 1:].replace('+', '')


def replace_stress_before(text):
    if isinstance(text, str):
        text = list(text)

    text_copy = text.copy()
    for i, char in enumerate(text):
        if char == '+':
            text_copy.pop(i)
            text_copy.insert(i - 1, '+')
    return text_copy


def put_stresses(tokens_list: list, stress_place: str = 'after', stress_accuracy_threshold: float = 0.86):
    """
    Puts or replaces stresses.

    :param tokens_list: List of tokens.
    :param stress_place: 'after' - to place the stress symbol after the stressed vowel,
        'before' - to place the stress symbol before the stressed vowel.
    :param stress_accuracy_threshold: A threshold for the accuracy of stress placement for StressRNN.
    :return: List of tokens.
    """
    res = []
    for token in tokens_list:
        if ('+' in token) and (stress_place == 'before'):  # need to replace
            res.append(replace_stress(token))
        elif '+' not in token:  # use StressRNN
            res.append(place_stress(token, stress_accuracy_threshold))
        else:
            res.append(token)

    return res


"""
[
replace_stress(token) if ('+' in token) and (stress_place == 'before')  # need to replace
else place_stress(token, stress_accuracy_threshold) if ('+' not in token)  # use StressRNN
else token
for token in tokens_list
]
"""