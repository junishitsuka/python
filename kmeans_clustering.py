#! /usr/bin/python
# coding: utf-8

import random, math
import matplotlib.pyplot as plt
import numpy as np

# データの生成
a=np.random.random((100,2))+2
b=np.random.random((100,2))+5
c=np.random.random((100,2))+8
X=np.concatenate((a,b,c))

CLUSTER_NUM = 3 # クラスター数

def init(cluster):
    for i in range(len(cluster)):
        cluster[i] = random.randint(0, CLUSTER_NUM - 1)
    return cluster

def calc_centroid(cluster, elem):
    centroids = []
    for i in range(CLUSTER_NUM):
        tmp = [0] * len(elem[0])
        for j in range(len(cluster)):
            for k in range(len(elem[0])):
                if i == cluster[j]: tmp[k] += elem[j][k]
        if cluster.count(i) != 0:
            centroids.append([1.0 * x / cluster.count(i) for x in tmp])
        else:
            centroids.append(tmp)
    return centroids

def update_cluster(centroids, elem):
    cluster = []
    for i in range(len(elem)):
        min, min_index = -1, 0
        for j in range(CLUSTER_NUM):
            tmp = 0
            for k in range(len(elem[i])):
                tmp += math.pow((centroids[j][k] - elem[i][k]), 2)
            if min == -1: # minに値が一度も代入されていないとき
                min, min_index = tmp, j
            elif min > tmp:
                min, min_index = tmp, j
        cluster.append(min_index)
    return cluster

def main():
    cluster = [0] * int(len(X))
    cluster = init(cluster) 
    tmp_cluster = []

    while cluster != tmp_cluster:
        if tmp_cluster != []:
            cluster = tmp_cluster
        centroids = calc_centroid(cluster, X)
        tmp_cluster = update_cluster(centroids, X)
    label = cluster # ラベルを出力

    # plt.figsize(10, 5)
    plt.scatter(*zip(*X), c=label, vmin=0, vmax=2, s=12)
    plt.show()

if __name__ == '__main__':
    main()
