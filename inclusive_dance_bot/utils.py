import string


def check_slug(s: str) -> bool:
    alphabet = string.ascii_lowercase + string.digits + "_"
    return all(l in alphabet for l in s)


class NotSet:
    pass


NOT_SET = NotSet()
