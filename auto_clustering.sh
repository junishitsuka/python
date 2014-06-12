#! /usr/bin/sh
for i in `seq 1 5`
do
for j in `seq 5 40`
do
python cluster.py $j >> dbindex_$i.txt
done
done
