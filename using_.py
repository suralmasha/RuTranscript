from RuTranscript.src.ru_transcript import RuTranscript

if __name__ == "__main__":
    a_texts = [
        # 'И никогд+а, н+и в ед+иной с+амой уб+огой с+амой фантаст+ической петерб+ургской комп+ании — мен+я н+е объявл+яли г+ением.',  # 'aʲ'
        # 'Н+о пр+отив +Агнии Фр+анцевны, у мен+я б+ыло с+ильное ор+ужие — в+ежливость.',  # 'ʒʲ'
        # 'Чт+о апперц+епция у Бальз+ака неорган+ична.',  # 't͡sʲ'
        # 'Башк+ирия, Уф+а, эваку+ация, мн+е тр+и нед+ели.',  # 't͡sʲ'
        # 'Насто+ящие мужч+ины г+ибнут н+а передов+ой.',  # 'ɕːʲ'
        # 'Неукл+южие эпигр+аммы.',  # last 'ɨ'
        # 'Д+а и с В+ольфом у мен+я хор+ошие отнош+ения.',  # 'ʂʲ'
        # 'Хот+я наиб+олее чуд+овищные эпат+ирующие подр+обности л+агерной ж+изни, я к+ак говор+ится опуст+ил.',  # 'ɕːʲ'
        # 'Мы+шка, ко+шка и+ соба+ка',  # 'ɨ'
        'ёлка для её ёжика пёрышка подвёл конёк нёбо мёд.',
        'елка для ее ежика перышка подвел конек небо мед.',
    ]

    for a_text in a_texts:
        text = a_text.replace('+', '')
        ru_transcript = RuTranscript(text, a_text, accent_place='before')
        ru_transcript.transcribe()

        print("{:<15} {:}".format('text:', text))
        print("{:<15} {:}".format('transcription:', ru_transcript.transcription))
        print("{:<15} {:}".format('allophones:', ru_transcript.allophones))
        print("{:<15} {:}\n".format('phonemes:', ru_transcript.phonemes))
