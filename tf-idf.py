# coding: UTF-8
import MeCab,math

# get article data from file
def get_articles():
    data = open("article.txt", "r").read()
    articles = data.split(',')
    articles.pop()
    return articles

# morphological analysis by mecab and count words
def mecab_parse(articles):
    result = []
    tagger = MeCab.Tagger()
    for i in articles:
        result.append(tagger.parse(i))
    wordCount = [0] * int(len(result))
    for i in range(len(result)):
        wordCount[i] = {}
        wordList = result[i].split()[:-1:2]
        for word in wordList:
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
    totalCount = 0
    wordNum = {}
    for i in wordCount[0].values():
        totalCount += i
    for k,v in wordCount[0].items():
        wordNum[k] = 1.0 * v / totalCount
    return wordNum

def calc_tf_idf(tf,idf):
    td_idf = {}
    for word in tf.keys():
        td_idf[word] = tf[word] * idf[word]
    return td_idf

def output(td_idf):
    for k,v in sorted(td_idf.items(), key=lambda x: x[1]):
        print k + ': ' + str(v)

def main():
    articles = get_articles() 
    wordCount = mecab_parse(articles)
    idf = calc_idf(wordCount)
    tf = calc_tf(wordCount)
    td_idf = calc_tf_idf(tf,idf)
    print td_idf
    output(td_idf) 

main()
