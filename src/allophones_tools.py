import spacy

from .sounds import allophones, rus_v

nlp = spacy.load('ru_core_news_sm')


def shch(section: list):
    for i, current_phon in enumerate(section[:-1]):
        try:
            next_phon = section[i + 1]
        except IndexError:
            next_phon = ''
        try:
            two_current = (section[i], section[i + 1])
        except IndexError:
            two_current = ''

        next_allophone = allophones[next_phon]
        if ((current_phon == 'ʒ') and (next_allophone['phon'] == 'C')
            and (next_allophone['voice'] == 'voiceless' and next_phon != 's')) \
                or (two_current in {('s', 't͡ɕ'), ('z', 't͡ɕ'), ('ʒ', 't͡ɕ')}):
            section[i] = 'ɕː'
            del section[i + 1]

    return section


def long_ge(section: list):
    for i, current_phon in enumerate(section[:-1]):
        try:
            next_phon = section[i + 1]
        except IndexError:
            next_phon = ''
        try:
            two_current = (section[i], section[i + 1])
        except IndexError:
            two_current = ''

        next_allophone = allophones[next_phon]
        if (current_phon == next_phon == 'ʒ') or (two_current == ('z', 'ʒ')):
            section[i] = 'ʑː'
            del section[i + 1]
        elif (current_phon == 'ɕː') and (next_allophone['phon'] == 'C')\
                and (next_allophone['voice'] == 'voiced') and ('nasal' not in next_allophone['manner']):
            section[i] = 'ʑː'

    return section


def nasal_m_n(section: list):
    for i, current_phon in enumerate(section[:-1]):
        try:
            next_phon = section[i + 1]
        except IndexError:
            next_phon = ''

        next_allophone = allophones[next_phon]
        if (current_phon == 'm' or current_phon == 'n') and (next_allophone['phon'] == 'C') \
                and (next_allophone['place'] == 'labial, labiodental'):
            section[i] = 'ɱ'

        elif (current_phon == 'mʲ' or current_phon == 'nʲ') and (next_allophone['phon'] == 'C') \
                and (next_allophone['place'] == 'labial, labiodental'):
            section[i] = 'ɱʲ'

    return section


def silent_r(section: list):
    for i, current_phon in enumerate(section):
        try:
            next_phon = section[i + 1]
        except IndexError:
            next_phon = ''

        next_allophone = allophones[next_phon]
        if (current_phon == 'r') and ((i == len(section) - 1) or ((next_allophone['phon'] == 'C')
                                                                  and (next_allophone['voice'] == 'voiceless'))):
                section[i] = 'r̥'

        elif (current_phon == 'rʲ') and (i == len(section) - 1):
            section[i] = 'r̥ʲ'

    return section


def voiced_ts(section: list):
    for i, current_phon in enumerate(section):
        try:
            next_phon = section[i + 1]
        except IndexError:
            next_phon = ''

        next_allophone = allophones[next_phon]
        if (current_phon == 't͡s') and (next_allophone['phon'] == 'C') and (next_allophone['voice'] == 'voiced'):
            section[i] = 'd̻͡z̪'

    return section


def fix_jotised(phonemes_list_section, letters_list_section):
    # ---- jotised vowels, i and j ----
    phonemes_list_to_iterate = phonemes_list_section[:]
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
            phonemes_list_section.insert(i + n, 'j')
            n += 1

        elif current_let in 'ё е я ю'.split():
            if previous_let[-1] in ['ь', 'ъ']:
                if (previous_allophone['phon'] == 'C')\
                        and ('ʲ' not in previous_phon)\
                        and (previous_allophone['palatalization'][0] != 'a'):
                    phonemes_list_section[i + n - 1 - sub_symb] = previous_phon + 'ʲ'
                phonemes_list_section.insert(i + n, 'j')
                n += 1

            elif previous_let in rus_v:
                phonemes_list_section.insert(i + n, 'j')
                n += 1

            elif (current_let != 'э') \
                    and (previous_allophone['phon'] == 'C') \
                    and ('ʲ' not in previous_phon) \
                    and ('a' not in previous_allophone['palatalization'][0]):
                phonemes_list_section[i + n - 1 - sub_symb] = previous_phon + 'ʲ'

            elif (after_next_let == '+') and (previous_phon != 'j'):
                phonemes_list_section.insert(i + n, 'j')
                n += 1

        elif current_let == 'и':
            if sub_symb and (phonemes_list_to_iterate[i - 1] == '_') and (previous_allophone['phon'] == 'C'):
                phonemes_list_section[i + n] = 'ɨ'

            elif previous_let[-1] in {'ь', 'ъ'}:
                phonemes_list_section.insert(i + n, 'j')
                n += 1

            elif (previous_allophone['phon'] == 'C') \
                    and ('ʲ' not in previous_phon) \
                    and (previous_allophone['palatalization'][0] != 'a'):
                phonemes_list_section[i + n - 1 - sub_symb] = previous_phon + 'ʲ'

    if phonemes_list_section[0] == 'j':
        phonemes_list_section[0] = 'ʝ'

    return phonemes_list_section


def assimilative_palatalization(tokens_section, phonemes_list_section):
    exceptions = 'сосиска злить после ёлка день транскрипция джаз неуклюжий'.split()

    token_index = 0
    token = tokens_section[token_index]
    nlp_token = nlp(token)[0]
    lemma = nlp_token.lemma_

    for i, current_phon in enumerate(phonemes_list_section):
        if current_phon == '_':
            token_index += 1
            token = tokens_section[token_index]
            nlp_token = nlp(token)[0]
            lemma = nlp_token.lemma_

        current_allophone = allophones[current_phon]
        if (lemma not in exceptions) and ('i+zm' not in token):
            try:
                n = 1
                next_phon = phonemes_list_section[i + n]
                next_allophone = allophones[next_phon]
                while next_allophone['phon'] == 'symb':
                    n += 1
                    next_phon = phonemes_list_section[i + n]
            except IndexError:
                next_phon = ''
                next_allophone = allophones[next_phon]

            # доминирует не смягчение зубных перед мягкими губно-зубными ([д’в’]е́рь - [дв’]е́рь)
            if (current_allophone['phon'] == 'C') and (current_allophone['place'] == 'lingual, dental') \
                    and (next_allophone['phon'] == 'C') and (next_allophone['place'] == 'labial, labiodental'):
                continue

            # доминирует не смягчение губных перед мягкими губными (лю[б’в’]и́ - лю[бв’]и́)
            elif (current_allophone['phon'] == 'C') and (current_allophone['place'] == 'labial, bilabial') \
                    and (next_allophone['phon'] == 'C') and (next_allophone['place'] == 'labial, bilabial') \
                    and lemma != 'лобби':
                continue

            # не смягчение губных и зубных перед мягкими заднеязычными (гри[пк’]и́; ко́[фт’]е)
            elif (current_allophone['phon'] == 'C') \
                    and (current_allophone['place'] in ['lingual, dental', 'labial, bilabial']) \
                    and (next_allophone['phon'] == 'C') and (next_allophone['place'] == 'lingual, velar'):
                continue

            # не смягчение звуков [р], [г] перед мягкими согласными (а[рт’]и́ст, а[гн’]ия)
            elif current_phon in {'r', 'ɡ'}:
                continue

            # не смягчение звука [т] перед [р] ([тр’]и́)
            elif (current_phon == 't') and (next_phon == 'rʲ'):
                continue

            elif (current_allophone['phon'] == 'C') and (current_allophone['palatalization'][0] != 'a') \
                    and ('ʲ' not in current_phon) \
                    and (next_allophone['phon'] == 'C') and (next_allophone['palatalization'] == 'soft'):
                phonemes_list_section[i] = current_phon + 'ʲ'

    return phonemes_list_section


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

        if (current_phon[0] in 'ʂ̺bpfkstrlmngdz') and (current_phon == next_phon):
            del phonemes_list_section[i + n]
            del phonemes_list_section[i + n + add_symb]
            phonemes_list_section.insert(i + n, current_phon + 'ː')
            n -= 1

    return phonemes_list_section


def vowels(segment: list):
    for i, current_phon in enumerate(segment):
        try:
            next_phon = segment[i + 1]
        except IndexError:
            next_phon = ''
        try:
            after_next_phon = segment[i + 2]
        except IndexError:
            after_next_phon = ''
        try:
            previous_phon = segment[i - 1]
        except IndexError:
            previous_phon = ''
        try:
            after_previous_phon = segment[i - 2]
        except IndexError:
            after_previous_phon = ''

        previous_allophone = allophones[previous_phon]
        after_next_allophone = allophones[after_next_phon]
        after_previous_allophone = allophones[after_previous_phon]
        if current_phon == 'a':
            if (i != len(segment) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

                if next_phon == '+':  # ударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ɐ.'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization'])\
                            and (after_next_phon == 'l'):
                        segment[i] = 'ɑ'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'a'
                    else:
                        segment[i] = 'æ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ᵻ'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'ɐ'
                    else:
                        segment[i] = 'ɪ'

                else:  # заударные / второй предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') \
                            and ((previous_allophone['hissing'] == 'hissing')
                                 or ('hard' in previous_allophone['palatalization'])):
                        segment[i] = 'ə'
                    else:
                        segment[i] = 'ɪ.'

            elif (i == len(segment) - 1) or (next_phon == '_'):   # заударные (last)
                if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                    segment[i] = 'ə'
                elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                    segment[i] = 'ʌ'
                else:
                    segment[i] = 'æ.'

            else:
                if next_phon == '-':
                    segment[i] = 'ɐ'  # первый предударный (first)
                elif next_phon != '+':
                    segment[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'o':
            if (i != len(segment) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

                if next_phon == '+':  # ударный (not last, not first)
                    if previous_allophone['phon'] == 'C' and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ɐ.'
                    elif (previous_allophone['phon'] == 'C' and 'soft' in previous_allophone['palatalization'])\
                            or (previous_allophone['phon'] == 'V'):
                        segment[i] = 'ɵ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ᵻ'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'ɐ'
                    else:
                        segment[i] = 'ɪ'

                else:  # заударные/второй предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') \
                            and ((previous_allophone['hissing'] == 'hissing')
                                 or ('hard' in previous_allophone['palatalization'])):
                        segment[i] = 'ə'
                    else:
                        segment[i] = 'ɪ.'

            elif (i == len(segment) - 1) or (next_phon == '_'):  # заударные (last)
                if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                    segment[i] = 'ə'
                elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                    segment[i] = 'ʌ'
                else:
                    segment[i] = 'æ.'

            else:
                if next_phon == '-':
                    segment[i] = 'ɐ'  # первый предударный (first)
                elif next_phon != '+':
                    segment[i] = 'ə'  # заударные / второй предударный (first)

        elif current_phon == 'e':
            if (i != len(segment) - 1) and (next_phon != '_') \
                    and (i != 0) and (previous_phon != '_'):  # not last, not first

                if (next_phon == '+') and (previous_allophone['phon'] == 'C'):  # ударный (not last, not first)
                    if previous_allophone['hissing'] == 'hissing':
                        segment[i] = 'ᵻ'
                    elif 'hard' in previous_allophone['palatalization']:
                        segment[i] = 'ɛ'

                elif next_phon == '-':  # первый предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ə'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'ᵻ'
                    else:
                        segment[i] = 'ɪ'

                else:  # заударные / второй предударный (not last, not first)
                    if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                        segment[i] = 'ə'
                    elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'ᵻ'
                    else:
                        segment[i] = 'ɪ.'

            elif (i == len(segment) - 1) or (next_phon == '_'):  # заударные (last)
                if (previous_allophone['phon'] == 'C') and (previous_allophone['hissing'] == 'hissing'):
                    segment[i] = 'ə'
                elif (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                    segment[i] = 'ᵻ'
                else:
                    segment[i] = 'æ.'

            else:
                if next_phon == '+':
                    segment[i] = 'ɛ'  # ударный (first)
                elif next_phon == '-':
                    segment[i] = 'ᵻ'  # первый предударный (first)
                else:
                    segment[i] = 'ɪ.'  # заударные / второй предударный (first)

        elif current_phon == 'u':
            if (i != len(segment) - 1) and (next_phon != '_'):  # not last

                if next_phon == '+':  # ударный (not last)
                    if (previous_allophone['phon'] == 'C') and ('soft' in previous_allophone['palatalization']):
                        segment[i] = 'ʉ'

                else:  # первый / второй предударный / заударные (not last)
                    if (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                        segment[i] = 'ʊ'
                    else:
                        segment[i] = 'ᵿ'

            else:  # первый / второй предударный / заударные (last)
                if (previous_allophone['phon'] == 'C') and ('hard' in previous_allophone['palatalization']):
                    segment[i] = 'ʊ'
                else:
                    segment[i] = 'ᵿ'

        elif (current_phon == 'i') and (previous_allophone['phon'] == 'C'):
            if previous_allophone['hissing'] == 'hissing':  # после шипящей
                segment[i] = 'ɨ'
            elif next_phon != '+':  # безударный
                segment[i] = 'ɪ'

        elif (current_phon == 'ɨ') and (previous_allophone['phon'] == 'C'):
            if (i != len(segment) - 1) and (next_phon != '_'):  # not last

                if next_phon == '+':  # ударный (not last)
                    if (previous_phon == 'l') and (len(segment) > 4) \
                            and (after_previous_allophone['phon'] == 'C') \
                            and ('lab' in after_previous_allophone['place']):
                        segment[i] = 'ɯ̟ɨ̟'
                    elif (after_next_allophone['phon'] == 'C') \
                            and ((previous_allophone['place'] == 'lingual, dental'
                                  and after_next_allophone['place'] == 'lingual, velar')
                                 or (previous_allophone['place'] == 'lingual, palatinоdental'
                                     and after_next_allophone['place'] == 'lingual, velar')):
                        segment[i] = 'ɨ̟'

                elif previous_allophone['hissing'] == 'hissing':  # предударный / заунарный (not last)
                    segment[i] = 'ə'
                else:
                    segment[i] = 'ᵻ'

            elif previous_allophone['hissing'] == 'hissing':  # заударный (last)
                segment[i] = 'ə'
            else:
                segment[i] = 'ᵻ'

    return segment


def labia_velar(segment: list):
    result_segment = []
    for i, current_phon in enumerate(segment):
        if i != 0:
            previous_phon = segment[i - 1]
        else:
            previous_phon = ''

        current_allophone = allophones[current_phon]
        previous_allophone = allophones[previous_phon]
        if (current_allophone['phon'] == 'V') \
                and (i != 0) and (previous_phon != '_') \
                and (previous_allophone['phon'] == 'C') \
                and (current_allophone['round'] == 'round') \
                and ('ʷ' not in previous_phon) and ('ᶣ' not in previous_phon):
            if 'ʲ' in previous_phon:
                new = previous_phon.replace('ʲ', '') + 'ᶣ'
                if new in allophones.keys():
                    del result_segment[-1]
                    result_segment.append(new)
                    result_segment.append(current_phon)
            elif previous_allophone['palatalization'] == 'asoft':
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

        elif (current_allophone['phon'] == 'V') \
                and (i != 0) and (previous_phon != '_') \
                and (previous_allophone['phon'] == 'C') \
                and (current_allophone['round'] == 'velarize') \
                and ('soft' not in previous_allophone['palatalization']) \
                and ('ˠ' not in previous_phon):  # в русском нет слов, начинающихся с ы
            new = previous_phon + 'ˠ'
            if new in allophones.keys():
                del result_segment[-1]
                result_segment.append(new)
                result_segment.append(current_phon)

        else:
            result_segment.append(current_phon)

    return result_segment
