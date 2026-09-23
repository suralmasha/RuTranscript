class UnknownTranscriptionSymbolError(ValueError):
    """Raised when transcription contains a symbol unknown to the phoneme parser."""

    def __init__(self, symbol: str) -> None:
        """Create an error for an unknown transcription symbol."""
        super().__init__(f'Unknown symbol found in transcription: {symbol!r}')


class StressedTextMismatchError(ValueError):
    """Raised when text and its stressed version do not match."""

    def __init__(self) -> None:
        """Create an error for mismatched text."""
        super().__init__('Text and stressed text must match')
