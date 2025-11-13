import unittest

from ru_transcript import RuTranscript


class TestConsonants(unittest.TestCase):

    def test_fricative_g_1(self):
        testing_text = 'господи'
        testing_a_text = 'го+споди'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['γʷ', 'o', 's', 'p', 'ə', 'dʲ', 'ɪ'], ru_transcript.get_allophones())

    def test_fricative_g_2(self):
        testing_text = 'ах да'
        testing_a_text = 'а+х да+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['a', 'γ', 'd', 'ʌ'], ru_transcript.get_allophones())

    def test_nasal_m_n(self):  # 'м' / 'н' перед губно-зубными согласными
        testing_text = 'амфора'
        testing_a_text = 'а+мфора'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['a', 'ɱ', 'f', 'ə', 'r', 'ʌ'], ru_transcript.get_allophones())

    def test_silent_r(self):  # 'р' перед глухими согласными и в конце слова
        testing_text = 'арфа'
        testing_a_text = 'а+рфа'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['a', 'r̥', 'f', 'ʌ'], ru_transcript.get_allophones())

    def test_long_sh(self):  # долгий 'ш', в сочетании 'сш'
        testing_text = 'сшить'
        testing_a_text = 'сши+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂːˠ', 'ɨ', 'tʲ'], ru_transcript.get_allophones())

    def test_ts(self):  # 'ц'
        testing_text = 'цапля'
        testing_a_text = 'ца+пля'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t͡s', 'ɐ.', 'p', 'lʲ', 'æ.'], ru_transcript.get_allophones())

    def test_voiced_ts(self):  # 'ц' перед звонкой согласной
        testing_text = 'плацдарм'
        testing_a_text = 'плацда+рм'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['p', 'l', 'ɐ', 'd̻͡z̪', 'd', 'a', 'r', 'm'], ru_transcript.get_allophones())

    def test_dj(self):  # сочетание 'дж'
        testing_text = 'джунгли'
        testing_a_text = 'джу+нгли'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['d͡ʒᶣ', 'ʉ', 'n', 'ɡ', 'lʲ', 'ɪ'], ru_transcript.get_allophones())

    def test_shch_1(self):  # 'щ'
        testing_text = 'щегол'
        testing_a_text = 'щего+л'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɕː', 'ə', 'ɡʷ', 'o', 'l'], ru_transcript.get_allophones())

    def test_shch_2(self):  # 'ж' перед глух.согл.
        testing_text = 'мужчина'
        testing_a_text = 'мужчи+на'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['mʷ', 'ʊ', 'ɕː', 'i', 'n', 'ʌ'], ru_transcript.get_allophones())

    def test_shch_3(self):  # сочетания 'сч', 'зч', 'жч'
        testing_text = 'считать'
        testing_a_text = 'счита+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɕː', 'ɪ', 't', 'a', 'tʲ'], ru_transcript.get_allophones())

    def test_ch(self):  # 'ч'
        testing_text = 'течь'
        testing_a_text = 'те+чь'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tʲ', 'e', 't͡ɕ'], ru_transcript.get_allophones())

    def test_long_ge_1(self):  # 'ж' долгий
        testing_text = 'жужжать'
        testing_a_text = 'жужжа+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʐʷ', 'ʊ', 'ʑː', 'ɐ.', 'tʲ'], ru_transcript.get_allophones())

    def test_long_ge_2(self):  # 'щ' пред звонкой согласной
        testing_text = 'вещдок'
        testing_a_text = 'вещдо+к'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['vʲ', 'ɪ', 'ʑː', 'dʷ', 'o', 'k'], ru_transcript.get_allophones())

    def test_long_ge_3(self):  # сочетание 'зж'
        testing_text = 'заезжий'
        testing_a_text = 'зае+зжий'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['z', 'ɐ', 'j', 'e', 'ʑːˠ', 'ɨ', 'j'], ru_transcript.get_allophones())

    def test_j_1(self):  # 'й'
        testing_text = 'май'
        testing_a_text = 'ма+й'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['m', 'a', 'j'], ru_transcript.get_allophones())

    def test_j_2(self):  # йотированный гласный после разделительных ъ и ь
        testing_text = 'объявление'
        testing_a_text = 'объявле+ние'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ə', 'bʲ', 'j', 'ɪ', 'v', 'lʲ', 'e', 'nʲ', 'j', 'æ.'], ru_transcript.get_allophones())

    def test_j_3(self):  # йотированный гласный между двумя гласными
        testing_text = 'заяц'
        testing_a_text = 'за+яц'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['z', 'a', 'j', 'ɪ.', 't͡s'], ru_transcript.get_allophones())

    def test_j_4(self):  # йотированный гласный перед ударным гласным
        testing_text = 'заезжий'
        testing_a_text = 'зае+зжий'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['z', 'ɐ', 'j', 'e', 'ʑːˠ', 'ɨ', 'j'], ru_transcript.get_allophones())

    def test_j_5(self):  # йотированный гласный в начале слова
        testing_text = 'яхта'
        testing_a_text = 'я+хта'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʝ', 'æ', 'x', 't', 'ʌ'], ru_transcript.get_allophones())

    def test_j_first(self):  # йот в начале слога
        testing_text = 'я'
        testing_a_text = 'я+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʝ', 'æ'], ru_transcript.get_allophones())

    def test_long_consonant_junction_of_words(self):  # долгий согласный на стыке слов
        testing_text = 'вот так'
        testing_a_text = 'вот так'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['v', 'ɐ', 'tː', 'a', 'k'], ru_transcript.get_allophones())

    def test_consonants_stunning_in_the_end_of_a_word(self):
        testing_text = 'всерьёз'
        ru_transcript = RuTranscript(testing_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['vʲ', 'sʲ', 'ɪ', 'rʲ', 'jᶣ', 'ɵ', 's'], ru_transcript.get_allophones())


if __name__ == '__main__':
    unittest.main()
