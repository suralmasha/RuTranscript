import unittest

from ru_transcript import RuTranscript
from tests.helpers import transcribe


class TestPublicApi(unittest.TestCase):
    """Test public transcription results and output options."""

    def test_phonemes_are_not_changed_by_allophone_rules(self) -> None:
        """Keep phonemes isolated from consonant allophone rules."""
        transcription = transcribe('амфора')

        self.assertEqual(['a', 'm', 'f', 'o', 'r', 'a'], transcription.get_phonemes())
        self.assertEqual(['a', 'ɱ', 'f', 'ə', 'r', 'ʌ'], transcription.get_allophones())

    def test_join_phonemes_rejects_unknown_symbol(self) -> None:
        """Reject an unknown transliteration symbol."""
        with self.assertRaisesRegex(ValueError, "Unknown symbol found in transcription: 'w'"):
            RuTranscript._join_phonemes(['unknown'])

    def test_output_options(self) -> None:
        """Preserve requested markers and replace the stress symbol."""
        transcription = transcribe('нос дом.', 'но+с до+м.')

        phonemes = transcription.get_phonemes(
            save_stresses=True,
            save_spaces=True,
            save_pauses=True,
            stress_symbol='*',
        )
        allophones = transcription.get_allophones(
            save_stresses=True,
            save_spaces=True,
            save_pauses=True,
            stress_symbol='*',
        )

        self.assertEqual(['n', 'o', '*', 's', '_', 'd', 'o', '*', 'm', '||'], phonemes)
        self.assertEqual(['nʷ', 'o', '*', 's', '_', 'dʷ', 'o', '*', 'm', '||'], allophones)

    def test_stress_can_be_returned_before_vowel(self) -> None:
        """Move custom stress markers before stressed vowels."""
        transcription = transcribe('нос дом', 'но+с до+м')

        self.assertEqual('н*ос д*ом', transcription.get_stressed_text(stress_place='before', stress_symbol='*'))

    def test_reserved_stress_symbol_warns(self) -> None:
        """Warn when a requested stress symbol conflicts with transcription symbols."""
        transcription = transcribe('нос', 'но+с')

        with self.assertWarns(UserWarning):
            transcription.get_allophones(save_stresses=True, stress_symbol='.')

    def test_empty_text(self) -> None:
        """Return empty transcription results for empty text."""
        transcription = transcribe('')

        self.assertEqual([], transcription.get_phonemes())
        self.assertEqual([], transcription.get_allophones())
        self.assertEqual('', transcription.get_stressed_text())

    def test_transcribe_is_idempotent(self) -> None:
        """Keep results unchanged after repeated transcription."""
        transcription = transcribe('Как получить транскрипцию?')
        expected_allophones = transcription.get_allophones()
        expected_phonemes = transcription.get_phonemes()

        transcription.transcribe()

        self.assertEqual(expected_allophones, transcription.get_allophones())
        self.assertEqual(expected_phonemes, transcription.get_phonemes())


if __name__ == '__main__':
    unittest.main()
