require(RSQLite);
require(cluster);


#Functions:
#sql.pam <- function(x, k, table, connect){
#	#get the size of the database.
#	print(dbGetQuery(connect, paste("SELECT count(\"row_names\") from ",table,sep=""))[1])
#	#Pick k random data points, make them mediods, save them back to the db
#	
#}

#Main operations:
## Load the data from SQL
drin <- dbDriver("SQLite")
fin <- "baa.ratios.sqlite"
conin <- dbConnect(drin, dbname = fin)

ratios <- dbReadTable(conin, "ba_ratios")

## Make a driver for SQLite OUTPUT
mm <- dbDriver("SQLite")

## Make a file
fileout <- "clusters.sqlite"

## Connect to the DB
con <- dbConnect(mm, dbname = fileout)


#### This part below can be repeated as many times as cluster sets wanted

## do the clustering
#k.ratios <- pam(ratios[0:999,], 15, cluster.only=TRUE)
k.ratios <- sql.pam(ratios, 50, "ba_ratios", conin)


## Write the ratios to the DB
#dbWriteTable(con, "k15", data.frame(k.ratios))

