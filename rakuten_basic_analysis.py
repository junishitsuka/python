# /usr/bin/python
# coding: utf-8

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_jsonline(filename):
    key = ['review_count', 'description', 'title', 'price', 'maker', 'link', 'genre', 'review']
    csv = ''
    f = open(filename)
    for k in key:
        csv += k + ','
    csv = csv[0:-1] + '\n'
    for line in f:
        js = json.loads(line)
        for k in key:
            if js.has_key(k):
                csv += js.get(k) + ','
            else:
                csv += '0,'
        csv = csv[0:-1] + '\n'
    f.close()
    return csv

def main():
    data = pd.read_csv('item.csv')
    
    ion = data[data['genre'] == 'イオン導入器']
    wave = data[data['genre'] == '超音波美顔器']
    laser = data[data['genre'] == 'レーザー美顔器']
    other = data[data['genre'] == 'その他']

    print np.corrcoef(ion['price'], ion['review'])
    print np.corrcoef(wave['price'], wave['review'])
    print np.corrcoef(laser['price'], laser['review'])
    print np.corrcoef(other['price'], other['review'])

    # データの読み込み
    # csv = read_jsonline('rakutenscrapy/rakutenscrapy/spiders/item.jl')
    # f = open('item.csv', 'w')
    # f.write(csv.encode('utf-8'))
    # f.close()

    # ヒストグラム
    # plt.hist(data["price"])
    # plt.xlabel('price')
    # plt.xlabel('frq')
    # plt.show()
   
    # ピボットテーブル
    # print pd.pivot_table(data, index="genre", aggfunc=np.mean)
    
    # 箱ひげ図
    # box = [ion['price'], wave['price'], laser['price'], other['price']]
    # plt.boxplot(box)
    # plt.xlabel("genre")
    # plt.ylabel("price")
    # plt.ylim(0, 50000)
    # ax = plt.gca()
    # plt.setp(ax, xticklabels=['ion', 'wave', 'laser', 'other'])
    # plt.show()

if __name__ == '__main__':
    main()
