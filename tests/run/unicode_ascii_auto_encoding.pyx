#cython: c_string_type = unicode
#cython: c_string_encoding = ascii

auto_string_type = unicode

from libc.string cimport strcmp


def _as_string(x):
    try:
        return x.decode('latin1')
    except AttributeError:
        return x


def as_objects(char* ascii_data):
    """
    >>> x = as_objects('abc')
    >>> isinstance(x, auto_string_type) or type(x)
    True
    >>> _as_string(x) == 'abc' or repr(x)
    True
    """
    assert isinstance(<object>ascii_data, auto_string_type)
    assert isinstance(<bytes>ascii_data, bytes)
    assert isinstance(<str>ascii_data, str)
    assert isinstance(<unicode>ascii_data, unicode)
    return ascii_data


def charptr_as_bool(char *ascii_data):
    """
    >>> charptr_as_bool('abc')
    (True, True, True, True, True, True)
    >>> charptr_as_bool('')
    (True, False, False, False, False, False)
    """
    a = False
    if ascii_data:  # Tests the pointer, not the string.
        a = True

    b = bool(ascii_data)
    c = bool(<object> ascii_data)
    d = bool(<bytes> ascii_data)
    e = bool(<str> ascii_data)
    f = bool(<unicode> ascii_data)

    return (a, b, c, d, e, f)


def carray_as_bool(char *ascii_data):
    """
    >>> carray_as_bool('abc')
    (True, True, True, True, True)
    >>> carray_as_bool('')
    (False, False, False, False, False)
    """
    cdef char[4] array
    for i in range(4):
        array[i] = ascii_data[i]
        if not ascii_data[i]:
            break

    b = bool(array)
    c = bool(<object> array)
    d = bool(<bytes> array)
    e = bool(<str> array)
    f = bool(<unicode> array)

    return (b, c, d, e, f)


def from_object():
    """
    >>> from_object()
    """
    cdef bytes b = b"abc"
    cdef str s = "abc"
    cdef unicode u = u"abc"
    assert strcmp(<char*>b, "abc") == 0
    assert strcmp(<char*>s, "abc") == 0
    assert strcmp(<char*>u, "abc") == 0


def slice_as_objects(char* ascii_data, int start, int end):
    """
    >>> x = slice_as_objects('grok', 1, 3)
    >>> isinstance(x, auto_string_type) or type(x)
    True
    >>> _as_string(x) == 'ro' or repr(x)
    True
    """
    assert isinstance(<object>ascii_data[start:end], auto_string_type)
    assert isinstance(<bytes>ascii_data[start:end], bytes)
    assert isinstance(<str>ascii_data[start:end], str)
    assert isinstance(<unicode>ascii_data[start:end], unicode)

    assert isinstance(<object>ascii_data[start:], auto_string_type)
    assert isinstance(<bytes>ascii_data[start:], bytes)
    assert isinstance(<str>ascii_data[start:], str)
    assert isinstance(<unicode>ascii_data[start:], unicode)

    return ascii_data[start:end]
