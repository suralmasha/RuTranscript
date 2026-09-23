import unittest

from ru_transcript.tools import nasal_m_n, silent_r, voiced_ts


class TestAllophoneRules(unittest.TestCase):
    """Test isolated consonant allophone transformations."""

    def test_nasal_assimilation(self) -> None:
        """Convert a nasal before a labiodental consonant."""
        section = ['m', 'f']

        nasal_m_n(section)

        self.assertEqual(['ɱ', 'f'], section)

    def test_sonorant_devoicing(self) -> None:
        """Devoice a sonorant before a voiceless consonant."""
        section = ['r', 'f']

        silent_r(section)

        self.assertEqual(['r̥', 'f'], section)

    def test_ts_voicing(self) -> None:
        """Voice an affricate before a voiced consonant."""
        section = ['t͡s', 'd']

        voiced_ts(section)

        self.assertEqual(['d̻͡z̪', 'd'], section)


if __name__ == '__main__':
    unittest.main()
