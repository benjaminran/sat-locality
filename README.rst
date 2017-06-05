sat-locality
============

Structured random CNF formula generators for SAT-solver explorations

Generators
----------

Circle
~~~~~~

Overview
^^^^^^^^

For variables uniformly randomly distributed around a circle, clauses are generated such that variables in the clause are within a certain "width" along the circle from a randomly chosen "center" specific to that clause. Variables are inverted with 50% probability.

Run with ::

  rm -r experiment; nohup sl -n 10000 -m 100000 >/tmp/sl.out 2>&1 && cp experiment "archive/experiment-$(date +%Y-%m-%d-%H:%M:%S)" &

Example
^^^^^^^

::

   $ circle.py -n 10 -m 10 -k 3 -w 0.25 | tee gen.cnf | docker run --rm msoos/cryptominisat:v2


Creates formula::

  c generator: circle
  c version: 0.0.1
  c k: 3
  c w: 0.25
  p cnf 10 10
  8 -3 -9 0
  4 -10 -5 -6 1 0
  -10 -4 2 5 6 0
  5 -7 -1 -4 -10 0
  8 3 0
  4 7 -10 1 -6 0
  -3 8 9 0
  -8 3 9 0
  -4 -6 -5 -10 -9 0
  1 4 5 9 6 0

With solver result::

  c Outputting solution to console
  c CryptoMiniSat version 4.5.3
  c CryptoMiniSat SHA revision 92f61087be0c768da4ac78c7b0f3f3b3f89ac508
  c CryptoMiniSat compilation env CMAKE_CXX_COMPILER = /usr/bin/c++ | CMAKE_CXX_FLAGS =  -std=c++11 -g -pthread -Wall -Wextra -Wunused -pedantic -Wsign-compare -fno-omit-frame-pointer -Wtype-limits -Wuninitialized -Wno-deprecated -Wstrict-aliasing -Wpointer-arith -Wpointer-arith -Wformat-nonliteral -Winit-self -Wparentheses -Wunreachable-code -ggdb3 -fPIC | COMPILE_DEFINES =  -DUSE_PTHREADS -DBOOST_TEST_DYN_LINK -DSTATS_NEEDED -DUSE_SQLITE3 -DUSE_ZLIB -DUSE_VALGRIND -DUSE_M4RI | STATICCOMPILE = OFF | ONLY_SIMPLE = OFF | Boost_FOUND = 1 | TBB_FOUND =  | STATS = ON | MYSQL_FOUND =  | SQLITE3_FOUND = TRUE | ZLIB_FOUND = TRUE | VALGRIND_FOUND = TRUE | ENABLE_TESTING = ON | M4RI_FOUND = TRUE | SLOW_DEBUG = OFF | PYTHON_EXECUTABLE = /usr/bin/python2.7 | PYTHON_LIBRARY = /usr/lib/x86_64-linux-gnu/libpython2.7.so | PYTHON_INCLUDE_DIRS = /usr/include/python2.7;/usr/include/x86_64-linux-gnu/python2.7 | MY_TARGETS =  | compilation date time = Feb  6 2016 21:44:55
  c compiled with gcc version 4.9.2
  c Executed with command line: ./cryptominisat4
  c Reading from standard input... Use '-h' or '--help' for help.
  c -- header says num vars:             10
  c -- header says num clauses:          10
  c -- clauses added: 10
  c -- xor clauses added: 0
  c -- vars added 10
  c Parsing time: 0.00 s
  c --> Executing strategy token: sub-impl
  c [impl sub] bin: 0 tri: 0 (stamp: 0, cache: 0) T: 0.00 T-out: N w-visit: 20
  c --> Executing strategy token: scc-vrepl
  c --> Executing OCC strategy token(s): 'occ-backw-sub-str,occ-clean-implicit,occ-bve,'
  c [clean] T: 0.0000 s
  c [simp] mem usage for occur      0 MB
  c [simp] Not linked in 0/6 (0.00 %)
  c [simp] mem usage for occur      0 MB
  c [simp] Not linked in 0/0 (0.00 %)
  c Mem for watch alloc      : 0           MB (0.01      %)
  c Mem for watch array      : 0           MB (0.01      %)
  c --> Executing OCC strategy token: occ-backw-sub-str
  c [sub] tri upI: 15 subs w bin: 0 str w bin: 0 subs w tri: 0 str w tri: 0 tried: 4 str: 0 0-depth ass: 0 T: 0.00 T-out: N T-r: 100.00%
  c [sub] rem cl: 0 tried: 60/6 (1000.0%) T: 0.00 T-out: N
  c [str] sub: 0 str: 0 tried: 18/6 (300.0)  T: 0.00 T-out: N
  c [occ-substr] sub_str_with sub: 0 str: 0 0-depth ass: 0 T: 0.00 T-out: N T-r: 100.00%
  c --> Executing OCC strategy token: occ-clean-implicit
  c --> Executing OCC strategy token: occ-bve
  c Empty resolvent elimed: 4 T: 0.00 T-out: N
  c [occ-substr] sub_str_with sub: 0 str: 0 0-depth ass: 0 T: 0.00 T-out: N T-r: 100.00%
  c [occ-bve] process impls_sub_lits  T: 0.00
  c [occ-bve] iter v-elim 6
  c [occ-substr] sub_str_with sub: 0 str: 0 0-depth ass: 0 T: 0.00 T-out: N T-r: 100.00%
  c [occ-bve] process impls_sub_lits  T: 0.00
  c [occ-bve] iter v-elim 0
  c  #try to eliminate: 6
  c  #var-elim: 6
  c  #T-o: N
  c  #T-r: 100.00%
  c  #T: 0.00
  c [occur] 0.00 is overhead
  c [occur] link-in T: 0.00 cleanup T: 0.00
  c [scc] new: 0 BP 0M T: 0.00
  c [clean] T: 0.0000 s
  c [vrep] vars 0 lits 0 rem-bin-cls 0 rem-tri-cls 0 rem-long-cls 0 BP 0M T: 0.00
  c calculated reachability. T: 0.000
  c [polar] default polars -  pos:       0 neg:       0 undec:      10 T: 0.00
  c ------- FINAL TOTAL SEARCH STATS ---------
  c UIP search time          : 0.00        (0.00      % time)
  c restarts                 : 1           (0.00      confls per restart)
  c blocked restarts         : 0           (0.00      per normal restart)
  c time                     : 0.00        
  c decisions                : 0           (0.00      % random)
  c decisions/conflicts      : 0.00        
  c conflicts                : 0           (0.00      / sec)
  c conf lits non-minim      : 0           (0.00      lit/confl)
  c conf lits final          : 0.00        
  c props/decision           : 0.00        
  c props/conflict           : 0.00        
  c 0-depth assigns          : 0           (0.00      % vars)
  c 0-depth assigns by thrds : 0           (0.00      % vars)
  c 0-depth assigns by CNF   : 0           (0.00      % vars)
  c reduceDB time            : 0.00        (0.00      % time)
  c [probe] 0-depth assigns: 0 bsame: 0 Flit: 0 Visited: 0/0(0.0%)
  c [probe] probed: 0(0.0%) hyperBin:0 transR-Irred:0 transR-Red:0
  c [probe] BP: 0.0M HP: 0.0M T: 0.00 T-out: N T-r: 0.00%
  c probing time             : 0.00        (0.00      % time)
  c [probe] 0-depth assigns: 0 bsame: 0 Flit: 0 Visited: 0/0(0.0%)
  c [probe] probed: 0(0.0%) hyperBin:0 transR-Irred:0 transR-Red:0
  c [probe] BP: 0.0M HP: 0.0M T: 0.00 T-out: N T-r: 0.00%
  c OccSimplifier time       : 0.00        (0.00      % time)
  c [occur] 0.00 is overhead
  c [occur] link-in T: 0.00 cleanup T: 0.00
  c SCC time                 : 0.00        (0.00      % time)
  c [scc] new: 0 BP 0M  T: 0.00
  c vrep replace time        : 0.00        (0.00      % time)
  c vrep tree roots          : 0           
  c vrep trees' crown        : 0           (0.00      leafs/tree)
  c distill time             : 0.00        (0.00      % time)
  c strength cache-irred time: 0.00        (0.00      % time)
  c strength cache-red time  : 0.00        (0.00      % time)
  c Conflicts in UIP         : 0           (0.00      confl/TOTAL_TIME_SEC)
  c Total time               : 0.02        
  c Mem used                 : 0           MB
  c lits having cache        : 0.00        % of decision lits
  c num elems in cache/lit   : 0.00        extralits
  s SATISFIABLE
  v 1 2 3 4 5 6 7 8 9 -10 0
