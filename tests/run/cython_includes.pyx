
from libc.stdio cimport sprintf
from python cimport PyType_Check
from cpython.type cimport PyType_Check as PyType_Check2

def libc_imports():
    """
    >>> libc_imports()
    hello
    """
    cdef char buf[10]
    sprintf(buf, b'hello')
    print (<object>buf).decode('ASCII')

def python_imports():
    """
    >>> python_imports()
    True
    False
    True
    False
    """
    print PyType_Check(list)
    print PyType_Check([])
    print PyType_Check2(list)
    print PyType_Check2([])
    
