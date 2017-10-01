sat-locality
============

Structured random CNF formula generators for SAT-solver explorations


Set Up
------

::

  virtualenv -p python3 venv && source venv/bin/activate
  pip3 install -e .
  pip3 install jupyter pandas matplotlib
  brew install parallel  # notebook uses gnu parallel


Run Me
------

Uninteractively ::

  jupyter nbconvert --to html --execute notebooks/Circle.ipynb


Interactively ::

  jupyter notebook notebooks/Circle.ipynb

