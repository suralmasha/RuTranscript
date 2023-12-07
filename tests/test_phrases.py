import unittest

from ..src import RuTranscript


class TestPhrases(unittest.TestCase):

    def test_readme_transcription(self):
        testing_text = 'Как получить транскрипцию?'
        testing_a_text = 'Ка+к получи+ть транскри+пцию?'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['k', 'a', 'k', 'p', 'ə', 'lʷ', 'ʊ', 't͡ɕ', 'i', 'tʲ', 't', 'r', 'ɐ', 'n', 's', 'k', 'rʲ',
                          'i', 'p', 't͡sˠ', 'ɨ', 'jᶣ', 'ᵿ'], ru_transcript.get_allophones())

    def test_readme_comma(self):
        testing_text = 'Мышка, кошка и собака'
        testing_a_text = 'Мы+шка, ко+шка и+ соба+ка'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['mˠ', 'ɨ', 'ʂ', 'k', 'ʌ', 'kʷ', 'o', 'ʂ', 'k', 'ʌ', 'i', 's', 'ɐ', 'b', 'a', 'k', 'ʌ'],
                         ru_transcript.get_allophones())

    def test_1(self):
        testing_text = 'И никогда, ни в единой самой убогой самой фантастической петербургской компании ' \
                       '— меня не объявляли гением.'
        testing_a_text = 'И никогд+а, н+и в ед+иной с+амой уб+огой с+амой фантаст+ической петерб+ургской комп+ании ' \
                         '— мен+я н+е объявл+яли г+ением.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['i', 'nʲ', 'ɪ', 'k', 'ɐ', 'ɡ', 'd', 'a', 'nʲ', 'ɪ', 'vʲ', 'j', 'ɪ', 'dʲ', 'i', 'n', 'ə', 'j',
                          's', 'a', 'm', 'ə', 'j', 'ᵿ', 'bʷ', 'o', 'ɡ', 'ə', 'j', 's', 'a', 'm', 'ə', 'j', 'f', 'ə',
                          'n', 't', 'ɐ', 'sʲ', 'tʲ', 'i', 't͡ɕ', 'ə', 's', 'k', 'ə', 'j', 'pʲ', 'ɪ.', 'tʲ', 'ɪ', 'r',
                          'bʷ', 'u', 'r', 'ʐ', 's', 'k', 'ə', 'j', 'k', 'ɐ', 'm', 'p', 'a', 'nʲ', 'ɪ', 'i', 'mʲ', 'ɪ',
                          'nʲ', 'æ', 'nʲ', 'ɪ.', 'ə', 'bʲ', 'j', 'ɪ', 'v', 'lʲ', 'æ', 'lʲ', 'ɪ', 'ɡʲ', 'e', 'nʲ',
                          'ɪ', 'j', 'ɪ.', 'm'], ru_transcript.get_allophones())

    def test_2(self):
        testing_text = 'Но против Агнии Францевны, у меня было сильное оружие — вежливость.'
        testing_a_text = 'Н+о пр+отив +Агнии Фр+анцевны, у мен+я б+ыло с+ильное ор+ужие — в+ежливость.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['n', 'ɐ', 'p', 'rʷ', 'o', 'tʲ', 'ɪ', 'v', 'a', 'ɡ', 'nʲ', 'ɪ', 'i', 'f', 'r', 'a', 'n',
                          't͡s', 'ə', 'v', 'nˠ', 'ᵻ', 'ᵿ', 'mʲ', 'ɪ', 'nʲ', 'æ', 'bˠ', 'ɨ', 'l', 'ʌ', 'sʲ', 'i', 'lʲ',
                          'n', 'ə', 'j', 'æ.', 'ɐ', 'rʷ', 'u', 'ʐ', 'j', 'æ.', 'vʲ', 'e', 'ʐ', 'lʲ', 'ɪ', 'v', 'ə',
                          'sʲ', 'tʲ'], ru_transcript.get_allophones())

    def test_3(self):
        testing_text = 'Что апперцепция у Бальзака неорганична.'
        testing_a_text = 'Чт+о апперц+епция у Бальз+ака неорган+ична.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂ', 'tʷ', 'o', 'ə', 'p', 'pʲ', 'ɪ', 'r̥', 't͡sˠ', 'ᵻ', 'p', 't͡sˠ', 'ɨ', 'j', 'æ.', 'ᵿ', 'b',
                          'ɐ', 'lʲ', 'z', 'a', 'k', 'ʌ', 'nʲ', 'ɪ.', 'ə', 'r', 'ɡ', 'ɐ', 'nʲ', 'i', 't͡ɕ', 'n', 'ʌ'],
                         ru_transcript.get_allophones())

    def test_4(self):
        testing_text = 'Башкирия, Уфа, эвакуация, мне три недели.'
        testing_a_text = 'Башк+ирия, Уф+а, эваку+ация, мн+е тр+и нед+ели.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['b', 'ɐ', 'ʂ', 'kʲ', 'i', 'rʲ', 'j', 'æ.', 'ᵿ', 'f', 'a', 'ɪ.', 'v', 'ə', 'kʷ', 'ʊ', 'æ',
                          't͡sˠ', 'ɨ', 'j', 'æ.', 'mʲ', 'nʲ', 'e', 't', 'rʲ', 'i', 'nʲ', 'ɪ', 'dʲ', 'e', 'lʲ', 'ɪ'],
                         ru_transcript.get_allophones())

    def test_5(self):
        testing_text = 'Настоящие мужчины гибнут на передовой.'
        testing_a_text = 'Насто+ящие мужч+ины г+ибнут н+а передов+ой.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['n', 'ə', 's', 't', 'ɐ', 'j', 'æ', 'ɕː', 'ɪ', 'j', 'æ.', 'mʷ', 'ʊ', 'ɕː', 'i', 'nˠ', 'ᵻ',
                          'ɡʲ', 'i', 'b', 'nʷ', 'ʊ', 't', 'n', 'ə', 'pʲ', 'ɪ.', 'rʲ', 'ɪ.', 'd', 'ɐ', 'vʷ', 'o', 'j'],
                         ru_transcript.get_allophones())

    def test_6(self):
        testing_text = 'Неуклюжие эпиграммы.'
        testing_a_text = 'Неукл+южие эпигр+аммы.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['nʲ', 'ɪ.', 'ᵿ', 'k', 'lᶣ', 'ʉ', 'ʐ', 'j', 'æ.', 'ɪ.', 'pʲ', 'ɪ', 'ɡ', 'r', 'a', 'mːˠ', 'ᵻ'],
                         ru_transcript.get_allophones())

    def test_7(self):
        testing_text = 'Да и с Вольфом у меня хорошие отношения.'
        testing_a_text = 'Д+а и с В+ольфом у мен+я хор+ошие отнош+ения.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        self.assertEqual(['d', 'a', 'i', 's', 'vʷ', 'o', 'lʲ', 'f', 'ə', 'm', 'ᵿ', 'mʲ', 'ɪ', 'nʲ', 'æ', 'x', 'ɐ',
                          'rʷ', 'o', 'ʂ', 'j', 'æ.', 'ə', 't', 'n', 'ɐ', 'ʂˠ', 'ᵻ', 'nʲ', 'j', 'æ.'],
                         ru_transcript.get_allophones())

    def test_8(self):
        testing_text = 'Хотя наиболее чудовищные эпатирующие подробности лагерной жизни, я как говорится опустил.'
        testing_a_text = 'Хот+я наиб+олее чуд+овищные эпат+ирующие подр+обности л+агерной ж+изни, я к+ак говор+ится ' \
                         'опуст+ил.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['x', 'ɐ', 'tʲ', 'æ', 'n', 'ə', 'i', 'bʷ', 'o', 'lʲ', 'ɪ.', 'j', 'æ.', 't͡ɕᶣ', 'ᵿ', 'dʷ', 'o',
                          'vʲ', 'ɪ', 'ɕː', 'nˠ', 'ᵻ', 'j', 'æ.', 'ɪ.', 'p', 'ɐ', 'tʲ', 'i', 'rʷ', 'ʊ', 'jᶣ', 'ᵿ', 'ɕː',
                          'ɪ', 'j', 'æ.', 'p', 'ɐ', 'd', 'rʷ', 'o', 'b', 'n', 'ə', 'sʲ', 'tʲ', 'ɪ', 'l', 'a', 'ɡʲ',
                          'ɪ.', 'r', 'n', 'ɐ', 'j', 'ʐˠ', 'ɨ', 'zʲ', 'nʲ', 'ɪ', 'ʝ', 'æ', 'k', 'a', 'k', 'ɡ', 'ə', 'v',
                          'ɐ', 'rʲ', 'i', 't͡s', 'ə', 'ə', 'pʷ', 'ʊ',
                          'sʲ', 'tʲ', 'i', 'l'], ru_transcript.get_allophones())

    def test_yo(self):
        testing_text = 'елка для ее ежика перышка подвел конек мед.'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʝᶣ', 'ɵ', 'l', 'k', 'ʌ', 'd', 'lʲ', 'æ', 'j', 'ɪ', 'jᶣ', 'ɵ', 'jᶣ', 'ɵ', 'ʐˠ', 'ɨ', 'k', 'ʌ',
                          'pᶣ', 'ɵ', 'rˠ', 'ᵻ', 'ʂ', 'k', 'ʌ', 'p', 'ɐ', 'd', 'vᶣ', 'ɵ', 'l', 'k', 'ɐ', 'nᶣ', 'ɵ', 'kʲ',
                          'mᶣ', 'ɵ', 't'], ru_transcript.get_allophones())

    def test_dashes(self):
        testing_text = 'Синтез речи - это что-то увлекательное!'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['sʲ', 'i', 'n', 'tˠ', 'ᵻ', 'z', 'rʲ', 'e', 't͡ɕ', 'ɪ', 'ɛ', 't', 'ʌ', 'ʂ', 'tʷ', 'o', 't',
                          'ʌ', 'ᵿ', 'v', 'lʲ', 'ɪ', 'k', 'a', 'tʲ', 'ɪ.', 'lʲ', 'n', 'ə', 'j', 'æ.'],
                         ru_transcript.get_allophones())

    def test_spaces(self):
        testing_text = 'Синтез речи     - это что-то        увлекательное!\n'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['sʲ', 'i', 'n', 'tˠ', 'ᵻ', 'z', 'rʲ', 'e', 't͡ɕ', 'ɪ', 'ɛ', 't', 'ʌ', 'ʂ', 'tʷ', 'o', 't',
                          'ʌ', 'ᵿ', 'v', 'lʲ', 'ɪ', 'k', 'a', 'tʲ', 'ɪ.', 'lʲ', 'n', 'ə', 'j', 'æ.'],
                         ru_transcript.get_allophones())

    def test_skipping_proclitic(self):
        testing_text = 'Они расцветают и становятся заметными лишь на фоне какого-нибудь безобразия.'
        testing_a_text = 'Он+и расцвет+ают и стан+овятся зам+етными л+ишь н+а ф+оне какого-нибудь безобр+азия.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, stress_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɐ', 'nʲ', 'i', 'r', 'ə', 's', 'd̻͡z̪', 'vʲ', 'ɪ', 't', 'a', 'jᶣ', 'ᵿ', 't', 'ᵻ', 's', 't',
                          'ɐ', 'nʷ', 'o', 'vʲ', 'ɪ.', 't͡s', 'ə', 'z', 'ɐ', 'mʲ', 'e', 't', 'nˠ', 'ᵻ', 'mʲ', 'ɪ',
                          'lʲ', 'ɪ', 'ʂ', 'n', 'ɐ', 'fʷ', 'o', 'nʲ', 'æ.', 'k', 'ɐ', 'kʷ', 'o', 'v', 'ə', 'nʲ', 'ɪ',
                          'bʷ', 'ʊ', 'dʲ', 'bʲ', 'ɪ.', 'z', 'ɐ', 'b', 'r', 'a', 'zʲ', 'j', 'æ.'],
                         ru_transcript.get_allophones())

    def test_skipping_enclitic(self):
        testing_text = 'Да это же писатель!'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['d', 'ɐ', 'e', 't', 'ə', 'ʐ', 'ə', 'pʲ', 'ɪ', 's', 'a', 'tʲ', 'ɪ.', 'lʲ'],
                         ru_transcript.get_allophones())


if __name__ == '__main__':
    unittest.main()
