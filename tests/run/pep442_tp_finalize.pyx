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
    dealloc
    finish
    """
    print("start")
    i = immortal()
    i = None
    import gc
    gc.collect()
    print("finish")
