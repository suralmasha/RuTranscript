import spacy
import re
import nltk
from nltk import Tree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from string import punctuation
import ru_number_to_text
from ru_number_to_text.num2t4ru import num2text
import pymorphy2

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_ru')
nlp = spacy.load('ru_core_news_sm')

class TextPreprocessing:
  def __init__(self, text: str, accented_text=''):
    if not accented_text:
      accented_text = text

    self.text = text
    self.accented_text = accented_text
    self.tokens = []
    self.accented_tokens = []
    self.tokens_len = 0
    self.stems = {}
    self.lemmas = {}
    self.tags = {}
    self.pos_tags = {}
  
  def _num_to_text(self, tokens: list, accented: bool):
    n = 0
    for i, word in enumerate(tokens):
      if word.isnumeric():
        if len(word) == 1:
          tokens[i + n] = num2text(int(word))
        else:
          add = num2text(int(word)).split(' ')
          tokens = tokens[:i + n] + add + tokens[i + n + 1:]
          n += len(add) - 1
    
    if accented:
      self.accented_tokens = tokens
    else:
      self.tokens = tokens
  
  def _tokenization(self, text, accented: bool):
    tokens = [w.lower() for w in text.split()]
    tokens = [re.sub('[^а-яё0-9\’\'\у́\-\+]', ' ', w, flags=re.IGNORECASE)\
              for w in tokens if w != '']
    tokens = [re.sub(r"\у́", 'у', w) for w in tokens if w != '']
    tokens = [re.sub(r"\’", '', w) for w in tokens if w != '']
    tokens = [re.sub(r"\'", '', w) for w in tokens if w != '']
    tokens = [re.sub(r'\s+', ' ', w) for w in tokens if w != '']
    tokens = [re.sub(r'\s$^\s', '', w) for w in tokens if w != '']
    n = 0
    for i, w in enumerate(tokens):
      if ' ' in w:
        tokens = tokens[:i + n] + w.split() + tokens[i + n + 1:]
        n += len(w.split()) - 1

    self._num_to_text(tokens, accented)
    self.tokens_len = len(self.tokens)

  def full_tokenization(self):
    self._tokenization(self.text, False)
    self._tokenization(self.accented_text, True)

    n = 0
    for i, a_word in enumerate(self.accented_tokens):
      while '-' in a_word:
        word = self.tokens[i + n]
        plus_counter = len([let for let in a_word if let == '+'])
        if plus_counter == 1:
          self.accented_tokens = self.accented_tokens[:i + n] + [a_word.replace('-', '')]\
                                 + self.accented_tokens[i + n + 1:]
          self.tokens = self.tokens[:i + n] + [word.replace('-', '')] + self.tokens[i + n + 1:]
          a_word = ''
        else:
          self.accented_tokens = self.accented_tokens[:i + n] + [a_word[:a_word.index('-')]]\
                                 + [a_word[a_word.index('-') + 1:]] + self.accented_tokens[i + n + 1:]
          self.tokens = self.tokens[:i + n] + [word[:word.index('-')]] + [word[word.index('-') + 1:]]\
                        + self.tokens[i + n + 1:]
          a_word = a_word[a_word.index('-') + 1:]
          n += 1

  def stemming(self):
    snowball = SnowballStemmer('russian')
    for word in self.tokens:
      self.stems[word] = snowball.stem(word)
    
  def lemmatization(self):
    morph = pymorphy2.MorphAnalyzer()
    for word in self.tokens:
      p = morph.parse(word)[0]
      self.lemmas[word] = p.normal_form
      self.tags[word] = p.tag
  
  def word_form(self, new_word: str, orig_word):
    morph = pymorphy2.MorphAnalyzer()
    wp = morph.parse(new_word)[0]
    tags = {'aspect': self.tags[orig_word].aspect, 'case': self.tags[orig_word].case,
            'gender': self.tags[orig_word].gender, 'mood': self.tags[orig_word].mood,
            'number': self.tags[orig_word].number, 'person': self.tags[orig_word].person,
            'tense': self.tags[orig_word].tense, 'voice': self.tags[orig_word].voice}

    if wp.tag.POS == 'NOUN':
      del tags['gender']
        
    tags_str = []
    for k, v in tags.items():
      if v:
        tags_str.append(v)

    new_word = wp.inflect(set(tags_str))
    return new_word.word
