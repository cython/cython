#cython: c_string_type = str
#cython: c_string_encoding = ascii

from libc.string cimport strcmp

def as_objects(char* ascii_data):
    """
    >>> as_objects('abc')
    'abc'
    """
    assert isinstance(<object>ascii_data, str)
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
    >>> slice_as_objects('grok', 1, 3)
    'ro'
    """
    assert isinstance(<object>ascii_data[start:end], str)
    assert isinstance(<bytes>ascii_data[start:end], bytes)
    assert isinstance(<str>ascii_data[start:end], str)
    assert isinstance(<unicode>ascii_data[start:end], unicode)
    
    assert isinstance(<object>ascii_data[start:], str)
    assert isinstance(<bytes>ascii_data[start:], bytes)
    assert isinstance(<str>ascii_data[start:], str)
    assert isinstance(<unicode>ascii_data[start:], unicode)
    
    return ascii_data[start:end]
