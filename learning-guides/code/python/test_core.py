import unittest
from atlas_core import retrieve, cosine, rrf, validate_citations


class RetrievalContract(unittest.TestCase):
    def test_scoped_retrieval(self):
        rows = retrieve("payments rollback", "acme")
        self.assertEqual(rows[0][1].id, "payments-r7")
        self.assertTrue(all(doc.tenant == "acme" for _, doc in rows))
        self.assertNotIn("private-r1", [doc.id for _, doc in rows])

    def test_unknown_scope_and_unknown_query_abstain(self):
        self.assertEqual(retrieve("payments", "unknown"), [])
        self.assertEqual(retrieve("xyzzynonexistent", "acme"), [])

    def test_cosine_and_invalid_vectors(self):
        self.assertAlmostEqual(cosine([1, 0], [.8, .6]), .8)
        for a, b in [([], []), ([1], [1, 2]), ([0, 0], [1, 0]),
                     ([float("nan")], [1])]:
            with self.assertRaises(ValueError):
                cosine(a, b)

    def test_rrf_trace_and_duplicate_handling(self):
        ranked = rrf([["A", "X", "B", "Y"], ["B", "Z", "W", "A"]])
        self.assertEqual(ranked[0][0], "B")
        self.assertAlmostEqual(dict(ranked)["B"], 1/63 + 1/61)
        self.assertEqual(rrf([["A", "A", "B"]]), rrf([["A", "B"]]))

    def test_citations(self):
        self.assertEqual(validate_citations("Restore it [payments-r7]", {"payments-r7"}),
                         {"payments-r7"})
        for text in ["No citation", "Wrong [private-r1]"]:
            with self.assertRaises(ValueError):
                validate_citations(text, {"payments-r7"})

    def test_top_k_bounds(self):
        for k in [0, 21]:
            with self.assertRaises(ValueError):
                retrieve("rollback", "acme", k)


if __name__ == "__main__":
    unittest.main()
