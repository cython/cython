
cimport cython
import sys

IS_PY3 = sys.version_info[0] >= 3

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

def _long():
    """
    >>> IS_PY3 or _long() == long()
    True
    """
    return long()

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
    >>> IS_PY3 and _bytes() == bytes() or _bytes() == str()
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
    >>> IS_PY3 and _unicode() == str() or _unicode() == unicode()
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
