# -*- coding: utf-8 -*-

__doc__ = u"""
>>> len(u)
15
"""

cimport cython

_bytes = bytes

cdef unicode text = u'abcäöüöéèâÁÀABC'

u = text

def default():
    """
    >>> default() == 'abcdefg'.encode()
    True
    """
    return u'abcdefg'.encode()

def encode_non_constant(encoding):
    """
    >>> isinstance(encode_non_constant('utf8'), _bytes)
    True
    >>> encode_non_constant('utf8') == u.encode('UTF-8')
    True
    """
    return text.encode(encoding)

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsUTF8String"]')
def utf8():
    """
    >>> isinstance(utf8(), _bytes)
    True
    >>> utf8() == u.encode('UTF-8')
    True
    """
    return text.encode(u'UTF-8')

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsUTF8String"]')
def utf8_strict():
    """
    >>> isinstance(utf8_strict(), _bytes)
    True
    >>> utf8_strict() == u.encode('UTF-8', 'strict')
    True
    """
    return text.encode(u'UTF-8', u'strict')

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsUTF8String"]')
def utf8_str_strict():
    """
    >>> isinstance(utf8_str_strict(), _bytes)
    True
    >>> utf8_str_strict() == u.encode('UTF-8', 'strict')
    True
    """
    return text.encode('UTF-8', 'strict')

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsUTF8String"]')
def utf8_bytes_strict():
    """
    >>> isinstance(utf8_bytes_strict(), _bytes)
    True
    >>> utf8_bytes_strict() == u.encode('UTF-8', 'strict')
    True
    """
    return text.encode(b'UTF-8', b'strict')

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsEncodedString"]')
def ascii_replace():
    """
    >>> isinstance(ascii_replace(), _bytes)
    True
    >>> ascii_replace() == u.encode('ASCII', 'replace')
    True
    """
    return text.encode(u'ASCII', u'replace')

def cp850_strict():
    """
    >>> isinstance(cp850_strict(), _bytes)
    True
    >>> cp850_strict() == u.encode('cp850', 'strict')
    True
    """
    return text.encode(u'cp850', u'strict')

@cython.test_assert_path_exists('//PythonCapiFunctionNode[@cname = "PyUnicode_AsLatin1String"]')
def latin1():
    """
    >>> isinstance(latin1(), _bytes)
    True
    >>> latin1() == u.encode('latin-1')
    True
    """
    return text.encode(u'latin-1')

@cython.test_fail_if_path_exists('//PythonCapiFunctionNode', '//SimpleCallNode')
def latin1_constant():
    """
    >>> isinstance(latin1_constant(), _bytes)
    True
    >>> latin1_constant() == latin1()
    True
    """
    return u'abcäöüöéèâÁÀABC'.encode('latin1')
