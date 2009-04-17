__doc__ = u"""
>>> global_c_and_s()
99
abcdef

>>> local_c_and_s()
98
bcdefg
"""

cdef char c = 'c'
cdef char* s = 'abcdef'

def global_c_and_s():
    pys = s
    print c
    print pys.decode('ASCII')

def local_c_and_s():
    cdef char c = 'b'
    cdef char* s = 'bcdefg'
    pys = s
    print c
    print pys.decode('ASCII')
