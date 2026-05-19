import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path


class TestPanphonEncoding(unittest.TestCase):
    def test_panphon_feature_table_reads_utf8_with_ascii_locale(self):
        project_root = Path(__file__).resolve().parents[1]
        patch_module = project_root / 'src' / 'ru_transcript' / '_panphon_encoding.py'
        code = textwrap.dedent(
            f"""
            import importlib.util

            spec = importlib.util.spec_from_file_location('panphon_encoding_patch', {str(patch_module)!r})
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.patch_panphon_resource_encoding()

            import panphon.featuretable

            panphon.featuretable.FeatureTable()
            """
        )

        env = os.environ.copy()
        env['LC_ALL'] = 'C'
        env['PYTHONUTF8'] = '0'

        result = subprocess.run(
            [sys.executable, '-c', code],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == '__main__':
    unittest.main()
