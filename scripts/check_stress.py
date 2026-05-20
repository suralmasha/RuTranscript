import argparse
import warnings

from ru_transcript.consts import STRESS_ACCURACY_THRESHOLD
from ru_transcript.tools.stress_tools import place_stress, stress_rnn


def main() -> None:
    parser = argparse.ArgumentParser(description='Manually check stress placement for a word or phrase.')
    parser.add_argument('text', help='Russian word or phrase to check.')
    parser.add_argument(
        '--threshold',
        type=float,
        default=STRESS_ACCURACY_THRESHOLD,
        help=f'StressRNN accuracy threshold used by place_stress. Default: {STRESS_ACCURACY_THRESHOLD}.',
    )
    args = parser.parse_args()

    print(f'Input: {args.text}')
    print(f'StressRNN: {stress_rnn.put_stress(args.text, accuracy_threshold=args.threshold)}')
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter('always')
        print(f'place_stress: {place_stress(args.text, stress_accuracy_threshold=args.threshold)}')

    for warning in caught_warnings:
        print(f'Warning: {warning.message}')


if __name__ == '__main__':
    main()
