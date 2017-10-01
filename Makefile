all:
	circle.py -n 10 -m 10 -k 3 -w 0.25 | tee gen.cnf | docker run --rm -i msoos/cryptominisat:v2 || true

foo:
	jupyter nbconvert --to html --execute notebooks/Circle.ipynb

clean:
	- rm -r sat_locality.egg-info notebooks/experiments
