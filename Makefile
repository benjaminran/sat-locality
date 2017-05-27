all:
	circle.py -n 10 -m 10 -k 3 -w 0.25 | tee gen.cnf | docker run --rm -i msoos/cryptominisat:v2 || true
