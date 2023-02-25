from ru_transcript.src.RuTranscript import RuTranscript

if __name__ == "__main__":
    text = 'Как получить транскрипцию?'
    ru_transcript = RuTranscript(text)
    ru_transcript.transcribe()

    print("{:<15} {:}".format('text:', text))
    print("{:<15} {:}".format('accented_text:', ru_transcript.accented_text))
    print("{:<15} {:}".format('transcription:', ru_transcript.transcription))
    print("{:<15} {:}".format('allophones:', ru_transcript.allophones))
    print("{:<15} {:}".format('phonemes:', ru_transcript.phonemes))
