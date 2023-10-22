# mode: run
# tag: cpp, werror, no-cpp-locals

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

    cdef cppclass C[C1](B[i64, C1]):
        C1 funcC(C1)

    cdef cppclass D[D1](C[pair[D1, D1]]):
        pass

    cdef cppclass E(D[f64]):
        pass

def testA(x):
    """
    >>> testA(10)
    10.0
    """
    cdef Base *base
    cdef A[f64] *a = NULL
    try:
        a = new A[f64]()
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
    cdef A[f64] *a
    cdef B[i64, f64] *b = NULL
    try:
        base = a = b = new B[i64, f64]()
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
    cdef A[vector[i64]] *a
    cdef B[i64, vector[i64]] *b
    cdef C[vector[i64]] *c = NULL
    try:
        base = a = b = c = new C[vector[i64]]()
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
    cdef A[pair[f64, f64]] *a
    cdef B[i64, pair[f64, f64]] *b
    cdef C[pair[f64, f64]] *c
    cdef D[f64] *d = NULL
    try:
        base = a = b = c = d = new D[f64]()
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
    cdef A[pair[f64, f64]] *a
    cdef B[i64, pair[f64, f64]] *b
    cdef C[pair[f64, f64]] *c
    cdef D[f64] *d
    cdef E *e = NULL
    try:
        base = a = b = c = d = e = new E()
        assert base.name() == b"E", base.name()
        assert <object>a.funcA((y, y)) == (y, y)
        assert <object>b.funcB(x, (y, y + 1)) == (x, (y, y + 1))
        assert <object>c.funcC((y, y)) == (y, y)
    finally:
        del e

pub pair[i32, f64] public_return_pair(a, b) except *:
  return pair[i32, f64](a, b)

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

cdef cppclass GetInt(Getter[i32]):
    i32 get(bint fire) except *:
        if fire:
            raise RuntimeError
        else:
            return 389

def test_subclass_exception_values(bint fire):
    """
    >>> test_subclass_exception_values(false)
    389
    >>> test_subclass_exception_values(true)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    cdef GetInt getter
    return getter.get(fire)
