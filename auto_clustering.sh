#! /usr/bin/sh
for i in `seq 1 10`
do
for j in 5 10 20 30 40 50 60 70 80 90 100 500 1000
do
python cluster.py $j >> dbindex_$i.txt
done
done
