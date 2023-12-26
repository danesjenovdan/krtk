import unittest

from services import _generate_next_alias


class TestGenerateNextAlias(unittest.TestCase):
    def test_simple_examples(self):
        self.assertEqual(_generate_next_alias("a"), "b")
        self.assertEqual(_generate_next_alias("h"), "i")
        self.assertEqual(_generate_next_alias("y"), "z")
        self.assertEqual(_generate_next_alias("aaab"), "aaac")
        self.assertEqual(_generate_next_alias("zzzy"), "zzzz")
        self.assertEqual(_generate_next_alias("lulek"), "lulel")

    def test_all_zs(self):
        self.assertEqual(_generate_next_alias("z"), "aa")
        self.assertEqual(_generate_next_alias("zzz"), "aaaa")
        self.assertEqual(_generate_next_alias("zzzzzzzzzz"), "aaaaaaaaaaa")

    def test_overflow(self):
        self.assertEqual(_generate_next_alias("az"), "ba")
        self.assertEqual(_generate_next_alias("azz"), "baa")
        self.assertEqual(_generate_next_alias("yzzzzz"), "zaaaaa")
