import string


def check_slug(slug: str) -> bool:
    alphabet = string.ascii_lowercase + string.digits + "_"
    return all(symbol in alphabet for symbol in slug)


class NotSet:
    pass


NOT_SET = NotSet()
