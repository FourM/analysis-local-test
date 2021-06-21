import sys

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedLineDocument

if len(sys.argv) != 2:
    print('引数を確認してください。')
    print('usage: python3 create_model.py (folder_name)')
    exit()

# Doc2Vecの各オプション
# https://onemuri.space/note/1ceozcpdt/

# 設定
# 次元数
SIZE = 300
# 学習に使う前後の単語数
WINDOW = 5
# N回未満登場する単語を破棄
MIN_COUNT = 3
# スレッド数
WORKERS = 3
FOLDER_NAME = sys.argv[1].replace('/', '')


class create_model(str):
    sentences = TaggedLineDocument(f'{FOLDER_NAME}/split-word.txt')
    model = Doc2Vec(
        sentences,
        dm=1,
        vector_size=SIZE,
        window=WINDOW,
        min_count=MIN_COUNT,
        WORKERS=WORKERS,
    )
    model.save(f'{FOLDER_NAME}/word.model')
