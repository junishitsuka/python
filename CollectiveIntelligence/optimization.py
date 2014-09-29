#! /usr/bin/python
# coding: utf-8

import time, random, math

people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]

# NewYork Laguardia
destination='LGA'

flights = {}

for line in file('PCI_Code/chapter5/schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    flights[(origin, dest)].append((depart, arrive, int(price)))

# ある時刻tが一日の中で何分目かを返す関数
def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

# 結果を出力する関数(r: 行きの飛行機の番号, 帰り野飛行機の番号)
def printschedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][int(r[2 * d])]
        ret = flights[(destination, origin)][int(r[2 * d + 1])]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%d' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2 * d])]
        returnf = flights[(destination, origin)][int(sol[2 * d + 1])]

        # 飛行機の運賃
        totalprice += (outbound[2] + returnf[2])

        # 最も遅い到着時刻と最も早い出発時刻を記録
        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])

    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2 * d])]
        returnf = flights[(destination, origin)][int(sol[2 * d + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    # タクシーの追加料金 $50
    if latestarrival < earliestdep: totalprice += 50

    return totalprice + totalwait

# domain: 解の最大値・最小値, costf: コスト関数
def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(10000):
        r = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

        cost = costf(r)

        if cost < best:
            best = cost
            bestr = r
    return bestr

def hillclimb(domain, costf):
    sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while 1:
        neighbors = []
        for j in range(len(domain)):
            if sol[j] > domain[j][0]: # > 0
                neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j+1:])
            if sol[j] < domain[j][1]: # < 8
                neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j+1:])

        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]
        
        if best == current: break

    return sol

