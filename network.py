#! /usr/bin/python
# coding: utf-8

import MySQLdb
import networkx as nx

def init():
    restaurants = {}
    sql = 'SELECT placeID, price FROM restaurant'
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        restaurants[r[0]] = {}
        restaurants[r[0]]['scores'] = {}
        restaurants[r[0]]['price'] = r[1]

    sql = 'SELECT distinct userID from rating'
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        sql = 'SELECT placeID from rating where userID = "%s"' % r[0]
        cursor.execute(sql)
        place = cursor.fetchall()
        for p in place:
            for plc in place:
                if (p[0] == plc[0]): continue
                if restaurants[p[0]]["scores"].has_key(plc[0]):
                    restaurants[p[0]]["scores"][plc[0]] += 1
                else:
                    restaurants[p[0]]["scores"][plc[0]] = 1

    return restaurants

def main():
    restaurants = init()

    G = nx.MultiDiGraph()
    for r in restaurants:
        G.add_node(r, price=restaurants[r]['price'])
    for r1 in restaurants:
        for r2 in restaurants[r1]["scores"]:
            if restaurants[r1]['scores'][r2] > 0:
                G.add_edge(r1, r2, weight = restaurants[r1]["scores"][r2])
    nx.write_gexf(G, 'network.gexf')

if __name__ == '__main__':
    connector = MySQLdb.connect(host='localhost', user='root', passwd='root', db='restaurant', charset='utf8', unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock')
    cursor = connector.cursor()

    main()

    cursor.close()
    connector.close()
