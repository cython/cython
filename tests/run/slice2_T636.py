# mode: run
# ticket 636
# tag: slicing, getitem

class Sliceable(object):
    """
    >>> sl = Sliceable()

    >>> sl[1:2]
    (1, 2, None)
    >>> py_slice2(sl, 1, 2)
    (1, 2, None)

    >>> sl[1:None]
    (1, None, None)
    >>> py_slice2(sl, 1, None)
    (1, None, None)

    >>> sl[None:2]
    (None, 2, None)
    >>> py_slice2(sl, None, 2)
    (None, 2, None)

    >>> sl[None:None]
    (None, None, None)
    >>> py_slice2(sl, None, None)
    (None, None, None)
    """
    def __getitem__(self, sl):
        return (sl.start, sl.stop, sl.step)

def py_slice2(obj,a,b):
    """
    >>> [1,2,3][1:2]
    [2]
    >>> py_slice2([1,2,3], 1, 2)
    [2]

    >>> [1,2,3][None:2]
    [1, 2]
    >>> py_slice2([1,2,3], None, 2)
    [1, 2]

    >>> [1,2,3][None:None]
    [1, 2, 3]
    >>> py_slice2([1,2,3], None, None)
    [1, 2, 3]
    """
    return obj[a:b]
