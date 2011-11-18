clusters: pam.py baa.ratios.sqlite
	./pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite -k 10
dists: build_dist.py baa.ratios.sqlite
	./build_dist.py	
reset: baa.ratios.sqlite.bak
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
