from enum import Enum


class Position(Enum):
    """The position of the phoneme in the word."""

    FIRST = 'first'
    MIDDLE = 'middle'
    LAST = 'last'
