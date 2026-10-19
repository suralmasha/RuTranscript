from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent / 'data'


def spacy_model_path() -> Path:
    """
    Вернуть путь к русской модели spaCy.

    :return: Путь к каталогу модели spaCy.
    """
    return _DATA_PATH / 'spacy' / 'ru_core_news_sm-3.8.0'


def stress_model_path() -> Path:
    """
    Вернуть путь к ONNX-модели ударений.

    :return: Путь к ONNX-модели ударений.
    """
    return _DATA_PATH / 'stress' / 'model.onnx'


def stress_dictionary_path() -> Path:
    """
    Вернуть путь к словарю ударений.

    :return: Путь к словарю ударений.
    """
    return _DATA_PATH / 'stress' / 'exception_dictionary.txt'


def e_dictionary_path() -> Path:
    """
    Вернуть путь к словарю произношения буквы е.

    :return: Путь к словарю произношения буквы е.
    """
    return _DATA_PATH / 'pronunciation' / 'e.dict'


def yo_dictionary_path() -> Path:
    """
    Вернуть путь к словарю восстановления буквы е с двумя точками.

    :return: Путь к словарю восстановления буквы е с двумя точками.
    """
    return _DATA_PATH / 'pronunciation' / 'yo.dict'


__all__ = [
    'e_dictionary_path',
    'spacy_model_path',
    'stress_dictionary_path',
    'stress_model_path',
    'yo_dictionary_path',
]
