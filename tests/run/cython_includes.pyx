
from libc.stdio cimport sprintf
from cpython cimport PyType_Check
from cpython cimport PyType_Check as PyType_Check2
from cpython.type cimport PyType_Check as PyType_Check3

def libc_cimports():
    """
    >>> libc_cimports()
    hello
    """
    cdef char buf[10]
    sprintf(buf, "%s", b'hello')
    print (<object>buf).decode('ASCII')

def cpython_cimports():
    """
    >>> cpython_cimports()
    True
    False
    True
    False
    True
    False
    """
    print PyType_Check(list)
    print PyType_Check([])
    print PyType_Check2(list)
    print PyType_Check2([])
    print PyType_Check3(list)
    print PyType_Check3([])

