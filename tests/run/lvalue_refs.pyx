# tag: cpp

from libcpp.vector cimport vector

__doc__ = u"""
   >>> test_lvalue_ref_assignment()
"""

ctypedef double*  dp
ctypedef double** dpp

cdef void foo(vector[dpp] &bar, vector[vector[dp]] &baz) nogil:
    bar[0] = &baz[0][0]

def test_lvalue_ref_assignment():
    cdef vector[dpp]        bar
    cdef vector[vector[dp]] baz
    cdef vector[double]     data = [0.0]
    cdef dp                 bongle = &data[0]

    bar.resize(1)
    bar[0] = NULL
    baz.resize(1)
    baz[0].resize(1)
    baz[0][0] = bongle

    foo(bar, baz)

    assert bar[0] == &baz[0][0]
    assert bar[0][0] == bongle
