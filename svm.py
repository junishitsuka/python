#! /usr/bin/python
# coding: utf-8

from sklearn import svm

X = [[-4,-4,-1],[-2,-2,0],[1,1,2],[3,3,5]] #入力事例
y = [1,1,0,0] #クラスラベル
clf = svm.SVC(kernel='rbf') #Support Vector Classification(分類)、RBFカーネルを使用
clf.fit(X, y) #学習
result = clf.predict([2,2,4]) #予測

print result
