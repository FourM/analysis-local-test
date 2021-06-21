import abc
import os
from typing import List, Optional

import MeCab
import treetaggerwrapper

from domain.entities.language_type import LanguageType
from domain.exceptions import DomainException


class IMorphologicalAnalysisService(abc.ABC):
    @abc.abstractmethod
    def get_tokenized(self, sentence: str, word_classes: Optional[List[str]] = None) -> List[str]:
        ...

    def get_wakati(self, sentence: str, word_classes: Optional[List[str]] = None) -> str:
        """
        Return string with a space between words filtered by word classes (noun/verb...etc.)
        """
        return ' '.join(self.get_tokenized(sentence=sentence, word_classes=word_classes))


class JAMorphologicalAnalysisService(IMorphologicalAnalysisService):
    MECAB_COMMAND = os.getenv('MECAB_COMMAND', '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    DEFAULT_WORD_CLASSES = ['名詞']

    def get_tokenized(self, sentence: str, word_classes: Optional[List[str]] = None) -> List[str]:
        """
        Word-separation of sentences

        :returns: List of characters containing two or more adjectives, nouns, or adverbs
        """
        available_word_classes = word_classes or self.DEFAULT_WORD_CLASSES

        tagger = MeCab.Tagger(self.MECAB_COMMAND)
        node = tagger.parseToNode(sentence)
        output = []
        while node:
            word_class = node.feature.split(',')[0]
            if word_class in available_word_classes and len(node.surface) > 1:
                output.append(node.surface)
            node = node.next
        return output


class ENMorphologicalAnalysisService(IMorphologicalAnalysisService):
    TREE_TAGGER_DIR = os.getenv('TREE_TAGGER_DIR', '/treeTagger')
    DEFAULT_WORD_CLASSES = [
        'NN',  # 名詞
        'NNS',
        'NP',
        'NPS',
    ]
    TAG_LANG = 'en'

    def get_tokenized(self, sentence: str, word_classes: Optional[List[str]] = None) -> List[str]:
        available_word_classes = word_classes or self.DEFAULT_WORD_CLASSES

        tag_separate = treetaggerwrapper.TreeTagger(TAGLANG=self.TAG_LANG, TAGDIR=self.TREE_TAGGER_DIR).tag_text(
            sentence
        )
        tags = treetaggerwrapper.make_tags(tag_separate)

        output = []
        for tag in tags:
            if tag.pos in available_word_classes:
                output.append(tag.lemma)
        return output


def get_morphological_analysis(language_type: LanguageType) -> IMorphologicalAnalysisService:
    if language_type == LanguageType.JAPANESE:
        return JAMorphologicalAnalysisService()
    if language_type == LanguageType.ENGLISH:
        return ENMorphologicalAnalysisService()
    raise DomainException('The language is not support yet.')
