# rutranscript-resources

Versioned linguistic models and dictionaries used by
[RuTranscript](https://github.com/suralmasha/RuTranscript).

This package is installed automatically with RuTranscript and is not intended as a standalone public API.

## Included resources

- `ru_core_news_sm` 3.8.0 from Explosion, licensed under MIT.
- StressRNN ONNX model and exception dictionary from the pinned upstream revision, licensed under Apache-2.0.
- SOVA-TTS TPS `yo.dict` and `e.dict`, kept unchanged from the upstream distribution.

Redistribution terms for the two SOVA-TTS dictionaries are being clarified in
[sovaai/sova-tts-tps#3](https://github.com/sovaai/sova-tts-tps/issues/3). This package must not be published until the
maintainers confirm the applicable license.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact sources and checksums.
