class UnknownTranscriptionSymbolError(ValueError):
    """Raised when transcription contains a symbol unknown to the phoneme parser."""

    def __init__(self, symbol: str) -> None:
        """Create an error for an unknown transcription symbol."""
        super().__init__(f'Unknown symbol found in transcription: {symbol!r}')
