from RuTranscript.src.ru_transcript import RuTranscript

text = 'Как получить транскрипцию?'
ru_transcript = RuTranscript(text)
ru_transcript.transcribe()

print(ru_transcript.transcription)
print(ru_transcript.allophones)
