import json
import unittest
from pathlib import Path

from ru_transcript.data_constants import ALPHABET, EPI_SYMBOLS
from ru_transcript.tools import epi_symbols


class TestDataFiles(unittest.TestCase):
    """Data file validation tests."""

    def test_epi_symbols_public_import(self) -> None:
        """Check backward-compatible public import of Epitran symbols."""
        self.assertIs(epi_symbols, EPI_SYMBOLS)

    def test_sorted_allophones_json_is_valid(self) -> None:
        """Check that allophone groups are well-formed and reference known allophones."""
        path = Path(__file__).resolve().parents[1] / 'src' / 'ru_transcript' / 'data' / 'sorted_allophones.json'

        with path.open(encoding='utf-8') as file:
            sorted_allophones = json.load(file)

        self.assertIsInstance(sorted_allophones, dict)
        self.assertTrue(sorted_allophones)

        known_allophones = set(ALPHABET)
        for group_name, allophone_group in sorted_allophones.items():
            self.assertIsInstance(group_name, str)
            self.assertTrue(group_name)
            self.assertIsInstance(allophone_group, list)
            self.assertTrue(allophone_group)
            self.assertEqual(len(allophone_group), len(set(allophone_group)), group_name)

            for allophone in allophone_group:
                self.assertIsInstance(allophone, str)
                self.assertTrue(allophone)
                self.assertIn(allophone, known_allophones, f'{allophone!r} in {group_name!r}')


if __name__ == '__main__':
    unittest.main()
