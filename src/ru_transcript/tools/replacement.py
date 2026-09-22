import re
import string
from functools import lru_cache
from pathlib import Path

_SEPARATORS = (
    string.punctuation.replace('+', '').replace('-', '').replace('_', '') + ' \u2014\u201c\u201d\u201e\u00ab\u00bb'
)
_TOKEN_SEPARATOR_RE = re.compile(f'([{re.escape(_SEPARATORS)}])')


@lru_cache(maxsize=4)
def load_replacements(path: Path) -> dict[str, str]:
    """
    Загрузить пары замен из текстового словаря.

    :param path: Путь к словарю в формате `исходное|замена`.
    :return: Словарь замен.
    """
    replacements: dict[str, str] = {}
    with path.open(encoding='utf-8') as dictionary_file:
        for line in dictionary_file:
            source, replacement = line.rstrip('\n').split('|', maxsplit=1)
            replacements[source] = replacement
    return replacements


def replace_word(word: str, replacements: dict[str, str]) -> str:
    """
    Заменить слово по точному совпадению со словарем.

    :param word: Исходное слово.
    :param replacements: Словарь замен.
    :return: Замененное или исходное слово.
    """
    return replacements.get(word, word)


def replace_text(text: str, replacements: dict[str, str]) -> str:
    """
    Заменить отдельные токены текста с сохранением разделителей.

    :param text: Исходный текст.
    :param replacements: Словарь замен.
    :return: Текст после словарных замен.
    """
    tokens = _TOKEN_SEPARATOR_RE.split(text)
    return ''.join(replacements.get(token, token) for token in tokens)
