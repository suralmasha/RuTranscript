from .sounds import allophones, ru_vowel_symbols

# def is_jotised_vowel(symbol: str) -> bool:
#     """
#     Check if a symbol represents a jotised (i.e., iotated) vowel.
#
#     param symbol: Phoneme symbol to check.
#     return: True if the symbol is jotised (e.g., 'ja', 'ju', 'je', 'jo'); False otherwise.
#     """
#     return symbol in jotised
#
#
# def replace_jotised_after_vowel(phonemes: list[str]) -> list[str]:
#     """
#     Replace jotised vowels that follow another vowel with a glide [j] + non-jotised vowel.
#
#     param phonemes: List of phonemes in the current segment.
#     return: Updated phoneme list with [j] inserted between vowels where needed.
#     """
#     result = []
#     for i, ph in enumerate(phonemes):
#         if i > 0 and is_jotised_vowel(ph) and phonemes[i - 1] in 'aeiouɐɵɨʊʌ':
#             result.append('j')
#             result.append(ph.replace('ʲ', ''))
#         else:
#             result.append(ph)
#
#     return result
#
#
# def replace_jotised_after_consonant(phonemes: list[str]) -> list[str]:
#     """
#     Adjust consonants before jotised vowels by adding palatalization.
#
#     param phonemes: List of phonemes in the current segment.
#     return: Updated phoneme list with preceding consonants palatalized before jotised vowels.
#     """
#     result = []
#     for i, ph in enumerate(phonemes):
#         if i > 0 and is_jotised_vowel(ph) and phonemes[i - 1].isalpha():
#             prev = phonemes[i - 1]
#             if not prev.endswith('ʲ'):
#                 result[-1] = prev + 'ʲ'
#             result.append(ph.replace('ʲ', ''))
#         else:
#             result.append(ph)
#
#     return result
#
#
# def handle_word_initial_jotised(phonemes: list[str]) -> list[str]:
#     """
#     Handle word-initial jotised vowels (they stay with initial [j] glide).
#
#     param phonemes: List of phonemes in the current segment.
#     return: Updated phoneme list where word-initial jotised vowels are prefixed with [j].
#     """
#     if phonemes and is_jotised_vowel(phonemes[0]):
#         phonemes = ['j', phonemes[0].replace('ʲ', ''), *phonemes[1:]]
#
#     return phonemes
#
#
# def fix_jotised(phonemes: list[str]) -> list[str]:
#     """
#     Fix jotised vowel representations based on their phonetic context.
#
#     param phonemes: List of phonemes in the current segment.
#     return: A modified phoneme list with correct handling of jotised vowels.
#     """
#     phonemes = handle_word_initial_jotised(phonemes)
#     phonemes = replace_jotised_after_vowel(phonemes)
#
#     return replace_jotised_after_consonant(phonemes)


def fix_jotised(phonemes_list_section: list[str], letters_list_section: list[str]) -> list[str]:  # noqa: PLR0912, PLR0915
    """
    Adjust phoneme sequence for jotised (palatalized and iotated) contexts in Russian.

    param phonemes_list_section: List of phonemes in the current segment.
    param letters_list_section: Corresponding list of graphemes (letters).
    return: A copy of the phoneme list with inserted or modified [j] and palatalized consonants.
    """
    phonemes_list_section_copy = phonemes_list_section.copy()
    # ---- jotised vowels and i ----
    phonemes_list_to_iterate = phonemes_list_section_copy[:]
    letters_list_to_iterate = letters_list_section[:]

    for i, let in enumerate(letters_list_to_iterate):
        try:
            next_let = letters_list_to_iterate[i + 1]
        except IndexError:
            next_let = ''
        if (let == 'д') and (next_let == 'ж'):
            del letters_list_to_iterate[i + 1]
            letters_list_to_iterate[i] = 'дж'
        elif next_let in ['ь', 'ъ']:
            del letters_list_to_iterate[i + 1]
            letters_list_to_iterate[i] = letters_list_to_iterate[i] + next_let

    n = 0
    for i, current_phon in enumerate(phonemes_list_to_iterate):
        sub_symb = False
        current_allophone = allophones[current_phon]
        if current_allophone['phon'] == 'symb':
            continue
        if current_phon == 'j' and letters_list_to_iterate[i] != 'й':
            letters_list_to_iterate.insert(i, 'й')
        current_let = letters_list_to_iterate[i]
        try:
            if allophones[phonemes_list_to_iterate[i - 1]]['phon'] != 'symb':
                previous_let = letters_list_to_iterate[i - 1]
                previous_phon = phonemes_list_to_iterate[i - 1]
            else:
                previous_let = letters_list_to_iterate[i - 2]
                previous_phon = phonemes_list_to_iterate[i - 2]
                sub_symb = True
        except IndexError:
            previous_let = ''
            previous_phon = ''
        try:
            next_let = letters_list_to_iterate[i + 1]
        except IndexError:
            next_let = ''
        try:
            after_next_let = letters_list_to_iterate[i + 2]
        except IndexError:
            after_next_let = ''

        previous_allophone = allophones[previous_phon]
        if (current_let == 'о') and (previous_let[-1] == 'ь') and (next_let == '+'):
            phonemes_list_section_copy.insert(i + n, 'j')
            n += 1

        elif current_let in ['ё', 'е', 'я', 'ю']:
            if previous_let[-1] in ['ь', 'ъ']:
                if (
                    (previous_allophone['phon'] == 'C')
                    and ('ʲ' not in previous_phon)
                    and (previous_allophone['palatalization'][0] != 'a')
                ):
                    phonemes_list_section_copy[i + n - 1 - sub_symb] = previous_phon + 'ʲ'
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

            elif previous_let in ru_vowel_symbols:
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

            elif (
                (current_let != 'э')
                and (previous_allophone['phon'] == 'C')
                and ('ʲ' not in previous_phon)
                and ('a' not in previous_allophone['palatalization'][0])
            ):
                phonemes_list_section_copy[i + n - 1 - sub_symb] = previous_phon + 'ʲ'

            elif (after_next_let == '+') and (previous_phon != 'j'):
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

        elif current_let == 'и':
            if sub_symb and (phonemes_list_to_iterate[i - 1] == '_') and (previous_allophone['phon'] == 'C'):
                phonemes_list_section_copy[i + n] = 'ɨ'

            elif previous_let[-1] in {'ь', 'ъ'}:
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

            elif (
                (previous_allophone['phon'] == 'C')
                and ('ʲ' not in previous_phon)
                and (previous_allophone['palatalization'][0] != 'a')
            ):
                phonemes_list_section_copy[i + n - 1 - sub_symb] = previous_phon + 'ʲ'

    return phonemes_list_section_copy
