"""
>>> f()
'hello'
"""

from libc.stdio cimport sprintf

def f():
    cdef char buf[10]
    sprintf(buf, b'hello')
    return str((<object>buf).decode('ASCII'))
