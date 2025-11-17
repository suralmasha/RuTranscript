from .sounds import allophones, zh_sh_ts


def get_neighbors(section: list[str], i: int) -> tuple[str, str]:
    """
    Safely get previous and next phonemes from a section.

    param section: Full phoneme list.
    param i: Index of the current phoneme.
    return: Tuple of (previous_phoneme, next_phoneme), or '' if out of range.
    """
    prev = section[i - 1] if i > 0 else ''
    next_ = section[i + 1] if i + 1 < len(section) else ''
    return prev, next_


def process_a(section: list[str], i: int) -> str:
    """
    Determine the allophone of /a/ depending on stress, neighboring consonants, and position.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /a/.
    """
    # Access helpers for neighbors and allophones
    prev, next_ = get_neighbors(section, i)
    prev_allo = allophones.get(prev, {})

    # Core rules (simplified example, keep your existing logic)
    if next_ == '+':
        return 'a' if 'hard' in prev_allo.get('palatalization', '') else 'æ'
    if next_ == '-':
        return 'ɐ'
    return 'ə'


def process_o(section: list[str], i: int) -> str:
    """
    Determine the allophone of /o/ depending on stress and surrounding context.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /o/.
    """
    prev, next_ = get_neighbors(section, i)
    prev_allo = allophones.get(prev, {})

    if next_ == '+':
        return 'o' if 'hard' in prev_allo.get('palatalization', '') else 'ɵ'
    if next_ == '-':
        return 'ɐ'
    return 'ə'


def process_e(section: list[str], i: int) -> str:
    """
    Determine the allophone of /e/ depending on stress, softness, and context.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /e/.
    """
    prev, next_ = get_neighbors(section, i)
    prev_allo = allophones.get(prev, {})

    if next_ == '+':
        return 'ɛ' if 'hard' in prev_allo.get('palatalization', '') else 'e'
    if next_ == '-':
        return 'ᵻ'
    return 'ə'


def process_u(section: list[str], i: int) -> str:
    """
    Determine the allophone of /u/ depending on stress and palatalization.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /u/.
    """
    prev, next_ = get_neighbors(section, i)
    prev_allo = allophones.get(prev, {})

    if next_ == '+':
        return 'ʉ' if 'soft' in prev_allo.get('palatalization', '') else 'u'
    return 'ʊ' if 'hard' in prev_allo.get('palatalization', '') else 'ᵿ'


def process_i(section: list[str], i: int) -> str:
    """
    Determine the allophone of /i/ depending on preceding consonant and stress.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /i/.
    """
    prev, next_ = get_neighbors(section, i)
    if prev in zh_sh_ts:
        return 'ɨ'
    if next_ != '+':
        return 'ɪ'
    return 'i'


def process_y(section: list[str], i: int) -> str:
    """
    Determine the allophone of /ɨ/ depending on stress and adjacent consonants.

    param section: Full phoneme list.
    param i: Index of the current vowel.
    return: Context-dependent allophone of /ɨ/.
    """
    prev, next_ = get_neighbors(section, i)
    prev_allo = allophones.get(prev, {})
    if next_ == '+':
        return 'ɨ̟' if prev_allo.get('place', '') == 'lingual, dental' else 'ɨ'
    if prev_allo.get('hissing', '') == 'hissing':
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
