import re

_snakecase_re = re.compile(r"((?<=[a-z\d])[A-Z]|(?!^)[A-Z](?=[a-z]))")
_snakecase_spaces_re = re.compile(r"[ -_]+")


def snakecase(string: str) -> str:
    normalized = _snakecase_re.sub(r"_\1", string).lower()
    return _snakecase_spaces_re.sub("_", normalized)
