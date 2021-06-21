from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.exceptions import ValidationException


@dataclass(frozen=True)
class OutputSize:
    height: int
    width: int


@dataclass(frozen=True)
class WordCloudInput:
    content: str

    def __post_init__(self) -> None:
        if len(self.content) == 0:
            raise ValidationException('At least one character is required.')


@dataclass(frozen=True)
class WordCloudImageInput:
    content: str
    output: OutputSize

    def __post_init__(self) -> None:
        if len(self.content) == 0:
            raise ValidationException('At least one character is required.')
        if self.output.height <= 0:
            raise ValidationException('Height must be a positive integer.')
        if self.output.width <= 0:
            raise ValidationException('Width must be a positive integer.')


@dataclass(frozen=True)
class WordWeight:
    name: str
    weight: float


@dataclass(frozen=True)
class WordCloudImageResult:
    url: str
    expiration: Optional[datetime]
