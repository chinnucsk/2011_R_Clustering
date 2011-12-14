#!/usr/bin/env python
from sqlite3 import *
from math import sqrt
def euclid(x,y):
	run=0;
	for i in range(1,51):
		run=run+((x[i]-y[i])**2)
	return run#sqrt(run)

conn = connect("baa.ratios.sqlite")
curs = conn.cursor()
curs2 = conn.cursor()

print "Counting genes"
curs.execute("select count(row_names) from %s" % "ba_ratios")

for r in curs:
  n=r[0]
print "%d genes found"%n

for i in range(0, n):
	curs.execute("select * from ba_ratios limit 1 offset %s"%i)
	for r in curs:
		cout = connect("dist_temp/%s.sqlite"%r[0])
		curout = cout.cursor()
		curout.execute("create table dist (gene text, d real, id integer primary key autoincrement)") 
		for j in range(i, n):
			offset2 = j
			curs2.execute("select * from ba_ratios limit 1 offset %s"%offset2)
			for s in curs2:
				ind = s[0]
				dist = euclid(r,s)
				#print r[0], ind, dist
				curout.execute(("insert or replace into dist (gene, d) values (\'%s\', %s)"%(ind, dist)))
		print r[0]
		cout.commit()

