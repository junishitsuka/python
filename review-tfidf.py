# coding: UTF-8
import MeCab,math,json,sys,re

NUM_CLUSTERS = 4

# get article data from file
def get_reviews():
    reviews = ['', '', '', '']
    f = open("rakutenscrapy/rakutenscrapy/spiders/review.jl")
    for line in f:
        tmp = json.loads(line)
        if tmp['genre'] == u'イオン導入器': reviews[0] += tmp['review'].encode('utf-8')
        if tmp['genre'] == u'超音波美顔器': reviews[1] += tmp['review'].encode('utf-8')
        if tmp['genre'] == u'レーザー美顔器': reviews[2] += tmp['review'].encode('utf-8')
        if tmp['genre'] == u'その他': reviews[3] += tmp['review'].encode('utf-8')
    return reviews

def mecab_parse(reviews):
    wordList = []
    tagger = MeCab.Tagger()
    for i in reviews:
        node = tagger.parseToNode(i)
        word_in_cluster = []
        while node:
            if node.feature.split(',')[0] == '名詞' and int(len(node.surface)) >= 2:
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
    f = open('review-tfidf.txt', 'w')
    for i in range(len(tf_idf)):
        f.write(str(i) + '\n')
        output = 0
        for k,v in sorted(tf_idf[i].items(), key=lambda x: x[1], reverse=True):
            if (output != 20):
                f.write(k + ',')
                output += 1
            else:
                f.write('\n')
                break
    f.close()

def main():
    reviews = get_reviews() 
    wordCount = mecab_parse(reviews)
    idf = calc_idf(wordCount)
    tf = calc_tf(wordCount)
    td_idf = calc_tf_idf(tf,idf)
    output(td_idf)

main()
