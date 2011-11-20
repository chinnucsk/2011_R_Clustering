#!/usr/bin/env python
from sqlite3 import *
from optparse import OptionParser

MEDOIDS = [] # An array of medoid gene names
NUM_COLS = 51

parser = OptionParser()

parser.add_option("-d", "--db", dest="dbname", help="SQLite3 database file to read from")
parser.add_option("-t", "--table", dest="tablename", help="SQLite3 table to read")
parser.add_option("-o", "--output", dest="outfile", help="SQLite3 db to write to")
(options, args) = parser.parse_args()

if \
options.dbname == None or \
options.tablename == None or \
options.outfile == None:
	exit("usage ./pam.py -d DBNAME -t TABLENAME -o OUTPUTDBNAME \n ./pam-py --help for more help")

""" Load up the SQL driver """
conn = connect(options.dbname)
curs = conn.cursor()

""" Count the number of rows in the DB """
print "Counting genes" 
curs.execute("select count(row_names) from %s" % options.tablename)

for r in curs:
	n=r[0]
print "%d genes found"%n

""" Load up the MEDOID array """

curs.execute("select * from ba_ratios where isMedoid=1")
for r in curs:
	MEDOIDS.append(r)

""" For Each MEDOID M """
for m in MEDOIDS:
	""" For Each non-medoid o """
	for i in range(0,n-len(MEDOIDS)):
		curs.execute("select * from ba_ratios where isMedoid=0 limit 1 offset %d"%i)
		for o in curs:
			print o
