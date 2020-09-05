# mode: run

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
    import gc
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
    import gc
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
    import gc
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
    import gc
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
    import gc
    gc.collect()
    print("finish")


cdef class immortal:
    def __del__(self):
        global c
        print("del")
        c = self

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
    global c
    print("start")
    i = immortal()
    i = None
    import gc
    print("del global")
    del c
    gc.collect()
    print("finish")


# Same as above, but the member
# makes the class GC, so it
# is deallocated
cdef class gc_immortal:
    cdef object x

    def __del__(self):
        global c
        print("del")
        c = self

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
    global c
    print("start")
    i = gc_immortal()
    i = None
    import gc
    print("del global")
    del c
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
    import gc
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
    import gc
    gc.collect()
    print("finish")
