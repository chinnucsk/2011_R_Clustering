#!/usr/bin/env python
from sqlite3 import *
from math import sqrt
def euclid(x,y):
	run=0;
	for i in range(1,51):
		run=run+(x[i]-y[i])**2
	return run#sqrt(run)

conn = connect("baa.ratios.sqlite")
curs = conn.cursor()
curs2 = conn.cursor()
curs3 = conn.cursor()

print "Counting genes"
curs.execute("select count(row_names) from %s" % "ba_ratios")

for r in curs:
  n=r[0]
print "%d genes found"%n

curs.execute("CREATE TABLE dist (hash text, d real)")
conn.commit()
for i in range(0, n):
	curs.execute("select * from ba_ratios limit 1 offset %s"%i)
	for r in curs:
		for j in range(0, n):
			offset2 = j
			curs2.execute("select * from ba_ratios limit 1 offset %s"%offset2)
			for s in curs2:
				ind = (r[0]+s[0]) if r[0] < s[0] else s[0]+r[0]
				dist = euclid(r,s)
				print ind, dist
				curs3.execute(("insert or replace into dist values (\'%s\', %s)"%(ind, dist)))
	conn.commit()

