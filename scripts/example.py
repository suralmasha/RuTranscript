from ru_transcript import RuTranscript

if __name__ == '__main__':
    text = 'Как получить транскрипцию?'
    stressed_text_if_have = 'Как получ+ить транскрипцию?'

    ru_transcript = RuTranscript(text, stressed_text_if_have)
    ru_transcript.transcribe()

    print('{:<15} {:}'.format('Original text:', text))
    print(
        '{:<15} {:}'.format('Stressed text:', ru_transcript.get_stressed_text(stress_place='before', stress_symbol='+'))
    )

    print('------------------------------------------------------')
    print('Transcription (allophones):')
    print(' '.join(ru_transcript.get_allophones()))
    print('Transcription (allophones) with spaces, pauses and stresses:')
    print(
        ' '.join(
            ru_transcript.get_allophones(
                stress_place='before', save_stresses=True, save_spaces=True, save_pauses=True, stress_symbol='+'
            )
        )
    )

    print('------------------------------------------------------')
    print('Transcription (phonemes):')
    print(' '.join(ru_transcript.get_phonemes()))
    print('Transcription (phonemes) with spaces, pauses and stresses:')
    print(
        ' '.join(
            ru_transcript.get_phonemes(
                stress_place='before', save_stresses=True, save_spaces=True, save_pauses=True, stress_symbol='+'
            )
        )
    )
