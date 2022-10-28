epi_starterpack = 'a b bʲ v vʲ ɡ ɡʲ d dʲ e ʒ z zʲ i j k kʲ l lʲ m mʲ n nʲ o '\
                  'p pʲ r rʲ s sʲ t tʲ u f fʲ x xʲ t͡s t͡ɕ ʂ ɕː ɨ d͡ʒ'.split()
ru_starterpack = 'ё й ц у к е н г ш щ з х ъ ф ы в а п р о л д ж э я ч с м и т ь б ю'.split()
rus_v = 'а е ё и о у э ю я ы'.split(' ')  # russian vowels

with open('../alphabet.txt', 'r', encoding='utf-8') as f:
    alphabet = f.read().split(', ')

with open('../sorted_allophones.txt', 'r', encoding='utf-8') as f:
    sorted_phonemes_txt = [line.replace('\n', '') for i, line in enumerate(f.readlines())]
    sorted_phonemes = {}
    for group in sorted_phonemes_txt:
        group_name, phonemes = group.split(' = ')
        sorted_phonemes[group_name] = phonemes.split(', ')

with open('../paired_consonants.txt', 'r', encoding='utf-8') as f:
    paired_c_txt = f.read().replace(')', ')_').split('_, ')
    paired_c = {}
    for pair in paired_c_txt:
        voiced, silent = pair.split(', ')
        paired_c[voiced.replace('(', '')] = silent.replace(')', '')

# creating a dictionary with all allophones
allophones = dict.fromkeys(alphabet)
for key in allophones.keys():
    # vowels
    if key in sorted_phonemes['total_v']:
        allophones[key] = {'phon': 'V', 'row': '', 'rise': '', 'round': ''}
        # row
        if key in sorted_phonemes['front_v']:
            allophones[key]['row'] = 'front'
        elif key in sorted_phonemes['near_front_v']:
            allophones[key]['row'] = 'near front'
        elif key in sorted_phonemes['central_v']:
            allophones[key]['row'] = 'central'
        elif key in sorted_phonemes['near_back_v']:
            allophones[key]['row'] = 'near back'
        elif key in sorted_phonemes['back_v']:
            allophones[key]['row'] = 'back'
        # rise
        if key in sorted_phonemes['close_v']:
            allophones[key]['rise'] = 'close'
        elif key in sorted_phonemes['near_close_v']:
            allophones[key]['rise'] = 'near close'
        elif key in sorted_phonemes['close_mid_v']:
            allophones[key]['rise'] = 'close mid'
        elif key in sorted_phonemes['mid_v']:
            allophones[key]['rise'] = 'mid'
        elif key in sorted_phonemes['open_mid_v']:
            allophones[key]['rise'] = 'open mid'
        elif key in sorted_phonemes['near_open_v']:
            allophones[key]['rise'] = 'near open'
        elif key in sorted_phonemes['open_v']:
            allophones[key]['rise'] = 'open'
        # round / velarize
        if key in sorted_phonemes['rounded_v']:
            allophones[key]['round'] = 'round'
        elif key in sorted_phonemes['velarize_v']:
            allophones[key]['round'] = 'velarize'
        else:
            allophones[key]['round'] = 'not round and not velarize'
    # consonants
    elif key in sorted_phonemes['total_c']:
        allophones[key] = {'phon': 'C', 'place': '', 'manner': '',
                           'palatalization': '', 'voice': '',
                           'pair': None, 'hissing': None}
        # place
        if key in sorted_phonemes['bilabial_c']:
            allophones[key]['place'] = 'labial, bilabial'
        elif key in sorted_phonemes['labiodental_c']:
            allophones[key]['place'] = 'labial, labiodental'
        elif key in sorted_phonemes['dental_c']:
            allophones[key]['place'] = 'lingual, dental'
        elif key in sorted_phonemes['palatinodental_c']:
            allophones[key]['place'] = 'lingual, palatinоdental'
        elif key in sorted_phonemes['palatal_c']:
            allophones[key]['place'] = 'lingual, palatal'
        elif key in sorted_phonemes['velar_c']:
            allophones[key]['place'] = 'lingual, velar'
        elif key in sorted_phonemes['glottal_c']:
            allophones[key]['place'] = 'glottal'
        # manner
        if key in sorted_phonemes['explosive_c']:
            allophones[key]['manner'] = 'obstruent, explosive'
        elif key in sorted_phonemes['affricate_c']:
            allophones[key]['manner'] = 'obstruent, affricate'
        elif key in sorted_phonemes['fricative_c']:
            allophones[key]['manner'] = 'obstruent, fricative'
        elif key in sorted_phonemes['nasal_c']:
            allophones[key]['manner'] = 'sonorant, nasal'
        elif key in sorted_phonemes['lateral_c']:
            allophones[key]['manner'] = 'sonorant, lateral'
        elif key in sorted_phonemes['vibrant_c']:
            allophones[key]['manner'] = 'sonorant, vibrant'
        # hard / soft
        if key in sorted_phonemes['hard_c']:
            allophones[key]['palatalization'] = 'hard'
        elif key in sorted_phonemes['always_hard_c']:
            allophones[key]['palatalization'] = 'ahard'
        elif key in sorted_phonemes['soft_c']:
            allophones[key]['palatalization'] = 'soft'
        elif key in sorted_phonemes['always_soft_c']:
            allophones[key]['palatalization'] = 'asoft'
        # voice / silent
        if key in sorted_phonemes['voiced_c']:
            allophones[key]['voice'] = 'voiced'
            if key in paired_c.keys():
                allophones[key]['pair'] = paired_c[key]
        elif key in sorted_phonemes['voiceless_c']:
            allophones[key]['voice'] = 'voiceless'
            if key in paired_c.values():
                allophones[key]['pair'] = [k for k, v in paired_c.items() if v == key][0]
        # hissing sounds
        if key in sorted_phonemes['ship_c']:
            allophones[key]['hissing'] = 'hissing'
# symbols
allophones.update({'+': {'phon': 'symb'},
                   '-': {'phon': 'symb'},
                   '|': {'phon': 'symb'},
                   '||': {'phon': 'symb'},
                   '_': {'phon': 'symb'},
                   '': {'phon': 'symb'}})
