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

    def test_1(self):
        testing_text = 'И никогда, ни в единой самой убогой самой фантастической петербургской компании ' \
                       '— меня не объявляли гением.'
        testing_a_text = 'И никогд+а, н+и в ед+иной с+амой уб+огой с+амой фантаст+ической петерб+ургской комп+ании ' \
                         '— мен+я н+е объявл+яли г+ением.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('i nʲ ɪ k ɐ ɡ d a | nʲ ɪ v j ɪ dʲ i n ə j s a m ə j ᵿ bʷ o ɡ ə j s a m ə j f ə n t ɐ sʲ tʲ '
                         'i t͡ɕ ə s k ə j pʲ ɪ. tʲ ɪ r bʷ u r ʒ s k ə j k ɐ m p a nʲ ɪ i | mʲ ɪ nʲ æ nʲ ɪ. ə bʲ j ɪ '
                         'v lʲ æ lʲ ɪ ɡʲ e nʲ ɪ j ɪ. m ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['i', 'nʲ', 'ɪ', 'k', 'ɐ', 'ɡ', 'd', 'a', 'nʲ', 'ɪ', 'v', 'j', 'ɪ', 'dʲ', 'i', 'n', 'ə', 'j',
                          's', 'a', 'm', 'ə', 'j', 'ᵿ', 'bʷ', 'o', 'ɡ', 'ə', 'j', 's', 'a', 'm', 'ə', 'j', 'f', 'ə',
                          'n', 't', 'ɐ', 'sʲ', 'tʲ', 'i', 't͡ɕ', 'ə', 's', 'k', 'ə', 'j', 'pʲ', 'ɪ.', 'tʲ', 'ɪ', 'r',
                          'bʷ', 'u', 'r', 'ʒ', 's', 'k', 'ə', 'j', 'k', 'ɐ', 'm', 'p', 'a', 'nʲ', 'ɪ', 'i', 'mʲ', 'ɪ',
                          'nʲ', 'æ', 'nʲ', 'ɪ.', 'ə', 'bʲ', 'j', 'ɪ', 'v', 'lʲ', 'æ', 'lʲ', 'ɪ', 'ɡʲ', 'e', 'nʲ',
                          'ɪ', 'j', 'ɪ.', 'm'], ru_transcript.allophones)

    def test_2(self):
        testing_text = 'Но против Агнии Францевны, у меня было сильное оружие — вежливость.'
        testing_a_text = 'Н+о пр+отив +Агнии Фр+анцевны, у мен+я б+ыло с+ильное ор+ужие — в+ежливость.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('n ɐ p rʷ o tʲ ɪ v a ɡ nʲ ɪ i f r a n t͡s ə v nˠ ᵻ | ᵿ mʲ ɪ nʲ æ bˠ ɨ l ʌ sʲ i lʲ n ə j æ. ɐ '
                         'rʷ u ʒ j æ. | vʲ e ʒ lʲ ɪ v ə sʲ tʲ ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['n', 'ɐ', 'p', 'rʷ', 'o', 'tʲ', 'ɪ', 'v', 'a', 'ɡ', 'nʲ', 'ɪ', 'i', 'f', 'r', 'a', 'n',
                          't͡s', 'ə', 'v', 'nˠ', 'ᵻ', 'ᵿ', 'mʲ', 'ɪ', 'nʲ', 'æ', 'bˠ', 'ɨ', 'l', 'ʌ', 'sʲ', 'i', 'lʲ',
                          'n', 'ə', 'j', 'æ.', 'ɐ', 'rʷ', 'u', 'ʒ', 'j', 'æ.', 'vʲ', 'e', 'ʒ', 'lʲ', 'ɪ', 'v', 'ə',
                          'sʲ', 'tʲ'], ru_transcript.allophones)

    def test_3(self):
        testing_text = 'Что апперцепция у Бальзака неорганична.'
        testing_a_text = 'Чт+о апперц+епция у Бальз+ака неорган+ична.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('ʂ tʷ o ə p pʲ ɪ r̥ t͡sˠ ᵻ p t͡sˠ ɨ j æ. ᵿ b ɐ lʲ z a k ʌ nʲ ɪ. ə r ɡ ɐ nʲ i t͡ɕ n ʌ ||',
                         ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['ʂ', 'tʷ', 'o', 'ə', 'p', 'pʲ', 'ɪ', 'r̥', 't͡sˠ', 'ᵻ', 'p', 't͡sˠ', 'ɨ', 'j', 'æ.', 'ᵿ', 'b',
                          'ɐ', 'lʲ', 'z', 'a', 'k', 'ʌ', 'nʲ', 'ɪ.', 'ə', 'r', 'ɡ', 'ɐ', 'nʲ', 'i', 't͡ɕ', 'n', 'ʌ'],
                         ru_transcript.allophones)

    def test_4(self):
        testing_text = 'Башкирия, Уфа, эвакуация, мне три недели.'
        testing_a_text = 'Башк+ирия, Уф+а, эваку+ация, мн+е тр+и нед+ели.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('b ɐ ʂ kʲ i rʲ j æ. | ᵿ f a | ɪ. v ə kʷ ʊ æ t͡sˠ ɨ j æ. | mʲ nʲ e t rʲ i nʲ ɪ dʲ e lʲ ɪ ||',
                         ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['b', 'ɐ', 'ʂ', 'kʲ', 'i', 'rʲ', 'j', 'æ.', 'ᵿ', 'f', 'a', 'ɪ.', 'v', 'ə', 'kʷ', 'ʊ', 'æ',
                          't͡sˠ', 'ɨ', 'j', 'æ.', 'mʲ', 'nʲ', 'e', 't', 'rʲ', 'i', 'nʲ', 'ɪ', 'dʲ', 'e', 'lʲ', 'ɪ'],
                         ru_transcript.allophones)

    def test_5(self):
        testing_text = 'Настоящие мужчины гибнут на передовой.'
        testing_a_text = 'Насто+ящие мужч+ины г+ибнут н+а передов+ой.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('n ə s t ɐ j æ ɕː ɨ j æ. mʷ ʊ ɕː ɨ nˠ ᵻ ɡʲ i b nʷ ʊ t n ə pʲ ɪ. rʲ ɪ. d ɐ vʷ o j ||',
                         ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['n', 'ə', 's', 't', 'ɐ', 'j', 'æ', 'ɕː', 'ɨ', 'j', 'æ.', 'mʷ', 'ʊ', 'ɕː', 'ɨ', 'nˠ', 'ᵻ',
                          'ɡʲ', 'i', 'b', 'nʷ', 'ʊ', 't', 'n', 'ə', 'pʲ', 'ɪ.', 'rʲ', 'ɪ.', 'd', 'ɐ', 'vʷ', 'o', 'j'],
                         ru_transcript.allophones)

    def test_6(self):
        testing_text = 'Неуклюжие эпиграммы.'
        testing_a_text = 'Неукл+южие эпигр+аммы.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('nʲ ɪ. ᵿ k lᶣ ʉ ʒ j æ. ɪ. pʲ ɪ ɡ r a mːˠ ᵻ ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['nʲ', 'ɪ.', 'ᵿ', 'k', 'lᶣ', 'ʉ', 'ʒ', 'j', 'æ.', 'ɪ.', 'pʲ', 'ɪ', 'ɡ', 'r', 'a', 'mːˠ', 'ᵻ'],
                         ru_transcript.allophones)

    def test_7(self):
        testing_text = 'Да и с Вольфом у меня хорошие отношения.'
        testing_a_text = 'Д+а и с В+ольфом у мен+я хор+ошие отнош+ения.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('d a i s vʷ o lʲ f ə m u mʲ ɪ nʲ æ x ɐ rʷ o ʂ j æ. ə t n ɐ ʂˠ ᵻ nʲ j æ. ||',
                         ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['d', 'a', 'i', 's', 'vʷ', 'o', 'lʲ', 'f', 'ə', 'm', 'u', 'mʲ', 'ɪ', 'nʲ', 'æ', 'x', 'ɐ',
                          'rʷ', 'o', 'ʂ', 'j', 'æ.', 'ə', 't', 'n', 'ɐ', 'ʂˠ', 'ᵻ', 'nʲ', 'j', 'æ.'],
                         ru_transcript.allophones)

    def test_8(self):
        testing_text = 'Хотя наиболее чудовищные эпатирующие подробности лагерной жизни, я как говорится опустил.'
        testing_a_text = 'Хот+я наиб+олее чуд+овищные эпат+ирующие подр+обности л+агерной ж+изни, я к+ак говор+ится ' \
                         'опуст+ил.'
        ru_transcript = RuTranscript(testing_text, testing_a_text, accent_place='before')
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('x ɐ tʲ æ n ə i bʷ o lʲ ɪ. j æ. t͡ɕᶣ ᵿ dʷ o vʲ ɪ ɕː nˠ ᵻ j æ. ɪ. p ɐ tʲ i rʷ ʊ jᶣ ᵿ ɕː ɨ j æ. '
                         'p ɐ d rʷ o b n ə sʲ tʲ ɪ l a ɡʲ ɪ. r n ɐ j ʒˠ ɨ zʲ nʲ ɪ | ʝ æ k a k ɡ ə v ɐ rʲ i t͡s ə ə pʷ '
                         'ʊ sʲ tʲ i l ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['x', 'ɐ', 'tʲ', 'æ', 'n', 'ə', 'i', 'bʷ', 'o', 'lʲ', 'ɪ.', 'j', 'æ.', 't͡ɕᶣ', 'ᵿ', 'dʷ', 'o',
                          'vʲ', 'ɪ', 'ɕː', 'nˠ', 'ᵻ', 'j', 'æ.', 'ɪ.', 'p', 'ɐ', 'tʲ', 'i', 'rʷ', 'ʊ', 'jᶣ', 'ᵿ', 'ɕː',
                          'ɨ', 'j', 'æ.', 'p', 'ɐ', 'd', 'rʷ', 'o', 'b', 'n', 'ə', 'sʲ', 'tʲ', 'ɪ', 'l', 'a', 'ɡʲ',
                          'ɪ.', 'r', 'n', 'ɐ', 'j', 'ʒˠ', 'ɨ', 'zʲ', 'nʲ', 'ɪ', 'ʝ', 'æ', 'k', 'a', 'k', 'ɡ', 'ə', 'v',
                          'ɐ', 'rʲ', 'i', 't͡s', 'ə', 'ə', 'pʷ', 'ʊ', 'sʲ', 'tʲ', 'i', 'l'], ru_transcript.allophones)

    def test_jo(self):
        testing_text = 'елка для ее ежика перышка подвел конек мед.'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.transcription)
        self.assertEqual('ʝᶣ ɵ l k ʌ d lʲ æ j ɪ jᶣ ɵ jᶣ ɵ ʒˠ ɨ k ʌ pᶣ ɵ rˠ ᵻ ʂ k ʌ p ɐ d vᶣ ɵ l k ɐ nᶣ ɵ kʲ '
                         'mᶣ ɵ d ||', ru_transcript.transcription)
        print(testing_text, ru_transcript.allophones)
        self.assertEqual(['ʝᶣ', 'ɵ', 'l', 'k', 'ʌ', 'd', 'lʲ', 'æ', 'j', 'ɪ', 'jᶣ', 'ɵ', 'jᶣ', 'ɵ', 'ʒˠ', 'ɨ', 'k', 'ʌ',
                          'pᶣ', 'ɵ', 'rˠ', 'ᵻ', 'ʂ', 'k', 'ʌ', 'p', 'ɐ', 'd', 'vᶣ', 'ɵ', 'l', 'k', 'ɐ', 'nᶣ', 'ɵ', 'kʲ',
                          'mᶣ', 'ɵ', 'd'], ru_transcript.allophones)


if __name__ == '__main__':
    unittest.main()
