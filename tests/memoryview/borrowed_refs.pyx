# mode: run
# tag: memoryview, parallel

from cython.parallel import prange

import gc

include "../buffers/mockbuffers.pxi"

cdef extern from *:
    """
    static int __pyx_v_incref_count = 0;
    static int __pyx_v_clear_count = 0;

    #define IGNORE_VARIABLE(x)
    """
    void __PYX_INC_MEMVIEW(...)
    void __PYX_XCLEAR_MEMVIEW(...)
    ctypedef struct memviewslicetype "__Pyx_memviewslice"

    # Here we slightly abuse the "cname" feature to be able to inject arbitrary C code under
    # the guise of a variable declaration.
    ctypedef int undef_inc_memview "#undef __PYX_INC_MEMVIEW //"
    ctypedef int define_inc_memview "#define __PYX_INC_MEMVIEW(o, have_gil) inc_memoryview(o, have_gil), ++__pyx_v_incref_count //"
    ctypedef int undef_clear_memview "#undef __PYX_XCLEAR_MEMVIEW //"
    ctypedef int define_clear_memview "#define __PYX_XCLEAR_MEMVIEW(o, have_gil) clear_memoryview(o, have_gil), ++__pyx_v_clear_count //"

    # Ignore variable can just be used so Cython doesn't optimize out our definitions entirely
    void IGNORE_VARIABLE(...)

    int __pyx_v_incref_count
    int __pyx_v_clear_count

# These two functions are "public" to have predictable naming.
# They call the original unaltered __PYX_INC_MEMVIEW macros
cdef public void inc_memoryview(memviewslicetype* memslice, int have_gil):
    __PYX_INC_MEMVIEW(memslice, have_gil)

cdef public void clear_memoryview(memviewslicetype* memslice, int have_gil):
    __PYX_XCLEAR_MEMVIEW(memslice, have_gil)

cdef void do_macro_redefinitions():
    # From this point on, __PYX_INC_MEMVIEW and __PYX_XCLEAR_MEMVIEW are redefined
    # so that they track the number of increfs and clears, referring to function local
    # variables if available, and some fallbacks in the global scope if not (just so that
    # code compiles)
    cdef undef_inc_memview dummy1
    cdef define_inc_memview dummy2
    cdef undef_clear_memview dummy3
    cdef define_clear_memview dummy4
    IGNORE_VARIABLE(dummy1)
    IGNORE_VARIABLE(dummy2)
    IGNORE_VARIABLE(dummy3)
    IGNORE_VARIABLE(dummy4)

do_macro_redefinitions() # stop C complaining about unused function

def use_borrowed_refs1(double[:, :] x):
    """
    >>> use_borrowed_refs1(DoubleMockBuffer("x", range(300), (2,150)))
    acquired x
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    for i in range(x.shape[1]):
        y = x[:, i]

    assert incref_count == 1, incref_count
    # The clear count comes from the iteration (on the unassigned buffer)
    # It *is* cleared properly on function exit, but after the assertion
    assert clear_count == 1, clear_count

      # This assignment to x doesn't prevent the optimization
    x = DoubleMockBuffer(None, range(4), (2, 2))

    print("done")

def use_borrowed_refs2(double[:] x):
    """
    >>> use_borrowed_refs2(DoubleMockBuffer("x", range(150), (150,)))
    acquired x
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0
    cdef double[:] y

    for i in range(x.shape[0]):
        y = x[i:]

    assert incref_count == 1, incref_count
    # It *is* cleared properly on function exit, but after the assertion
    assert clear_count == 1, clear_count

    print("done")


'''
# TODO - optimization currently misses here
def use_borrowed_refs3(double[:, :] x):
    """
    >>> use_borrowed_refs3(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    for y in x:
        pass

    assert incref_count == 1, incref_count
    assert clear_count == 1, clear_count

    print("done")
'''


cdef void empty(double[:] x) nogil noexcept:
    pass

def use_borrowed_refs4(double[:, :] x):
    """
    >>> use_borrowed_refs4(DoubleMockBuffer("x", range(300), (2,150)))
    acquired x
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    for i in range(x.shape[1]):
        empty(x[:, i])

    # Never increfed inside the function - we always pass a borrowed reference
    assert incref_count == 0, incref_count
    # Never cleared inside the function - we always pass a borrowed reference
    assert clear_count == 0, clear_count

def use_borrowed_refs5(double[:] x, double[:] y):
    """
    >>> use_borrowed_refs5(DoubleMockBuffer("x", range(100), (100,)), DoubleMockBuffer("y", range(100), (100,)))
    acquired x
    acquired y
    done
    released x
    released y
    """
    cdef int incref_count = 0
    cdef int clear_count = 0
    cdef double[:] target

    target = x[1:]  # 0 decref (first assignment), 1 incref
    target = y[1:]  # 1 decref, 1 incref
    target = y[:-1]  # 0 decref, 0 incref (same)

    assert incref_count == 2, incref_count
    assert clear_count == 1, clear_count

    print("done")

'''
TODO - doesn't work currently
def use_borrowed_refs_prange(double[:, :] x):
    """
    >>> use_borrowed_refs_prange(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0
    cdef Py_ssize_t i

    for i in prange(x.shape[0], nogil=True):
        empty(x[i, :])

    # same as equivalent test with range
    assert incref_count == 0, incref_count
    assert clear_count == 0, clear_count

    print("done")
'''

def use_borrowed_refs_generator(double[:, :] x):
    """
    Unlike for a closure, being in a generator shouldn't be an issue

    >>> gen = use_borrowed_refs_generator(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    >>> _ = list(gen)
    done
    released x
    """
    cdef int incref_count_before = __pyx_v_incref_count
    cdef int clear_count_before = __pyx_v_clear_count
    cdef Py_ssize_t i

    yield

    for i in range(x.shape[1]):
        y = x[:, i]

    # In a generator, we just need to use the global incref and clear count
    # because names we define aren't at function scope
    delta_incref_count = __pyx_v_incref_count - incref_count_before
    delta_clear_count = __pyx_v_clear_count - clear_count_before
    assert delta_incref_count == 1, delta_incref_count
    assert delta_clear_count == 1, delta_clear_count

    print("done")
    yield


# Follow tests are for the things that should prevent use of borrowed references.
# The tests may have to be made stricter if the logic gets cleverer (so not everything
# tester here should always be banned long-term)

def dont_use_borrowed_refs_walrus(double[:,:] x):
    """
    >>> dont_use_borrowed_refs_walrus(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """

    cdef int incref_count = 0
    cdef int clear_count = 0

    if x.shape[0] == -1:
        (x := x)  # doesn't actually happen, but possibility of walrus assignment
            # is currently enough that we distrust 'x' for borrowed references
    for i in range(x.shape[0]):
        y = x[i, :]

    assert incref_count == x.shape[0], incref_count
    assert clear_count == x.shape[0], clear_count

    print("done")

def dont_use_borrowed_refs_parallel(double[:,:] x):
    """
    >>> dont_use_borrowed_refs_parallel(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """

    cdef int incref_count = 0
    cdef int clear_count = 0

    if x.shape[0] == -1:
        # doesn't actually happen, but possibility of walrus assignment
        # is currently enough that we distrust 'x' for borrowed references
        x, dummy = x, 5
    for i in range(x.shape[0]):
        y = x[i, :]

    assert incref_count == x.shape[0], incref_count
    assert clear_count == x.shape[0], clear_count

    print("done")

cdef double[:,:] global_memview = DoubleMockBuffer(None, range(300), (150,2))

def dont_use_borrowed_refs_global():
    """
    >>> dont_use_borrowed_refs_global()
    done
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    for i in range(global_memview.shape[0]):
        y = global_memview[i, :]

    assert incref_count == global_memview.shape[0], incref_count
    assert clear_count == global_memview.shape[0], clear_count

    print("done")

cdef class C:
    cdef double[:, :] attr

    def __init__(self, obj):
        self.attr = obj

def dont_use_borrowed_refs_attr(C c):
    """
    >>> c = C(DoubleMockBuffer(None, range(300), (150,2)))
    >>> dont_use_borrowed_refs_attr(c)
    done
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    for i in range(c.attr.shape[0]):
        y = c.attr[i, :]

    assert incref_count == c.attr.shape[0], incref_count
    assert clear_count == c.attr.shape[0], clear_count

    print("done")

def dont_use_borrowed_refs_closure1(double[:,:] x):
    """
    >>> dont_use_borrowed_refs_closure1(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """
    def inner():
        cdef int incref_count = 0
        cdef int clear_count = 0

        for i in range(x.shape[0]):
            y = x[i, :]

        # >= because it's hard to reason about what is needed to capture it
        assert incref_count >= x.shape[0], incref_count
        assert clear_count >= x.shape[0], clear_count

    inner()
    print("done")
    # Limited API needs GC to clean up the closure
    del inner
    gc.collect()

def dont_use_borrowed_refs_closure2(double[:,:] x):
    """
    >>> dont_use_borrowed_refs_closure2(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    0.0
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0

    def inner():
        print(x[0, 0])

    for i in range(x.shape[0]):
        y = x[i, :]

    # >= because it's hard to reason about what is needed to capture it
    assert incref_count >= x.shape[0], incref_count
    assert clear_count >= x.shape[0], clear_count

    inner()
    print("done")
    # Limited API needs GC to clean up the closure
    del inner
    gc.collect()

def dont_use_borrowed_refs_prange(double[:, :] x):
    """
    >>> dont_use_borrowed_refs_prange(DoubleMockBuffer("x", range(300), (150,2)))
    acquired x
    done
    released x
    """
    cdef int incref_count = 0
    cdef int clear_count = 0
    cdef Py_ssize_t i

    for i in prange(x.shape[0], nogil=True):
        empty(x[i, :])

    assert incref_count >= x.shape[0], incref_count
    assert clear_count >= x.shape[0], clear_count

    # any assignment to x means that we don't trust borrowed refs in a prange
    x = DoubleMockBuffer(None, range(4), (2, 2))

    print("done")
