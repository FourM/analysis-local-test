import io
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

from google.cloud import storage
from matplotlib import pyplot as plt
from wordcloud import WordCloud

from domain.entities.wordcloud import OutputSize, WordCloudImageInput, WordCloudImageResult, WordCloudInput, WordWeight
from domain.exceptions import MissingFileDataException, ValidationException
from domain.services.morphological_analysis import IMorphologicalAnalysisService


class WordCloudService:
    GCS_BUCKET_NAME = 'am-nlp'
    GCS_OUTPUT_PATH = 'wordcloud/output'
    GCS_EXPIRATION = timedelta(seconds=86400)
    BACKGROUND_COLOR = 'white'
    FONT_PATH = os.getenv('FONT_PATH', 'assets/font/Arial_Unicode.ttf')

    def __init__(self, ma_service: IMorphologicalAnalysisService) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.GCS_BUCKET_NAME)
        self.ma_service = ma_service

    def get_wordcloud_image(self, content: str, output_height: int, output_width: int) -> WordCloudImageResult:
        wordcloud_input = WordCloudImageInput(
            content=content,
            output=OutputSize(
                height=output_height,
                width=output_width,
            ),
        )
        data = self.generate_wordcloud(wordcloud_input=wordcloud_input)
        url = self.upload_file_to_gcs(data=data, file_name=self.file_name)
        expiration = self.get_expiration_from_url(url=url)
        return WordCloudImageResult(url=url, expiration=expiration)

    def get_results(self, content: str) -> List[WordWeight]:
        wordcloud_input = WordCloudInput(content=content)
        results = self.get_wordcloud_weight(wordcloud_input=wordcloud_input)
        return results

    @property
    def file_name(self) -> str:
        return f'{self.GCS_OUTPUT_PATH}/{uuid.uuid4().hex}.png'

    @staticmethod
    def get_expiration_from_url(url: str) -> Optional[datetime]:
        expires: Optional[List[str]] = parse_qs(urlparse(url).query).get('Expires')
        if expires is None or len(expires) != 1:
            return None
        return datetime.fromtimestamp(int(expires[0]))

    def upload_file_to_gcs(self, data: bytes, file_name: str, extension: str = 'png') -> str:
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(data, content_type=extension)
        return blob.generate_signed_url(expiration=self.GCS_EXPIRATION)

    def get_wakati_text(self, content: str) -> str:
        wakati = self.ma_service.get_wakati(content)
        if not wakati:
            raise ValidationException('Need at least 1 word to plot a word cloud.')
        return wakati

    def get_wordcloud_weight(self, wordcloud_input: WordCloudInput) -> List[WordWeight]:
        text = self.get_wakati_text(wordcloud_input.content)

        frequency = WordCloud().process_text(text)
        results = []
        for name, weight in frequency.items():
            results.append(
                WordWeight(
                    name=name,
                    weight=weight,
                )
            )
        return results

    def generate_wordcloud(self, wordcloud_input: WordCloudImageInput) -> bytes:
        # TODO: will remove the method and handle by highchart instead of image
        if not os.path.exists(self.FONT_PATH):
            raise MissingFileDataException('Fail to generate word cloud.')

        text = self.get_wakati_text(wordcloud_input.content)

        wc = WordCloud(
            font_path=self.FONT_PATH,
            background_color=self.BACKGROUND_COLOR,
            height=wordcloud_input.output.height,
            width=wordcloud_input.output.width,
        ).generate(text)

        figure = plt.figure()
        figure.patch.set_alpha(0)
        plt.imshow(wc)
        # (x,y) axis hidden
        plt.axis('off')

        io_bytes = io.BytesIO()
        plt.savefig(io_bytes)
        io_bytes.seek(0)
        return io_bytes.read()
