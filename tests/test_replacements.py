import unittest

from tests.helpers import transcribe


class TestReplacements(unittest.TestCase):
    """Test pronunciation and user replacement dictionaries."""

    def test_replace_e(self) -> None:
        """Apply pronunciation replacements for the letter e."""
        transcription = transcribe('синтез речи в библиотеке')

        self.assertEqual([['синтэз', 'речи', 'в', 'библиотеке']], transcription._tokens)

    def test_replace_yo(self) -> None:
        """Restore the letter yo from the pronunciation dictionary."""
        transcription = transcribe('елка для ее ежика перышка подвел конек мед')

        self.assertEqual(
            [['ёлка', 'для', 'её', 'ёжика', 'пёрышка', 'подвёл', 'конёк', 'мёд']],
            transcription._tokens,
        )

    def test_replace_user_dict(self) -> None:
        """Apply user replacements before transcription."""
        transcription = transcribe('TTS - это увлекательно', replacement_dict={'tts': 'синтез речи'})

        self.assertEqual([['синтэз', 'речи'], ['это', 'увлекательно']], transcription._tokens)


if __name__ == '__main__':
    unittest.main()
