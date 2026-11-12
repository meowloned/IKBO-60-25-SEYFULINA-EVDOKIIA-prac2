import unittest
from src.config import parse_args
from src.graph import build_graph, validate_test_repository


class GraphTests(unittest.TestCase):

    def setUp(self):
        self.args = parse_args([
            "--package", "A", "--version", "1",
            "--test-mode", "--repository", "examples/repository.json",
        ])

    def test_full_graph(self):
        expected = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D", "E"],
            "D": [],
            "E": ["A"],
        }

        self.assertEqual(build_graph(self.args), expected)

    def test_depth_zero(self):
        self.args.max_depth = 0
        self.assertEqual(build_graph(self.args), {"A": []})

    def test_depth_one(self):
        self.args.max_depth = 1
        expected = {"A": ["B", "C"], "B": [], "C": []}

        self.assertEqual(build_graph(self.args), expected)

    def test_filter(self):
        self.args.filter = "B"
        expected = {
            "A": ["C"],
            "C": ["D", "E"],
            "D": [],
            "E": ["A"],
        }

        self.assertEqual(build_graph(self.args), expected)

    def test_filter_root(self):
        self.args.filter = "A"
        self.assertEqual(build_graph(self.args), {})

    def test_isolated_package(self):
        self.args.package = "F"
        self.assertEqual(build_graph(self.args), {"F": []})

    def test_unknown_package(self):
        self.args.package = "Z"

        with self.assertRaises(ValueError):
            build_graph(self.args)

    def test_missing_dependency(self):
        with self.assertRaises(ValueError):
            validate_test_repository({"A": ["B"]})