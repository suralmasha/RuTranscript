import spacy

from .sounds import allophones, ts, zh_sh_ts

nlp = spacy.load('ru_core_news_sm', disable=['tagger', 'morphologizer', 'attribute_ruler'])


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


def long_ge(section: list[str]) -> list[str]:
    """
    Transform sequences like ('ʐ', 'ʐ') or ('z', 'ʐ') and voiced [ɕː] into [ʑː].

    param section: List of phonemes in the input segment.
    return: List with transformed [ʑː] sequences.
    """
    section_copy = section.copy()
    for i, current_phon in enumerate(section_copy[:-1]):
        try:
            next_phon = section_copy[i + 1]
        except IndexError:
            next_phon = ''
        try:
            two_current = (section_copy[i], section_copy[i + 1])
        except IndexError:
            two_current = ''

        next_allophone = allophones[next_phon]
        if two_current in [('ʐ', 'ʐ'), ('z', 'ʐ')]:
            section_copy[i] = 'ʑː'
            del section_copy[i + 1]
        elif (
            (current_phon == 'ɕː')
            and (next_allophone.get('voice', '') == 'voiced')
            and ('nasal' not in next_allophone.get('manner', ''))
        ):
            section_copy[i] = 'ʑː'

    return section_copy


def nasal_m_n(section: list[str]) -> list[str]:
    """
    Transform 'm' or 'n' into labiodental [ɱ] before labial or labiodental consonants.

    param section: List of phonemes in the input segment.
    return: List with nasal consonants adjusted to labiodental allophones where applicable.
    """
    result = section.copy()

    for i in range(len(result) - 1):
        current = result[i]
        next_phon = result[i + 1]
        next_allophone = allophones.get(next_phon, {})

        if next_allophone.get('place') == 'labial, labiodental':
            if current in {'m', 'n'}:
                result[i] = 'ɱ'
            elif current in {'mʲ', 'nʲ'}:
                result[i] = 'ɱʲ'

    return result


def silent_r(section: list[str]) -> list[str]:
    """
    Devoice [r] or [rʲ] to [r̥] or [r̥ʲ] before voiceless consonants.

    param section: List of phonemes in the input segment.
    return: List with devoiced [r] where applicable.
    """
    section_copy = section.copy()
    for i, current_phon in enumerate(section_copy):
        try:
            if (i < len(section_copy) - 1) and (allophones[section_copy[i + 1]].get('voice', '') != 'voiceless'):
                continue
        except IndexError:
            break

        if current_phon == 'r':
            section_copy[i] = 'r̥'
        elif current_phon == 'rʲ':
            section_copy[i] = 'r̥ʲ'

    return section_copy


def voiced_ts(section: list[str]) -> list[str]:
    """
    Voiced [t͡s] becomes [d̻͡z̪] before a voiced consonant.

    param section: List of phonemes in the input segment.
    return: List with 't͡s' voiced to 'd̻͡z̪' where applicable.
    """
    result = section.copy()

    for i in range(len(result) - 1):
        current = result[i]
        next_phon = result[i + 1]
        next_allophone = allophones.get(next_phon, {})

        if next_allophone.get('voice') == 'voiced' and current == 't͡s':
            result[i] = 'd̻͡z̪'

    return result


def first_jot(phonemes_list_section: list[str]) -> list[str]:
    """
    Replace a word-initial 'j' with the palatal approximant [ʝ].

    param phonemes_list_section: List of phonemes in the input segment.
    return: Modified phoneme list with initial 'j' replaced by 'ʝ'.
    """
    result = phonemes_list_section.copy()

    if result and result[0] == 'j':
        result[0] = 'ʝ'

    return result


def assimilative_palatalization(tokens_section: list[str], phonemes_list_section: list[str]) -> list[str]:
    """
    Apply palatalization to consonants based on following soft vowel or soft consonant, except for specific exceptions.

    param tokens_section: List of word tokens corresponding to the phoneme segment.
    param phonemes_list_section: List of phonemes in the current segment.
    return: Modified phoneme list with assimilative palatalization applied.
    """
    result = phonemes_list_section.copy()
    exceptions = {'сосиска', 'злить', 'после', 'ёлка', 'день', 'транскрипция', 'джаз', 'неуклюжий', 'шахтёр'}

    token_index = 0
    token = tokens_section[token_index]
    lemma = nlp(token)[0].lemma_

    for i, current_phon in enumerate(result):
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
        while i + n < len(result) and allophones.get(result[i + n], {}).get('phon') == 'symb':
            n += 1
        next_phon = result[i + n] if i + n < len(result) else None
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
            result[i] = current_phon + 'ʲ'

    return result


def long_consonants(phonemes_list_section: list[str]) -> list[str]:
    """
    Merge identical consecutive consonants into long (geminate) consonants.

    param phonemes_list_section: List of phonemes for the current segment.
    return: A modified phoneme list with long consonants marked by `ː`.
    """
    n = 0
    phonemes_list_to_iterate = phonemes_list_section[:]
    for i, current_phon in enumerate(phonemes_list_to_iterate):
        add_symb = False
        try:
            if allophones[phonemes_list_to_iterate[i + 1]]['phon'] != 'symb':
                next_phon = phonemes_list_to_iterate[i + 1]
            else:
                next_phon = phonemes_list_to_iterate[i + 2]
                add_symb = True
        except IndexError:
            next_phon = ''

        if (current_phon[0] in 'ʂbpfkstrlmngdz') and (current_phon == next_phon):
            del phonemes_list_section[i + n]
            del phonemes_list_section[i + n + add_symb]
            phonemes_list_section.insert(i + n, current_phon + 'ː')
            n -= 1

    return phonemes_list_section


def stunning(segment: list[str]) -> list[str]:
    """
    Devoice voiced consonants at the end of a word or before pauses.

    param segment: List of phonemes in a word or phrase segment.
    return: A modified phoneme list with final voiced consonants devoiced.
    """
    segment_copy = segment.copy()
    for i, current_phon in enumerate(segment_copy):
        try:
            if (i < len(segment_copy) - 1) and (segment_copy[i + 1] != '_'):
                continue
        except IndexError:
            break
        try:
            if (i < len(segment_copy) - 1) and (
                (allophones[segment_copy[i + 2]].get('voice', '') == 'voiced')
                or (allophones[segment_copy[i + 2]]['phon'] == 'V')
            ):
                continue
        except IndexError:
            break

        allophone_info = allophones[current_phon]
        pair = allophone_info.get('pair', None)
        if (allophone_info.get('voice', '') == 'voiced') and (pair is not None):
            segment_copy[i] = pair

    return segment_copy


def vowels(section: list[str]) -> list[str]:  # noqa: PLR0912, PLR0915
    """
    Replace vowels in the given phoneme section with appropriate allophones.

    param section: List of phonemes in the current word segment (with stress markers +, -).
    return: A modified phoneme list with context-dependent vowel allophones.
    """
    section_copy = section.copy()
    for i, current_phon in enumerate(section_copy):
        try:
            next_phon = section_copy[i + 1]
        except IndexError:
            next_phon = ''
        try:
            after_next_phon = section_copy[i + 2]
        except IndexError:
            after_next_phon = ''
        try:
            previous_phon = section_copy[i - 1]
        except IndexError:
            previous_phon = ''
        try:
            after_previous_phon = section_copy[i - 2]
        except IndexError:
            after_previous_phon = ''

        previous_allophone = allophones[previous_phon]
        after_next_allophone = allophones[after_next_phon]
        after_previous_allophone = allophones[after_previous_phon]
        if current_phon == 'a':
            if (
                (i != len(section_copy) - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_')
            ):  # not last, not first
                if next_phon == '+':  # ударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ɐ.'
                    elif ('hard' in previous_allophone.get('palatalization', '')) and (after_next_phon == 'l'):
                        section_copy[i] = 'ɑ'
                    elif 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'a'
                    else:
                        section_copy[i] = 'æ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ᵻ'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        section_copy[i] = 'ɐ'
                    else:
                        section_copy[i] = 'ɪ'

                elif (
                    (previous_allophone.get('hissing', '')) == 'hissing'
                    or (previous_phon in ts)
                    or ('hard' in previous_allophone.get('palatalization', ''))
                ) or (previous_allophone['phon'] == 'V'):
                    section_copy[i] = 'ə'
                else:
                    section_copy[i] = 'ɪ.'

            elif (i == len(section_copy) - 1) or (next_phon == '_'):  # заударные (last)
                if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ʌ'
                else:
                    section_copy[i] = 'æ.'

            elif next_phon == '-':
                section_copy[i] = 'ɐ'  # первый предударный (first)
            elif next_phon != '+':
                section_copy[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'o':
            if (
                (i != len(section_copy) - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_')
            ):  # not last, not first
                if next_phon == '+':  # ударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ɐ.'
                    elif ('soft' in previous_allophone.get('palatalization', '')) or (
                        previous_allophone['phon'] == 'V'
                    ):
                        section_copy[i] = 'ɵ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ᵻ'
                    elif 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ɐ'
                    else:
                        section_copy[i] = 'ɪ'

                elif (
                    (previous_allophone.get('hissing', '') == 'hissing')
                    or (previous_phon in ts)
                    or ('hard' in previous_allophone.get('palatalization', ''))
                ) or (previous_allophone['phon'] == 'V'):
                    section_copy[i] = 'ə'
                else:
                    section_copy[i] = 'ɪ.'

            elif (i == len(section_copy) - 1) or (next_phon == '_'):  # заударные (last)
                if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ʌ'
                else:
                    section_copy[i] = 'æ.'

            elif next_phon == '-':
                section_copy[i] = 'ɐ'  # первый предударный (first)
            elif next_phon != '+':
                section_copy[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'e':
            if (
                (i != len(section_copy) - 1) and (next_phon != '_') and (i != 0) and (previous_phon != '_')
            ):  # not last, not first
                if next_phon == '+':  # ударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ᵻ'
                    elif 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ɛ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                        section_copy[i] = 'ə'
                    elif 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ᵻ'
                    else:
                        section_copy[i] = 'ɪ'

                elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ᵻ'
                else:
                    section_copy[i] = 'ɪ.'

            elif (i == len(section_copy) - 1) or (next_phon == '_'):  # заударные (last)
                if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ᵻ'
                else:
                    section_copy[i] = 'æ.'

            elif next_phon == '+':
                section_copy[i] = 'ɛ'  # ударный (first)
            elif next_phon == '-':
                section_copy[i] = 'ᵻ'  # первый предударный (first)
            else:
                section_copy[i] = 'ɪ.'  # заударные / второй предударный (first)

        elif current_phon == 'u':
            if (i != len(section_copy) - 1) and (next_phon != '_'):  # not last
                if next_phon == '+':  # ударный (not last)
                    if 'soft' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ʉ'

                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ʊ'
                else:
                    section_copy[i] = 'ᵿ'

            elif 'hard' in previous_allophone.get('palatalization', ''):
                section_copy[i] = 'ʊ'
            else:
                section_copy[i] = 'ᵿ'

        elif (current_phon == 'i') and (previous_allophone['phon'] == 'C'):
            # после ж, ш, ц
            if previous_phon in zh_sh_ts:
                section_copy[i] = 'ɨ'
            elif next_phon != '+':  # безударный
                section_copy[i] = 'ɪ'

        elif current_phon == 'ɨ':
            if (i != len(section_copy) - 1) and (next_phon != '_'):  # not last
                if next_phon == '+':  # ударный (not last)
                    if (
                        (previous_phon == 'l')
                        and (len(section_copy) > 4)  # noqa: PLR2004
                        and ('lab' in after_previous_allophone.get('place', ''))
                    ):
                        section_copy[i] = 'ɯ̟ɨ̟'
                    elif (
                        previous_allophone.get('place', '') == 'lingual, dental'
                        and after_next_allophone.get('place', '') == 'lingual, velar'
                    ) or (
                        previous_allophone.get('place', '') == 'lingual, palatinоdental'
                        and after_next_allophone.get('place', '') == 'lingual, velar'
                    ):
                        section_copy[i] = 'ɨ̟'

                # предударный / заунарный (not last)
                elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                else:
                    section_copy[i] = 'ᵻ'

            elif (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):  # заударный (last)
                section_copy[i] = 'ə'
            else:
                section_copy[i] = 'ᵻ'

    return section_copy


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
