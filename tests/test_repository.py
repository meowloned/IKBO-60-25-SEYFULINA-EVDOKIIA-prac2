import unittest

from src.repository import extract_dependencies


class RepositoryTests(unittest.TestCase):
    def test_dependencies(self):
        dependencies = ["idna>=2.5", "urllib3<3"]
        data = {"info": {"requires_dist": dependencies}}

        self.assertEqual(extract_dependencies(data), dependencies)

    def test_no_dependencies(self):
        data = {"info": {"requires_dist": None}}

        self.assertEqual(extract_dependencies(data), [])

    def test_invalid_response(self):
        with self.assertRaises(ValueError):
            extract_dependencies({})