import json
import os
import requests
from typing import Dict, List

from requests_oauthlib import OAuth1Session

from domain.services.morphological_analysis import IMorphologicalAnalysisService


class FollowerSearchService:
    url = 'https://api.twitter.com/1.1/followers/list.json'
    url_v2 = 'https://api.twitter.com/2/users/1287922033993453568/followers' #FourM_AppのID直指定している

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
    def twitter_oauth_v2(self) -> List:
        headers = {'Authorization': 'Bearer ' + os.getenv('TWITTER_BEARER_TOKEN')}
        params = {'max_results': 1000, 'user.fields': 'description,public_metrics'}
        r = requests.get(self.url_v2, headers=headers, params=params).json()
        users: List = r['data']
        while 'next_token' not in r['meta']:
            params['pagination_token'] = r['meta']['next_token']
            r = requests.get(self.url_v2, headers=headers, params=params).json()
            users.extend(r['data'])

        return users

    @property
    def twitter_oauth_v1(self) -> List:
        params = {'screen_name': self.follower_id, 'count': 200, 'cursor': -1}
        req = self.twitter_oauth.get(self.url, params=params)
        if req.status_code != 200:
            raise Exception('Limit Over RequestCount')

        users = json.loads(req.text)['users']
        while json.loads(req.text)['next_cursor'] != 0:
            params['cursor'] = json.loads(req.text)['next_cursor']
            req = self.twitter_oauth.get(self.url, params=params)
            if req.status_code != 200:
                raise Exception('Limit Over RequestCount')
            users.extend(json.loads(req.text)['users'])
        return users

    def get_results_v2(self) -> List:
        users = self.twitter_oauth_v2
        follower_list = []
        sorted_users = sorted(users, key=lambda x: -x['public_metrics']['followers_count'])
        for user in sorted_users:
            follower_list.append(
                {
                    'id': user['username'],
                    'name': user['name'],
                    'url': 'https://twitter.com/' + user['username'],
                    'keyword': self.ma_service.get_wakati(user['description'])
                }
            )

        return follower_list

    def get_results_v1(self):
        users = self.twitter_oauth_v1
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
