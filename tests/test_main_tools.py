import unittest

from ru_transcript.tools.main_tools import merge_phrasal_words


class TestMergePhrasalWords(unittest.TestCase):
    """Test deterministic phrasal word merging."""

    def test_multiple_clitics_are_merged_in_text_order(self) -> None:
        """Merge clitics on both sides of a main word deterministically."""
        phonemes = ['a', '+', '_', 'b', '+', '_', 'c', '+']

        result = merge_phrasal_words(phonemes, {(1, 2), (1, 0)})

        self.assertEqual(['a', 'b', '+', 'c'], result)

    def test_explicit_clitic_stress_is_preserved(self) -> None:
        """Keep stress on a clitic explicitly marked by the user."""
        result = merge_phrasal_words(['a', '+', '_', 'b', '+'], {(1, 0)}, {0})

        self.assertEqual(['a', '+', 'b', '+'], result)

    def test_stale_relation_is_skipped(self) -> None:
        """Skip a relation whose boundary was removed by an earlier sound rule."""
        result = merge_phrasal_words(['a'], {(1, 0)})

        self.assertEqual(['a'], result)


if __name__ == '__main__':
    unittest.main()
