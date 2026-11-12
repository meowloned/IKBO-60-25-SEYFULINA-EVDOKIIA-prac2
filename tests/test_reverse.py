import unittest
from src.config import parse_args
from src.graph import build_reverse_graph, reverse_repository


class ReverseTests(unittest.TestCase):

    def setUp(self):
        self.args = parse_args([
            "--package", "A", "--version", "1", "--test-mode",
            "--repository", "examples/repository.json",
            "--reverse", "D", "--max-depth", "4",
        ])

    def test_reverse_edges(self):
        repository = {"A": ["B"], "B": []}
        expected = {"A": [], "B": ["A"]}

        self.assertEqual(reverse_repository(repository), expected)

    def test_reverse_graph(self):
        expected = {
            "D": ["B", "C"],
            "B": ["A"],
            "C": ["A"],
            "A": ["E"],
            "E": ["C"],
        }

        self.assertEqual(build_reverse_graph(self.args), expected)

    def test_reverse_depth(self):
        self.args.max_depth = 1
        expected = {"D": ["B", "C"], "B": [], "C": []}

        self.assertEqual(build_reverse_graph(self.args), expected)

    def test_reverse_filter(self):
        self.args.filter = "B"
        expected = {
            "D": ["C"],
            "C": ["A"],
            "A": ["E"],
            "E": ["C"],
        }

        self.assertEqual(build_reverse_graph(self.args), expected)

    def test_reverse_isolated(self):
        self.args.reverse = "F"

        self.assertEqual(build_reverse_graph(self.args), {"F": []})

    def test_reverse_unknown(self):
        self.args.reverse = "Z"

        with self.assertRaises(ValueError):
            build_reverse_graph(self.args)