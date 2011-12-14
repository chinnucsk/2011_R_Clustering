#!/usr/bin/env python
from sqlite3 import *
from optparse import OptionParser
import sys

def row_dist(a,b):
	first, second = ((a[0], b[0]) if a[0]<b[0] else (b[0], a[0]))
	d_conn=connect("dist2/%s.sqlite"%first)
	c = d_conn.cursor()
	query = "select * from dist where gene = \'%s\' limit 1"%second
	c.execute(query)
	for r in c:
		d=r
		return d[1]

def mswap(m,o):
	global MEDOIDS
	MEDOIDS[MEDOIDS.index(m)]=o # swaps in place for continuity
	fconn=connect(options.dbname)
	fcurs=fconn.cursor()
	fcurs.execute("update ba_ratios set isMedoid=0 where row_names=\'%s\'"%m[0])
	fcurs.execute("update ba_ratios set isMedoid=1, medoid=\'%s\' where row_names=\'%s\'"%(o[0],o[0]))
	fcurs.execute("update ba_ratios set medoid=' ' where isMedoid=0")
	fconn.commit()
	#assign_to_medoids() # Don't do this.

def assign_to_medoids():
	global MEDOIDS
	print "Reassigning data to Medoids"
	# Associate Medoids with themselves
	fconn=connect(options.dbname)
	fcurs=fconn.cursor()
	for g in MEDOIDS:
		fcurs.execute("update ba_ratios set medoid=\'%s\' where row_names=\'%s\'"%(g[0],g[0]))
	fconn.commit()
	fcurs2=fconn.cursor()
	prog = -1
	for i in range(0, (n/100)+1):
		i=i*100
		if ((100*i)/n)%1==0 and not ((100*i)/n)==prog :
			prog = (100*i)/n
			sys.stdout.write("\r%d percent complete" % prog)
			sys.stdout.flush()
		fcurs.execute("select * from ba_ratios limit 100 offset %d"%i)
		for r in fcurs:
			d=-1
			for m in MEDOIDS:
				if d == -1:
					d=row_dist(r,m)
					newdist=d
					winner=m[0]
				else:
					newdist=row_dist(r,m)
				if d > newdist:
					d=newdist
					winner=m[0]
			fcurs2.execute("update ba_ratios set medoid=\'%s\' where row_names=\'%s\'"%(winner, r[0]))
		fconn.commit()
	print "\nDone"

def get_total_cost():
	global MEDOIDS
	print "computing total cost"
	curr_cost=0.0
	for m in MEDOIDS:
		curr_cost += get_medoid_cost(m)
	return curr_cost

def get_medoid_cost(m):
	cost=0
	fconn=connect(options.dbname)
	fcurs=fconn.cursor()
	fcurs.execute("select count(row_names) from ba_ratios where isMedoid=0 and medoid=\'%s\'"%m[0])
	fn=fcurs.fetchone()[0]
	for i in range(0,fn):
		fcurs.execute("select * from ba_ratios where isMedoid=0 and medoid=\'%s\' limit 1 offset %d"%(m[0], i))
		cost+= row_dist(m, fcurs.fetchone())
	sys.stdout.write("\rmedoid "+ m[0]+ " cost "+ str(cost))
	sys.stdout.flush()
	return cost

msaved=[]
csaved=0.0
def save_config(medoids, cost):
	global csaved
	global msaved
	msaved=medoids
	csaved=cost

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
	options.k = len(MEDOIDS)

""" Save the current total cost """
curr_cost = get_total_cost()
print "Initial cost: %d"%curr_cost
save_config(MEDOIDS, curr_cost)
print "csaved ", csaved

""" For Each MEDOID m """
changed=True
broke=False
while changed:
	print "Swapping on the new set of medoids"
	changed=False
	for m in MEDOIDS:
		mc=m
		""" For Each non-medoid o """ 
		for i in range(0,n-len(MEDOIDS)):
			curs.execute("select * from ba_ratios where isMedoid=0 limit 1 offset %d"%i)
			for o in curs:
				""" Swap o with m """
				print "Swapping med ", mc[0], " with non-med ", o[0]
				mswap(mc,o)
				assign_to_medoids()
				curr_cost=get_total_cost()
				print "\nCost is ", curr_cost
				if curr_cost < csaved:
					save_config(MEDOIDS, curr_cost)
					mc=o
					changed=True
					print "Found an \033[1;32mimprovement\033[1;m from the old medoid."
				else:
					print "\033[1;32mIncumbant\033[1;m cost ", csaved," lower than new cost ", curr_cost
					mswap(o,mc)
					save_config(MEDOIDS, csaved)
print "No more improvements could be found. Re assigning to nearest medoids now"
assign_to_medoids()
print "Clustered!"
