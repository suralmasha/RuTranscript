import unittest

from RuTranscript.src.ru_transcript import RuTranscript


class TestPhrases(unittest.TestCase):

    def test_readme_transcription(self):
        testing_text = 'Как получить транскрипцию?'
        testing_a_text = 'Ка+к получи+ть транскри+пцию?'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('k a k p ə lʷ ʊ t͡ɕ ɨ tʲ t r ɐ n s k rʲ i p t͡sˠ ɨ jᶣ ᵿ ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'ɨ', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ',
                          'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ'], ru_transcript.allophones)

    def test_readme_comma(self):
        testing_text = 'Мышка, кошка и собака'
        testing_a_text = 'Мы+шка, ко+шка и+ соба+ка'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('mˠ ɨ ʂ k ʌ | kʷ o ʂ k ʌ i s ɐ b a k ʌ', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['mˠ', 'ɨ', 'ʂ', 'k', 'ʌ', 'kʷ', 'o', 'ʂ', 'k', 'ʌ', 'i', 's', 'ɐ', 'b', 'a', 'k', 'ʌ'],
                         ru_transcript.allophones)


if __name__ == '__main__':
    unittest.main()
