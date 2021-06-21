import os
from typing import List

from gensim.models.doc2vec import Doc2Vec

from domain.entities.doc2vec import Doc2VecResult
from domain.services.morphological_analysis import IMorphologicalAnalysisService


class SearchService:
    DOC2VEC_MODEL_PATH = os.getenv('DOC2VEC_MODEL_PATH', 'assets/App_Annie/word.model')
    DOCUMENT_LIST_PATH = os.getenv('DOCUMENT_LIST_PATH', 'assets/App_Annie/original-data.txt')
    EPOCHS = 50
    TOP_N = 10

    def __init__(self, sentence: str, ma_service: IMorphologicalAnalysisService) -> None:
        self.model = Doc2Vec.load(self.DOC2VEC_MODEL_PATH)
        self.sentence = sentence
        self.ma_service = ma_service
        with open(self.DOCUMENT_LIST_PATH, encoding='utf-8') as f:
            self.document_list = f.readlines()

    def get_results(self) -> List[Doc2VecResult]:
        # Add the words you want to learn.
        # The measurement time and system can be guaranteed to some extent
        # by setting the number of repetitions to about 50.
        vector = self.model.infer_vector(self.ma_service.get_tokenized(self.sentence), epochs=self.EPOCHS)
        answer = self.model.docvecs.most_similar([vector], topn=self.TOP_N)

        results = []
        for sentence_id, similarity in answer:
            similarity = round(similarity * 100, 2)
            sentence = self.document_list[sentence_id].replace('\\n', '')
            results.append(Doc2VecResult(sentence=sentence, similarity=similarity))
        return results
