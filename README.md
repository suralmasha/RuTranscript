# RuTranscript

This package was created in order to make a phonetic transcription of the Russian text. The library is based on the literary norm of phonetic transcription for the Russian language and uses symbols of the International Phonetic Alphabet [https://en.wikipedia.org/wiki/International_Phonetic_Alphabet]. Transcription takes into account the allocation of allophones. The resulting library can be used in automatic speech recognition and synthesis tasks.

# Example of usage
## Downloading
!git clone https://github.com/suralmasha/RuTranscript

## How to get a transcription
```
>>>text = 'Как получить транскрипцию?'
>>>accented_text_if_have = ''
>>>data = TextPreprocessing(text, accented_text_if_have)
>>>data.full_tokenization()
>>>data.stemming()
>>>data.lemmatization()

>>>transcriber = RuTranscript(data)
>>>transcriber.full_transcription()
>>>transcriber.transcription
\['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'ɪ', '+ʲ', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'kʲ', 'rʲ', 'i', 'p', 't͡s', 'ə', 'jʷ', 'ᵿ']
```
