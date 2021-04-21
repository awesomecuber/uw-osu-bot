import re


def sanitize(s: str) -> str:
    return re.sub(r"([*_~`>])", r"\1", s)
