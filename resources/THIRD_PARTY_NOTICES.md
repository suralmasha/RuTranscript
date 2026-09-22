# Third-party notices

## spaCy Russian pipeline

- Resource: `ru_core_news_sm` 3.8.0
- Author: Explosion
- Source: <https://github.com/explosion/spacy-models/releases/tag/ru_core_news_sm-3.8.0>
- License: MIT
- Included license: `src/rutranscript_resources/data/spacy/ru_core_news_sm-3.8.0/LICENSE`
- Upstream source notices: `src/rutranscript_resources/data/spacy/ru_core_news_sm-3.8.0/LICENSES_SOURCES`

The model files are included without modification.

## StressRNN resources

- Resources: `model.onnx`, `exception_dictionary.txt`
- Source: <https://github.com/Desklop/StressRNN/tree/0afefac146033b41ef558ac356989c87ef764c79>
- License: Apache-2.0
- Included license: `licenses/Apache-2.0.txt`
- SHA-256 `model.onnx`: `1a8ce777cd2e8ca27f2773692882a56685aec3a4fd07e5eef7efc9544b3fa599`
- SHA-256 `exception_dictionary.txt`: `6f5c63e78a888bed6d9c9af9b3340eec2520a1aaeb235ebc154bd45ca2069983`

The resource files are included without modification. RuTranscript uses its own minimal ONNX adapter and does not
redistribute the StressRNN Python package.

## SOVA-TTS pronunciation dictionaries

- Resources: `yo.dict`, `e.dict`
- Source project: <https://github.com/sovaai/sova-tts-tps/tree/v1.2.0>
- Download host used by TPS: <http://dataset.sova.ai/SOVA-TTS/tps_data/>
- Upstream project license: Apache-2.0
- License clarification: <https://github.com/sovaai/sova-tts-tps/issues/3>
- SHA-256 `yo.dict`: `fe83ef9a7725b912f66fc7e7021c8e43408022d0af494fd8cb29241933d5e365`
- SHA-256 `e.dict`: `a532bd7ba1dcf1fefb5c0ca1baceb44719dc62fcfceafeb8c55ee2f0154bafa4`

The dictionary files are included without modification for compatibility testing. Do not publish this package until the
upstream maintainers confirm redistribution terms.
