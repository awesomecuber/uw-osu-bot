import re


def sanitize(s):
    return re.sub("_", "\\_", s)
