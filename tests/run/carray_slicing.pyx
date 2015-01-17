
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

#### BROKEN: this test assumes that the result of a char* iteration
#### becomes a bytes object, which is not the case when applying
#### carray iteration.  Contradiction.
##
## @cython.test_assert_path_exists("//ForFromStatNode",
##                                 "//ForFromStatNode//SliceIndexNode")
## @cython.test_fail_if_path_exists("//ForInStatNode")
## def slice_charptr_for_loop_py():
##     """
##     >>> slice_charptr_for_loop_py()
##     ['a', 'b', 'c']
##     ['b', 'c', 'A', 'B']
##     ['B', 'C', 'q', 't', 'p']
##     """
##     print str([ c for c in cstring[:3] ]).replace(" b'", " '").replace("[b'", "['")
##     print str([ c for c in cstring[1:5] ]).replace(" b'", " '").replace("[b'", "['")
##     print str([ c for c in cstring[4:9] ]).replace(" b'", " '").replace("[b'", "['")

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c():
    """
    >>> slice_charptr_for_loop_c()
    ['a', 'b', 'c']
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    cdef char c
    print [ chr(c) for c in cstring[:3] ]
    print [ chr(c) for c in cstring[None:3] ]
    print [ chr(c) for c in cstring[1:5] ]
    print [ chr(c) for c in cstring[4:9] ]

#@cython.test_assert_path_exists("//ForFromStatNode",
#                                "//ForFromStatNode//IndexNode")
#@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_to_bytes():
    """
    >>> slice_charptr_for_loop_c_to_bytes()
    ['a', 'b', 'c']
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    cdef bytes b
    print str([ b for b in cstring[:3] ]).replace(" b'", " '").replace("[b'", "['")
    print str([ b for b in cstring[None:3] ]).replace(" b'", " '").replace("[b'", "['")
    print str([ b for b in cstring[1:5] ]).replace(" b'", " '").replace("[b'", "['")
    print str([ b for b in cstring[4:9] ]).replace(" b'", " '").replace("[b'", "['")

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_step():
    """
    >>> slice_charptr_for_loop_c_step()
    Acba ['A', 'c', 'b', 'a']
    Acba ['A', 'c', 'b', 'a']
    bA ['b', 'A']
    acB ['a', 'c', 'B']
    acB ['a', 'c', 'B']
     []
    ptqC ['p', 't', 'q', 'C']
    pq ['p', 'q']
    """
    cdef object ustring = cstring.decode('ASCII')
    cdef char c
    print ustring[3::-1],     [ chr(c) for c in cstring[3::-1] ]
    print ustring[3:None:-1], [ chr(c) for c in cstring[3:None:-1] ]
    print ustring[1:5:2],     [ chr(c) for c in cstring[1:5:2] ]
    print ustring[:5:2],      [ chr(c) for c in cstring[:5:2] ]
    print ustring[None:5:2],  [ chr(c) for c in cstring[None:5:2] ]
    print ustring[4:9:-1],    [ chr(c) for c in cstring[4:9:-1] ]
    print ustring[8:4:-1],    [ chr(c) for c in cstring[8:4:-1] ]
    print ustring[8:4:-2],    [ chr(c) for c in cstring[8:4:-2] ]

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_dynamic_bounds():
    """
    >>> slice_charptr_for_loop_c_dynamic_bounds()
    ['a', 'b', 'c']
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    cdef char c
    print [ chr(c) for c in cstring[0:return3()] ]
    print [ chr(c) for c in cstring[None:return3()] ]
    print [ chr(c) for c in cstring[return1():return5()] ]
    print [ chr(c) for c in cstring[return4():return9()] ]

cdef return1(): return 1
cdef return3(): return 3
cdef return4(): return 4
cdef return5(): return 5
cdef return9(): return 9

#### BROKEN: this test assumes that the result of a char* iteration
#### becomes a bytes object, which is not the case when applying
#### carray iteration.  Contradiction.
##
## @cython.test_assert_path_exists("//ForFromStatNode",
##                                 "//ForFromStatNode//SliceIndexNode")
## @cython.test_fail_if_path_exists("//ForInStatNode")
## def slice_charptr_for_loop_py_enumerate():
##     """
##     >>> slice_charptr_for_loop_py_enumerate()
##     [(0, 'a'), (1, 'b'), (2, 'c')]
##     [(0, 'b'), (1, 'c'), (2, 'A'), (3, 'B')]
##     [(0, 'B'), (1, 'C'), (2, 'q'), (3, 't'), (4, 'p')]
##     """
##     print str([ (i,c) for i,c in enumerate(cstring[:3]) ]).replace(" b'", " '")
##     print str([ (i,c) for i,c in enumerate(cstring[1:5]) ]).replace(" b'", " '")
##     print str([ (i,c) for i,c in enumerate(cstring[4:9]) ]).replace(" b'", " '")

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_charptr_for_loop_c_enumerate():
    """
    >>> slice_charptr_for_loop_c_enumerate()
    [(0, 97), (1, 98), (2, 99)]
    [(0, 97), (1, 98), (2, 99)]
    [(0, 98), (1, 99), (2, 65), (3, 66)]
    [(0, 66), (1, 67), (2, 113), (3, 116), (4, 112)]
    """
    cdef int c,i
    print [ (i,c) for i,c in enumerate(cstring[:3]) ]
    print [ (i,c) for i,c in enumerate(cstring[None:3]) ]
    print [ (i,c) for i,c in enumerate(cstring[1:5]) ]
    print [ (i,c) for i,c in enumerate(cstring[4:9]) ]


############################################################
# tests for int* slicing

cdef int[6] cints
for i in range(6):
    cints[i] = i

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_intarray_for_loop_c():
    """
    >>> slice_intarray_for_loop_c()
    [0, 1, 2]
    [0, 1, 2]
    [1, 2, 3, 4]
    [4, 5]
    """
    cdef int i
    print [ i for i in cints[:3] ]
    print [ i for i in cints[None:3] ]
    print [ i for i in cints[1:5] ]
    print [ i for i in cints[4:6] ]

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def iter_intarray_for_loop_c():
    """
    >>> iter_intarray_for_loop_c()
    [0, 1, 2, 3, 4, 5]
    """
    cdef int i
    print [ i for i in cints ]

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_intptr_for_loop_c():
    """
    >>> slice_intptr_for_loop_c()
    [0, 1, 2]
    [0, 1, 2]
    [1, 2, 3, 4]
    [4, 5]
    """
    cdef int* nums = cints
    cdef int i
    print [ i for i in nums[:3] ]
    print [ i for i in nums[None:3] ]
    print [ i for i in nums[1:5] ]
    print [ i for i in nums[4:6] ]


############################################################
# tests for slicing other arrays

cdef double[6] cdoubles
for i in range(6):
    cdoubles[i] = i + 0.5

cdef double* cdoubles_ptr = cdoubles

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def slice_doublptr_for_loop_c():
    """
    >>> slice_doublptr_for_loop_c()
    [0.5, 1.5, 2.5]
    [0.5, 1.5, 2.5]
    [1.5, 2.5, 3.5, 4.5]
    [4.5, 5.5]
    """
    cdef double d
    print [ d for d in cdoubles_ptr[:3] ]
    print [ d for d in cdoubles_ptr[None:3] ]
    print [ d for d in cdoubles_ptr[1:5] ]
    print [ d for d in cdoubles_ptr[4:6] ]

## @cython.test_assert_path_exists("//ForFromStatNode",
##                                 "//ForFromStatNode//IndexNode")
## @cython.test_fail_if_path_exists("//ForInStatNode")
## def slice_doublptr_for_loop_c_step():
##     """
##     >>> slice_doublptr_for_loop_c_step()
##     """
##     cdef double d
##     print [ d for d in cdoubles_ptr[:3:1] ]
##     print [ d for d in cdoubles_ptr[5:1:-1] ]
##     print [ d for d in cdoubles_ptr[:2:-2] ]
##     print [ d for d in cdoubles_ptr[4:6:2] ]
##     print [ d for d in cdoubles_ptr[4:6:-2] ]

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def iter_doublearray_for_loop_c():
    """
    >>> iter_doublearray_for_loop_c()
    [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    """
    cdef double d
    print [ d for d in cdoubles ]


cdef struct MyStruct:
    int i

@cython.test_assert_path_exists("//ForFromStatNode",
                                "//ForFromStatNode//IndexNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def struct_ptr_iter():
    """
    >>> struct_ptr_iter()
    ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    """
    cdef MyStruct[5] my_structs
    for i in range(5):
        my_structs[i].i = i
    cdef MyStruct value
    cdef MyStruct *ptr
    return ([ value.i for value in my_structs[:5] ],
            [ ptr.i for ptr in my_structs[:5] ],
            [ inferred.i for inferred in my_structs[:5] ])
