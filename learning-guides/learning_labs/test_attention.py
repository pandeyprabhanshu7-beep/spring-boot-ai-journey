import math
import unittest
from attention import attention


class AttentionTests(unittest.TestCase):
    def test_worked_result(self):
        weights, output = attention([1, 0], [[2, 0], [1, 1]], [[10, 0], [0, 20]])
        self.assertAlmostEqual(weights[0], 0.6697615493266569)
        self.assertAlmostEqual(sum(weights), 1.0)
        self.assertAlmostEqual(output[0], 6.697615493266569)
        self.assertAlmostEqual(output[1], 6.604769013466862)

    def test_equal_scores_mix_equally(self):
        weights, output = attention([0, 0], [[2, 0], [1, 1]], [[10, 0], [0, 20]])
        self.assertEqual(weights, [0.5, 0.5])
        self.assertEqual(output, [5.0, 10.0])

    def test_stable_softmax(self):
        weights, _ = attention([1000], [[1000], [999]], [[1], [2]])
        self.assertTrue(all(math.isfinite(x) for x in weights))
        self.assertAlmostEqual(sum(weights), 1.0)

    def test_shape_rejected(self):
        with self.assertRaises(ValueError):
            attention([1, 2], [[1]], [[1]])

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):
            attention([float("nan")], [[1]], [[1]])


if __name__ == "__main__":
    unittest.main()
