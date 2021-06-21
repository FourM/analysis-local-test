from dataclasses import dataclass


@dataclass(frozen=True)
class Doc2VecResult:
    sentence: str
    similarity: float
