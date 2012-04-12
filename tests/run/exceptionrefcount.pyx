__doc__ = u"""
>>> class SampleException(Exception): pass

>>> def assert_refcount(rc1, rc2, func):
...     # test ref-counts, but allow a bit of freedom
...     assert rc2 <= rc1 + 4, "%s, before: %d, after %d" % (
...         func.__name__, rc1, rc2)

>>> def run_test(repeat, test_func):
...     initial_refcount = get_refcount(SampleException)
...     for i in range(repeat):
...         try: raise SampleException
...         except:
...             refcount1 = get_refcount(SampleException)
...             test_func()
...             refcount2 = get_refcount(SampleException)
...
...             assert_refcount(refcount1, refcount2, test_func)
...             assert_refcount(initial_refcount, refcount2, test_func)
...         refcount3 = get_refcount(SampleException)
...         assert_refcount(refcount1, refcount3, test_func)
...         assert_refcount(initial_refcount, refcount3, test_func)

>>> run_test(50, test_no_exception_else)
>>> run_test(50, test_no_exception)
>>> run_test(50, test_exception)
>>> run_test(50, test_finally)
"""

from cpython.ref cimport PyObject

def get_refcount(obj):
    return (<PyObject*>obj).ob_refcnt

def test_no_exception():
    try:
        a = 1+1
    except:
        pass

def test_no_exception_else():
    try:
        a = 1+1
    except:
        pass
    else:
        b = 1+1

def test_exception():
    try:
        raise TypeError
    except:
        pass

def test_finally():
    try:
        a = 1+1
    finally:
        b = 1+1
