import spacy

from .sounds import allophones, rus_v

nlp = spacy.load('ru_core_news_sm', disable=["tagger", "morphologizer", "attribute_ruler"])


def get_allophone_info(allophone):
    return allophones[allophone]


def shch(section: list):
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
        if ((current_phon == 'ʐ') and (next_allophone.get('voice', '') == 'voiceless') and (next_phon != 's')) \
                or (two_current in {('s', 't͡ɕ'), ('z', 't͡ɕ'), ('ʐ', 't͡ɕ')}):
            section_copy[i] = 'ɕː'
            del section_copy[i + 1]

    return section_copy


def long_ge(section: list):
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
        elif (current_phon == 'ɕː') and (next_allophone.get('voice', '') == 'voiced') \
                and ('nasal' not in next_allophone.get('manner', '')):
            section_copy[i] = 'ʑː'

    return section_copy


def nasal_m_n(section: list):
    section_copy = section.copy()
    for i, current_phon in enumerate(section_copy[:-1]):
        try:
            if allophones[section_copy[i + 1]].get('place', '') != 'labial, labiodental':
                continue
        except IndexError:
            break

        if current_phon in ['m', 'n']:
            section_copy[i] = 'ɱ'
        elif current_phon in ['mʲ', 'nʲ']:
            section_copy[i] = 'ɱʲ'

    return section_copy


def silent_r(section: list):
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


def voiced_ts(section: list):
    section_copy = section.copy()
    for i, current_phon in enumerate(section_copy):
        try:
            if allophones[section_copy[i + 1]].get('voice', '') != 'voiced':
                continue
        except IndexError:
            break

        if current_phon == 't͡s':
            section_copy[i] = 'd̻͡z̪'

    return section_copy


def first_jot(phonemes_list_section):
    phonemes_list_section_copy = phonemes_list_section.copy()
    if phonemes_list_section_copy[0] == 'j':
        phonemes_list_section_copy[0] = 'ʝ'

    return phonemes_list_section_copy


def fix_jotised(phonemes_list_section, letters_list_section):
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

        elif current_let in 'ё е я ю'.split():
            if previous_let[-1] in ['ь', 'ъ']:
                if (previous_allophone['phon'] == 'C')\
                        and ('ʲ' not in previous_phon)\
                        and (previous_allophone['palatalization'][0] != 'a'):
                    phonemes_list_section_copy[i + n - 1 - sub_symb] = previous_phon + 'ʲ'
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

            elif previous_let in rus_v:
                phonemes_list_section_copy.insert(i + n, 'j')
                n += 1

            elif (current_let != 'э') \
                    and (previous_allophone['phon'] == 'C') \
                    and ('ʲ' not in previous_phon) \
                    and ('a' not in previous_allophone['palatalization'][0]):
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

            elif (previous_allophone['phon'] == 'C') \
                    and ('ʲ' not in previous_phon) \
                    and (previous_allophone['palatalization'][0] != 'a'):
                phonemes_list_section_copy[i + n - 1 - sub_symb] = previous_phon + 'ʲ'

    return phonemes_list_section_copy


def assimilative_palatalization(tokens_section, phonemes_list_section):
    phonemes_list_section_copy = phonemes_list_section.copy()
    exceptions = 'сосиска злить после ёлка день транскрипция джаз неуклюжий шахтёр'.split()

    token_index = 0
    token = tokens_section[token_index]
    nlp_token = nlp(token)[0]
    lemma = nlp_token.lemma_

    for i, current_phon in enumerate(phonemes_list_section_copy):
        if current_phon == '_':
            token_index += 1
            token = tokens_section[token_index]
            nlp_token = nlp(token)[0]
            lemma = nlp_token.lemma_

        current_allophone = allophones[current_phon]
        if (lemma not in exceptions) and ('i+zm' not in token):
            try:
                n = 1
                next_phon = phonemes_list_section_copy[i + n]
                next_allophone = allophones[next_phon]
                while next_allophone['phon'] == 'symb':
                    n += 1
                    next_phon = phonemes_list_section_copy[i + n]
                    next_allophone = allophones[next_phon]
            except IndexError:
                next_phon = ''
                next_allophone = allophones[next_phon]

            # не смягчение перед [л] (для, глина, длинный, блин, злиться, влить, тлеть)
            if 'l' in next_phon:
                continue

            # доминирует не смягчение зубных перед мягкими губно-зубными ([д’в’]е́рь - [дв’]е́рь)
            elif (current_allophone.get('place', '') == 'lingual, dental') \
                    and (next_allophone.get('place', '') == 'labial, labiodental'):
                continue

            # доминирует не смягчение губных перед мягкими губными (лю[б’в’]и́ - лю[бв’]и́)
            elif (current_allophone.get('place', '') == 'labial, bilabial')\
                    and (next_allophone.get('place', '') == 'labial, bilabial') and lemma != 'лобби':
                continue

            # не смягчение губных и зубных перед мягкими заднеязычными (гри[пк’]и́; ко́[фт’]е)
            elif (current_allophone.get('place', '') in ['lingual, dental', 'labial, bilabial'])\
                    and (next_allophone.get('place', '') == 'lingual, velar'):
                continue

            # не смягчение звуков [р], [г] перед мягкими согласными (а[рт’]и́ст, а[гн’]ия)
            elif ('r' in current_phon) or ('ɡ' in current_phon):
                continue

            # не смягчение звуков [т], [з], [к] перед [р] ([тр’]и́, тряска, зрелый, транскрипция)
            elif ('t' in current_phon or 'z' in current_phon or 'k' in current_phon)\
                    and (next_phon in {'rʲ', 'rʲː', 'r̥ʲ'}):
                continue

            elif (current_allophone['phon'] == 'C') and (current_allophone.get('palatalization', ' ')[0] != 'a')\
                    and ('ʲ' not in current_phon) and ('soft' in next_allophone.get('palatalization', '')):
                phonemes_list_section_copy[i] = current_phon + 'ʲ'

    return phonemes_list_section_copy


def long_consonants(phonemes_list_section):
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


ts = {'t͡s', 't͡sʷ', 't͡sˠ', 'd͡ʒᶣ', 'd͡ʒˠ', 'd̻͡z̪', 'd͡ʒ'}
zh_sh_ts = {'ʐ', 'ʐʷ', 'ʐˠ', 'ʑː', 'ʑːʷ', 'ʑːˠ', 'ʑʲː', 'ʑːᶣ',
            'ʂ', 'ʂʷ', 'ʂˠ', 'ʂː', 'ʂːʷ', 'ʂːˠ',
            't͡s', 't͡sʷ', 't͡sˠ', 'd͡ʒᶣ', 'd͡ʒˠ', 'd̻͡z̪', 'd͡ʒ'}


def stunning(segment: list):
    segment_copy = segment.copy()
    for i, current_phon in enumerate(segment_copy):
        try:
            if (i < len(segment_copy) - 1) and (segment_copy[i + 1] != '_'):
                continue
        except IndexError:
            break
        try:
            if (i < len(segment_copy) - 1) and ((allophones[segment_copy[i + 2]].get('voice', '') == 'voiced')
                                           or (allophones[segment_copy[i + 2]]['phon'] == 'V')):
                continue
        except IndexError:
            break

        allophone_info = allophones[current_phon]
        pair = allophone_info.get('pair', None)
        if (allophone_info.get('voice', '') == 'voiced') and (pair is not None):
            segment_copy[i] = pair

    return segment_copy


def vowels(section: list):
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
            if (i != len(section_copy) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

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

                else:  # заударные / второй предударный (not last, not first)
                    if ((previous_allophone.get('hissing', '')) == 'hissing' or (previous_phon in ts)
                        or ('hard' in previous_allophone.get('palatalization', ''))) \
                            or (previous_allophone['phon'] == 'V'):
                        section_copy[i] = 'ə'
                    else:
                        section_copy[i] = 'ɪ.'

            elif (i == len(section_copy) - 1) or (next_phon == '_'):   # заударные (last)
                if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
                    section_copy[i] = 'ə'
                elif 'hard' in previous_allophone.get('palatalization', ''):
                    section_copy[i] = 'ʌ'
                else:
                    section_copy[i] = 'æ.'

            else:
                if next_phon == '-':
                    section_copy[i] = 'ɐ'  # первый предударный (first)
                elif next_phon != '+':
                    section_copy[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'o':
            if (i != len(section_copy) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

                if next_phon == '+':  # ударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ɐ.'
                    elif ('soft' in previous_allophone.get('palatalization', '')) \
                            or (previous_allophone['phon'] == 'V'):
                        section_copy[i] = 'ɵ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if previous_phon in zh_sh_ts:
                        section_copy[i] = 'ᵻ'
                    elif 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ɐ'
                    else:
                        section_copy[i] = 'ɪ'

                else:  # заударные/второй предударный (not last, not first)
                    if ((previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts)
                        or ('hard' in previous_allophone.get('palatalization', ''))) \
                            or (previous_allophone['phon'] == 'V'):
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

            else:
                if next_phon == '-':
                    section_copy[i] = 'ɐ'  # первый предударный (first)
                elif next_phon != '+':
                    section_copy[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'e':
            if (i != len(section_copy) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

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

                else:  # заударные / второй предударный (not last, not first)
                    if (previous_allophone.get('hissing', '') == 'hissing') or (previous_phon in ts):
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

            else:
                if next_phon == '+':
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

                else:  # первый / второй предударный / заударные (not last)
                    if 'hard' in previous_allophone.get('palatalization', ''):
                        section_copy[i] = 'ʊ'
                    else:
                        section_copy[i] = 'ᵿ'

            else:  # первый / второй предударный / заударные (last)
                if 'hard' in previous_allophone.get('palatalization', ''):
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
                    if (previous_phon == 'l') and (len(section_copy) > 4) \
                            and ('lab' in after_previous_allophone.get('place', '')):
                        section_copy[i] = 'ɯ̟ɨ̟'
                    elif (previous_allophone.get('place', '') == 'lingual, dental'
                          and after_next_allophone.get('place', '') == 'lingual, velar')\
                            or (previous_allophone.get('place', '') == 'lingual, palatinоdental'
                                and after_next_allophone.get('place', '') == 'lingual, velar'):
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


def labia_velar(segment: list):
    result_segment = []
    for i, current_phon in enumerate(segment):
        if i != 0:
            previous_phon = segment[i - 1]
        else:
            previous_phon = ''

        current_allophone = allophones[current_phon]
        previous_allophone = allophones[previous_phon]
        if (i != 0) and (current_allophone.get('round', '') == 'round') and (previous_phon != '_')\
                and (previous_allophone['phon'] == 'C') and ('ʷ' not in previous_phon) and ('ᶣ' not in previous_phon):
            if 'ʲ' in previous_phon:
                new = previous_phon.replace('ʲ', '') + 'ᶣ'
                if new in allophones.keys():
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)
            elif previous_allophone.get('palatalization', '') == 'asoft':
                new = previous_phon + 'ᶣ'
                if new in allophones.keys():
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)
            else:
                new = previous_phon + 'ʷ'
                if new in allophones.keys():
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)

        elif (i != 0) and (current_allophone.get('round', '') == 'velarize') and (previous_phon != '_')\
                and (previous_allophone['phon'] == 'C') and ('ˠ' not in previous_phon)\
                and ('soft' not in previous_allophone.get('palatalization', '')):
            # в русском нет слов, начинающихся с ы
            new = previous_phon + 'ˠ'
            if new in allophones.keys():
                del result_segment[-1]
                result_segment.append(new)
                result_segment.append(current_phon)

        else:
            result_segment.append(current_phon)

    return result_segment
