from typing import Final

_CHAR: Final[str] = "\u00a7"

_TRANSLATIONS: Final[dict[str, str]] = {
    c: f"{_CHAR}{c}"
    for c in "0123456789abcdefghijklmnopqrstuv"
}

_MAX_LENGTH: Final[int] = 32767


def translate(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text[:_MAX_LENGTH]

    chars = list(text)
    result: list[str] = []

    i = 0
    while i < len(chars):
        char = chars[i]

        if (
            char == "&"
            and i + 1 < len(chars)
        ):
            code = chars[i + 1].lower()

            if code in _TRANSLATIONS:
                result.append(_TRANSLATIONS[code])
                i += 2
                continue

        result.append(char)
        i += 1

    return "".join(result)


def strip_color(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text[:_MAX_LENGTH]

    chars = list(text)
    result: list[str] = []

    i = 0
    while i < len(chars):
        char = chars[i]

        if (
            char == "&"
            and i + 1 < len(chars)
            and chars[i + 1].lower() in _TRANSLATIONS
        ):
            i += 2
            continue

        result.append(char)
        i += 1

    return "".join(result)
