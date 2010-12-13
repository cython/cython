__doc__ = u"""
    >>> class Test(object):
    ...     def __setitem__(self, key, value):
    ...         print((key, value))
    ...     def __getitem__(self, key):
    ...         print(key)
    ...         return self

    >>> ellipsis(Test())
    Ellipsis

    >>> full(Test())
    slice(None, None, None)

    >>> select(0, Test(), 10, 20, 30)
    slice(10, None, None)
    slice(None, 20, None)
    slice(None, None, 30)
    slice(10, 20, None)
    slice(10, None, 30)
    slice(None, 20, 30)
    slice(10, 20, 30)
    slice(1, 2, 3)

    >>> set(Test(), -11)
    (slice(1, 2, 3), -11)
"""

def ellipsis(o):
    obj1 = o[...]

def full(o):
    obj1 = o[::]

def set(o, v):
    cdef int int3, int4, int5
    int3, int4, int5 = 1,2,3
    o[int3:int4:int5] = v

def select(obj1, obj2, obj3, obj4, obj5):
    cdef int int3, int4, int5
    int3, int4, int5 = 1,2,3

    obj1 = obj2[obj3::]
    obj1 = obj2[:obj4:]
    obj1 = obj2[::obj5]
    obj1 = obj2[obj3:obj4:]
    obj1 = obj2[obj3::obj5]
    obj1 = obj2[:obj4:obj5]
    obj1 = obj2[obj3:obj4:obj5]
    obj1 = obj2[int3:int4:int5]

