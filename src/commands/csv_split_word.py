import logging
import sys

import pandas

if len(sys.argv) != 3:
    print('引数を確認してください')
    print('usage: python3 csv_split_word.py (folder_name) (target_column)')
    exit()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

FOLDER_NAME = sys.argv[1]
TARGET_COLUMN = sys.argv[2]

dataframe = pandas.read_csv(f'{FOLDER_NAME}/original-data.csv', encoding='utf8', header=0)
# 特定列のみ抽出
dataframe = dataframe[[TARGET_COLUMN]]

with open(f'{FOLDER_NAME}/original-data.txt', mode='w') as f:
    for sentences in dataframe.values:
        print(str(sentences[0]))
        f.write(str(sentences[0]) + '\r\n')
