# distutils: language=c++

import cython
from cython.cimports.libcpp.vector import vector

def primes(nb_primes: cython.uint):
    i: cython.int
    p: vector[cython.int]
    p.reserve(nb_primes)  # allocate memory for 'nb_primes' elements.

    n: cython.int = 2
    while p.size() < nb_primes:  # size() for vectors is similar to len()
        for i in p:
            if n % i == 0:
                break
        else:
            p.push_back(n)  # push_back is similar to append()
        n += 1

    # If possible, C values and C++ objects are automatically
    # converted to Python objects at need.
    return p  # so here, the vector will be copied into a Python list.
