#! /usr/bin/sh
for j in 2 5 10 20 30 40 50 60 70 80 90 100 500 1000
do
python cluster.py $j >> dbindex.txt
done
