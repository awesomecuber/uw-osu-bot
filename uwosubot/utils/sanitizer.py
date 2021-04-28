import re


def sanitize(s: str) -> str:
    underscore_index = s.find("_")
    if underscore_index != -1:
        return s[:underscore_index] + "\\" + s[underscore_index:]
    return s
    # NOT WORKING
    # return re.sub(r"([*_~`>])", r"\1", s)
