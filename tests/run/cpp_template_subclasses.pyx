# mode: run
# tag: cpp, werror

from cython.operator import dereference as deref
from libcpp.pair cimport pair
from libcpp.vector cimport vector

cdef extern from "cpp_template_subclasses_helper.h":
    cdef cppclass Base:
        char* name()

    cdef cppclass A[A1](Base):
        A1 funcA(A1)

    cdef cppclass B[B1, B2](A[B2]):
        pair[B1, B2] funcB(B1, B2)

    cdef cppclass C[C1](B[long, C1]):
        C1 funcC(C1)

    cdef cppclass D[D1](C[pair[D1, D1]]):
        pass

    cdef cppclass E(D[double]):
        pass

def testA(x):
    """
    >>> testA(10)
    10.0
    """
    cdef Base *base
    cdef A[double] *a = NULL
    try:
        a = new A[double]()
        base = a
        assert base.name() == b"A", base.name()
        return a.funcA(x)
    finally:
        del a

def testB(x, y):
    """
    >>> testB(1, 2)
    >>> testB(1, 1.5)
    """
    cdef Base *base
    cdef A[double] *a
    cdef B[long, double] *b = NULL
    try:
        base = a = b = new B[long, double]()
        assert base.name() == b"B", base.name()
        assert a.funcA(y) == y
        assert <object>b.funcB(x, y) == (x, y)
    finally:
        del b

def testC(x, y):
    """
    >>> testC(37, [1, 37])
    >>> testC(25, [1, 5, 25])
    >>> testC(105, [1, 3, 5, 7, 15, 21, 35, 105])
    """
    cdef Base *base
    cdef A[vector[long]] *a
    cdef B[long, vector[long]] *b
    cdef C[vector[long]] *c = NULL
    try:
        base = a = b = c = new C[vector[long]]()
        assert base.name() == b"C", base.name()
        assert <object>a.funcA(y) == y
        assert <object>b.funcB(x, y) == (x, y)
        assert <object>c.funcC(y) == y
    finally:
        del c

def testD(x, y):
    """
    >>> testD(1, 1.0)
    >>> testD(2, 0.5)
    >>> testD(4, 0.25)
    """
    cdef Base *base
    cdef A[pair[double, double]] *a
    cdef B[long, pair[double, double]] *b
    cdef C[pair[double, double]] *c
    cdef D[double] *d = NULL
    try:
        base = a = b = c = d = new D[double]()
        assert base.name() == b"D", base.name()
        assert <object>a.funcA((y, y)) == (y, y)
        assert <object>b.funcB(x, (y, y + 1)) == (x, (y, y + 1))
        assert <object>c.funcC((y, y)) == (y, y)
    finally:
        del d

def testE(x, y):
    """
    >>> testD(1, 1.0)
    >>> testD(2, 0.5)
    >>> testD(4, 0.25)
    """
    cdef Base *base
    cdef A[pair[double, double]] *a
    cdef B[long, pair[double, double]] *b
    cdef C[pair[double, double]] *c
    cdef D[double] *d
    cdef E *e = NULL
    try:
        base = a = b = c = d = e = new E()
        assert base.name() == b"E", base.name()
        assert <object>a.funcA((y, y)) == (y, y)
        assert <object>b.funcB(x, (y, y + 1)) == (x, (y, y + 1))
        assert <object>c.funcC((y, y)) == (y, y)
    finally:
        del e


cdef public pair[int, double] public_return_pair(a, b) except *:
  return pair[int, double](a, b)

def test_GH1599(a, b):
  """
  >>> test_GH1599(1, 2)
  (1, 2.0)
  """
  return public_return_pair(a, b)


# Related to GH Issue #1852.

cdef cppclass Callback[T]:#(UntypedCallback):
    pass

cdef cppclass MyClass[O]:
    void Invoke(Callback[O]*)

cdef cppclass MySubclass[T](MyClass[T]):
    void Invoke(Callback[T]* callback):
      pass


cdef cppclass Getter[T]:
    T get(bint fire) except *:
        if fire:
            raise RuntimeError
        else:
           raise NotImplementedError

cdef cppclass GetInt(Getter[int]):
    int get(bint fire) except *:
        if fire:
            raise RuntimeError
        else:
            return 389

def test_subclass_exception_values(bint fire):
    """
    >>> test_subclass_exception_values(False)
    389
    >>> test_subclass_exception_values(True)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    cdef GetInt getter
    return getter.get(fire)
