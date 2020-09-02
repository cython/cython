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
    d = nontrivial_del()
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
