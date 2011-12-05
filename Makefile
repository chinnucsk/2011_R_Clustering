run: 
	make init
	make swap
init: init_pam.py baa.ratios.sqlite
	./init_pam.py --d baa.ratios.sqlite  -t ba_ratios -k 130
	cp baa.ratios.sqlite baa.ratios.sqlite.bak
swap: swap_pam.py baa.ratios.sqlite
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
	./swap_pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite 
dists: build_dist.py baa.ratios.sqlite
	./build_dist.py	
reset: baa.ratios.sqlite.bak
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
