def get_key(d, value):
  for k, v in d.items():
    if v == value:
      return k

class Sounds:
  def __init__(self, alphabet:str, sorted_phonems: dict, paired_consonants:dict, sound: str):
    self.alphabet = alphabet.split(', ')
    self._sorted_phonems = sorted_phonems
    self._paired_consonants = paired_consonants
    self.sound = sound

    self.phon = ''
    self.row = ''
    self.rise = ''
    self.round = ''

    self.place = ''
    self.manner = ''
    self.palatalization = 'b'
    self.voice = ''
    self.pair = None
    self.hissing = None
  
  def analize(self):
    if self.sound not in self.alphabet:
      return 'Sound not from the russian alphabet'

    if self.sound in self._sorted_phonems['total_v']:
      self.phon = 'V'

      if self.sound in self._sorted_phonems['front_v']:  # row
        self.row = 'front'
      elif self.sound in self._sorted_phonems['near_front_v']:
        self.row = 'near front'
      elif self.sound in self._sorted_phonems['central_v']:
        self.row = 'central'
      elif self.sound in self._sorted_phonems['near_back_v']:
        self.row = 'near back'
      elif self.sound in self._sorted_phonems['back_v']:
        self.row = 'back'
      
      if self.sound in self._sorted_phonems['close_v']:  # rise
        self.rise = 'close'
      elif self.sound in self._sorted_phonems['near_close_v']:
        self.rise = 'near close'
      elif self.sound in self._sorted_phonems['close_mid_v']:
        self.rise = 'close mid'
      elif self.sound in self._sorted_phonems['mid_v']:
        self.rise = 'mid'
      elif self.sound in self._sorted_phonems['open_mid_v']:
        self.rise = 'open mid'
      elif self.sound in self._sorted_phonems['near_open_v']:
        self.rise = 'near open'
      elif self.sound in self._sorted_phonems['open_v']:
        self.rise = 'open'
      
      if self.sound in self._sorted_phonems['rounded_v']:  # round / velarize
        self.round = 'round'
      elif self.sound in self._sorted_phonems['velarize_v']:
        self.round = 'velarize'
      else:
        self.round = 'not round and not velarize'

    elif self.sound in self._sorted_phonems['total_c']:
      self.phon = 'C'

      if self.sound in self._sorted_phonems['bilabial_c']:  # place
        self.place = 'labial, bilabial'
      elif self.sound in self._sorted_phonems['labiodental_c']:
        self.place = 'labial, labiodental'
      elif self.sound in self._sorted_phonems['dental_c']:
        self.place = 'lingual, dental'
      elif self.sound in self._sorted_phonems['palatinоdental_c']:
        self.place = 'lingual, palatinоdental'
      elif self.sound in self._sorted_phonems['palatal_c']:
        self.place = 'lingual, palatal'
      elif self.sound in self._sorted_phonems['velar_c']:
        self.place = 'lingual, velar'
      elif self.sound in self._sorted_phonems['glottal_c']:
        self.place = 'glottal'
      
      if self.sound in self._sorted_phonems['explosive_c']:  # manner
        self.manner = 'obstruent, explosive'
      elif self.sound in self._sorted_phonems['affricate_c']:
        self.manner = 'obstruent, affricate'
      elif self.sound in self._sorted_phonems['fricative_c']:
        self.manner = 'obstruent, fricative'
      elif self.sound in self._sorted_phonems['nasal_c']:
        self.manner = 'sonorant, nasal'
      elif self.sound in self._sorted_phonems['lateral_c']:
        self.manner = 'sonorant, lateral'
      elif self.sound in self._sorted_phonems['vibrant_c']:
        self.manner = 'sonorant, vibrant'
      
      if self.sound in self._sorted_phonems['hard_c']:  # hard / soft
        self.palatalization = 'hard'
      elif self.sound in self._sorted_phonems['always_hard_c']:
        self.palatalization = 'ahard'
      elif self.sound in self._sorted_phonems['soft_c']:
        self.palatalization = 'soft'
      elif self.sound in self._sorted_phonems['always_soft_c']:
        self.palatalization = 'asoft'
      
      if self.sound in self._sorted_phonems['voiced_c']:  # voice / silent
        self.voice = 'voiced'
        if self.sound in self._paired_consonants.keys():
          self.pair = self._paired_consonants[self.sound]
      elif self.sound in self._sorted_phonems['voiceless_c']:
        self.voice = 'voiceless'
        if self.sound in self._paired_consonants.values():
          self.pair = get_key(self._paired_consonants, self.sound)

      if self.sound in self._sorted_phonems['ship_c']:  # hissing sounds
        self.hissing = 'hissing'
