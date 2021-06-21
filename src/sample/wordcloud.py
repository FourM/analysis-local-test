import os

import grpc
from anymanagerapis.nlp.protos import language_pb2, wordcloud_pb2, wordcloud_pb2_grpc


def run() -> None:
    port = os.getenv('PORT', '5000')
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = wordcloud_pb2_grpc.WordCloudStub(channel)
        try:
            response: wordcloud_pb2.WordCloudReply = stub.GetWordCloudResults(
                wordcloud_pb2.WordCloudRequest(
                    content='すもももももももものうち',
                    language=language_pb2.Language.JAPANESE,
                )
            )
            for result in response.results:
                print(result.name, result.weight)
        except grpc.RpcError as e:
            print(e.code())
            print(e.details())


if __name__ == '__main__':
    run()
