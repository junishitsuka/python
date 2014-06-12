#! /usr/bin/sh
for j in `seq 5 40`
do
python cluster.py $j >> dbindex.txt
done
