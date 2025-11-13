from collections import defaultdict
from os.path import abspath, dirname, join

epi_starterpack = [
    'a',
    'b',
    'bʲ',
    'v',
    'vʲ',
    'ɡ',
    'ɡʲ',
    'd',
    'dʲ',
    'e',
    'ʒ',
    'z',
    'zʲ',
    'i',
    'j',
    'k',
    'kʲ',
    'l',
    'lʲ',
    'm',
    'mʲ',
    'n',
    'nʲ',
    'o',
    'p',
    'pʲ',
    'r',
    'rʲ',
    's',
    'sʲ',
    't',
    'tʲ',
    'u',
    'f',
    'fʲ',
    'x',
    'xʲ',
    't͡s',
    't͡ɕ',
    'ʂ',
    'ɕː',
    'ɨ',
    'd͡ʒ',
]
ru_starterpack = [
    'ё',
    'й',
    'ц',
    'у',
    'к',
    'е',
    'н',
    'г',
    'ш',
    'щ',
    'з',
    'х',
    'ъ',
    'ф',
    'ы',
    'в',
    'а',
    'п',
    'р',
    'о',
    'л',
    'д',
    'ж',
    'э',
    'я',
    'ч',
    'с',
    'м',
    'и',
    'т',
    'ь',
    'б',
    'ю',
]
rus_v = ['а', 'е', 'ё', 'и', 'о', 'у', 'э', 'ю', 'я', 'ы']  # russian vowels

ROOT_DIR = dirname(abspath(__file__))  # noqa: PTH100, PTH120

with open(join(ROOT_DIR, '../data/alphabet.txt'), encoding='utf-8') as f:  # noqa: PTH118, PTH123
    alphabet = f.read().split(', ')

with open(join(ROOT_DIR, '../data/sorted_allophones.txt'), encoding='utf-8') as f:  # noqa: PTH118, PTH123
    sorted_phonemes_txt = (line.replace('\n', '') for line in f)
    sorted_phonemes_1 = {}
    for group in sorted_phonemes_txt:
        group_name, phonemes = group.split(' = ')
        sorted_phonemes_1[group_name] = phonemes.split(', ')

sorted_phonemes = defaultdict(list)
for key, value in sorted_phonemes_1.items():
    for element in value:
        sorted_phonemes[element].append(key)

with open(join(ROOT_DIR, '../data/paired_consonants.txt'), encoding='utf-8') as f:  # noqa: PTH118, PTH123
    paired_c_txt = f.read().replace(')', ')_').split('_, ')
    paired_c = {
        voiced.replace('(', ''): silent.replace(')', '')
        for voiced, silent in (pair.split(', ') for pair in paired_c_txt)
    }

# creating a dictionary with all allophones
allophones = {
    key: {'phon': 'V', 'row': None, 'rise': None, 'round': None, 'class': 'vowel'}
    if 'total_v' in sorted_phonemes[key]
    else {
        'phon': 'C',
        'place': None,
        'manner': None,
        'palatalization': None,
        'voice': None,
        'pair': None,
        'hissing': None,
        'class': None,
    }
    for key in alphabet
}
# vowels
# row
row_map = {
    'front_v': 'front',
    'near_front_v': 'near front',
    'central_v': 'central',
    'near_back_v': 'near back',
    'back_v': 'back',
}
# rise
rise_map = {
    'close_v': 'close',
    'near_close_v': 'near close',
    'close_mid_v': 'close mid',
    'mid_v': 'mid',
    'open_mid_v': 'open mid',
    'near_open_v': 'near open',
    'open_v': 'open',
}
# round / velarize
round_map = {'rounded_v': 'round', 'velarize_v': 'velarize'}
# consonants
# place
place_map = {
    'bilabial_c': 'labial, bilabial',
    'labiodental_c': 'labial, labiodental',
    'dental_c': 'lingual, dental',
    'palatinodental_c': 'lingual, palatinоdental',
    'palatal_c': 'lingual, palatal',
    'velar_c': 'lingual, velar',
    'glottal_c': 'glottal',
}
# manner
manner_map = {
    'explosive_c': 'obstruent, explosive',
    'affricate_c': 'obstruent, affricate',
    'fricative_c': 'obstruent, fricative',
    'nasal_c': 'sonorant, nasal',
    'lateral_c': 'sonorant, lateral',
    'vibrant_c': 'sonorant, vibrant',
}
# hard / soft
palatalization_map = {'hard_c': 'hard', 'always_hard_c': 'ahard', 'soft_c': 'soft', 'always_soft_c': 'asoft'}
# voice / silent
voice_map = {'voiced_c': 'voiced', 'voiceless_c': 'voiceless'}
paired_c_inv = {v: k for k, v in paired_c.items()}
# hissing sounds
hissing_map = {'hissing_c': 'hissing'}
# class
class_map = {
    'sonorous_class': 'sonorous',
    'voiced_class': 'voiced',
    'voiceless_class': 'voiceless',
    'hissing_class': 'hissing',
}
# experiments
# allophones = {key: {'phon': 'V', 'row': None, 'rise': None, 'round': None, 'class': 'vowel', 'experiment': None} if
# 'total_v' in sorted_phonemes[key] else {'phon': 'C', 'place': None, 'manner': None,
# 'palatalization': None, 'voice': None, 'pair': None, 'hissing': None, 'class': None,
# 'experiment': None} for key in alphabet}
# experiment_map = {'complex_experiment': 'complex', 'rare_experiment': 'rare',
# 'random_vowels_experiment': 'random_vowel', 'long_consonants_experiment': 'long_consonant'}

for key in allophones:  # noqa: PLC0206
    for group in sorted_phonemes[key]:
        # experiments
        # experiment = experiment_map.get(group, None)
        # allophones[key]['experiment'] = experiment if experiment is not None else allophones[key]['experiment']

        # vowels
        if allophones[key]['phon'] == 'V':
            row = row_map.get(group)
            allophones[key]['row'] = row if row is not None else allophones[key]['row']
            rise = rise_map.get(group)
            allophones[key]['rise'] = rise if rise is not None else allophones[key]['rise']
            round_ph = round_map.get(group)
            allophones[key]['round'] = round_ph if round_ph is not None else allophones[key]['round']

        # consonants
        if allophones[key]['phon'] == 'C':
            place = place_map.get(group)
            allophones[key]['place'] = place if place is not None else allophones[key]['place']
            manner = manner_map.get(group)
            allophones[key]['manner'] = manner if manner is not None else allophones[key]['manner']
            palatalization = palatalization_map.get(group)
            allophones[key]['palatalization'] = (
                palatalization if palatalization is not None else allophones[key]['palatalization']
            )
            hissing = hissing_map.get(group)
            allophones[key]['hissing'] = hissing if hissing is not None else allophones[key]['hissing']
            class_consonants = class_map.get(group)
            allophones[key]['class'] = class_consonants
            voice = voice_map.get(group)
            allophones[key]['voice'] = voice if voice is not None else allophones[key]['voice']
            if (allophones[key]['voice'] == 'voiced') and (key in paired_c):
                allophones[key]['pair'] = paired_c[key]
            elif (allophones[key]['voice'] == 'voiceless') and (key in paired_c.values()):
                allophones[key]['pair'] = paired_c_inv[key]

# symbols
allophones.update({symbol: {'phon': 'symb'} for symbol in ['+', '-', '|', '||', '_', '']})

# Special consonant sets
ts = {'t͡s', 't͡sʷ', 't͡sˠ', 'd͡ʒᶣ', 'd͡ʒˠ', 'd̻͡z̪', 'd͡ʒ'}
zh_sh_ts = {
    'ʐ',
    'ʐʷ',
    'ʐˠ',
    'ʑː',
    'ʑːʷ',
    'ʑːˠ',
    'ʑʲː',
    'ʑːᶣ',
    'ʂ',
    'ʂʷ',
    'ʂˠ',
    'ʂː',
    'ʂːʷ',
    'ʂːˠ',
    't͡s',
    't͡sʷ',
    't͡sˠ',
    'd͡ʒᶣ',
    'd͡ʒˠ',
    'd̻͡z̪',
    'd͡ʒ',
}

jotised = {'j', 'ʲa', 'ʲo', 'ʲu', 'ʲe'}
