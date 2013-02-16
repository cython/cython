
import cython

class Unhashable(object):
    def __hash__(self):
        raise TypeError('I am not hashable')

class Hashable(object):
    def __hash__(self):
        return 1
    def __eq__(self, other):
        return isinstance(other, Hashable)

class CountedHashable(object):
    def __init__(self):
        self.hash_count = 0
        self.eq_count = 0
    def __hash__(self):
        self.hash_count += 1
        return 42
    def __eq__(self, other):
        self.eq_count += 1
        return id(self) == id(other)

@cython.test_fail_if_path_exists('//AttributeNode')
@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.locals(d=dict)
def setdefault1(d, key):
    """
    >>> d = {}
    >>> setdefault1(d, 1)
    >>> len(d)
    1
    >>> setdefault1(d, 1)
    >>> len(d)
    1
    >>> d[1]
    >>> setdefault1(d, Unhashable())
    Traceback (most recent call last):
    TypeError: I am not hashable
    >>> len(d)
    1
    >>> h1 = setdefault1(d, Hashable())
    >>> len(d)
    2
    >>> h2 = setdefault1(d, Hashable())
    >>> len(d)
    2
    >>> d[Hashable()]

    # CPython's behaviour depends on version and py_debug setting, so just compare to it
    >>> py_hashed1 = CountedHashable()
    >>> y = {py_hashed1: 5}
    >>> py_hashed2 = CountedHashable()
    >>> y.setdefault(py_hashed2)

    >>> cy_hashed1 = CountedHashable()
    >>> y = {cy_hashed1: 5}
    >>> cy_hashed2 = CountedHashable()
    >>> setdefault1(y, cy_hashed2)
    >>> py_hashed1.hash_count - cy_hashed1.hash_count
    0
    >>> py_hashed2.hash_count - cy_hashed2.hash_count
    0
    >>> (py_hashed1.eq_count + py_hashed2.eq_count) - (cy_hashed1.eq_count + cy_hashed2.eq_count)
    0
    """
    return d.setdefault(key)

@cython.test_fail_if_path_exists('//AttributeNode')
@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.locals(d=dict)
def setdefault2(d, key, value):
    """
    >>> d = {}
    >>> setdefault2(d, 1, 2)
    2
    >>> len(d)
    1
    >>> setdefault2(d, 1, 2)
    2
    >>> len(d)
    1
    >>> l = setdefault2(d, 2, [])
    >>> len(d)
    2
    >>> l.append(1)
    >>> setdefault2(d, 2, [])
    [1]
    >>> len(d)
    2
    >>> setdefault2(d, Unhashable(), 1)
    Traceback (most recent call last):
    TypeError: I am not hashable
    >>> h1 = setdefault2(d, Hashable(), 55)
    >>> len(d)
    3
    >>> h2 = setdefault2(d, Hashable(), 66)
    >>> len(d)
    3
    >>> d[Hashable()]
    55

    # CPython's behaviour depends on version and py_debug setting, so just compare to it
    >>> py_hashed1 = CountedHashable()
    >>> y = {py_hashed1: 5}
    >>> py_hashed2 = CountedHashable()
    >>> y.setdefault(py_hashed2, [])
    []

    >>> cy_hashed1 = CountedHashable()
    >>> y = {cy_hashed1: 5}
    >>> cy_hashed2 = CountedHashable()
    >>> setdefault2(y, cy_hashed2, [])
    []
    >>> py_hashed1.hash_count - cy_hashed1.hash_count
    0
    >>> py_hashed2.hash_count - cy_hashed2.hash_count
    0
    >>> (py_hashed1.eq_count + py_hashed2.eq_count) - (cy_hashed1.eq_count + cy_hashed2.eq_count)
    0
    """
    return d.setdefault(key, value)
