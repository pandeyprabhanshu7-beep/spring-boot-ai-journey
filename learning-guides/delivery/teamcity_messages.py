"""Encode TeamCity log attributes. Restrict message type/attribute names in callers."""
import re


def escape(value: str) -> str:
    replacements = {"|": "||", "'": "|'", "\n": "|n", "\r": "|r", "[": "|[", "]": "|]"}
    return "".join(replacements.get(char, char) for char in value)


def message(kind: str, **attributes: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", kind):
        raise ValueError("invalid message kind")
    if any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", key) for key in attributes):
        raise ValueError("invalid attribute name")
    body = " ".join(f"{key}='{escape(value)}'" for key, value in attributes.items())
    return f"##teamcity[{kind}{' ' if body else ''}{body}]"


if __name__ == "__main__":
    print(message("testStarted", name="retrieval.tenantIsolation"))
