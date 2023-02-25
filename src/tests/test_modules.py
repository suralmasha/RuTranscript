import unittest

from ru_transcript.src.RuTranscript import RuTranscript


class TestModules(unittest.TestCase):

    def test_stress_one_syllable(self):
        testing_text = 'нос'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.accented_text)
        self.assertEqual('но+с', ru_transcript.accented_text)

    def test_stress_yo(self):
        testing_text = 'ёлка'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.accented_text)
        self.assertEqual('ё+лка', ru_transcript.accented_text)

    def test_stress_readme_transcription(self):
        testing_text = 'Как получить транскрипцию?'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.accented_text)
        self.assertEqual('ка+к получи+ть транскри+пцию', ru_transcript.accented_text)

    def test_replace_e(self):
        testing_text = 'синтез речи в библиотеке'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript._tokens)
        self.assertEqual([['синтэз', 'речи', 'в', 'библиотеке']], ru_transcript._tokens)

    def test_replace_yo(self):
        testing_text = 'елка для ее ежика перышка подвел конек мед'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript._tokens)
        self.assertEqual([['ёлка', 'для', 'её', 'ёжика', 'пёрышка', 'подвёл', 'конёк', 'мёд']], ru_transcript._tokens)

    def test_replace_user_dict(self):
        testing_text = 'TTS - это увлекательно'
        ru_transcript = RuTranscript(testing_text, replacement_dict={"tts": "синтез речи"})
        ru_transcript.transcribe()
        print(testing_text, ru_transcript._tokens)
        self.assertEqual([['синтэз', 'речи', 'это', 'увлекательно']], ru_transcript._tokens)


if __name__ == '__main__':
    unittest.main()
