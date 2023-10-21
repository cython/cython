# tag: cpp, no-cpp-locals

import cython

cimport libcpp

# cimport libcpp.atomic
cimport libcpp.deque
cimport libcpp.list
cimport libcpp.map
cimport libcpp.pair
cimport libcpp.queue
cimport libcpp.set
cimport libcpp.stack
cimport libcpp.vector
cimport libcpp.complex
cimport libcpp.limits

# from libcpp.atomic cimport *
from libcpp.deque  cimport *
from libcpp.list   cimport *
from libcpp.map    cimport *
from libcpp.pair   cimport *
from libcpp.queue  cimport *
from libcpp.set    cimport *
from libcpp.stack  cimport *
from libcpp.vector cimport *
from libcpp.complex cimport *
from libcpp.limits cimport *

# cdef libcpp.atomic.atomc[i32]  a1 = atomic[i32]()
cdef libcpp.deque.deque[i32]    d1 = deque[i32]()
cdef libcpp.list.list[i32]      l1 = list[i32]()
cdef libcpp.map.map[i32, i32]   m1 = map[i32, i32]()
cdef libcpp.pair.pair[i32, i32] p1 = pair[i32, i32](1, 2)
cdef libcpp.queue.queue[i32]    q1 = queue[i32]()
cdef libcpp.set.set[i32]        s1 = set[i32]()
cdef libcpp.stack.stack[i32]    t1 = stack[i32]()
cdef libcpp.vector.vector[i32]  v1 = vector[i32]()

cdef deque[i32].iterator id1 = d1.begin()
cdef deque[i32].iterator id2 = d1.end()
cdef deque[i32].reverse_iterator rid1 = d1.rbegin()
cdef deque[i32].reverse_iterator rid2 = d1.rend()

cdef list[i32].iterator il1 = l1.begin()
cdef list[i32].iterator il2 = l1.end()
cdef list[i32].reverse_iterator ril1 = l1.rbegin()
cdef list[i32].reverse_iterator ril2 = l1.rend()

cdef map[i32, i32].iterator im1 = m1.begin()
cdef map[i32, i32].iterator im2 = m1.end()
cdef map[i32, i32].reverse_iterator rim1 = m1.rbegin()
cdef map[i32, i32].reverse_iterator rim2 = m1.rend()
cdef pair[map[i32, i32].iterator, bint] pimb = m1.insert(p1)

cdef set[i32].iterator is1 = s1.begin()
cdef set[i32].iterator is2 = s1.end()
cdef set[i32].reverse_iterator ris1 = s1.rbegin()
cdef set[i32].reverse_iterator ris2 = s1.rend()
cdef pair[set[i32].iterator, bint] pisb = s1.insert(4)

cdef vector[i32].iterator iv1 = v1.begin()
cdef vector[i32].iterator iv2 = v1.end()
cdef vector[i32].reverse_iterator riv1 = v1.rbegin()
cdef vector[i32].reverse_iterator riv2 = v1.rend()

def test_vector_coercion(*args):
    """
    >>> test_vector_coercion(1.75)
    [1.75]
    >>> test_vector_coercion(1, 10, 100)
    [1.0, 10.0, 100.0]
    """
    v = new vector[f64]()
    for a in args:
        v.push_back(a)
    return [v[0][i] for i in range(v.size())]

def test_const_vector(*args):
    """
    >>> test_const_vector(1.75)
    [1.75]
    >>> test_const_vector(1, 10, 100)
    [1.0, 10.0, 100.0]
    """
    cdef vector[f64] v
    for a in args:
        v.push_back(a)
    return const_vector_to_list(v)

cdef const_vector_to_list(const vector[f64]& cv):
    cdef vector[f64].const_iterator iter = cv.const_begin()
    cdef lst = []
    while iter != cv.const_end():
        lst.append(cython.operator.dereference(iter))
        cython.operator.preincrement(iter)
    return lst

cdef f64 dmax = numeric_limits[f64].max()
cdef f64 dmin = numeric_limits[f64].min()
cdef f64 deps = numeric_limits[f64].epsilon()
cdef f64 dqnan = numeric_limits[f64].quiet_NaN()
cdef f64 dsnan = numeric_limits[f64].signaling_NaN()
cdef f64 dinf = numeric_limits[f64].infinity()

cdef i32 imax = numeric_limits[i32].max()
cdef i32 imin = numeric_limits[i32].min()
cdef i32 ieps = numeric_limits[i32].epsilon()
cdef i32 iqnan = numeric_limits[i32].quiet_NaN()
cdef i32 isnan = numeric_limits[i32].signaling_NaN()
cdef i32 iinf = numeric_limits[i32].infinity()

#API checks for containers with std::allocator declared
from libcpp.memory cimport allocator

cdef libcpp.vector.vector[i32, allocator[i32]] vec_alloc_int = libcpp.vector.vector[i32, allocator[i32]](10, 1)
assert vec_alloc_int.size() == 10

cdef libcpp.list.list[i32, allocator[i32]] list_alloc_int = libcpp.list.list[i32, allocator[i32]](10, 1)
assert list_alloc_int.size() == 10

##Something about the default params breaks the auto-conversion...
def convert_to_vector(I):
    """
    >>> convert_to_vector([1,2,3,4])
    """
    cdef vector[i32] x = I

def complex_operators():
    """
    >>> complex_operators()
    [-1.0, 0.0, 0.0, 2.0, 0.0, 2.0]
    """
    cdef libcpp.complex.complex[f64] a = libcpp.complex.complex[f64](0.0, 1.0)
    cdef libcpp.complex.complex[f64] r1 = a*a
    cdef libcpp.complex.complex[f64] r2 = a*2.0
    cdef libcpp.complex.complex[f64] r3 = 2.0*a
    return [r1.real(), r1.imag(), r2.real(), r2.imag(), r3.real(), r3.imag()]

def pair_comparison():
    """
    >>> pair_comparison()
    [False, True, False, True, False]
    """
    cdef pair[f64, f64] p1 = pair[f64, f64](1.0, 2.0)
    cdef pair[f64, f64] p2 = pair[f64, f64](2.0, 2.0)
    return [p1==p2, p1==p1, p1>p2, p1<p2, p2>p2]
