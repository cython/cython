cimport crashT245_pxd

"""
>>> f()
{'x': 1}
"""

def f():
    cdef crashT245_pxd.MyStruct s
    s.x = 1
    print s

