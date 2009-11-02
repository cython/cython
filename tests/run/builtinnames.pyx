def test_file_py(file):
    assert isinstance(file, (str, unicode)), \
        u"not a string, found '%s' instead" % file.__class__.__name__
    return file

cdef test_file_c(file):
    assert isinstance(file, (str, unicode)), \
        u"not a string, found '%s' instead" % file.__class__.__name__
    return u'file' + file


def range(arg):
    return u'range' + arg

cdef type(arg):
    return u'type' + arg


def test_c(arg):
    """
    >>> test_c('abc')
    fileabc
    typeabc
    >>> print(test_file_py('abc'))
    abc
    >>> print(range('abc'))
    rangeabc
    """
    print test_file_c(arg)
    print type(arg)
