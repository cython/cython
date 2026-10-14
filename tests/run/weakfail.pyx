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


cdef class Inherited1(Foo):
    pass

cdef class Inherited2(Foo):
    cdef int something_else

cdef class Inherited3(Foo):
    cdef object __weakref__  # It's allowed for classes to reimplement this

cdef class NoWeakref:
    pass

cdef class Inherited4(NoWeakref):
    cdef object __weakref__

def test_inherited_weakref(tp):
    """
    >>> test_inherited_weakref(Inherited1)
    >>> test_inherited_weakref(Inherited2)
    >>> test_inherited_weakref(Inherited3)
    >>> test_inherited_weakref(Inherited4) 
    """
    inst = tp()
    weakinst = weakref.ref(inst)
    assert weakinst() is not None
    del inst
    gc.collect()
    assert weakinst() is None
