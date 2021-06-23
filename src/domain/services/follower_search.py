import json
import os
import csv
import datetime
from typing import Dict, List

from requests_oauthlib import OAuth1Session

from domain.services.morphological_analysis import IMorphologicalAnalysisService


class FollowerSearchService:
    url = 'https://api.twitter.com/1.1/followers/list.json'

    def __init__(self, follower_id: str, ma_service: IMorphologicalAnalysisService) -> None:
        self.follower_id = follower_id
        self.ma_service = ma_service

    @property
    def twitter_oauth(self) -> OAuth1Session:
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        return OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)

    @property
    def create_params(self) -> Dict:
        return {'screen_name': self.follower_id, 'count': 200, 'cursor': -1}

    def get_results(self) -> List:
        req = self.twitter_oauth.get(self.url, params=self.create_params)
        if req.status_code != 200:
            raise Exception('Limit Over RequestCount')

        users = json.loads(req.text)['users']
        # print(len(users))
        # while json.loads(req.text)['next_cursor'] != 0:
        #     self.create_params['cursor'] = json.loads(req.text)['next_cursor']
        #     req = self.twitter_oauth.get(self.url, params=self.create_params)
        #     if req.status_code != 200:
        #         raise Exception('Limit Over RequestCount')
        #     users.append(json.loads(req.text)['users'])
        #     print(len(users))

        sorted_users = sorted(users, key=lambda x: -x['followers_count'])
        follower_list = []

        for user in sorted_users:
            follower_list.append(
                {
                    'id': user['screen_name'],
                    'name': user['name'],
                    'url': 'https://twitter.com/' + user['screen_name'],
                    'keyword': self.ma_service.get_wakati(user['description']),
                }
            )

        return follower_list
