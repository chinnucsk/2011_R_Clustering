require(cluster)
load('baa.ratios.rda')

m <- matrix(,1,2)
for(i in 2:250){
	cobj <- clara(ratios, i, samples=6)
	output <- c(i, cobj$silinfo$avg.width)
	m<-rbind(m, output)
	print(output)
}
print(m[order(m[,2])[1:50],])
