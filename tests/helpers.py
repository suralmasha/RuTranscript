from ru_transcript import RuTranscript
from ru_transcript.consts import STRESS_ACCURACY_THRESHOLD


def transcribe(
    text: str,
    stressed_text: str | None = None,
    *,
    stress_place: str = 'after',
    replacement_dict: dict[str, str] | None = None,
    stress_accuracy_threshold: float = STRESS_ACCURACY_THRESHOLD,
) -> RuTranscript:
    """
    Create and run a transcription.

    :param text: Source text.
    :param stressed_text: Optional manually stressed text.
    :param stress_place: Position of stress markers in manually stressed text.
    :param replacement_dict: Optional word replacement dictionary.
    :param stress_accuracy_threshold: Minimum stress prediction accuracy.
    :return: Completed transcription object.
    """
    transcription = RuTranscript(
        text,
        stressed_text,
        stress_place=stress_place,
        replacement_dict=replacement_dict,
        stress_accuracy_threshold=stress_accuracy_threshold,
    )
    transcription.transcribe()
    return transcription
