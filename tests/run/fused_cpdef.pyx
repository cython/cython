# cython: language_level=3str
# mode: run

cimport cython
import sys, io

cy = __import__("cython")

cpdef func1(self, cython.integral x):
    print(f"{self},", end=' ')
    if cython.integral is int:
        print('x is int', x, cython.typeof(x))
    else:
        print('x is long', x, cython.typeof(x))


class A(object):
    meth = func1

    def __str__(self):
        return "A"

cdef class B:
    cpdef int meth(self, cython.integral x):
        print(f"{self},", end=' ')
        if cython.integral is int:
            print('x is int', x, cython.typeof(x))
        else:
            print('x is long', x, cython.typeof(x))
        return 0

    def __str__(self):
        return "B"

pyfunc = func1

def test_fused_cpdef():
    """
    >>> test_fused_cpdef()
    None, x is int 2 int
    None, x is long 2 long
    None, x is long 2 long
    <BLANKLINE>
    None, x is int 2 int
    None, x is long 2 long
    <BLANKLINE>
    A, x is int 2 int
    A, x is long 2 long
    A, x is long 2 long
    A, x is long 2 long
    <BLANKLINE>
    B, x is long 2 long
    """
    func1[int](None, 2)
    func1[long](None, 2)
    func1(None, 2)

    print()

    pyfunc[cy.int](None, 2)
    pyfunc(None, 2)

    print()

    A.meth[cy.int](A(), 2)
    A.meth(A(), 2)
    A().meth[cy.long](2)
    A().meth(2)

    print()

    B().meth(2)


midimport_run = io.StringIO()
realstdout = sys.stdout
sys.stdout = midimport_run

try:
    # Run `test_fused_cpdef()` during import and save the result for
    #        `test_midimport_run()`.
    test_fused_cpdef()
except Exception as e:
    midimport_run.write(f"{e!r}\n")
finally:
    sys.stdout = realstdout

def test_midimport_run():
    # At one point, dynamically calling fused cpdef functions during import
    #        would fail because the type signature-matching indices weren't
    #        yet initialized.
    #        (See Compiler.FusedNode.FusedCFuncDefNode._fused_signature_index,
    #        GH-3366.)
    """
    >>> test_midimport_run()
    None, x is int 2 int
    None, x is long 2 long
    None, x is long 2 long
    <BLANKLINE>
    None, x is int 2 int
    None, x is long 2 long
    <BLANKLINE>
    A, x is int 2 int
    A, x is long 2 long
    A, x is long 2 long
    A, x is long 2 long
    <BLANKLINE>
    B, x is long 2 long
    """
    print(midimport_run.getvalue(), end='')


def assert_raise(func, *args):
    try:
        func(*args)
    except TypeError:
        pass
    else:
        assert False, "Function call did not raise TypeError"

def test_badcall():
    """
    >>> test_badcall()
    """
    assert_raise(pyfunc)
    assert_raise(pyfunc, 1, 2, 3)
    assert_raise(pyfunc[cy.int], 10, 11, 12)
    assert_raise(pyfunc, None, object())
    assert_raise(A().meth)
    assert_raise(A.meth)
    assert_raise(A().meth[cy.int])
    assert_raise(A.meth[cy.int])
    assert_raise(B().meth, 1, 2, 3)

def test_nomatch():
    """
    >>> func1(None, ())
    Traceback (most recent call last):
    TypeError: No matching signature found
    """

ctypedef long double long_double

cpdef multiarg(cython.integral x, cython.floating y):
    if cython.integral is int:
        print("x is an int,", end=' ')
    else:
        print("x is a long,", end=' ')

    if cython.floating is long_double:
        print("y is a long double:", end=' ')
    elif float is cython.floating:
        print("y is a float:", end=' ')
    else:
        print("y is a double:", end=' ')

    print(x, y)

def test_multiarg():
    """
    >>> test_multiarg()
    x is an int, y is a float: 1 2.0
    x is an int, y is a float: 1 2.0
    x is a long, y is a double: 4 5.0
    >>> multiarg()
    Traceback (most recent call last):
    TypeError: Expected at least 2 arguments, got 0
    >>> multiarg(1, 2.0, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...2...arg...3...
    """
    multiarg[int, float](1, 2.0)
    multiarg[cy.int, cy.float](1, 2.0)
    multiarg(4, 5.0)

def test_ambiguousmatch():
    """
    >>> multiarg(5, ())
    Traceback (most recent call last):
    TypeError: Function call with ambiguous argument types
    >>> multiarg((), 2.0)
    Traceback (most recent call last):
    TypeError: Function call with ambiguous argument types
    """

# https://github.com/cython/cython/issues/4409
# default arguments + fused cpdef were crashing
cpdef literal_default(cython.integral x, some_string="value"):
    return x, some_string

cpdef mutable_default(cython.integral x, some_value=[]):
    some_value.append(x)
    return some_value

def test_defaults():
    """
    >>> literal_default(1)
    (1, 'value')
    >>> literal_default(1, "hello")
    (1, 'hello')
    >>> mutable_default(1)
    [1]
    >>> mutable_default(2)
    [1, 2]
    >>> mutable_default(3,[])
    [3]
    """

cdef class C:
    cpdef object has_default_struct(self, cython.floating x, a=None):
        return x, a

# https://github.com/cython/cython/issues/5588
# On some Python versions this was causing a compiler crash
def test_call_has_default_struct(C c, double x):
    """
    >>> test_call_has_default_struct(C(), 5.)
    (5.0, None)
    """
    return c.has_default_struct(x)
