
cimport cython

############################################################
# tests for char* slicing

cdef char* cstring = "abcABCqtp"

def slice_charptr_end():
    """
    >>> print(str(slice_charptr_end()).replace("b'", "'"))
    ('a', 'abc', 'abcABCqtp')
    """
    return cstring[:1], cstring[:3], cstring[:9]

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

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//SliceIndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_py():
    """
    >>> slice_charptr_for_loop_py()
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    print str([ c for c in cstring[:3] ]).replace(" b'", " '").replace("[b'", "['")
    print str([ c for c in cstring[1:5] ]).replace(" b'", " '").replace("[b'", "['")
    print str([ c for c in cstring[4:9] ]).replace(" b'", " '").replace("[b'", "['")

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c():
    """
    >>> slice_charptr_for_loop_c()
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    cdef char c
    print [ chr(c) for c in cstring[:3] ]
    print [ chr(c) for c in cstring[1:5] ]
    print [ chr(c) for c in cstring[4:9] ]

## @cython.test_assert_path_exists("//ForFromStatNode",
##                                 "//ForFromStatNode//IndexNode")
## @cython.test_fail_if_path_exists("//ForInStatNode")
## def slice_charptr_for_loop_c_step():
##     """
##     >>> slice_charptr_for_loop_c()
##     ['c', 'b', 'a']
##     ['b', 'c', 'A', 'B']
##     ['p', 't', 'q', 'C', 'B']
##     """
##     cdef char c
##     print [ chr(c) for c in cstring[:3:-1] ]
##     print [ chr(c) for c in cstring[1:5:2] ]
##     print [ chr(c) for c in cstring[4:9:-1] ]

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_dynamic_bounds():
    """
    >>> slice_charptr_for_loop_c()
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    cdef char c
    print [ chr(c) for c in cstring[0:return3()] ]
    print [ chr(c) for c in cstring[return1():return5()] ]
    print [ chr(c) for c in cstring[return4():return9()] ]

cdef return1(): return 1
cdef return3(): return 3
cdef return4(): return 4
cdef return5(): return 5
cdef return9(): return 9

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//SliceIndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_py_enumerate():
    """
    >>> slice_charptr_for_loop_py_enumerate()
    [(0, 'a'), (1, 'b'), (2, 'c')]
    [(0, 'b'), (1, 'c'), (2, 'A'), (3, 'B')]
    [(0, 'B'), (1, 'C'), (2, 'q'), (3, 't'), (4, 'p')]
    """
    print str([ (i,c) for i,c in enumerate(cstring[:3]) ]).replace(" b'", " '")
    print str([ (i,c) for i,c in enumerate(cstring[1:5]) ]).replace(" b'", " '")
    print str([ (i,c) for i,c in enumerate(cstring[4:9]) ]).replace(" b'", " '")

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_enumerate():
    """
    >>> slice_charptr_for_loop_c_enumerate()
    [(0, 97), (1, 98), (2, 99)]
    [(0, 98), (1, 99), (2, 65), (3, 66)]
    [(0, 66), (1, 67), (2, 113), (3, 116), (4, 112)]
    """
    cdef int c,i
    print [ (i,c) for i,c in enumerate(cstring[:3]) ]
    print [ (i,c) for i,c in enumerate(cstring[1:5]) ]
    print [ (i,c) for i,c in enumerate(cstring[4:9]) ]


############################################################
# tests for int* slicing

## cdef int cints[6]
## for i in range(6):
##     cints[i] = i

## @cython.test_assert_path_exists("//ForFromStatNode",
##                                 "//ForFromStatNode//IndexNode")
## @cython.test_fail_if_path_exists("//ForInStatNode")
## def slice_intptr_for_loop_c():
##     """
##     >>> slice_intptr_for_loop_c()
##     [0, 1, 2]
##     [1, 2, 3, 4]
##     [4, 5]
##     """
##     cdef int i
##     print [ i for i in cints[:3] ]
##     print [ i for i in cints[1:5] ]
##     print [ i for i in cints[4:6] ]
