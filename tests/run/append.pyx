class A:
    def append(self, x):
        print u"appending", x
        return x

class B(list):
    def append(self, *args):
        for arg in args:
            list.append(self, arg)

cdef class C:
    """
    >>> c = C(100)
    appending 100
    """
    def __init__(self, value):
        self.append(value)
    cdef append(self, value):
        print u"appending", value
        return value

def test_append(L):
    """
    >>> test_append([])
    None
    None
    None
    got error
    [1, 2, (3, 4)]
    >>> _ = test_append(A())
    appending 1
    1
    appending 2
    2
    appending (3, 4)
    (3, 4)
    got error
    >>> test_append(B())
    None
    None
    None
    None
    [1, 2, (3, 4), 5, 6]
    """
    print L.append(1)
    print L.append(2)
    print L.append((3,4))
    try:
        print L.append(5,6)
    except TypeError:
        print u"got error"
    return L


def test_append_typed(list L not None):
    """
    >>> test_append_typed([])
    None
    None
    [1, 2, (3, 4)]
    """
    print L.append(1)
    L.append(2)
    print L.append((3,4))
    return L


def append_unused_retval(L):
    """
    >>> append_unused_retval([])
    got error
    [1, 2, (3, 4)]
    >>> _ = append_unused_retval(A())
    appending 1
    appending 2
    appending (3, 4)
    got error
    >>> append_unused_retval(B())
    [1, 2, (3, 4), 5, 6]
    """
    L.append(1)
    L.append(2)
    L.append((3,4))
    try:
        L.append(5,6)
    except TypeError:
        print u"got error"
    return L


def method_name():
    """
    >>> method_name()
    'append'
    """
    return [].append.__name__
