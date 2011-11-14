clusters: build_dist.py pam.py reset
	./build_dist.py
	./pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite -k 10

reset: baa.ratios.sqlite baa.ratios.sqlite.bak
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
