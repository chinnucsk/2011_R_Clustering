clusters: pam.py reset
	./pam.py --d baa.ratios.sqlite  -t ba_ratios -o pyclusters.sqlite -k 50
reset: baa.ratios.sqlite baa.ratios.sqlite.bak
	cp baa.ratios.sqlite.bak baa.ratios.sqlite
