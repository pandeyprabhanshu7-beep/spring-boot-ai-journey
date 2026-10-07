"""Pack authorized, ranked passages; counts must use the target tokenizer."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    id: str
    tokens: int


def pack(passages: list[Passage], budget: int) -> list[Passage]:
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    if any(p.tokens <= 0 for p in passages):
        raise ValueError("passage tokens must be positive")
    if len({p.id for p in passages}) != len(passages):
        raise ValueError("deduplicate passage IDs before packing")
    selected: list[Passage] = []
    remaining = budget
    for passage in passages:
        if passage.tokens <= remaining:
            selected.append(passage)
            remaining -= passage.tokens
    return selected


if __name__ == "__main__":
    values = [Passage("a", 1400), Passage("b", 1100), Passage("c", 700)]
    print([p.id for p in pack(values, 2200)])
