import unittest

from ..src import RuTranscript


class TestVowels(unittest.TestCase):

    def test_vowel_a_1(self):  # ударный после тв. согл.
        testing_text = 'трава'
        testing_a_text = 'трава+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t', 'r', 'ɐ', 'v', 'a'], ru_transcript.get_allophones())

    def test_vowel_a_2(self):  # ударный после тв. согл. перед 'л'
        testing_text = 'палка'
        testing_a_text = 'па+лка'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['p', 'ɑ', 'l', 'k', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_a_3(self):  # ударный не после тв. согл.
        testing_text = 'пять'
        testing_a_text = 'пя+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['pʲ', 'æ', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_a_4(self):  # ударный после шипящих и ц
        testing_text = 'цапнуть'
        testing_a_text = 'ца+пнуть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t͡s', 'ɐ.', 'p', 'nʷ', 'ʊ', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_a_5(self):  # предударный после тв.согл. или в начале слова
        testing_text = 'паром'
        testing_a_text = 'паро+м'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['p', 'ɐ', 'rʷ', 'o', 'm'], ru_transcript.get_allophones())

    def test_vowel_a_6(self):  # предударный не после тв.согл.
        testing_text = 'тяжёлый'
        testing_a_text = 'тяжё+лый'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tʲ', 'ɪ', 'ʐ', 'ɐ.', 'lˠ', 'ᵻ', 'j'], ru_transcript.get_allophones())

    def test_vowel_a_7(self):  # предударный после шипящих и 'ц'
        testing_text = 'жалеть'
        testing_a_text = 'жале+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʐˠ', 'ᵻ', 'lʲ', 'e', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_a_8(self):  # II предударный или заударный после тв.согл. или в начале слова
        testing_text = 'акварель'
        testing_a_text = 'акваре+ль'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ə', 'k', 'v', 'ɐ', 'rʲ', 'e', 'lʲ'], ru_transcript.get_allophones())

    def test_vowel_a_9(self):  # II предударный или заударный после тв.согл. в финальном слоге
        testing_text = 'собака'
        testing_a_text = 'соба+ка'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['s', 'ɐ', 'b', 'a', 'k', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_a_10(self):  # II предударный или заударный не после тв.согл. не в окончании
        testing_text = 'тяжеленный'
        testing_a_text = 'тяжеле+нный'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tʲ', 'ɪ.', 'ʐ', 'ə', 'lʲ', 'e', 'nːˠ', 'ᵻ', 'j'], ru_transcript.get_allophones())

    def test_vowel_a_11(self):  # II предударный или заударный не после тв.согл. (только в окончании)
        testing_text = 'гуляя'
        testing_a_text = 'гуля+я'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɡʷ', 'ʊ', 'lʲ', 'æ', 'j', 'æ.'], ru_transcript.get_allophones())

    def test_vowel_a_12(self):  # II предударный или заударный после шипящих и 'ц'
        testing_text = 'дача'
        testing_a_text = 'да+ча'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['d', 'a', 't͡ɕ', 'ə'], ru_transcript.get_allophones())

    def test_vowel_o_1(self):  # ударный после тв.согл. или в начале слова
        testing_text = 'облако'
        testing_a_text = 'о+блако'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['o', 'b', 'l', 'ə', 'k', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_o_2(self):  # ударный не после тв.согл.
        testing_text = 'тётя'
        testing_a_text = 'тё+тя'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tᶣ', 'ɵ', 'tʲ', 'æ.'], ru_transcript.get_allophones())

    def test_vowel_o_3(self):  # ударный после шипящих и 'ц'
        testing_text = 'цокать'
        testing_a_text = 'цо+кать'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t͡s', 'ɐ.', 'k', 'ə', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_o_4(self):  # предударный после тв.согл. или в начале слова
        testing_text = 'стопа'
        testing_a_text = 'стопа+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['s', 't', 'ɐ', 'p', 'a'], ru_transcript.get_allophones())

    def test_vowel_o_5(self):  # предударный не после тв.согл.
        testing_text = 'йодированный'
        testing_a_text = 'йоди+рованный'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʝ', 'ɪ', 'dʲ', 'i', 'r', 'ə', 'v', 'ə', 'nːˠ', 'ᵻ', 'j'], ru_transcript.get_allophones())

    def test_vowel_o_6(self):  # предударный после шипящих и ц
        testing_text = 'шокировать'
        testing_a_text = 'шоки+ровать'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂˠ', 'ᵻ', 'kʲ', 'i', 'r', 'ə', 'v', 'ə', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_o_7(self):  # II предударный или заударный после тв.согл. или в начале слога
        testing_text = 'молоко'
        testing_a_text = 'молоко+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['m', 'ə', 'l', 'ɐ', 'kʷ', 'o'], ru_transcript.get_allophones())

    def test_vowel_o_8(self):  # II предударный или заударный после тв.согл. в финальном слоге
        testing_text = 'озеро'
        testing_a_text = 'о+зеро'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['o', 'zʲ', 'ɪ.', 'r', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_o_9(self):  # II предударный или заударный не после тв.согл.
        testing_text = 'огайо'
        testing_a_text = 'ога+йо'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɐ', 'ɡ', 'a', 'j', 'æ.'], ru_transcript.get_allophones())

    def test_vowel_o_10(self):  # II предударный или заударный после шипящих и 'ц'
        testing_text = 'шоколад'
        testing_a_text = 'шокола+д'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂ', 'ə', 'k', 'ɐ', 'l', 'a', 't'], ru_transcript.get_allophones())

    def test_vowel_e_1(self):  # ударный после тв.согл. или в начале слова
        testing_text = 'это'
        testing_a_text = 'э+то'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ɛ', 't', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_e_2(self):  # ударный не после тв.согл.
        testing_text = 'пень'
        testing_a_text = 'пе+нь'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['pʲ', 'e', 'nʲ'], ru_transcript.get_allophones())

    def test_vowel_e_3(self):  # ударный после шипящих и 'ц'
        testing_text = 'шест'
        testing_a_text = 'ше+ст'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂˠ', 'ᵻ', 's', 't'], ru_transcript.get_allophones())

    def test_vowel_e_4(self):  # предударный после тв.согл. или в начале слова (ыэ)
        testing_text = 'этап'
        testing_a_text = 'эта+п'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ᵻ', 't', 'a', 'p'], ru_transcript.get_allophones())

    def test_vowel_e_5(self):  # предударный не после тв.согл. и не в начале слова
        testing_text = 'велюр'
        testing_a_text = 'велю+р'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['vʲ', 'ɪ', 'lᶣ', 'ʉ', 'r̥'], ru_transcript.get_allophones())

    def test_vowel_e_6(self):  # II предударный или заударный не после тв.согл. или в начале слова
        testing_text = 'пепел'
        testing_a_text = 'пе+пел'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['pʲ', 'e', 'pʲ', 'ɪ.', 'l'], ru_transcript.get_allophones())

    def test_vowel_e_7(self):  # предударный, II предударный или заударный после шипящих и 'ц'
        testing_text = 'шелестеть'
        testing_a_text = 'шелесте+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂ', 'ə', 'lʲ', 'ɪ', 'sʲ', 'tʲ', 'e', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_u_1(self):  # ударный после тв.согл.
        testing_text = 'пуля'
        testing_a_text = 'пу+ля'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['pʷ', 'u', 'lʲ', 'æ.'], ru_transcript.get_allophones())

    def test_vowel_u_2(self):  # ударный после мягк.согл.
        testing_text = 'чуть'
        testing_a_text = 'чу+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t͡ɕᶣ', 'ʉ', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_u_3(self):  # предударный после тв.согл.
        testing_text = 'мужчина'
        testing_a_text = 'мужчи+на'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['mʷ', 'ʊ', 'ɕː', 'i', 'n', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_u_4(self):  # предударный не после тв.согл.
        testing_text = 'ютиться'
        testing_a_text = 'юти+ться'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʝᶣ', 'ᵿ', 'tʲ', 'i', 't͡s', 'ə'], ru_transcript.get_allophones())

    def test_vowel_u_5(self):  # II предударный или заударный после тв.согл.
        testing_text = 'музыкальный'
        testing_a_text = 'музыка+льный'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['mʷ', 'ʊ', 'zˠ', 'ᵻ', 'k', 'a', 'lʲ', 'nˠ', 'ᵻ', 'j'], ru_transcript.get_allophones())

    def test_vowel_u_6(self):  # II предударный или заударный не после тв.согл.
        testing_text = 'чумовой'
        testing_a_text = 'чумово+й'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t͡ɕᶣ', 'ᵿ', 'm', 'ɐ', 'vʷ', 'o', 'j'], ru_transcript.get_allophones())

    def test_vowel_i_1(self):  # ударный перед мягк.согл.
        testing_text = 'синего'
        testing_a_text = 'си+него'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['sʲ', 'i', 'nʲ', 'ɪ.', 'v', 'ʌ'], ru_transcript.get_allophones())

    def test_vowel_i_2(self):  # ударный, предударный, II предударный или заударный после шипящих и 'ц'
        testing_text = 'жизнь'
        testing_a_text = 'жи+знь'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʐˠ', 'ɨ', 'zʲ', 'nʲ'], ru_transcript.get_allophones())

    def test_vowel_i_3(self):  # предударный, II предударный или заударный не после гласного или в начале слова
        testing_text = 'синица'
        testing_a_text = 'сини+ца'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['sʲ', 'ɪ', 'nʲ', 'i', 't͡s', 'ə'], ru_transcript.get_allophones())

    def test_vowel_ii_1(self):  # ударный после тв.согл.
        testing_text = 'ты'
        testing_a_text = 'ты+'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tˠ', 'ɨ'], ru_transcript.get_allophones())

    def test_vowel_ii_2(self):  # ударный между переднеязычными и велярными согласными
        testing_text = 'тыкать'
        testing_a_text = 'ты+кать'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['tˠ', 'ɨ̟', 'k', 'ə', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_ii_3(self):  # ударный после сочетания губной согласный + 'л'
        testing_text = 'плыть'
        testing_a_text = 'плы+ть'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['p', 'lˠ', 'ɯ̟ɨ̟', 'tʲ'], ru_transcript.get_allophones())

    def test_vowel_ii_4(self):  # предударный, II предударный или заударный не после 'ц'
        testing_text = 'чтобы'
        testing_a_text = 'что+бы'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['ʂ', 'tʷ', 'o', 'bˠ', 'ᵻ'], ru_transcript.get_allophones())

    def test_vowel_ii_5(self):  # предударный, II предударный или заударный после 'ц'
        testing_text = 'танцы'
        testing_a_text = 'та+нцы'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['t', 'a', 'n', 't͡s', 'ə'], ru_transcript.get_allophones())

    def test_jotised_1(self):
        testing_text = 'бульон'
        testing_a_text = 'бульо+н'
        ru_transcript = RuTranscript(testing_text, testing_a_text)
        ru_transcript.transcribe()
        print(testing_text, ru_transcript.get_allophones())
        self.assertEqual(['bʷ', 'ʊ', 'lʲ', 'jᶣ', 'ɵ', 'n'], ru_transcript.get_allophones())


if __name__ == '__main__':
    unittest.main()
