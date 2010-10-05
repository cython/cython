from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr

from libcpp.vector cimport vector

def simple_test(double x):
    """
    >>> simple_test(55)
    3
    """
    try:
        v = new vector[double]()
        v.push_back(1.0)
        v.push_back(x)
        from math import pi
        v.push_back(pi)
        return v.size()
    finally:
        del v

def list_test(L):
    """
    >>> list_test([1,2,4,8])
    (4, 4)
    >>> list_test([])
    (0, 0)
    >>> list_test([-1] * 1000)
    (1000, 1000)
    """
    try:
        v = new vector[int]()
        for a in L:
            v.push_back(a)
        return len(L), v.size()
    finally:
        del v

def index_test(L):
    """
    >>> index_test([1,2,4,8])
    (1.0, 8.0)
    >>> index_test([1.25])
    (1.25, 1.25)
    """
    try:
        v = new vector[double]()
        for a in L:
            v.push_back(a)
        return v[0][0], v[0][len(L)-1]
    finally:
        del v


def index_set_test(L):
    """
    >>> index_set_test([1,2,4,8])
    (-1.0, -8.0)
    >>> index_set_test([1.25])
    (-1.25, -1.25)
    """
    try:
        v = new vector[double]()
        for a in L:
            v.push_back(a)
        for i in range(v.size()):
            d(v)[i] = -d(v)[i]
        return d(v)[0], d(v)[v.size()-1]
    finally:
        del v

def iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    try:
        v = new vector[int]()
        for a in L:
            v.push_back(a)
        it = v.begin()
        while it != v.end():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v

def reverse_iteration_test(L):
    """
    >>> reverse_iteration_test([1,2,4,8])
    8
    4
    2
    1
    """
    try:
        v = new vector[int]()
        for a in L:
            v.push_back(a)
        it = v.rbegin()
        while it != v.rend():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v
