import os

import grpc
from anymanagerapis.nlp.protos import language_pb2, sentiment_pb2, sentiment_pb2_grpc


def run() -> None:
    port = os.getenv('PORT', '5000')
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = sentiment_pb2_grpc.SentimentStub(channel)
        try:
            response: sentiment_pb2.SentimentReply = stub.GetSentimentResults(
                sentiment_pb2.SentimentRequest(
                    contents=['すもももももももものうち'],
                    language=language_pb2.Language.JAPANESE,
                )
            )
            for result in response.results:
                print(result.content, result.sentiment_type)
        except grpc.RpcError as e:
            print(e.code())
            print(e.details())


if __name__ == '__main__':
    run()
