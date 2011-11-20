init: init_pam.py baa.ratios.sqlite
	./init_pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite -k 10
swap: swap_pam.py baa.ratios.sqlite
	./swap_pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite 
dists: build_dist.py baa.ratios.sqlite
	./build_dist.py	
reset: baa.ratios.sqlite.bak
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
