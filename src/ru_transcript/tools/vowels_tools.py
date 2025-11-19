from .sounds import allophones, zh_sh_ts


def get_vowel_neighbors(section: list[str], i: int) -> tuple[dict[str, str | None], str]:
    """
    Safely get previous and next phonemes from a section.

    param section: Full phoneme list.
    param i: Index of the current phoneme.
    return: Tuple of previous allophone and stress symbol ('+' or '-'), or ('', '') if out of range.
    """
    prev = section[i - 1] if i > 0 else ''
    stress_symbol = section[i + 1] if i + 1 < len(section) else ''
    prev_allophone = allophones.get(prev, {})

    return prev_allophone, stress_symbol


def process_a(section: list[str], i: int) -> str:
    """
    Determine the allophone of /a/ depending on stress, neighboring consonants, and position.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /a/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if stress_symbol == '+':
        return 'a' if 'hard' in prev_allophone.get('palatalization', '') else 'æ'
    if stress_symbol == '-':
        return 'ɐ'
    return 'ə'


def process_o(section: list[str], i: int) -> str:
    """
    Determine the allophone of /o/ depending on stress and surrounding context.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /o/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if stress_symbol == '+':
        return 'o' if 'hard' in prev_allophone.get('palatalization', '') else 'ɵ'
    if stress_symbol == '-':
        return 'ɐ'
    return 'ə'


def process_e(section: list[str], i: int) -> str:
    """
    Determine the allophone of /e/ depending on stress, softness, and context.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /e/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if stress_symbol == '+':
        return 'ɛ' if 'hard' in prev_allophone.get('palatalization', '') else 'e'
    if stress_symbol == '-':
        return 'ᵻ'
    return 'ə'


def process_u(section: list[str], i: int) -> str:
    """
    Determine the allophone of /u/ depending on stress and palatalization.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /u/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if stress_symbol == '+':
        return 'ʉ' if 'soft' in prev_allophone.get('palatalization', '') else 'u'
    return 'ʊ' if 'hard' in prev_allophone.get('palatalization', '') else 'ᵿ'


def process_i(section: list[str], i: int) -> str:
    """
    Determine the allophone of /i/ depending on preceding consonant and stress.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /i/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if prev_allophone in zh_sh_ts:
        return 'ɨ'
    if stress_symbol != '+':
        return 'ɪ'
    return 'i'


def process_y(section: list[str], i: int) -> str:
    """
    Determine the allophone of /ɨ/ depending on stress and adjacent consonants.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /ɨ/.
    """
    prev_allophone, stress_symbol = get_vowel_neighbors(section, i)

    if stress_symbol == '+':
        return 'ɨ̟' if prev_allophone.get('place', '') == 'lingual, dental' else 'ɨ'
    if prev_allophone.get('hissing', '') == 'hissing':
        return 'ə'
    return 'ᵻ'


def vowels(section: list[str]) -> list[str]:
    """
    Replace vowels in the given phoneme section with appropriate allophones.

    param section: List of phonemes in the current word segment (with stress markers +, -).
    return: A modified phoneme list with context-dependent vowel allophones.
    """
    section = section.copy()
    for i, current_phon in enumerate(section):
        if current_phon == 'a':
            section[i] = process_a(section, i)
        elif current_phon == 'o':
            section[i] = process_o(section, i)
        elif current_phon == 'e':
            section[i] = process_e(section, i)
        elif current_phon == 'u':
            section[i] = process_u(section, i)
        elif current_phon == 'i':
            section[i] = process_i(section, i)
        elif current_phon == 'ɨ':
            section[i] = process_y(section, i)
    return section
