import unittest

from ru_transcript import RuTranscript


class TestValidation(unittest.TestCase):
    """Test input and option validation."""

    def test_mismatched_stressed_text_is_rejected(self) -> None:
        """Reject incomplete manually stressed text."""
        with self.assertRaisesRegex(ValueError, 'Text and stressed text must match'):
            RuTranscript('молоко два', stressed_text='молоко')

    def test_invalid_stress_place_is_rejected(self) -> None:
        """Reject an unsupported stress marker position."""
        with self.assertRaisesRegex(ValueError, 'Stress place must be'):
            RuTranscript('молоко', stress_place='inside')

    def test_invalid_stress_threshold_is_rejected(self) -> None:
        """Reject stress accuracy thresholds outside the probability range."""
        for threshold in (-0.1, 1.1):
            with (
                self.subTest(threshold=threshold),
                self.assertRaisesRegex(ValueError, 'Stress accuracy threshold must be between 0 and 1'),
            ):
                RuTranscript('молоко', stress_accuracy_threshold=threshold)

    def test_clitic_spelling_is_accepted(self) -> None:
        """Accept a clitic joined to its host in manually stressed text."""
        RuTranscript('Муха по полю пошла', stressed_text='Муха по+полю пошла')


if __name__ == '__main__':
    unittest.main()
