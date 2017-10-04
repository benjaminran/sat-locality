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

  SL_A=<arity> SL_M=<clauses> SL_N=<vars> make bg


Interactively ::

  jupyter notebook notebooks/Circle.ipynb

