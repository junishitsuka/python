#! /usr/bin/python
# coding: utf-8

import MeCab, math, sys, re

NUM_CLUSTERS = int(sys.argv[1])
JOB_ID = 69
JOB_NAME = 'エンジニア'

def get_cluster_from_txt():
    cluster = NUM_CLUSTERS * ['']
    target = 0

    f = open('data/cluster_%d/cluster_%d.txt' % (NUM_CLUSTERS, NUM_CLUSTERS), 'r')
    data = f.read()
    data = data.split('\n')
    for d in data:
        d = d.replace('\n\r', '')
        if (d in [str(i) for i in range(NUM_CLUSTERS)]):
            target = int(d)
            continue
        cluster[target] = cluster[target] + d
    f.close()
    return cluster

def mecab_parse(articles):
    wordList = []
    tagger = MeCab.Tagger()
    for i in articles:
        # URLのhttp://(https://)を除去
        while re.search(r'(https?://[a-zA-Z0-9.-]*)', i):
            match = re.search(r'(https?://[a-zA-Z0-9.-]*)', i)
            if match:
                replace = match.group(1).split('://')
                i = i.replace(match.group(1), replace[1])
        node = tagger.parseToNode(i)
        word_in_cluster = []
        while node:
            if node.feature.split(',')[0] == '名詞' and node.surface != JOB_NAME and int(len(node.surface)) >= 2:
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
    wordNum = []
    for i in range(len(wordCount)):
        totalCount = 0
        Num = {}
        for j in wordCount[i].values():
            totalCount += j
        for k,v in wordCount[i].items():
            Num[k] = 1.0 * v / totalCount
        wordNum.append(Num)
    return wordNum

def calc_tf_idf(tf,idf):
    tf_idfs = []
    for i in range(len(tf)):
        tf_idf = {}
        for word in tf[i].keys():
            tf_idf[word] = tf[i][word] * idf[word]
        tf_idfs.append(tf_idf)
    return tf_idfs

def output(tf_idf):
    f = open('data/cluster_%d/tfidf_%d.txt' % (NUM_CLUSTERS, NUM_CLUSTERS), 'w')
    for i in range(len(tf_idf)):
        f.write(str(i) + '\n')
        output = 0
        for k,v in sorted(tf_idf[i].items(), key=lambda x: x[1], reverse=True):
            if (output != 20):
                f.write(k + ': ' + str(v) + '\n')
                output += 1
            else:
                break
    f.close()

def main():
    articles = get_cluster_from_txt() 
    wordCount = mecab_parse(articles)
    idf = calc_idf(wordCount)
    tf = calc_tf(wordCount)
    td_idf = calc_tf_idf(tf,idf)
    output(td_idf)

main()
