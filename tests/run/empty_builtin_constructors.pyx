# mode: run

cimport cython


def _bool():
    """
    >>> _bool() == bool()
    True
    """
    return bool()

def _int():
    """
    >>> _int() == int()
    True
    """
    return int()

def _float():
    """
    >>> _float() == float()
    True
    """
    return float()

def _complex():
    """
    >>> _complex() == complex()
    True
    """
    return complex()

def _bytes():
    """
    >>> _bytes() == bytes()
    True
    """
    return bytes()

def _str():
    """
    >>> _str() == str()
    True
    """
    return str()

def _unicode():
    """
    >>> _unicode() == str()
    True
    """
    return unicode()

def _tuple():
    """
    >>> _tuple() == tuple()
    True
    """
    return tuple()

def _list():
    """
    >>> _list() == list()
    True
    """
    return list()

def _dict():
    """
    >>> _dict() == dict()
    True
    """
    return dict()

py_set = cython.set

def _set():
    """
    >>> _set() == py_set()
    True
    """
    return set()

py_frozenset = cython.frozenset

def _frozenset():
    """
    >>> _frozenset() == py_frozenset()
    True
    """
    return frozenset()
