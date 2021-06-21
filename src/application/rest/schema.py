from marshmallow import Schema, fields, validate

from domain.entities.sentiment import SentimentOutputType


class Doc2VecSchema(Schema):
    data = fields.Str(required=True)
    language = fields.Int(required=True)


class SentimentSchema(Schema):
    reviews = fields.List(fields.Str(required=True))
    outputType = fields.Str(
        validate=validate.OneOf(
            [
                SentimentOutputType.ALL.value,
                SentimentOutputType.POSITIVE.value,
                SentimentOutputType.NEGATIVE.value,
            ]
        ),
    )
    language = fields.Int(required=True)


class WordCloudSchema(Schema):
    reviews = fields.List(fields.Str(required=True))
    outputHeight = fields.Int(required=True)
    outputWidth = fields.Int(required=True)
    language = fields.Int(required=True)


class SocialListeningSchema(Schema):
    keywords = fields.Str(required=True)
    language = fields.Int(required=True)


class FollowerSearchSchema(Schema):
    followerId = fields.Str(required=True)
    language = fields.Int(required=True)


doc2vec_schema = Doc2VecSchema()
sentiment_schema = SentimentSchema()
wordcloud_schema = WordCloudSchema()
social_listening_schema = SocialListeningSchema()
follower_search_schema = FollowerSearchSchema()