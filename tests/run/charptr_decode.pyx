
cimport cython

############################################################
# tests for char* slicing

cdef const char* cstring = "abcABCqtp"

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode():
    """
    >>> print(str(slice_charptr_decode()).replace("u'", "'"))
    ('a', 'abc', 'abcABCqtp')
    """
    return (cstring[:1].decode('UTF-8'),
            cstring[:3].decode('UTF-8'),
            cstring[:9].decode('UTF-8'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_platform_encoding():
    """
    >>> print(str(slice_charptr_decode()).replace("u'", "'"))
    ('a', 'abc', 'abcABCqtp')
    """
    cdef bytes s = u'abcABCqtp'.encode()
    cdef char* cstr = s
    return (cstr[:1].decode(),
            cstr[:3].decode(),
            cstr[:9].decode())

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_unknown_encoding():
    """
    >>> print(str(slice_charptr_decode_unknown_encoding()).replace("u'", "'"))
    ('abcABCqtp', 'abcABCqtp', 'abc', 'abcABCqt')
    """
    cdef const char* enc = 'UTF-8'
    cdef const char* error_handling = 'strict'
    return (cstring.decode(enc),
            cstring.decode(enc, error_handling),
            cstring[:3].decode(enc),
            cstring[:8].decode(enc, error_handling))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_slice2():
    """
    >>> print(str(slice_charptr_decode_slice2()).replace("u'", "'"))
    ('a', 'bc', 'tp')
    """
    return (cstring[0:1].decode('UTF-8'),
            cstring[1:3].decode('UTF-8'),
            cstring[7:9].decode('UTF-8'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_strlen():
    """
    >>> print(str(slice_charptr_decode_strlen()).replace("u'", "'"))
    ('abcABCqtp', 'bcABCqtp', '', 'BCq', 'abcA', '')
    """
    return (cstring.decode('UTF-8'),
            cstring[1:].decode('UTF-8'),
            cstring[9:].decode('UTF-8'),
            cstring[-5:-2].decode('UTF-8'),
            cstring[:-5].decode('UTF-8'),
            cstring[:-9].decode('UTF-8'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_unbound():
    """
    >>> print(str(slice_charptr_decode_unbound()).replace("u'", "'"))
    ('a', 'abc', 'abcABCqtp')
    """
    return (bytes.decode(cstring[:1], 'UTF-8'),
            bytes.decode(cstring[:3], 'UTF-8', 'replace'),
            bytes.decode(cstring[:9], 'UTF-8'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_decode_errormode():
    """
    >>> print(str(slice_charptr_decode_errormode()).replace("u'", "'"))
    ('a', 'abc', 'abcABCqtp')
    """
    return (cstring[:1].decode('UTF-8', 'strict'),
            cstring[:3].decode('UTF-8', 'replace'),
            cstring[:9].decode('UTF-8', 'unicode_escape'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_dynamic_bounds():
    """
    >>> print(str(slice_charptr_dynamic_bounds()).replace("u'", "'"))
    ('abc', 'abc', 'bcAB', 'BCqtp')
    """
    return (cstring[:return3()].decode('UTF-8'),
            cstring[0:return3()].decode('UTF-8'),
            cstring[return1():return5()].decode('UTF-8'),
            cstring[return4():return9()].decode('UTF-8'))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def slice_charptr_dynamic_bounds_non_name():
    """
    >>> print(str(slice_charptr_dynamic_bounds_non_name()).replace("u'", "'"))
    ('bcA', 'bcA', 'BCqtp', 'ABCqtp', 'bcABCqtp', 'bcABCqtp', 'cABC')
    """
    return ((cstring+1)[:return3()].decode('UTF-8'),
            (cstring+1)[0:return3()].decode('UTF-8'),
            (cstring+1)[return3():].decode('UTF-8'),
            (cstring+1)[2:].decode('UTF-8'),
            (cstring+1)[0:].decode('UTF-8'),
            (cstring+1)[:].decode('UTF-8'),
            (cstring+1)[return1():return5()].decode('UTF-8'))

cdef return1(): return 1
cdef return3(): return 3
cdef return4(): return 4
cdef return5(): return 5
cdef return9(): return 9
