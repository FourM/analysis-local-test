import json
import os
from typing import Dict, List

# import requests
from requests_oauthlib import OAuth1Session

from domain.entities.language_type import LanguageType
from domain.entities.sentiment import SentimentOutputType
from domain.services.sentiment import SentimentService


class SocialListeningService:
    url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, keywords: str, language_type: LanguageType) -> None:
        self.keywords = keywords
        self.language_type = language_type

    @property
    def twitter_oauth(self) -> OAuth1Session:
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        return OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)

    @property
    def create_params(self) -> Dict:
        return {
            'q': self.keywords + ' -RT',
            'locale': self.language_type.language_code,
            'lang': self.language_type.language_code,
            # 'count': 100
        }

    def add_attribute_score(self, tweets: List) -> None:
        for tweet in tweets:
            obj = SentimentService(
                reviews=[tweet['text']],
                output_type=SentimentOutputType.ALL,
                language_type=self.language_type,
            )
            tweet['score'] = str(obj.find_score())

    def get_results(self) -> List:
        req = self.twitter_oauth.get(self.url, params=self.create_params)
        if req.status_code != 200:
            raise Exception('Limit Over RequestCount')

        tweets = json.loads(req.text)['statuses']
        self.add_attribute_score(tweets)

        list = []
        for tweet in tweets:
            list.append(
                {
                    'name': tweet['user']['name'],
                    'account_name': tweet['user']['screen_name'],
                    'text': tweet['text'],
                    'score': tweet['score'],
                }
            )

        return list
