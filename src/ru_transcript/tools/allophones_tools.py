import spacy

from .sounds import allophones, ts, zh_sh_ts

nlp = spacy.load('ru_core_news_sm', disable=['tagger', 'morphologizer', 'attribute_ruler'])


def get_phon(segment: list[str], i: int) -> str:
    """
    ...

    param segment:
    param i:
    return:
    """
    try:
        phon = segment[i]
    except IndexError:
        phon = ''

    return phon


def get_allophone(segment: list[str], i: int) -> (str, dict[str, str | None]):
    """
    ...

    param segment:
    param i:
    return:
    """
    phon = get_phon(segment, i)

    return phon, allophones[phon]


def get_allophone_info(allophone: str) -> dict[str, str | None]:
    """
    Return all allophone phonetic information.

    param allophone: Input allophone.
    return: Phonetic information
    """
    return allophones[allophone]


def shch(section: list[str]) -> list[str]:
    """
    Merge specific consonant combinations into the long postalveolo-palatal fricative [ɕː].

    param section: List of phonemes in the input segment.
    return: List with merged affricate [ɕː] where applicable.
    """
    result = []
    i = 0

    while i < len(section):
        current = section[i]
        next_phon = section[i + 1] if i + 1 < len(section) else None

        if next_phon:
            pair = (current, next_phon)
            next_allophone = allophones.get(next_phon, {})

            if (current == 'ʐ' and next_allophone.get('voice') == 'voiceless' and next_phon != 's') or pair in {
                ('s', 't͡ɕ'),
                ('z', 't͡ɕ'),
                ('ʐ', 't͡ɕ'),
            }:
                result.append('ɕː')
                i += 2
                continue

        result.append(current)
        i += 1

    return result


def long_ge(section: list[str]) -> None:
    """
    Transform sequences like ('ʐ', 'ʐ') or ('z', 'ʐ') and voiced [ɕː] into [ʑː].

    param section: List of phonemes in the input segment.
    """
    for i, current_phon in enumerate(section[:-1]):
        _, next_allophone = get_allophone(section, i + 1)
        two_current = (get_phon(section, i), get_phon(section, i + 1))

        if two_current in [('ʐ', 'ʐ'), ('z', 'ʐ')]:
            section[i] = 'ʑː'
            del section[i + 1]
        elif (
            (current_phon == 'ɕː')
            and (next_allophone.get('voice', '') == 'voiced')
            and ('nasal' not in next_allophone.get('manner', ''))
        ):
            section[i] = 'ʑː'


def nasal_m_n(section: list[str]) -> None:
    """
    Transform 'm' or 'n' into labiodental [ɱ] before labial or labiodental consonants.

    param section: List of allophones in the input segment.
    """
    section_len = len(section)
    for i in range(section_len - 1):
        current = section[i]
        next_phon = section[i + 1]
        next_allophone = allophones.get(next_phon, {})

        if next_allophone.get('place') == 'labial, labiodental':
            if current in {'m', 'n'}:
                section[i] = 'ɱ'
            elif current in {'mʲ', 'nʲ'}:
                section[i] = 'ɱʲ'


def silent_r(section: list[str]) -> None:
    """
    Devoice [r] or [rʲ] to [r̥] or [r̥ʲ] before voiceless consonants.

    param section: List of allophones in the input segment.
    """
    section_len = len(section)
    for i, current_phon in enumerate(section):
        try:
            if (i < section_len - 1) and (allophones[section[i + 1]].get('voice', '') != 'voiceless'):
                continue
        except IndexError:
            break

        if current_phon == 'r':
            section[i] = 'r̥'
        elif current_phon == 'rʲ':
            section[i] = 'r̥ʲ'


def voiced_ts(section: list[str]) -> None:
    """
    Voiced [t͡s] becomes [d̻͡z̪] before a voiced consonant.

    param section: List of allophones in the input segment.
    """
    section_len = len(section)
    for i in range(section_len - 1):
        current = section[i]
        next_phon = section[i + 1]
        next_allophone = allophones.get(next_phon, {})

        if next_allophone.get('voice') == 'voiced' and current == 't͡s':
            section[i] = 'd̻͡z̪'


def first_jot(section: list[str]) -> None:
    """
    Replace a word-initial 'j' with the palatal approximant [ʝ].

    param section: List of phonemes in the input segment.
    """
    if section and section[0] == 'j':
        section[0] = 'ʝ'


def assimilative_palatalization(tokens_section: list[str], section: list[str]) -> None:
    """
    Apply palatalization to consonants based on following soft vowel or soft consonant, except for specific exceptions.

    param tokens_section: List of word tokens corresponding to the phoneme segment.
    param section: List of phonemes in the current segment.
    """
    exceptions = {'сосиска', 'злить', 'после', 'ёлка', 'день', 'транскрипция', 'джаз', 'неуклюжий', 'шахтёр'}
    # TODO: Вынести исключения в константы

    token_index = 0
    token = tokens_section[token_index]
    lemma = nlp(token)[0].lemma_

    section_len = len(section)

    for i, current_phon in enumerate(section):
        # Update token and lemma when encountering a boundary marker
        if current_phon == '_':
            token_index += 1
            token = tokens_section[token_index]
            lemma = nlp(token)[0].lemma_

        current_allophone = allophones.get(current_phon, {})

        if lemma in exceptions or 'i+zm' in token:
            continue

        # Find next non-symbol phoneme
        n = 1
        while i + n < section_len and allophones.get(section[i + n], {}).get('phon') == 'symb':
            n += 1
        next_phon = section[i + n] if i + n < section_len else None
        next_allophone = allophones.get(next_phon, {})

        # Skip specific cases where palatalization should not occur
        skip_conditions = (
            'l' in (next_phon or '')
            or (
                current_allophone.get('place') == 'lingual, dental'
                and next_allophone.get('place') == 'labial, labiodental'
            )
            or ('r' in current_phon)
            or ('ɡ' in current_phon)
            or ((current_phon[0] in 'tzk') and next_phon in {'rʲ', 'rʲː', 'r̥ʲ'})
            or (
                current_allophone.get('place') == 'labial, bilabial'
                and next_allophone.get('place') == 'labial, bilabial'
                and lemma != 'лобби'
            )
            or (
                current_allophone.get('place') in {'lingual, dental', 'labial, bilabial'}
                and next_allophone.get('place') == 'lingual, velar'
            )
        )
        if skip_conditions:
            continue

        # Apply palatalization if current consonant is hard and next is soft
        if (current_allophone.get('phon') == 'C' and 'ʲ' not in current_phon) and (
            'soft' in next_allophone.get('palatalization', '')
            and current_allophone.get('palatalization', ' ')[0] != 'a'
        ):
            section[i] = current_phon + 'ʲ'


def long_consonants(section: list[str]) -> None:
    """
    Merge identical consecutive consonants into long (geminate) consonants.

    param section: List of phonemes for the current segment.
    """
    n = 0
    section_iter = section[:]
    for i, current_phon in enumerate(section_iter):
        add_symb = False
        try:
            if allophones[section_iter[i + 1]]['phon'] != 'symb':
                next_phon = section_iter[i + 1]
            else:
                next_phon = section_iter[i + 2]
                add_symb = True
        except IndexError:
            next_phon = ''

        if (current_phon[0] in 'ʂbpfkstrlmngdz') and (current_phon == next_phon):
            del section[i + n]
            del section[i + n + add_symb]
            section.insert(i + n, current_phon + 'ː')
            n -= 1


def stunning(segment: list[str]) -> None:
    """
    Devoice voiced consonants at the end of a word or before pauses.

    param segment: List of phonemes in a word or phrase segment.
    """
    section_len = len(segment)
    for i, current_phon in enumerate(segment):
        try:
            if (i < section_len - 1) and (segment[i + 1] != '_'):
                continue
        except IndexError:
            break
        try:
            if (i < section_len - 1) and (
                (allophones[segment[i + 2]].get('voice', '') == 'voiced') or (allophones[segment[i + 2]]['phon'] == 'V')
            ):
                continue
        except IndexError:
            break

        allophone_info = allophones[current_phon]
        pair = allophone_info.get('pair', None)
        if (allophone_info.get('voice', '') == 'voiced') and (pair is not None):
            segment[i] = pair


def process_a(  # noqa: PLR0913
    section: list[str],
    next_phon: str,
    i: int,
    previous_phon: str,
    previous_allophone: dict[str, str | None],
    after_next_phon: str,
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_phon:
    param previous_allophone:
    param after_next_phon:
    """
    section_len = len(section)

    if (i != section_len - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_'):  # not last, not first
        if next_phon == '+':  # ударный (not last, not first)
            if previous_phon in zh_sh_ts:
                section[i] = 'ɐ.'
            elif ('hard' in previous_allophone.get('palatalization', '')) and (after_next_phon == 'l'):
                section[i] = 'ɑ'
            elif 'hard' in previous_allophone.get('palatalization', ''):
                section[i] = 'a'
            else:
                section[i] = 'æ'

        elif next_phon == '-':  # первый предударный (not last, not first)
            if previous_phon in zh_sh_ts:
                section[i] = 'ᵻ'
            elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                section[i] = 'ɐ'
            else:
                section[i] = 'ɪ'

        elif (
            (previous_allophone.get('hissing', '')) == 'hissing'
            or (previous_phon in ts)
            or ('hard' in previous_allophone.get('palatalization', ''))
        ) or (previous_allophone['phon'] == 'V'):
            section[i] = 'ə'
        else:
            section[i] = 'ɪ.'

    elif (i == section_len - 1) or (next_phon == '_'):  # заударные (last)
        if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
            section[i] = 'ə'
        elif 'hard' in previous_allophone.get('palatalization', ''):
            section[i] = 'ʌ'
        else:
            section[i] = 'æ.'

    elif next_phon == '-':
        section[i] = 'ɐ'  # первый предударный (first)
    elif next_phon != '+':
        section[i] = 'ə'  # заударные / второй предударный (first)


def process_o(
    section: list[str],
    next_phon: str,
    i: int,
    previous_phon: str,
    previous_allophone: dict[str, str | None],
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_phon:
    param previous_allophone:
    """
    section_len = len(section)

    if (i != section_len - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_'):  # not last, not first
        if next_phon == '+':  # ударный (not last, not first)
            if previous_phon in zh_sh_ts:
                section[i] = 'ɐ.'
            elif ('soft' in previous_allophone.get('palatalization', '')) or (previous_allophone['phon'] == 'V'):
                section[i] = 'ɵ'

        elif next_phon == '-':  # первый предударный (not last, not first)
            if previous_phon in zh_sh_ts:
                section[i] = 'ᵻ'
            elif 'hard' in previous_allophone.get('palatalization', ''):
                section[i] = 'ɐ'
            else:
                section[i] = 'ɪ'

        elif (
            (previous_allophone.get('hissing', '') == 'hissing')
            or (previous_phon in ts)
            or ('hard' in previous_allophone.get('palatalization', ''))
        ) or (previous_allophone['phon'] == 'V'):
            section[i] = 'ə'
        else:
            section[i] = 'ɪ.'

    elif (i == section_len - 1) or (next_phon == '_'):  # заударные (last)
        if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
            section[i] = 'ə'
        elif 'hard' in previous_allophone.get('palatalization', ''):
            section[i] = 'ʌ'
        else:
            section[i] = 'æ.'

    elif next_phon == '-':
        section[i] = 'ɐ'  # первый предударный (first)
    elif next_phon != '+':
        section[i] = 'ə'  # заударные / второй предударный (first)


def process_e(
    section: list[str],
    next_phon: str,
    i: int,
    previous_phon: str,
    previous_allophone: dict[str, str | None],
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_phon:
    param previous_allophone:
    """
    section_len = len(section)

    if (i != section_len - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_'):  # not last, not first
        if next_phon == '+':  # ударный (not last, not first)
            if previous_phon in zh_sh_ts:
                section[i] = 'ᵻ'
            elif 'hard' in previous_allophone.get('palatalization', ''):
                section[i] = 'ɛ'

        elif next_phon == '-':  # первый предударный (not last, not first)
            if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                section[i] = 'ə'
            elif 'hard' in previous_allophone.get('palatalization', ''):
                section[i] = 'ᵻ'
            else:
                section[i] = 'ɪ'

        elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
            section[i] = 'ə'
        elif 'hard' in previous_allophone.get('palatalization', ''):
            section[i] = 'ᵻ'
        else:
            section[i] = 'ɪ.'

    elif (i == section_len - 1) or (next_phon == '_'):  # заударные (last)
        if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
            section[i] = 'ə'
        elif 'hard' in previous_allophone.get('palatalization', ''):
            section[i] = 'ᵻ'
        else:
            section[i] = 'æ.'

    elif next_phon == '+':
        section[i] = 'ɛ'  # ударный (first)
    elif next_phon == '-':
        section[i] = 'ᵻ'  # первый предударный (first)
    else:
        section[i] = 'ɪ.'  # заударные / второй предударный (first)


def process_u(
    section: list[str],
    next_phon: str,
    i: int,
    previous_allophone: dict[str, str | None],
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_allophone:
    """
    section_len = len(section)

    if (i != section_len - 1) and (next_phon != '_'):  # not last
        if next_phon == '+':  # ударный (not last)
            if 'soft' in previous_allophone.get('palatalization', ''):
                section[i] = 'ʉ'

        elif 'hard' in previous_allophone.get('palatalization', ''):
            section[i] = 'ʊ'
        else:
            section[i] = 'ᵿ'

    elif 'hard' in previous_allophone.get('palatalization', ''):
        section[i] = 'ʊ'
    else:
        section[i] = 'ᵿ'


def process_i(
    section: list[str],
    next_phon: str,
    i: int,
    previous_phon: str,
    previous_allophone: dict[str, str | None],
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_phon:
    param previous_allophone:
    """
    if previous_allophone['phon'] == 'C':
        # после ж, ш, ц
        if previous_phon in zh_sh_ts:
            section[i] = 'ɨ'
        elif next_phon != '+':  # безударный
            section[i] = 'ɪ'


def process_ii(  # noqa: PLR0913
    section: list[str],
    next_phon: str,
    i: int,
    previous_phon: str,
    previous_allophone: dict[str, str | None],
    after_previous_allophone: dict[str, str | None],
    after_next_allophone: dict[str, str | None],
) -> None:
    """
    ...

    param section:
    param next_phon:
    param i:
    param previous_phon:
    param previous_allophone:
    """
    section_len = len(section)

    if (i != section_len - 1) and (next_phon != '_'):  # not last
        if next_phon == '+':  # ударный (not last)
            if (
                (previous_phon == 'l')
                and (section_len > 4)  # noqa: PLR2004
                and ('lab' in after_previous_allophone.get('place', ''))
            ):
                section[i] = 'ɯ̟ɨ̟'
            elif (
                previous_allophone.get('place', '') == 'lingual, dental'
                and after_next_allophone.get('place', '') == 'lingual, velar'
            ) or (
                previous_allophone.get('place', '') == 'lingual, palatinоdental'
                and after_next_allophone.get('place', '') == 'lingual, velar'
            ):
                section[i] = 'ɨ̟'

        # предударный / заунарный (not last)
        elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
            section[i] = 'ə'
        else:
            section[i] = 'ᵻ'

    elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):  # заударный (last)
        section[i] = 'ə'
    else:
        section[i] = 'ᵻ'


def vowels(section: list[str]) -> None:
    """
    Replace vowels in the given phoneme section with appropriate allophones.

    param section: List of phonemes in the current word segment (with stress markers +, -).
    """
    for i, current_phon in enumerate(section):
        next_phon = get_phon(section, i + 1)
        after_next_phon, after_next_allophone = get_allophone(section, i + 2)
        previous_phon, previous_allophone = get_allophone(section, i - 1)
        _, after_previous_allophone = get_allophone(section, i - 2)

        if current_phon == 'a':
            process_a(section, next_phon, i, previous_phon, previous_allophone, after_next_phon)
        elif current_phon == 'o':
            process_o(section, next_phon, i, previous_phon, previous_allophone)
        elif current_phon == 'e':
            process_e(section, next_phon, i, previous_phon, previous_allophone)
        elif current_phon == 'u':
            process_u(section, next_phon, i, previous_allophone)
        elif current_phon == 'i':
            process_i(section, next_phon, i, previous_phon, previous_allophone)

        elif current_phon == 'ɨ':
            process_ii(
                section, next_phon, i, previous_phon, previous_allophone, after_previous_allophone, after_next_allophone
            )


def labia_velar(segment: list[str]) -> list[str]:
    """
    Apply labialization or velarization to consonants before rounded or back vowels.

    param segment: List of phonemes in a word or phrase segment.
    return: A modified phoneme list with labialized (ʷ, ᶣ) or velarized (ˠ) consonants where applicable.
    """
    result_segment = []
    for i, current_phon in enumerate(segment):
        previous_phon = segment[i - 1] if i != 0 else ''

        current_allophone = allophones[current_phon]
        previous_allophone = allophones[previous_phon]
        if (
            (i != 0)
            and (current_allophone.get('round', '') == 'round')
            and (previous_phon != '_')
            and (previous_allophone['phon'] == 'C')
            and ('ʷ' not in previous_phon)
            and ('ᶣ' not in previous_phon)
        ):
            if 'ʲ' in previous_phon:
                new = previous_phon.replace('ʲ', '') + 'ᶣ'
                if new in allophones:
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)
            elif previous_allophone.get('palatalization', '') == 'asoft':
                new = previous_phon + 'ᶣ'
                if new in allophones:
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)
            else:
                new = previous_phon + 'ʷ'
                if new in allophones:
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)

        elif (
            (i != 0)
            and (current_allophone.get('round', '') == 'velarize')
            and (previous_phon != '_')
            and (previous_allophone['phon'] == 'C')
            and ('ˠ' not in previous_phon)
            and ('soft' not in previous_allophone.get('palatalization', ''))
        ):
            # в русском нет слов, начинающихся с ы
            new = previous_phon + 'ˠ'
            if new in allophones:
                del result_segment[-1]
                result_segment.append(new)
                result_segment.append(current_phon)

        else:
            result_segment.append(current_phon)

    return result_segment
