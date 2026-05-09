import re
from typing import Final

_CHAR: Final[str] = "\u00a7"

_TRANSLATIONS: Final[dict[str, str]] = {
    c: f"{_CHAR}{c}"
    for c in "0123456789abcdefghijklmnopqrstuv"
}

_ALLOWED_CODES: Final[str] = "0123456789a-vA-V"

_PATTERN: Final[re.Pattern[str]] = re.compile(
    rf"&([{re.escape(_ALLOWED_CODES)}])",
    re.IGNORECASE
)

_MAX_LENGTH: Final[int] = 32767


def translate(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text[:_MAX_LENGTH]

    def replacer(match: re.Match[str]) -> str:
        code = match.group(1).lower()
        return _TRANSLATIONS.get(code, match.group(0))

    return _PATTERN.sub(replacer, text)


def strip_color(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text[:_MAX_LENGTH]
    return _PATTERN.sub("", text)
