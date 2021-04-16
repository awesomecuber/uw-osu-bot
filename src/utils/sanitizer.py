import re


def sanitize(s: str) -> str:
    return re.sub("_", "\\_", s)
