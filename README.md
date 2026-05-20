# RuTranscript

This package was created in order to make a phonetic transcription in russian. 
The library is based on the literary norm of phonetic transcription for the Russian language and uses symbols 
of the International Phonetic Alphabet. Transcription takes into account the allocation of allophones. 
The resulting library can be used in automatic speech recognition and synthesis tasks.

At the moment, there is no functional for division into syllables in this framework, due to its variability. 
Therefore, allophones that depend on the place in the syllable 
(for example, *j* at the beginning of the syllable - *ʝ*) are allocated only in cases where the beginning of 
the syllable coincides with the beginning of the word or the end of the syllable coincides with the end of the word.

For a more detailed description of how the framework works, see the article: https://www.dialog-21.ru/media/5722/badasyana137.pdf

# Requirements

- Python 3.12
- Poetry, if you want to build the package or install development dependencies

The package is not published to a package registry at the moment. Install it from Git or build it locally from a cloned repository.

# Installation from Git

```shell
pip install git+https://github.com/suralmasha/RuTranscript
```

For Poetry-based projects:

```shell
poetry add git+https://github.com/suralmasha/RuTranscript
```

# Package Building

## Manual Build

1. Ensure that all package sources are located under `src/` and correctly declared in the `packages` section of `pyproject.toml`.
2. Build the package:

```shell
pip install poetry==2.2.0 build==1.3.0  # optional
make package
```

3. The generated artifacts (`.whl` and `.tar.gz`) will appear in the `dist/` directory.

## Manual Installation

To install the built package into another project:

```shell
pip install --force-reinstall */dist/*.whl
```

If multiple versions exist, specify the exact wheel file.

# Usage

Put your text in the appropriate variable (in the example - `text`). 
Pass it to the `RuTranscript()` and use method `transcribe()`.

```
from ru_transcript import RuTranscript

text = 'Как получить транскрипцию?'
ru_transcript = RuTranscript(text)
ru_transcript.transcribe()
```

You may define stresses both for one word and for all words in the text. 
To do this, put a stress symbol (preferably '+') before or after the stressed vowel 
and put the stressed text in an additional variable (in the example - `stressed_text_if_have`). 
To define where you've putted the stress mark use the parameter `stress_place` (possible values: `'after'` or `'before'`).  
**Important!** The number of words in these two texts must match.

```
text = 'Как получить транскрипцию?'
stressed_text_if_have = 'Как получи+ть транскрипцию?'
ru_transcript = RuTranscript(text, stressed_text_if_have)
ru_transcript.transcribe()
```

or

```
text = 'Как получить транскрипцию?'
stressed_text_if_have = 'Как получ+ить транскрипцию?'
ru_transcript = RuTranscript(text, stressed_text_if_have, stress_place='before')
ru_transcript.transcribe()
```

Pauses are arranged according to punctuation: the end of a sentence is indicated by a long pause (`'||'`), 
punctuation marks inside a sentence are indicated by short pauses (`'|'`).  
You can get a list of **allophones** by using method `get_allophones()`.

```
print(ru_transcript.get_allophones())
```

Output:
```
['k', 'a', 'k', 'p', 'ə', 'ɫ', 'ʊ', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ']
```

You can get a list of **phonemes (main allophones)** by using method `get_phonemes()` - 
this is a less detailed sort of transcription.

```
print(ru_transcript.get_phonemes())
```

Output:
```
['k', 'a', 'k', 'p', 'o', 'l', 'u', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'a', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡s', 'i', 'j', 'u']
```

You can see **how stresses were placed** by using method `get_stressed_text`.

```
print(ru_transcript.get_stressed_text())
```

Output:
```
'ка+к получи+ть транскри+пцию'
```

You can also find an example of using the framework in `example.py`.

# Development

Install dependencies:

```shell
poetry install --with dev,test
```

Run tests:

```shell
make test
```

Run linting and formatting checks:

```shell
make ruff-check
make ruff-format-check
```

# Version 2.0.0 Note

Version 2.0.0 updates the project to Python 3.12 and refreshes dependencies. The newer `epitran` version changes parts of the generated Russian transcription output, so the transcription and allophone processing logic was updated for compatibility.

If you use exact transcription output in tests or downstream processing, review the output after upgrading.
