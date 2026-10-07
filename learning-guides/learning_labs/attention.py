"""One-query attention arithmetic. Teaching code, not a model-serving engine."""
import math


def attention(query, keys, values):
    dimension = len(query)
    if dimension == 0 or not keys or len(keys) != len(values):
        raise ValueError("nonempty matching keys and values required")
    value_dimension = len(values[0])
    if value_dimension == 0 or any(len(k) != dimension for k in keys):
        raise ValueError("invalid key or value dimensions")
    if any(len(v) != value_dimension for v in values):
        raise ValueError("inconsistent value dimensions")
    if any(not math.isfinite(x) for row in [query, *keys, *values] for x in row):
        raise ValueError("finite inputs required")
    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(dimension)
              for key in keys]
    if any(not math.isfinite(score) for score in scores):
        raise ValueError("attention score overflow")
    largest = max(scores)
    exponentials = [math.exp(score - largest) for score in scores]
    denominator = sum(exponentials)
    weights = [value / denominator for value in exponentials]
    output = [sum(weight * value[j] for weight, value in zip(weights, values))
              for j in range(value_dimension)]
    return weights, output


if __name__ == "__main__":
    weights, output = attention([1, 0], [[2, 0], [1, 1]], [[10, 0], [0, 20]])
    print("weights:", [round(x, 6) for x in weights])
    print("output:", [round(x, 6) for x in output])
