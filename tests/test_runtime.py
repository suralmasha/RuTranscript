import subprocess
import sys
import textwrap
import unittest

from ru_transcript.tools.nlp import get_nlp
from ru_transcript.tools.stress_tools import get_stress_rnn


class TestRuntimeModels(unittest.TestCase):
    """Test lazy shared model initialization."""

    def test_models_are_not_initialized_during_import(self) -> None:
        """Keep spaCy and stress model caches empty after package import."""
        code = textwrap.dedent(
            """
            import ru_transcript
            from ru_transcript.tools.nlp import get_nlp
            from ru_transcript.tools.stress_tools import get_stress_rnn

            assert get_nlp.cache_info().currsize == 0
            assert get_stress_rnn.cache_info().currsize == 0
            """
        )

        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_models_are_shared(self) -> None:
        """Reuse the same spaCy and stress model instances."""
        self.assertIs(get_nlp(), get_nlp())
        self.assertIs(get_stress_rnn(), get_stress_rnn())


if __name__ == '__main__':
    unittest.main()
