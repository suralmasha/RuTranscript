# RuTranscript

This package was created in order to make a phonetic transcription in russian. The library is based on the literary norm of phonetic transcription for the Russian language and uses symbols of the International Phonetic Alphabet. Transcription takes into account the allocation of allophones. The resulting library can be used in automatic speech recognition and synthesis tasks.

At the moment, there is no functional for division into syllables in this framework, due to its variability. Therefore, allophones that depend on the place in the syllable (for example, *j* at the beginning of the syllable - *ʝ*) are allocated only in cases where the beginning of the syllable coincides with the beginning of the word or the end of the syllable coincides with the end of the word.

# Example of usage
## Downloading
```
>>> git clone https://github.com/suralmasha/RuTranscript
>>> from RuTranscript.src.ru_transcript import RuTranscript
```

## How to get a transcription

Put your text in the appropriate variable (in the example - `text`). Pass it to the `RuTranscript()` and use method `transcribe()`.

```
>>> text = 'Как получить транскрипцию?'
>>> ru_transcript = RuTranscript(text)
>>> ru_transcript.transcribe()
```

You may define stresses both for one word and for all words in the text.
To do this, put a stress symbol (preferably '+') before or after the stressed vowel 
and put the stressed text in an additional variable (in the example - `stressed_text_if_have`).
To define where you've putted the stress mark use the parameter `stress_place='before'`.

**Important!** The number of words in these two texts must match.

```
>>> text = 'Как получить транскрипцию?'
>>> stressed_text_if_have = 'Как получи+ть транскрипцию?'
>>> ru_transcript = RuTranscript(text, stressed_text_if_have)
>>> ru_transcript.transcribe()
```

or

```
>>> text = 'Как получить транскрипцию?'
>>> stressed_text_if_have = 'Как получ+ить транскрипцию?'
>>> ru_transcript = RuTranscript(text, stressed_text_if_have, stress_place='before')
>>> ru_transcript.transcribe()
```

You can get a full **transcription with pauses** by using method `transcription()`. Pauses are arranged according to punctuation: the end of a sentence is indicated by a long pause (`'||'`), punctuation marks inside a sentence are indicated by short pauses (`'|'`).

```
>>> print(ru_transcript.transcription)
k a k p ə lʷ ʊ t͡ɕ ɨ tʲ t r ɐ n s k rʲ i p t͡sˠ ɨ jᶣ ᵿ ||
```

You can get a list of **allophones** by using the method `allophones()`.

```
>>> print(ru_transcript.allophones())
['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'ɨ', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ']
```

You can get a list of **phonemes (main allophones)** without pauses by using attribute `phonemes` - this is a less detailed sort of transcription.

```
>>> print(ru_transcript.phonemes)
['k', 'a', 'k', 'p', 'o', 'l', 'u', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'a', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡s', 'i', 'j', 'u']
```

You can see **how stresses were placed** by using attribute `stressed_text`.

```
>>> print(ru_transcript.stressed_text)
'ка+к получи+ть транскри+пцию'
```

You can also find an example of using the framework in `jpt_example.ipynb` or `example.py`.
