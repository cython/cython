import cython


def test_missing_type(l1, l2):
    """
    >>> test_missing_type([1], [2])
    tuple[Python object,Python object] object
    """
    for l in zip(l1, l2):
        print(cython.typeof(l))

def test_known_missing_type(l2):
    """
    >>> test_known_missing_type([2])
    tuple[int,Python object] object
    """
    l1: list[cython.int] = [1]
    for l in zip(l1, l2):
        print(cython.typeof(l))

def test_c_type():
    # FIXME: ctuple conversion to tuple object looses information about subscripted types
    """
    >>> test_c_type()
    tuple object
    """
    l1: list[cython.int] = [1]
    l2: list[cython.int] = [1]
    for l in zip(l1, l2):
        print(cython.typeof(l))

def test_str_type():
    """
    >>> test_str_type()
    tuple[str object,str object] object
    """
    l1: list[str] = ['a']
    l2: list[str] = ['b']
    for l in zip(l1, l2):
        print(cython.typeof(l))

def test_str_int_type():
    """
    >>> test_str_int_type()
    tuple[str object,int object] object
    """
    l1: list[str] = ['a']
    l2: list[int] = [1]
    for l in zip(l1, l2):
        print(cython.typeof(l))

cdef class A:
    pass

cdef class B(A):
    pass

def test_common_type():
    """
    >>> test_common_type()
    tuple[A,A,B,Python object] object
    tuple[A,A,B,Python object] object
    """
    l1: tuple[A, B] = (A(), B()) # Common type: A
    l2: tuple[B, A] = (B(), A()) # Common type: A
    l3: tuple[B, B] = (B(), B()) # Common type: B
    l4: tuple[A, int] = (A(), 5) # Common type: python object
    for l in zip(l1, l2, l3, l4):
        print(cython.typeof(l))

def _zip(l1, l2):
    return "Custom zip"

def test_overriden_zip():
    """
    >>> test_overriden_zip()
    """
    l1 = []
    l2 = []
    zip = _zip
    assert zip(l1, l2) == "Custom zip", zip(l1, l2)

def test_star():
    """
    >>> test_star()
    Python object
    """
    ll = [[1], [2]]
    for l in zip(*ll):
        print(cython.typeof(l))
