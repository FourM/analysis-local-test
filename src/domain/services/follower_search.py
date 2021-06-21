import json
import os
from typing import Dict, List

# import requests
from requests_oauthlib import OAuth1Session

from domain.entities.language_type import LanguageType
from domain.entities.sentiment import SentimentOutputType
from domain.services.sentiment import SentimentService


class FollowerSearchService:
    url = 'https://api.twitter.com/1.1/followers/list.json'

    def __init__(self, follower_id: str, language_type: LanguageType) -> None:
        self.follower_id = follower_id
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
            'screen_name': self.follower_id,
            'count': 100
        }

    def get_results(self) -> List:
        req = self.twitter_oauth.get(self.url, params=self.create_params)
        if req.status_code != 200:
            raise Exception('Limit Over RequestCount')

        users = json.loads(req.text)['users']
        list = []
        for user in users:
            list.append(
                {
                    'screen_name': user['screen_name'],
                    'name': user['name'],
                    'url': 'https://twitter.com/' + user['screen_name'],
                    'description': user['description'],
                }
            )

        return list
