__doc__ = u"""
>>> test_c(u'abc')
fileabc
typeabc
>>> print test_file_py(u'abc')
abc
>>> print range(u'abc')
rangeabc
"""


def test_file_py(file):
    return file

cdef test_file_c(file):
    return u'file' + file


def range(arg):
    return u'range' + arg

cdef type(arg):
    return u'type' + arg


def test_c(arg):
    print test_file_c(arg)
    print type(arg)
