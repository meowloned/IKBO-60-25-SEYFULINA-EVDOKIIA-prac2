import subprocess
import sys
import unittest

BASE_ARGS = ["--package", "requests", "--version", "2.32.3"]


def run_program(arguments):
    return subprocess.run(
        [sys.executable, "-m", "src.main"] + arguments,
        capture_output=True,
        text=True,
    )


class ConfigTests(unittest.TestCase):

    def test_default_settings(self):
        result = run_program(BASE_ARGS)

        expected = [
            "package=requests", "version=2.32.3",
            "repository=https://pypi.org/pypi", "test_mode=False",
            "ascii=False", "max_depth=3", "filter=",
        ]

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), expected)

    def test_custom_settings(self):
        result = run_program(BASE_ARGS + [
            "--ascii", "--max-depth", "2", "--filter", "urllib",
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ascii=True", result.stdout)
        self.assertIn("max_depth=2", result.stdout)
        self.assertIn("filter=urllib", result.stdout)

    def test_invalid_settings(self):
        cases = [
            ["--package", "bad/name"],
            ["--version", "abc"],
            ["--version", ""],
            ["--repository", "not-a-url"],
            ["--repository", "https://[broken"],
            ["--repository", "https://example.org:bad"],
            ["--test-mode", "yes"],
            ["--ascii", "yes"],
            ["--max-depth", "-1"],
            ["--max-depth", "101"],
            ["--max-depth", "text"],
            ["--filter", "   "],
            ["--package", "A", "--test-mode",
             "--repository", "missing.json"],
        ]

        for arguments in cases:
            result = run_program(BASE_ARGS + arguments)
            self.assertEqual(result.returncode, 2, str(arguments))

    def test_missing_settings(self):
        result = run_program([])
        self.assertEqual(result.returncode, 2)