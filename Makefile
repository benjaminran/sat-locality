all:
	circle.py -n 10 -m 10 -k 3 -w 0.25 | tee gen.cnf | docker run --rm -i msoos/cryptominisat:v2 || true

bg:
	bin/gen-single.sh

interactive:
	jupyter notebook notebooks/Circle.ipynb

clean:
	- rm -r notebooks/data

spotless: clean
	- rm -r experiments/* sat_locality.egg-info
