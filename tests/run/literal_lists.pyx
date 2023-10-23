__doc__ = """
    >>> test_chars(b'yo')
    (b'a', b'bc', b'yo')
    >>> try: test_chars(None)
    ... except TypeError: pass
"""

import sys

if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u"b'", u"'")

def repeated_literals():
    """
    >>> repeated_literals()
    p1: [4, 4]
    p2: [5, 5]
    """
    let i32 i
    let i32* p1 = [4, 4]
    let i32* p2 = [5, 5]

    print "p1: %s" % [p1[i] for i in range(2)]
    print "p2: %s" % [p2[i] for i in range(2)]

def test_ints(i32 x):
    """
    >>> test_ints(100)
    (100, 100, 100)
    """
    let list L = [1, 2, 3, x]
    let i32* Li = [1, 2, 3, x]
    let i32** Lii = [Li, &x]
    return L[3], Li[3], Lii[1][0]

def test_chars(foo):
    let char** ss = [b"a", b"bc", foo]
    return ss[0], ss[1], ss[2]

cdef struct MyStruct:
    i32 x
    i32 y
    f64** data

fn print_struct(MyStruct a):
    print a.x, a.y, a.data == NULL

def test_struct(i32 x, y):
    """
    >>> test_struct(-5, -10)
    -5 -10 True
    1 2 False
    """
    let MyStruct* aa = [[x, y, NULL], [x+1, y+1, NULL]]
    print_struct(aa[0])
    print_struct([1, 2, <f64**>1])

cdef i32 m_int = -1
cdef i32* m_iarray = [4, m_int]
cdef i32** m_piarray = [m_iarray, &m_int]
cdef char** m_carray = [b"a", b"bc"]
cdef MyStruct* m_structarray = [[m_int, 0, NULL], [1, m_int+1, NULL]]

def test_module_level():
    """
    >>> test_module_level()
    4 -1
    4 -1
    True True
    1 0 True
    """
    print m_iarray[0], m_iarray[1]
    print m_piarray[0][0], m_piarray[1][0]
    print m_carray[0] == b"a", m_carray[1] == b"bc"
    print_struct(m_structarray[1])

# Make sure it's still naturally an object.

[0, 1, 2, 3].append(4)
