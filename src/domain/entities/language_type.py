from enum import IntEnum


class LanguageType(IntEnum):
    ENGLISH = 0
    JAPANESE = 1

    @property
    def language_code(self) -> str:
        """
        ex) name = JAPANESE -> return ja
        ex) name = ENGLISH -> return en
        """
        return self.name.lower()[:2]
