import unittest

from RuTranscript.src.ru_transcript import RuTranscript


class TestConsonants(unittest.TestCase):

    def test_one_syllable(self):
        testing_text = 'нос'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('nʷ o s', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['nʷ', 'o', 's'], ru_transcript.allophones)

    def test_yo(self):
        testing_text = 'ёлка'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('ʝᶣ ɵ l k ʌ', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['ʝᶣ', 'ɵ', 'l', 'k', 'ʌ'], ru_transcript.allophones)

    def test_readme_transcription(self):
        testing_text = 'Как получить транскрипцию?'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('k a k p ə lʷ ʊ t͡ɕ ɨ tʲ t r ɐ n s k rʲ i p t͡sˠ ɨ jᶣ ᵿ ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'ɨ', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ',
                          'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ'], ru_transcript.allophones)


if __name__ == '__main__':
    unittest.main()
