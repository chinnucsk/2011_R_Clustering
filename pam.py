#!/usr/bin/env python
from sqlite3 import *
from optparse import OptionParser

MEDOIDS = [] # An array of medoid gene names
NUM_COLS = 51

def row_dist(a,b):
	d_conn=connect("baa.ratios.sqlite")
	c = d_conn.cursor()
	name = (a[0]+b[0] if a[0]<b[0] else b[0]+a[0])
	print name
	query = "select * from dist where hash = \'%s\' limit 1"%name
	c.execute(query)
	for r in c:
		d=r
	print d[0], d[1]
	return d[1]


parser = OptionParser()

parser.add_option("-d", "--db", dest="dbname", help="SQLite3 database file to read from")
parser.add_option("-t", "--table", dest="tablename", help="SQLite3 table to read")
parser.add_option("-o", "--output", dest="outfile", help="SQLite3 db to write to")
parser.add_option("-k", "--k", dest="k", type="int", help="Number of partitions")
(options, args) = parser.parse_args()

if \
options.dbname == None or \
options.tablename == None or \
options.outfile == None or \
options.k == None:
	exit("usage ./pam.py -d DBNAME -t TABLENAME -o OUTPUTDBNAME -k K\n ./pam-py --help for more help")

""" Load up the SQL driver """
conn = connect(options.dbname)
curs = conn.cursor()

""" Count the number of rows in the DB """
print "Counting genes" 
curs.execute("select count(row_names) from %s" % options.tablename)

for r in curs:
	n=r[0]
print "%d genes found"%n

""" add the mediod column if it doesn't exist """
curs.execute("SELECT * from sqlite_master")
schema=""
for r in curs:
	schema=schema+str(r)
if not "isMedoid" in schema:
	curs.execute("ALTER TABLE ba_ratios ADD isMedoid integer")

print "Initializing empty isMedoid col."
""" set all rows mediod = false """
curs.execute("UPDATE ba_ratios SET isMedoid=0")
conn.commit()

""" Select k random points from the db, set them as medoids """
print "Selecting %d random medoids" % options.k
curs.execute("SELECT * FROM ba_ratios WHERE isMedoid=0 ORDER BY RANDOM() LIMIT %d" % options.k)
queries = []
for t in curs:
	MEDOIDS.append(t)
	queries.append("UPDATE ba_ratios SET isMedoid=1 WHERE row_names=\'%s\'" % t[0])
for q in queries:
	curs.execute(q)
conn.commit()

""" Associate each datum with a mediod based on distance """
""" add the mediod column if it doesn't exist """
curs.execute("SELECT * from sqlite_master")
schema=""
for r in curs:
	schema=schema+str(r)
if not "medoid" in schema:
	curs.execute("ALTER TABLE ba_ratios ADD medoid text")
#First, associate mediods with themselves
for g in MEDOIDS:
	curs.execute(("UPDATE ba_ratios SET medoid=\'%s\' WHERE row_names=\'%s\'" % (g[0], g[0])))
conn.commit()
#Get genes in batches of 10, calculate their distances from medoids
print "Computing initial clusters for each gene"
prog=-1
for i in range(0, ((n)/10)+1): # python rounds ints down
	i=i*10
	if ((100*i)/n)%5==0 and not ((100*i)/n)==prog :
		prog = (100*i)/n
		print "%d percent complete" % prog
	curs.execute("SELECT * from ba_ratios limit 10 offset %d"%i)
	queries=[]
	for r in curs:
		# Calculate distance from all k mediods,
		# Associate this gene with the closest mediod
		# Add distance to database
		winner=-1
		winner_name=""
		for m in MEDOIDS:
			d=row_dist(r,m)
			if winner == -1:
				winner = d
				winner_name=m[0]
			if winner > d:
				winner = d
				winner_name=m[0]
		queries.append(("UPDATE ba_ratios SET medoid=\'%s\' WHERE row_names=\'%s\'" % (winner_name, r[0])))
	for q in queries:
		curs.execute(q)
conn.commit()
	

""" Make a table to store distances, calculate the distances, die a little on the inside """
""" print "Making cartesian product table to store distances."
curs.execute("CREATE TABLE dist(root_gene text)")
conn.commit()
# For each row in ratios, we add a row and a column to dist
last = -1
for i in range(0,n-1):
	if ((100*i)/n)%5==0:
		if not ((100*i)/n)==last:
			print "%d percent complete."%((100*i)/n)
			last=(100*i)/n
			conn.commit()
	curs.execute("SELECT * from ba_ratios LIMIT 1 OFFSET %d"%i)
	row=curs.fetchone()
	curs.execute("ALTER TABLE dist ADD %s text" % row[0])
	curs.execute("INSERT INTO dist (root_gene) VALUES (\'%s\')" % row[0])
conn.commit() """
