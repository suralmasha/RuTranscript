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


class InvalidStressPlaceError(ValueError):
    """Raised when the stress marker position is invalid."""

    def __init__(self) -> None:
        """Create an error for an invalid stress marker position."""
        super().__init__('Stress place must be "before" or "after"')


class InvalidStressThresholdError(ValueError):
    """Raised when the stress accuracy threshold is invalid."""

    def __init__(self) -> None:
        """Create an error for an invalid stress accuracy threshold."""
        super().__init__('Stress accuracy threshold must be between 0 and 1')


class EmptySyntaxTreeError(ValueError):
    """Raised when a dependency tree cannot be built from text."""

    def __init__(self) -> None:
        """Create an error for text without sentences."""
        super().__init__('Text must contain a sentence')
