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
