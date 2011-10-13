
import cython

class Unhashable(object):
    def __hash__(self):
        raise TypeError('I am not hashable')

class Hashable(object):
    def __hash__(self):
        return 1
    def __eq__(self, other):
        return isinstance(other, Hashable)

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
    """
    return d.setdefault(key, value)
