"""Deterministic retrieval lab. Standard library only; no LLM or vector database."""
from dataclasses import dataclass
from collections import Counter
import math
import re


@dataclass(frozen=True)
class Document:
    id: str
    tenant: str
    revision: int
    text: str


CORPUS = (
    Document("payments-r7", "acme", 7,
             "Payments rollback: restore the previous verified image digest. "
             "Check database migration compatibility before rollback."),
    Document("cache-r2", "acme", 2,
             "Prevent cache stampede with bounded single flight and randomized TTL. "
             "A Redis lock needs ownership-aware release."),
    Document("vectors-r3", "acme", 3,
             "Embedding migration requires a new index generation. "
             "Never mix vectors from incompatible embedding models."),
    Document("private-r1", "globex", 1,
             "Payments rollback uses the confidential Globex recovery procedure."),
)


def terms(text: str) -> Counter:
    return Counter(re.findall(r"[a-z0-9]+", text.lower()))


def lexical_score(query: str, text: str) -> float:
    """Bag-of-words cosine baseline; explicitly not BM25 or neural embeddings."""
    a, b = terms(query), terms(text)
    denominator = math.sqrt(sum(v*v for v in a.values()) *
                            sum(v*v for v in b.values()))
    return sum(v*b[k] for k, v in a.items()) / denominator if denominator else 0.0


def retrieve(query: str, trusted_tenant: str, top_k: int = 3):
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be in [1, 20]")
    eligible = [d for d in CORPUS if d.tenant == trusted_tenant]
    scored = [(lexical_score(query, d.text), d) for d in eligible]
    return sorted((pair for pair in scored if pair[0] > 0),
                  key=lambda pair: (-pair[0], pair[1].id))[:top_k]


def cosine(a, b) -> float:
    if not a or len(a) != len(b):
        raise ValueError("non-empty equal dimensions required")
    if not all(math.isfinite(v) for v in (*a, *b)):
        raise ValueError("finite vector coordinates required")
    aa, bb = sum(v*v for v in a), sum(v*v for v in b)
    if aa == 0 or bb == 0:
        raise ValueError("zero vector has no cosine direction")
    return sum(x*y for x, y in zip(a, b)) / math.sqrt(aa*bb)


def rrf(rankings, k: int = 60):
    if k < 1:
        raise ValueError("k must be positive")
    scores = Counter()
    for ranking in rankings:
        seen = set()
        rank = 0
        for doc_id in ranking:
            if doc_id in seen:
                continue
            seen.add(doc_id)
            rank += 1
            scores[doc_id] += 1 / (k + rank)
    return sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))


def validate_citations(answer: str, allowed_ids: set[str]) -> set[str]:
    cited = set(re.findall(r"\[([A-Za-z0-9_-]+)\]", answer))
    if not cited or not cited.issubset(allowed_ids):
        raise ValueError("missing or unknown evidence citation")
    return cited  # Membership is not a proof of factual support.


if __name__ == "__main__":
    for score, doc in retrieve("payments rollback", "acme"):
        print(f"{doc.id}\t{score:.6f}\t{doc.text}")
