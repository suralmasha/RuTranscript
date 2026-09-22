from pathlib import Path

import numpy as np
import onnxruntime

_STRESS_SYMBOL = '+'
_VOWELS = (
    '\u0430\u0435\u0438\u043e\u0443\u044d\u044e\u044f\u044b\u0451'
    '\u0410\u0415\u0418\u041e\u0423\u042d\u042e\u042f\u042b\u0401'
)
_MAX_INPUT_LENGTH = 40
_CHARACTERS = [
    "'",
    '-',
    '_',
    '\u0430',
    '\u0431',
    '\u0432',
    '\u0433',
    '\u0434',
    '\u0435',
    '\u0436',
    '\u0437',
    '\u0438',
    '\u0439',
    '\u043a',
    '\u043b',
    '\u043c',
    '\u043d',
    '\u043e',
    '\u043f',
    '\u0440',
    '\u0441',
    '\u0442',
    '\u0443',
    '\u0444',
    '\u0445',
    '\u0446',
    '\u0447',
    '\u0448',
    '\u0449',
    '\u044a',
    '\u044b',
    '\u044c',
    '\u044d',
    '\u044e',
    '\u044f',
    '\u0451',
]
_CHARACTER_INDICES = {character: index for index, character in enumerate(_CHARACTERS)}


class StressPredictor:
    """Предсказывать место ударения с помощью ONNX-модели."""

    def __init__(self, model_path: Path, dictionary_path: Path) -> None:
        """
        Инициализировать модель и словарь исключений.

        :param model_path: Путь к ONNX-модели.
        :param dictionary_path: Путь к словарю исключений.
        """
        session_options = onnxruntime.SessionOptions()
        session_options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
        session_options.inter_op_num_threads = 1
        session_options.intra_op_num_threads = 1
        self._session = onnxruntime.InferenceSession(
            str(model_path),
            sess_options=session_options,
            providers=['CPUExecutionProvider'],
        )
        self._input_names = [model_input.name for model_input in self._session.get_inputs()]
        self._exceptions = self._load_exceptions(dictionary_path)

    @staticmethod
    def _load_exceptions(dictionary_path: Path) -> dict[str, int]:
        """
        Загрузить первые варианты ударения из словаря исключений.

        :param dictionary_path: Путь к словарю исключений.
        :return: Позиции знака ударения для слов.
        """
        exceptions: dict[str, int] = {}
        with dictionary_path.open(encoding='utf-8') as dictionary_file:
            for line in dictionary_file:
                stressed_word = line.rstrip('\n')
                for stress_symbol in ("'", _STRESS_SYMBOL):
                    if stress_symbol in stressed_word:
                        word = stressed_word.replace(stress_symbol, '')
                        exceptions.setdefault(word, stressed_word.find(stress_symbol))
                        break
        return exceptions

    @staticmethod
    def _move_to_vowel(word: str, stress_index: int) -> int:
        """
        Переместить предсказанную позицию на ближайшую гласную.

        :param word: Слово без ударения.
        :param stress_index: Предсказанная позиция ударения.
        :return: Позиция гласной для ударения.
        """
        if word[stress_index] in _VOWELS:
            return stress_index

        vowel_indices = [index for index, character in enumerate(word) if character in _VOWELS]
        next_vowel = next((index for index in vowel_indices if index > stress_index), None)
        return next_vowel if next_vowel is not None else vowel_indices[-1]

    def _predict(self, word: str) -> tuple[int, float]:
        """
        Предсказать позицию и точность ударения.

        :param word: Слово без ударения.
        :return: Позиция ударения и точность предсказания.
        """
        prepared_word = f'_{word.lower()}'
        inputs: np.ndarray = np.zeros(
            (1, _MAX_INPUT_LENGTH, len(_CHARACTER_INDICES)),
            dtype=np.float32,
        )
        for character_index, character in enumerate(prepared_word):
            position = _MAX_INPUT_LENGTH - len(prepared_word) + character_index
            inputs[0, position, _CHARACTER_INDICES[character]] = 1

        model_inputs = dict.fromkeys(self._input_names, inputs)
        prediction: np.ndarray = self._session.run(None, model_inputs)[0][0]
        accuracy = float(np.max(prediction))
        stress_index = len(word) - _MAX_INPUT_LENGTH + int(np.argmax(prediction))
        return self._move_to_vowel(word, stress_index), accuracy

    def put_stress(self, word: str, accuracy_threshold: float) -> str:
        """
        Поставить ударение в слове при достаточной точности.

        :param word: Слово без ударения.
        :param accuracy_threshold: Минимальная точность предсказания.
        :return: Слово с ударением или исходное слово.
        """
        normalized_word = word.lower()
        stress_position = self._exceptions.get(normalized_word)
        if stress_position is None:
            stress_position = self._exceptions.get(normalized_word.replace('\u0451', '\u0435'))
        if stress_position is not None:
            return word[:stress_position] + _STRESS_SYMBOL + word[stress_position:]

        stress_index, accuracy = self._predict(word)
        if accuracy < accuracy_threshold:
            return word
        insertion_index = stress_index + 1
        return word[:insertion_index] + _STRESS_SYMBOL + word[insertion_index:]
