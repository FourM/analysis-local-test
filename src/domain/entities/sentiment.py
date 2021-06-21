from dataclasses import dataclass
from enum import Enum


class SentimentOutputType(Enum):
    ALL = 'all'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'


@dataclass(frozen=True)
class SentimentResult:
    text: str
    score: int
