import subprocess
import sys
import unittest
from src.config import parse_args

BASE_ARGS = ["--package", "requests", "--version", "2.32.3"]


def run_program(arguments):
    return subprocess.run(
        [sys.executable, "-m", "src.main"] + arguments,
        capture_output=True,
        text=True,
    )


class ConfigTests(unittest.TestCase):

    def test_default_settings(self):
        args = parse_args(BASE_ARGS)

        self.assertEqual(args.package, "requests")
        self.assertEqual(args.version, "2.32.3")
        self.assertEqual(args.repository, "https://pypi.org/pypi")
        self.assertFalse(args.test_mode)
        self.assertFalse(args.ascii)
        self.assertEqual(args.max_depth, 3)
        self.assertEqual(args.filter, "")

    def test_custom_settings(self):
        args = parse_args(BASE_ARGS + [
            "--ascii", "--max-depth", "2", "--filter", "urllib",
        ])

        self.assertTrue(args.ascii)
        self.assertEqual(args.max_depth, 2)
        self.assertEqual(args.filter, "urllib")

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