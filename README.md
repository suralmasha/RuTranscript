# RuTranscript

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22900230.svg)](https://doi.org/10.5281/zenodo.22900230)

RuTranscript converts **Russian text** into a **phonetic transcription** based on the literary pronunciation norm. It
provides both detailed allophone sequences and simplified phoneme sequences using symbols from the **International
Phonetic Alphabet** (IPA).

The library is intended for speech technology, linguistic analysis, and pronunciation-related experiments.

## Features

- Automatic stress placement with support for manually specified stress
- Detailed allophone transcription
- Simplified phoneme transcription
- Context-dependent consonant and vowel transformations
- Pause markers derived from punctuation
- Explicit handling of stressed clitics

## Requirements

- Python 3.11 or 3.12
- Git, because some dependencies are installed from Git repositories
- Poetry for development and package building

The package is not currently published to a package registry.

## Installation

Install the latest version from GitHub:

```shell
python -m pip install "git+https://github.com/suralmasha/RuTranscript.git"
```

For Poetry projects:

```shell
poetry add "git+https://github.com/suralmasha/RuTranscript.git"
```

## Quick start

```python
from ru_transcript import RuTranscript

transcription = RuTranscript('Как получить транскрипцию?')
transcription.transcribe()

print(transcription.get_allophones())
print(transcription.get_phonemes())
print(transcription.get_stressed_text())
```

Example allophone output:

```text
['k', 'a', 'k', 'p', 'ə', 'ɫʷ', 'ʊ', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ']
```

Example phoneme output:

```text
['k', 'a', 'k', 'p', 'o', 'l', 'u', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'a', 'n', 's', 'k', 'rʲ', 'i', 'p', 't͡s', 'i', 'j', 'u']
```

## Manual stress

Automatic stress placement can be unreliable for ambiguous or context-dependent words. When pronunciation matters,
provide the same text with `+` next to each known stressed vowel:

```python
from ru_transcript import RuTranscript

text = 'Как получить транскрипцию?'
stressed_text = 'Как получи+ть транскрипцию?'

transcription = RuTranscript(text, stressed_text)
transcription.transcribe()
```

By default, the stress mark follows the vowel. To place it before the vowel, set `stress_place='before'`:

```python
transcription = RuTranscript(
    text,
    'Как получ+ить транскрипцию?',
    stress_place='before',
)
```

The original text and the manually stressed text must contain the same words, except when explicitly marking clitic
stress.

### Clitic stress

To place logical stress on a clitic, join it to its host word in the manually stressed text:

```python
text = 'Муха по полю пошла'
stressed_text = 'Муха по+полю пошла'

transcription = RuTranscript(text, stressed_text)
transcription.transcribe()
```

Without logical stress on the clitic, keep the words separate and place stress on the host word:

```python
stressed_text = 'Муха по по+лю пошла'
```

## Output options

Sentence-ending punctuation produces the long pause marker `||`. Punctuation inside a sentence produces the short pause
marker `|`. Pauses, spaces, and stress marks can be preserved in the result:

```python
allophones = transcription.get_allophones(
    stress_place='before',
    save_stresses=True,
    save_spaces=True,
    save_pauses=True,
    stress_symbol='+',
)
```

The repository also contains small examples:

- `scripts/example.py` demonstrates the primary API.
- `scripts/check_stress.py` displays automatic stress placement.
- `scripts/get_info.py` displays information about an allophone.

## Limitations

- RuTranscript does not split words into syllables because Russian syllabification is variable. Syllable-dependent
  allophones are therefore identified only when a syllable boundary coincides with a word boundary.
- Automatic stress placement should be reviewed for ambiguous words and domain-specific vocabulary.
- Exact transcription output can change when linguistic dependencies are updated. Review downstream snapshots and
  expected values when upgrading.

## Development

Clone the repository and install all development dependencies:

```shell
git clone https://github.com/suralmasha/RuTranscript.git
cd RuTranscript
poetry install --with dev,test
```

Run the test suite:

```shell
make test
```

Format the code and apply safe Ruff fixes:

```shell
make ruff
```

Build the wheel and source distribution in `dist/`:

```shell
make package
```

Contributions are welcome through GitHub issues and pull requests.

## Research

The transcription rules and design are described in the
[project paper](https://doi.org/10.5281/zenodo.22900230) published in the proceedings of Dialogue 2022.

If you use RuTranscript in research, cite the paper and link to this repository:

> Badasyan, A. A. (2022). *Разработка библиотеки для получения фонетической транскрипции для русского языка*.
> Dialogue 2022 (Dialog-21). https://doi.org/10.5281/zenodo.22900230

## License

RuTranscript is distributed under the [MIT License](LICENSE).
