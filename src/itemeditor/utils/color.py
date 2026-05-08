import re
from typing import Final

_CHAR: Final[str] = "\u00a7"

_TRANSLATIONS: Final[dict[str, str]] = {
    "0": f"{_CHAR}0", "1": f"{_CHAR}1", "2": f"{_CHAR}2", "3": f"{_CHAR}3",
    "4": f"{_CHAR}4", "5": f"{_CHAR}5", "6": f"{_CHAR}6", "7": f"{_CHAR}7",
    "8": f"{_CHAR}8", "9": f"{_CHAR}9", "a": f"{_CHAR}a", "b": f"{_CHAR}b",
    "c": f"{_CHAR}c", "d": f"{_CHAR}d", "e": f"{_CHAR}e", "f": f"{_CHAR}f",
    "g": f"{_CHAR}g", "h": f"{_CHAR}h", "i": f"{_CHAR}i", "j": f"{_CHAR}j",
    "k": f"{_CHAR}k", "l": f"{_CHAR}l", "m": f"{_CHAR}m", "n": f"{_CHAR}n",
    "o": f"{_CHAR}o", "p": f"{_CHAR}p", "q": f"{_CHAR}q", "r": f"{_CHAR}r",
    "s": f"{_CHAR}s", "t": f"{_CHAR}t", "u": f"{_CHAR}u", "v": f"{_CHAR}v",
}

_PATTERN = re.compile(r"&([0-9a-vA-V])")
_MAX_LENGTH: Final[int] = 32767  # Minecraft text limit


def translate(text: str) -> str:
    if not text:
        return text
    text = text[:_MAX_LENGTH]
    return _PATTERN.sub(lambda m: _TRANSLATIONS.get(m.group(1).lower(), m.group(0)), text)


def strip_color(text: str) -> str:
    if not text:
        return text
    text = text[:_MAX_LENGTH]
    return _PATTERN.sub("", text)
