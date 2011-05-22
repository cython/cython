__doc__ = u"""
>>> import sys
>>> sys.getrefcount(Foo.__pyx_vtable__)
2
>>> sys.getrefcount(__pyx_capi__['bar'])
2
>>> sys.getrefcount(__pyx_capi__['spam'])
2
>>> sys.getrefcount(__pyx_capi__['ten'])
2
>>> sys.getrefcount(__pyx_capi__['pi'])
2
>>> sys.getrefcount(__pyx_capi__['obj'])
2
>>> sys.getrefcount(__pyx_capi__['dct'])
2
>>> sys.getrefcount(__pyx_capi__['tpl'])
2
>>> sys.getrefcount(__pyx_capi__['one'])
2
>>> sys.getrefcount(__pyx_capi__['two'])
Traceback (most recent call last):
  ...
KeyError: 'two'
"""

cdef public api class Foo [type FooType, object FooObject]:
    cdef void bar(self):
        pass

cdef public api void bar():
    pass
cdef api void spam():
    pass

cdef api int    ten = 10
cdef api double pi = 3.14
cdef api object obj = object()
cdef api dict   dct = {}

cdef public api tuple tpl = ()
cdef public api float one = 1
cdef public     float two = 2

