# mode: run

from __future__ import print_function

cimport cython

import gc

cdef class nontrivial_del:
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")

def test_del():
    """
    >>> test_del()
    start
    init
    del
    finish
    """
    print("start")
    d = nontrivial_del()
    d = None
    gc.collect()
    print("finish")


cdef class del_and_dealloc:
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")

    def __dealloc__(self):
        print("dealloc")

def test_del_and_dealloc():
    """
    >>> test_del_and_dealloc()
    start
    init
    del
    dealloc
    finish
    """
    print("start")
    d = del_and_dealloc()
    d = None
    gc.collect()
    print("finish")

@cython.final
cdef class FinalClass:
    def __init__(self):
        print("init")
    def __del__(self):
        print("del")

def test_final_class():
    """
    >>> test_final_class()
    start
    init
    del
    finish
    """
    print("start")
    d = FinalClass()
    d = None
    gc.collect()
    print("finish")

@cython.final
cdef class FinalInherits(nontrivial_del):
    def __init__(self):
        super().__init__()
        print("FinalInherits init")
    # no __del__ but nontrivial_del should still be called
    def __dealloc__(self):
        pass  # define __dealloc__ so as not to fall back on base __dealloc__

def test_final_inherited():
    """
    >>> test_final_inherited()
    start
    init
    FinalInherits init
    del
    finish
    """
    print("start")
    d = FinalInherits()
    d = None
    gc.collect()
    print("finish")

cdef class DummyBase:
    pass

class RegularClass:
    __slots__ = ()
    def __del__(self):
        print("del")

@cython.final
cdef class FinalMultipleInheritance(DummyBase, RegularClass):
    def __init__(self):
        super().__init__()
        print("init")
    def __dealloc__(self):
        pass

def test_final_multiple_inheritance():
    """
    >>> test_final_multiple_inheritance()
    start
    init
    del
    finish
    """
    print("start")
    d = FinalMultipleInheritance()
    d = None
    gc.collect()
    print("finish")

cdef class del_with_exception:
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")
        raise Exception("Error")

def test_del_with_exception():
    """
    >>> test_del_with_exception()
    start
    init
    del
    finish
    """
    print("start")
    d = nontrivial_del()
    d = None
    gc.collect()
    print("finish")


def test_nontrivial_del_with_exception():
    """
    >>> test_nontrivial_del_with_exception()
    start
    init
    del
    end
    """
    print("start")
    def inner():
        c = nontrivial_del()
        raise RuntimeError()

    try:
        inner()
    except RuntimeError:
        pass

    print("end")


cdef class parent:
    def __del__(self):
        print("del parent")

class child(parent):
    def __del__(self):
        print("del child")

def test_del_inheritance():
    """
    >>> test_del_inheritance()
    start
    del child
    finish
    """
    print("start")
    c = child()
    c = None
    gc.collect()
    print("finish")


cdef class cy_parent:
    def __del__(self):
        print("del cy_parent")

    def __dealloc__(self):
        print("dealloc cy_parent")

class py_parent:
    def __del__(self):
        print("del py_parent")

class multi_child(cy_parent, py_parent):
    def __del__(self):
        print("del child")

def test_multiple_inheritance():
    """
    >>> test_multiple_inheritance()
    start
    del child
    dealloc cy_parent
    finish
    """
    print("start")
    c = multi_child()
    c = None
    gc.collect()
    print("finish")


cdef class zombie_object:
    def __del__(self):
        global global_zombie_object
        print("del")
        global_zombie_object = self

    def __dealloc__(self):
        print("dealloc")

def test_zombie_object():
    """
    >>> test_zombie_object()
    start
    del
    del global
    del
    finish
    """
    global global_zombie_object
    print("start")
    i = zombie_object()
    i = None
    print("del global")
    del global_zombie_object
    gc.collect()
    print("finish")


# Same as above, but the member
# makes the class GC, so it
# is deallocated
cdef class gc_zombie_object:
    cdef object x

    def __del__(self):
        global global_gc_zombie_object
        print("del")
        global_gc_zombie_object = self

    def __dealloc__(self):
        print("dealloc")

def test_gc_zombie_object():
    """
    >>> test_gc_zombie_object()
    start
    del
    del global
    dealloc
    finish
    """
    global global_gc_zombie_object
    print("start")
    i = gc_zombie_object()
    i = None
    print("del global")
    del global_gc_zombie_object
    gc.collect()
    print("finish")


cdef class cdef_parent:
    pass

cdef class cdef_child(cdef_parent):
    def __del__(self):
        print("del")
    def __dealloc__(self):
        print("dealloc")

def test_cdef_parent_object():
    """
    >>> test_cdef_parent_object()
    start
    del
    dealloc
    finish
    """
    print("start")
    i = cdef_child()
    i = None
    gc.collect()
    print("finish")


cdef class cdef_nontrivial_parent:
    def __del__(self):
        print("del parent")
    def __dealloc__(self):
        print("dealloc parent")

cdef class cdef_nontrivial_child(cdef_nontrivial_parent):
    def __del__(self):
        print("del child")
    def __dealloc__(self):
        print("dealloc child")

def test_cdef_nontrivial_parent_object():
    """
    >>> test_cdef_nontrivial_parent_object()
    start
    del child
    dealloc child
    dealloc parent
    finish
    """
    print("start")
    i = cdef_nontrivial_child()
    i = None
    gc.collect()
    print("finish")


class python_child(cdef_nontrivial_parent):
    def __del__(self):
        print("del python child")
        super().__del__()

def test_python_child_object():
    """
    >>> test_python_child_object()
    Traceback (most recent call last):
    ...
    RuntimeError: End function
    """

    def func(tp):
        inst = tp()
        raise RuntimeError("End function")

    func(python_child)

def test_python_child_fancy_inherit():
    """
    >>> test_python_child_fancy_inherit()
    Traceback (most recent call last):
    ...
    RuntimeError: End function
    """

    # inherit using "true python" rather than Cython
    globs = { 'cdef_nontrivial_parent': cdef_nontrivial_parent }

    exec("""
class derived_python_child(cdef_nontrivial_parent):
    pass
""", globs)

    derived_python_child = globs['derived_python_child']

    def func(tp):
        inst = tp()
        raise RuntimeError("End function")

    func(derived_python_child)

