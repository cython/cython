__doc__ = u"""
>>> import sys
>>> sys.getrefcount(Foo.__pyx_vtable__)
2
>>> sys.getrefcount(__pyx_capi__['spam'])
2
"""

cdef public api class Foo [type FooType, object FooObject]:
    cdef void bar(self):
        pass

cdef api void spam():
    pass
