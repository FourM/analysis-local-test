import sys

import numpy
from adjustText import adjust_text
from gensim.models.doc2vec import Doc2Vec
from matplotlib import pyplot
from MulticoreTSNE import MulticoreTSNE

# ある単語をグラフの中心に、類似した単語をグラフ上に散りばめるイメージ

if len(sys.argv) != 3:
    print('引数を確認してください。')
    print('usage: python3 output_plot.py (folder_name) (search_word)')
    exit()

FOLDER_NAME = sys.argv[1].replace('/', '')
SEARCH_WORD = sys.argv[2]

JOB_COUNT = 4
FONT_NAME = 'MigMix 1M'
MAIN_WORD_COLOR = '#00FFFF'
LEFT_UP_WORD_COLOR = '#66FF66'
RIGHT_UP_WORD_COLOR = '#FF6666'
LEFT_DOWN_WORD_COLOR = '#6666FF'
RIGHT_DOWN_WORD_COLOR = '#FF66FF'


# 絵文字かどうか判別
def is_emoji(word: str):
    bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xFFFD)
    return word.translate(bmp_map) == '�'


# 類似単語一覧vectorを取得
def load_vector(model: Doc2Vec, word: str):
    split = word.split('+')
    positive_word_list = []
    negative_word_list = []
    for s in split:
        if '-' not in s:
            positive_word_list.append(s)
        else:
            _split = s.split('-')
            positive_word = _split.pop(0)
            positive_word_list.append(positive_word)
            negative_word_list.extend(_split)

    # try:
    results = model.wv.most_similar(positive=positive_word_list, negative=negative_word_list, topn=60)
    # except KeyError:
    # modelに存在しない単語であれば、学習させてもいいかもしれない
    # exit()
    # wakati = Tagger("-O wakati")
    # wakati_words = wakati.parse(word).strip().split()
    # temp_vector = model.infer_vector(wakati_words, epochs=30)
    # print(temp_vector)

    # model.build_vocab(wakati_words, update=False)
    # results = model.wv.most_similar(
    #   positive=positive_word_list, negative=negative_word_list, topn=150
    # )
    return results


# １文字や絵文字を除外した意味のある単語一覧を取得
def find_word_list(results):
    words = []
    for result in results:
        word = result[0]
        if is_emoji(word) or len(word) <= 1:
            continue

        words.append(word)
    return words


# (x, y)座標によって色変換
def find_color(x: float, y: float):
    if x < 0:
        if y < 0:
            color = LEFT_DOWN_WORD_COLOR
        else:
            color = LEFT_UP_WORD_COLOR
    else:
        if y < 0:
            color = RIGHT_DOWN_WORD_COLOR
        else:
            color = RIGHT_UP_WORD_COLOR
    return color


# 単語一覧をplotに出力
def output_relation_word_axes(axes: pyplot.axes, words, t_sne, annotate_text):
    i = 0
    for factor in t_sne:
        word = words[i]
        (x, y) = (factor[0], factor[1])
        color = find_color(x, y)
        axes.scatter(x=x, y=y, marker='.', facecolor=color, s=200, alpha=0.8)
        annotate_text.append(axes.annotate(word, (x, y), fontname='MigMix 1M', fontsize=6))
        i += 1


# Main処理
def main():
    figure = pyplot.figure()
    axes = figure.add_subplot()
    axes.set_title(FOLDER_NAME)
    annotate_text = []
    (x, y) = (0, 0)
    axes.scatter(x=x, y=y, marker='.', facecolor=MAIN_WORD_COLOR, s=1000)
    annotate_text.append(axes.annotate(SEARCH_WORD, (x, y), fontname='MigMix 1M', fontsize=8, fontweight='bold'))

    model = Doc2Vec.load(f'{FOLDER_NAME}/word.model')
    results = load_vector(model, SEARCH_WORD)

    words = find_word_list(results)
    weights = (model[word] for word in words)
    stack = numpy.vstack(tuple(weights))

    # CUI環境でshow()関数は使えないので、画像出力する
    t_sne = MulticoreTSNE(n_jobs=JOB_COUNT).fit_transform(stack)
    output_relation_word_axes(axes, words, t_sne, annotate_text)
    # ある程度文字同士が重ならないように出力
    adjust_text(annotate_text)
    pyplot.savefig(f'{FOLDER_NAME}.png', bbox_inches='tight', dpi=100)


main()
