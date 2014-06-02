#! /usr/bin/python
# coding: utf-8

import MeCab, math, sys, re

NUM_CLUSTERS = 5
GET_CLUSTER_NUM = 0 # 0 <= x <= 4

def get_cluster_from_txt():
    cluster = NUM_CLUSTERS * ['']
    target = 0

    f = open('cluster_%d.txt' % NUM_CLUSTERS, 'r')
    data = f.read()
    data = data.split('\n')
    for d in data:
        d = d.replace('\n\r', '')
        if (d in ['0', '1', '2', '3', '4']):
            target = int(d)
            continue
        cluster[target] = cluster[target] + d
    f.close()
    return cluster

def mecab_parse(articles):
    wordList = []
    tagger = MeCab.Tagger()
    for i in articles:
        node = tagger.parseToNode(i)
        word_in_cluster = []
        while node:
            if node.feature.split(',')[0] == '名詞':
                word_in_cluster.append(node.surface)
            node = node.next
        else:
            wordList.append(word_in_cluster)
    wordCount = [0] * int(len(wordList))
    for i in range(len(wordList)):
        wordCount[i] = {}
        for word in wordList[i]:
            wordCount[i].setdefault(word,0)
            wordCount[i][word]+=1
    print wordCount
    return wordCount

def calc_idf(wordCount):
    docNum = int(len(wordCount))
    wordNum = {}
    for i in range(docNum):
        for word in wordCount[i]:
            wordNum.setdefault(word,0)
            wordNum[word]+=1
    for k,v in wordNum.items():
        wordNum[k] = math.log((1.0*docNum/v), 2)
    return wordNum

# target the first article data (j = 0)
def calc_tf(wordCount):
    totalCount = 0
    wordNum = {}
    for i in wordCount[GET_CLUSTER_NUM].values():
        totalCount += i
    for k,v in wordCount[GET_CLUSTER_NUM].items():
        wordNum[k] = 1.0 * v / totalCount
    return wordNum

def calc_tf_idf(tf,idf):
    td_idf = {}
    for word in tf.keys():
        td_idf[word] = tf[word] * idf[word]
    return td_idf

def output(td_idf):
    f = open('tfidf_cluster%d' % GET_CLUSTER_NUM, 'w')
    for k,v in sorted(td_idf.items(), key=lambda x: x[1], reverse=True):
        # if (k.count('名詞') >= 1):
        # print k + ': ' + str(v)
        f.write(k + ': ' + str(v))
        f.write('\n')
    f.close()

def main():
    articles = get_cluster_from_txt() 
    wordCount = mecab_parse(articles)
    idf = calc_idf(wordCount)
    tf = calc_tf(wordCount)
    td_idf = calc_tf_idf(tf,idf)
    # print td_idf
    output(td_idf)

main()
