# mode: run
# tag: portability

# test some C-API functions that Cython replaces for portability reasons

from cpython.number cimport PyNumber_Index, PyIndex_Check

def number_index(x):
    """
    >>> number_index(1)
    1
    >>> try: number_index(1.1)
    ... except TypeError: pass
    ... else: print("FAILED")
    >>> try: number_index(1j)
    ... except TypeError: pass
    ... else: print("FAILED")
    >>> try: number_index('abc')
    ... except TypeError: pass
    ... else: print("FAILED")
    """
    # was not available in Py2.4
    return PyNumber_Index(x)

def index_check(x):
    """
    >>> index_check(1)
    True
    >>> index_check(1.1)
    False
    >>> index_check(1j)
    False
    >>> index_check('abc')
    False
    """
    # was not available in Py2.4
    return PyIndex_Check(x)
