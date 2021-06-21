import os
from typing import Dict, List, Optional

import requests

from domain.entities.language_type import LanguageType
from domain.entities.sentiment import SentimentOutputType, SentimentResult
from domain.exceptions import APIRequestException, MissingEnvironmentVariableException

GOOGLE_NLP_API_ENDPOINT = 'https://language.googleapis.com/v1/documents:analyzeSentiment'


def find_sentences(result: List[SentimentResult], output_type: SentimentOutputType):
    """
    Extract positive or negative sentences only

    :param result: Sentiment analytics result list
    :param output_type: "positive" or "negative"
    :return: "positive only sentence list" or "negative only sentence list"
    """
    sentences = []
    for item in result:
        score = float(item.score)
        if is_positive(output_type, score) or is_negative(output_type, score):
            sentences.append(item)

    return sentences


def is_positive(output_type: SentimentOutputType, score: float) -> bool:
    return output_type == SentimentOutputType.POSITIVE and score >= 0.4


def is_negative(output_type: SentimentOutputType, score: float) -> bool:
    return output_type == SentimentOutputType.NEGATIVE and score <= -0.4


class SentimentService:
    def __init__(self, reviews: List[str], output_type: SentimentOutputType, language_type: LanguageType) -> None:
        self.reviews = reviews
        self.output_type = output_type
        self.language_type = language_type

    @property
    def api_headers(self) -> Dict[str, str]:
        return {'Content-Type': 'application/json'}

    @property
    def api_params(self) -> Dict[str, str]:
        api_key: Optional[str] = os.getenv('GOOGLE_NLP_API_KEY')
        if api_key is None:
            raise MissingEnvironmentVariableException('`GOOGLE_NLP_API_KEY` is missing.')
        return {'key': api_key}

    def api_body(self, text: str) -> Dict[str, Dict[str, str]]:
        """
        review sentence list -> one long review sentences,
        prepare google Natural Language API data.

        return: {
            'document': {
                'type': 'PLAIN_TEXT',
                'language': 'ja',
                'content': 'review sentences'
            }
        }
        """

        return {
            'document': {
                'type': 'PLAIN_TEXT',
                'language': self.language_type.language_code,
                'content': text,
            }
        }

    def get_results(self) -> List:
        """
        Response Google Natural Language API data,
        Create text and score list.

        return: [
            {
                'text': 'review sentence',
                'score': 'sentiment score'
            },
            :
        ]
        """
        all_result = []
        for review in self.reviews:
            text = review.replace('\\n', '')
            res = requests.post(
                url=GOOGLE_NLP_API_ENDPOINT,
                headers=self.api_headers,
                params=self.api_params,
                json=self.api_body(text),
            )
            if not res.ok:
                raise APIRequestException('Failed to fetch the data.')

            all_result.append(SentimentResult(text=text, score=res.json()['documentSentiment']['score']))

            if self.output_type in (
                SentimentOutputType.POSITIVE,
                SentimentOutputType.NEGATIVE,
            ):
                all_result = find_sentences(all_result, output_type=self.output_type)

        return all_result

    def find_score(self) -> int:
        res = requests.post(
            url=GOOGLE_NLP_API_ENDPOINT,
            headers=self.api_headers,
            params=self.api_params,
            json=self.api_body,
        )
        if not res.ok:
            raise APIRequestException('Failed to fetch the data.')

        return res.json()['documentSentiment']['score']
