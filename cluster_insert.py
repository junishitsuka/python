#! /usr/bin/python
# coding: utf-8

import MeCab, sys, re, MySQLdb
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

NUM_CLUSTERS = int(sys.argv[1]) # 分割するクラスタ数
LSA_DIM = 500 # 削減する次元の数 
MAX_DF = 0.8 # DF>=0.8は除外
MIN_DF = 3 # tfが5以下を除去
MAX_FEATURES = 10000 # 考慮する単語の最大数
MINIBATCH = True
JOB_NAME = 'エンジニア'
JOB_ID = 69

# 改行区切りのファイルからレコードを読み込み
def get_bio_from_txt(filename):
    return open(filename, 'r').readlines()

# textを形態素解析にかけて、名詞のリストを返す関数
def analyzer(text):
    ret = []
    tagger = MeCab.Tagger()
    # URLのhttp://(https://)を除去
    while re.search(r'(https?://[a-zA-Z0-9.-]*)', text):
        match = re.search(r'(https?://[a-zA-Z0-9.-]*)', text)
        if match:
            replace = match.group(1).split('://')
            text = text.replace(match.group(1), replace[1])
    node = tagger.parseToNode(text)
    node = node.next
    while node.next:
        if node.feature.split(',')[0] == '名詞' and node.surface != JOB_NAME and int(len(node.surface)) >= 2:
            # 名詞かつ単語のみ格納する
            ret.append(node.surface)
        node = node.next
    return ret

def insert_cluster_id(data, cluster_id):
    for d in data:
        sql = "update users set cluster_id = %d where id = %d" % (cluster_id, d[1] + 45546)
        cursor.execute(sql)
    connector.commit()

def main():
    bio = get_bio_from_txt('data/biolist.txt')

    # TfidfVectorizerでBag-of-Wordsモデルに変換
    vectorizer = TfidfVectorizer(analyzer=analyzer, max_df=MAX_DF, min_df=MIN_DF)
    vectorizer.max_features = MAX_FEATURES
    X = vectorizer.fit_transform(bio)

    # LSAで次元削減
    lsa = TruncatedSVD(LSA_DIM)
    X = lsa.fit_transform(X)
    X = Normalizer(copy=False).fit_transform(X)

    # k-means法でクラスタリング
    if MINIBATCH:
        km = MiniBatchKMeans(n_clusters=NUM_CLUSTERS, init='k-means++', batch_size=1000, n_init=10, max_no_improvement=10, verbose=False)
    else:
        km = KMeans(n_clusters=NUM_CLUSTERS, init='k-means++', n_init=1, verbose=True)
    km.fit(X)
    labels = km.labels_
    centroids = km.cluster_centers_ # centroids

    # calc_var for confirm
    target, dst  = 0, [[] for i in range(NUM_CLUSTERS)]
    for x in X:
        # セントロイドと各要素ごとのベクトル距離
        # dst[labels[target]].append(np.linalg.norm(x-centroids[labels[target]]))
        # セントロイドの計算
        dst[labels[target]].append(x)
        target += 1
    cent = []
    for d in dst:
        # DB値の分子の計算
        # print sum(d) / len(d)
        length, center = len(d), np.array([])
        if length == 0:
            center = np.append(center, [0 for i in range(LSA_DIM)])
            cent.append(center)
        else:
            for i in range(LSA_DIM):
                sum = 0
                for x in d:
                    sum += x[i]
                else:
                    center = np.append(center, sum / length)
            else:
                cent.append(center)
    # centroids by my calculation
    cent = np.array(cent)
    
    # 各レコードの各Centroidsからの距離
    transformed = km.transform(X)
    dists = np.zeros(labels.shape)
    for i in range(len(labels)):
        dists[i] = transformed[i, labels[i]]

    # クラスタの中心距離でソート
    clusters, distances, num = [], [], 1
    for i in range(NUM_CLUSTERS):
        cluster = []
        ii = np.where(labels==i)[0] # 各クラスタに格納されているデータのラベル
        dd = dists[ii] # 各クラスタに格納されているデータの距離
        di = np.vstack([dd,ii]).transpose().tolist() # ラベル + 距離
        insert_cluster_id(di, num)
        di.sort()
        for d, j in di:
            cluster.append(bio[int(j)])
        clusters.append(cluster)
        distances.append(dd)
        num += 1

    calc_index(centroids, distances)
    calc_index(cent, distances)
    return clusters

# Davies-Bouldin index を計算し出力
def calc_index(centroids, distances):
    var, ret, none_cluster = [], 0, 0
    for d in distances:
        if len(d) != 0:
            var.append(sum(d) / len(d))
        else:
            var.append(0)
    for i in range(NUM_CLUSTERS):
        tmp = 0
        if len(distances[i]) == 0: 
            none_cluster += 1
            continue
        for j in range(NUM_CLUSTERS):
            if (i == j or np.linalg.norm(centroids[i]-centroids[j]) == 0 or len(distances[j]) == 0): continue
            tar = (var[i] + var[j]) / np.linalg.norm(centroids[i]-centroids[j])
            if (tmp < tar): tmp = tar
        else:
            ret += tmp
    print ret / (len(distances) - none_cluster)

if __name__ == '__main__':
    connector = MySQLdb.connect(host='localhost', user='ishitsuka', passwd='ud0nud0n', db='ishitsuka', charset='utf8')
    cursor = connector.cursor()
    
    clusters = main()
    filename = 'data/cluster_%d/cluster_%d.txt' % (NUM_CLUSTERS, NUM_CLUSTERS)
    f = open(filename, 'w')
    for i,bio in enumerate(clusters):
        f.write('%d\n' % i)
        for bio in bio:
            f.write('%s' % (bio.replace('/n', '')))
        f.write('\n')
    f.close()

    cursor.close()
    connector.close()

