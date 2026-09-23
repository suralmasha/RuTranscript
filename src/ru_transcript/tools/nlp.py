from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from ru_transcript.consts import SPACY_RUSSIAN_MODEL

if TYPE_CHECKING:
    from spacy.language import Language


@lru_cache(maxsize=1)
def get_nlp() -> Language:
    """Load and cache the shared Russian spaCy model."""
    import spacy  # noqa: PLC0415

    return spacy.load(SPACY_RUSSIAN_MODEL)
