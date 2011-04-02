# mode: error
# -*- coding: iso-8859-1 -*-

cdef Py_UCS4 char_ASCII = u'A'
cdef Py_UCS4 char_KLINGON = u'\uF8D2'

def char_too_long_ASCII():
    cdef Py_UCS4 c = u'AB'

def char_too_long_Unicode():
    cdef Py_UCS4 c = u'A\uF8D2'

def char_too_long_bytes():
    cdef Py_UCS4 c = b'AB'

def char_too_long_latin1():
    cdef Py_UCS4 char_bytes_latin1 = b'\xf6'


_ERRORS = """
 8:21: Only single-character Unicode string literals or surrogate pairs can be coerced into Py_UCS4/Py_UNICODE.
11:21: Only single-character Unicode string literals or surrogate pairs can be coerced into Py_UCS4/Py_UNICODE.
14:21: Only single-character string literals can be coerced into ints.
17:37: Bytes literals cannot coerce to Py_UNICODE/Py_UCS4, use a unicode literal instead.
"""
