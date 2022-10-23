# RuTranscript

This package was created in order to make a phonetic transcription of the Russian text. The library is based on the literary norm of phonetic transcription for the Russian language and uses symbols of the International Phonetic Alphabet. Transcription takes into account the allocation of allophones. The resulting library can be used in automatic speech recognition and synthesis tasks.

# Example of usage
## Downloading
```
>>> git clone https://github.com/suralmasha/RuTranscript
>>> from RuTranscript.src.ru_transcript import RuTranscript
```

## How to get a transcription
Put your text in the appropriate variable (in the example - `text`).
```
>>> text = 'Как получить транскрипцию?'
```
You can also highlight the accents in your text. You can stress both one word from the text and all words in the text. To do this, put the "+" sign **after** the stressed vowel and put the new text in an additional variable (in the example - `accented_text_if_have`). If you want to put an accent mark before a stressed vowel, specify it using the parameter `accent_place='before'`.

**Important!** The number of words in these two texts must match.

```
>>> text = 'Как получить транскрипцию?'
>>> accented_text_if_have = 'Как получи+ть транскрипцию?'
```
Then follow the instructions:
```
>>> ru_transcript = RuTranscript(text)
>>> ru_transcript.transcribe()

>>> print(ru_transcript.transcription)
['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'ɪ', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'kʲ', 'rʲ', 'i', 'p', 't͡s', 'ə', 'jʷ', 'ᵿ']
```
You can also find an example of using the framework in the "RuTranscript_example.ipynb" file.
