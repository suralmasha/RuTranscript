import unittest

from ru_transcript.tools.stress_tools import place_stress
from tests.helpers import transcribe


class TestStress(unittest.TestCase):
    """Test automatic stress placement."""

    def test_stress_one_syllable(self) -> None:
        """Stress the only vowel in a one-syllable word."""
        self.assertEqual('но+с', transcribe('нос').get_stressed_text())

    def test_stress_yo(self) -> None:
        """Always stress the letter yo."""
        self.assertEqual('ё+лка', transcribe('ёлка').get_stressed_text())

    def test_stress_readme_transcription(self) -> None:
        """Keep the documented automatic stress result."""
        self.assertEqual(
            'ка+к получи+ть транскри+пцию',
            transcribe('Как получить транскрипцию?').get_stressed_text(),
        )

    def test_place_stress_warns_when_stress_is_ambiguous(self) -> None:
        """Warn when the model cannot place stress confidently."""
        with self.assertWarnsRegex(UserWarning, 'Please specify the stress manually'):
            self.assertEqual('полю', place_stress('полю'))

    def test_error_stress(self) -> None:
        """Use the default stress override for a known model error."""
        self.assertEqual(
            'литературнохудо+жественный',
            transcribe('литературнохудожественный').get_stressed_text(),
        )


if __name__ == '__main__':
    unittest.main()
