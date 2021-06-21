from dataclasses import asdict

from flask import Blueprint, abort, request

from domain.entities.language_type import LanguageType
from domain.entities.sentiment import SentimentOutputType
from domain.exceptions import DomainException
from domain.services.doc2vec import SearchService
from domain.services.morphological_analysis import get_morphological_analysis
from domain.services.sentiment import SentimentService
from domain.services.social_listening import SocialListeningService
from domain.services.wordcloud import WordCloudService
from domain.services.follower_search import FollowerSearchService


from .schema import doc2vec_schema, sentiment_schema, social_listening_schema, wordcloud_schema, follower_search_schema

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/doc2vec', methods=['POST'])
def doc2vec():
    """Doc2Vec API

    :request body: {"data": xxx}
    :returns (Doc2Vec Result)|error:
        {
            "results": [
                {
                    "sentence": "similar sentence",
                    "similarity": 92.42
                },
                :
            ]
        }
    """
    data = request.get_json()
    errors = doc2vec_schema.validate(data)
    if errors:
        return abort(400, {'errors': ['Missing data.']})

    ma_service = get_morphological_analysis(language_type=LanguageType(data['language']))
    search = SearchService(sentence=data['data'], ma_service=ma_service)
    return {'results': [asdict(res) for res in search.get_results()]}


@api_blueprint.route('/sentiment', methods=['POST'])
def sentiment():
    """Google Natural Language API
    Sentiment analysis is performed using request body data, and the result is returned as response data.

    request body: {
        "reviews": [
            {
                review sentence,
            },
            :
        ]
    }
    returns (Sentiment Analytics Result)|error: {
        'result': [
            {
                'text': review sentence,
                'score': -1～1
            },
            :
        ]
    }
    """
    data = request.get_json()
    errors = sentiment_schema.validate(data)
    if errors:
        return abort(400, {'errors': ['Missing data.']})

    language_type = LanguageType(data['language'])
    obj = SentimentService(
        reviews=data['reviews'],
        output_type=SentimentOutputType(data['outputType']) if 'outputType' in data else SentimentOutputType.ALL,
        language_type=language_type,
    )

    try:
        return {'results': obj.get_results()}
    except DomainException as e:
        return abort(400, {'errors': [e.args[0]]})


@api_blueprint.route('/wordcloud', methods=['POST'])
def wordcloud():
    """WordCloud API
    Output word cloud image from request body, convert to base64 and return as response data.

    request body: {
        "reviews": [
            {
                "review sentence",
            },
            ...
        ]
    }

    :returns
    Response|KeyError
    """

    data = request.get_json()
    errors = wordcloud_schema.validate(data)
    if errors:
        return abort(400, {'errors': ['Missing data.']})

    ma_service = get_morphological_analysis(language_type=LanguageType(data['language']))
    wordcloud_service = WordCloudService(ma_service=ma_service)
    result = wordcloud_service.get_wordcloud_image(
        content=' '.join(data['reviews']),
        output_height=data['outputHeight'],
        output_width=data['outputWidth'],
    )
    try:
        return {'url': result.url}
    except DomainException as e:
        return abort(400, {'errors': [e.args[0]]})


@api_blueprint.route('/social-listening', methods=['POST'])
def social_listening():
    data = request.get_json()
    errors = social_listening_schema.validate(data)
    if errors:
        return abort(400, {'errors': ['Missing data.']})

    language_type = LanguageType(data['language'])
    social_listening_service = SocialListeningService(keywords=data['keywords'], language_type=language_type)
    results = social_listening_service.get_results()

    try:
        return {'results': results}
    except DomainException as e:
        return abort(400, {'errors': [e.args[0]]})


@api_blueprint.route('/follower-search', methods=['POST'])
def follower_search():
    data = request.get_json()
    errors = follower_search_schema.validate(data)
    if errors:
        return abort(400, {'errors': ['Missing data.']})

    language_type = LanguageType(data['language'])
    follower_search_service = FollowerSearchService(follower_id=data['followerId'], language_type=language_type)
    results = follower_search_service.get_results()

    try:
        return {'results': results}
    except DomainException as e:
        return abort(400, {'errors': [e.args[0]]})
