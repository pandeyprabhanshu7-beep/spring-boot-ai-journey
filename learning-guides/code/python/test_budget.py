import unittest
from budget import Passage, pack


class BudgetTests(unittest.TestCase):
    def test_skip_oversized_preserves_order(self):
        items = [Passage("a", 1400), Passage("b", 1100), Passage("c", 700)]
        self.assertEqual([p.id for p in pack(items, 2200)], ["a", "c"])

    def test_exact_fit(self):
        self.assertEqual(pack([Passage("a", 100)], 100), [Passage("a", 100)])

    def test_zero_budget(self):
        self.assertEqual(pack([Passage("a", 1)], 0), [])

    def test_negative_budget(self):
        with self.assertRaises(ValueError):
            pack([], -1)

    def test_nonpositive_count(self):
        with self.assertRaises(ValueError):
            pack([Passage("a", 0)], 100)

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            pack([Passage("a", 10), Passage("a", 10)], 100)


if __name__ == "__main__":
    unittest.main()
