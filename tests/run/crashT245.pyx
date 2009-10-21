__doc__ = """
>>> f()
{'x': 1}
"""

cimport crashT245_pxd

def f():
    cdef crashT245_pxd.MyStruct s
    s.x = 1
    print s

