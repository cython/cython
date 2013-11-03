import gc
import weakref

foo_dict = weakref.WeakValueDictionary()

cdef class Foo:
    cdef object __weakref__

def test_weakref(key):
    """
    Test af9cfeb5f94d9cd4f2989fc8e111c33208494ba4 fix.
    Originally running it using debug build of python lead to::

      visit_decref: Assertion `gc->gc.gc_refs != 0' failed

    >>> _ = gc.collect()
    >>> _ = test_weakref(48)
    >>> _ = gc.collect()
    """
    obj = Foo()
    foo_dict[key] = obj
    return obj

