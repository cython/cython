# -*- coding: iso-8859-1 -*-

cdef Py_UNICODE char_ASCII = u'A'
cdef Py_UNICODE char_KLINGON = u'\uF8D2'

def char_too_long_ASCII():
    cdef Py_UNICODE c = u'AB'

def char_too_long_Unicode():
    cdef Py_UNICODE c = u'A\uF8D2'

def char_too_long_bytes():
    cdef Py_UNICODE c = b'AB'

def char_too_long_latin1():
    cdef Py_UNICODE char_bytes_latin1 = b'\xf6'


_ERRORS = """
 7:24: Only single-character Unicode string literals or surrogate pairs can be coerced into Py_UCS4/Py_UNICODE.
10:24: Only single-character Unicode string literals or surrogate pairs can be coerced into Py_UCS4/Py_UNICODE.
13:24: Only single-character string literals can be coerced into ints.
16:40: Bytes literals cannot coerce to Py_UNICODE/Py_UCS4, use a unicode literal instead.
"""
