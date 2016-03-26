* To run demos do::

    cd Demos
    make test

  which runs run_primes.py, run_numeric_demo.py, run_spam.py,
  integrate_timing.py, callback/runcheese.py and embed/embedded

* For other demos::

    cd libraries
    python setup.py build_ext --inplace
    python -c 'import call_mymath;print(call_mymath.call_sinc(1))'

  To run one of the benchmarks for 10 iterations to compare cython and python::

    cd benchmarks
    python nqueens.py -n 10
    python -c 'import nqueens;print(nqueens.test_n_queens(10))'
    
* Known failures

  * benchmarks/chaos.py failing for both python2 and python3

  * embed and freeze work for python2, compile but fail for python3

