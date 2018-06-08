To run demos do::

    cd Demos
    make test

which runs ``run_primes.py``, ``run_numeric_demo.py``, ``run_spam.py``,
``integrate_timing.py``, ``callback/runcheese.py`` and ``embed/embedded``

For other demos::

    cd libraries
    python setup.py build_ext --inplace
    python -c 'import call_mymath;print(call_mymath.call_sinc(1))'

To run one of the benchmarks for 10 iterations to compare cython and python timings::

    cd benchmarks
    python setup.py build_ext --inplace
    python nqueens.py -n 10
    python -c 'import nqueens;print(nqueens.test_n_queens(10))'

To demo ``cython/bin/cython_freeze``::

    make
    ./nCr 10 5
    ./python

* Build notes

  * benchmarks/chaos.py requires cython 0.24 or newer

  * embed and freeze work for python2, require cython 0.24 or higher
    for python 3.5


