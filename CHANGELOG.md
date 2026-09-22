# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-09-22

### Added

- Support for Python 3.11 alongside Python 3.12.
- Continuous integration tests for all supported Python versions.
- Package metadata, the MIT License, and a stable DOI for the project paper.

### Changed

- Optimized transcription processing and consolidated package data files.
- Pinned Git dependencies to specific revisions for reproducible installations.
- Reworked the README and simplified the Ruff commands in the Makefile.

## [2.0.1] - 2026-05-19

### Fixed

- Explicitly loaded PanPhon resources as UTF-8.
- Prevented the TPS dependency from downloading NLTK data during import.

## [2.0.0] - 2026-05-19

### Changed

- Updated the project to Python 3.12 and refreshed dependencies.
- Adapted transcription and allophone processing to the updated linguistic dependencies.

[2.1.0]: https://github.com/suralmasha/RuTranscript/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/suralmasha/RuTranscript/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/suralmasha/RuTranscript/compare/v1.0.0...v2.0.0
