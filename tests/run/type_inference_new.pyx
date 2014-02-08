cimport cython

from cython cimport typeof, infer_types


def test_swap():
    """
    >>> test_swap()
    """
    a = 0
    b = 1
    tmp = a
    a = b
    b = tmp
    assert typeof(a) == "long", typeof(a)
    assert typeof(b) == "long", typeof(b)
    assert typeof(tmp) == "long", typeof(tmp)

def test_object_assmt():
    """
    >>> test_object_assmt()
    """
    a = 1
    b = a
    a = "str"
    assert typeof(a) == "Python object", typeof(a)
    assert typeof(b) == "long", typeof(b)


class RAdd(object):
    other = None
    def __radd__(self, other):
        self._other = other
        return self
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._other)


def test_inplace_assignment():
    """
    >>> test_inplace_assignment()
    RAdd([1, 2, 3])
    """
    l = [1, 2, 3]
    # inferred type of l is list, but assignment result is object
    l += RAdd()
    return l


def test_reassignment():
    """
    >>> test_reassignment()
    (1, 2, 3)
    """
    l = [1, 2, 3]
    l = (1, 2, 3)
    return l


def test_long_vs_double(cond):
    """
    >>> test_long_vs_double(0)
    """
    assert typeof(a) == "double", typeof(a)
    assert typeof(b) == "double", typeof(b)
    assert typeof(c) == "double", typeof(c)
    assert typeof(d) == "double", typeof(d)

    if cond:
        a = 1
        b = 2
        c = (a + b) / 2
    else:
        a = 1.0
        b = 2.0
        d = (a + b) / 2

def test_double_vs_pyobject():
    """
    >>> test_double_vs_pyobject()
    """
    assert typeof(a) == "Python object", typeof(a)
    assert typeof(b) == "Python object", typeof(b)
    assert typeof(d) == "double", typeof(d)

    a = []
    b = []

    a = 1.0
    b = 2.0
    d = (a + b) / 2

def test_python_objects(cond):
    """
    >>> test_python_objects(0)
    """
    if cond == 1:
        a = [1, 2, 3]
        o_list = a
    elif cond == 2:
        a = set([1, 2, 3])
        o_set = a
    else:
        a = {1:1, 2:2, 3:3}
        o_dict = a
    assert typeof(a) == "Python object", typeof(a)
    assert typeof(o_list) == "list object", typeof(o_list)
    assert typeof(o_dict) == "dict object", typeof(o_dict)
    assert typeof(o_set) == "set object", typeof(o_set)

# CF loops
def test_cf_loop():
    """
    >>> test_cf_loop()
    """
    cdef int i
    a = 0.0
    for i in range(3):
        a += 1
    assert typeof(a) == "double", typeof(a)

def test_cf_loop_intermediate():
    """
    >>> test_cf_loop()
    """
    cdef int i
    a = 0
    for i in range(3):
        b = a
        a = b + 1
    assert typeof(a) == "long", typeof(a)
    assert typeof(b) == "long", typeof(b)

# Integer overflow
def test_integer_overflow():
    """
    >>> test_integer_overflow()
    """
    a = 1
    b = 2
    c = a + b
    assert typeof(a) == "Python object", typeof(a)
    assert typeof(b) == "Python object", typeof(b)
    assert typeof(c) == "Python object", typeof(c)
