trans.data <- load("baa.anno.trans.rda")
list.data <- load("baa.anno.list.rda")
clusters.data <- read.table("k173-2.txt", header=T, sep=",")
setlength <- 5865
pvalnum <- 0.05/173

#get to the right cluster, label
current.label <- ""
current.cluster <- 0
i <- 1
#print(clusters.data[1,])
for(i in 1:setlength){
#while(i != NA){
	if(clusters.data[i,2] == current.label){
		NEXT
	}
	print(c("Current data cluster: ",clusters.data[i,1]))
	current.label <- clusters.data[i,2]
	current.cluster <- clusters.data[i,1]
	#counting
	label.total <- 0
	cluster.label <- 0
	cluster.length <- 0
	for(j in 1:setlength){
		#print(j)
		#print("j")
		#print("why is this taking so long?")
		#print("current cluster")
		#print(current.cluster)
		#print(" = ")
		#print(clusters.data[j,1])
		if(clusters.data[j,1] == current.cluster){
			cluster.length <- cluster.length+1
			if(clusters.data[j,2] == current.label){
				cluster.label<- cluster.label+1
			}
		}
		else{
			if(clusters.data[j,2] == current.label){
				label.total <-label.total+1
			}
		}
	}
	#print("done count")
	#populate matrix, run test
	contingency.table <- matrix(c(cluster.label, (cluster.length-cluster.label), label.total, (setlength - label.total)),2)
	test.run <- fisher.test(contingency.table)
	if(test.run$p.value < pvalnum){
		print(clusters.data[i:i+cluster.label,])
	}
	#label things
	#tmp2 <- get.label.counts( rownames( ratios)[arr1], anno.list )
	#anno.trans$go.trans[names(tmp2)]
}
