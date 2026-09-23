import unittest

from ru_transcript import text_norm_tok


class TestNormalization(unittest.TestCase):
    """Test public text normalization behavior."""

    def test_dirty_text(self) -> None:
        """Remove unsupported punctuation and preserve word boundaries."""
        text = 'синтез речи - это#$ «увлекательно»'

        result = text_norm_tok(text)

        self.assertEqual([['синтез', 'речи', '-', 'это', 'увлекательно']], result)

    def test_number_is_converted_to_words(self) -> None:
        """Convert a numeric token to Russian words."""
        self.assertEqual([['две', 'тысячи', 'двадцать', 'два']], text_norm_tok('2022'))


if __name__ == '__main__':
    unittest.main()
