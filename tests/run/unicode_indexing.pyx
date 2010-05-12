
cimport cython

cdef unicode _ustring = u'azerty123456'

ustring = _ustring

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
def index(unicode ustring, Py_ssize_t i):
    """
    >>> index(ustring, 0)
    u'a'
    >>> index(ustring, 2)
    u'e'
    >>> index(ustring, -1)
    u'6'
    >>> index(ustring, -len(ustring))
    u'a'

    >>> index(ustring, len(ustring))
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return ustring[i]

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
def index_literal(Py_ssize_t i):
    """
    >>> index_literal(0)
    u'a'
    >>> index_literal(2)
    u'e'
    >>> index_literal(-1)
    u'6'
    >>> index_literal(-len('azerty123456'))
    u'a'

    >>> index_literal(len(ustring))
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return u'azerty123456'[i]

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
@cython.boundscheck(False)
def index_no_boundscheck(unicode ustring, Py_ssize_t i):
    """
    >>> index_no_boundscheck(ustring, 0)
    u'a'
    >>> index_no_boundscheck(ustring, 2)
    u'e'
    >>> index_no_boundscheck(ustring, -1)
    u'6'
    >>> index_no_boundscheck(ustring, len(ustring)-1)
    u'6'
    >>> index_no_boundscheck(ustring, -len(ustring))
    u'a'
    """
    return ustring[i]

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
@cython.boundscheck(False)
def unsigned_index_no_boundscheck(unicode ustring, unsigned int i):
    """
    >>> unsigned_index_no_boundscheck(ustring, 0)
    u'a'
    >>> unsigned_index_no_boundscheck(ustring, 2)
    u'e'
    >>> unsigned_index_no_boundscheck(ustring, len(ustring)-1)
    u'6'
    """
    return ustring[i]

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode",
                                "//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
def index_compare(unicode ustring, Py_ssize_t i):
    """
    >>> index_compare(ustring, 0)
    True
    >>> index_compare(ustring, 1)
    False
    >>> index_compare(ustring, -1)
    False
    >>> index_compare(ustring, -len(ustring))
    True

    >>> index_compare(ustring, len(ustring))
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return ustring[i] == u'a'

@cython.test_assert_path_exists("//CoerceToPyTypeNode",
                                "//IndexNode",
                                "//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//IndexNode//CoerceToPyTypeNode")
def index_compare_string(unicode ustring, Py_ssize_t i, unicode other):
    """
    >>> index_compare_string(ustring, 0, ustring[0])
    True
    >>> index_compare_string(ustring, 0, ustring[:4])
    False
    >>> index_compare_string(ustring, 1, ustring[0])
    False
    >>> index_compare_string(ustring, 1, ustring[1])
    True
    >>> index_compare_string(ustring, -1, ustring[0])
    False
    >>> index_compare_string(ustring, -1, ustring[-1])
    True
    >>> index_compare_string(ustring, -len(ustring), ustring[-len(ustring)])
    True

    >>> index_compare_string(ustring, len(ustring), ustring)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return ustring[i] == other
