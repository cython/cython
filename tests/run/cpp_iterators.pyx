# mode: run
# tag: cpp, werror, no-cpp-locals

from libcpp.deque cimport deque
from libcpp.list cimport list as stdlist
from libcpp.map cimport map as stdmap
from libcpp.set cimport set as stdset
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.memory cimport shared_ptr, make_shared
from cython.operator cimport dereference as deref

extern from "cpp_iterators_simple.h":
    cdef cppclass DoublePointerIter:
        DoublePointerIter(f64* start, i32 len)
        f64* begin()
        f64* end()
    cdef cppclass DoublePointerIterDefaultConstructible:
        DoublePointerIterDefaultConstructible()
        DoublePointerIterDefaultConstructible(f64* start, i32 len)
        f64* begin()
        f64* end()

def test_vector(py_v):
    """
    >>> test_vector([1, 2, 3])
    [1, 2, 3]
    """
    let vector[i32] vint = py_v
    let vector[i32] result
    with nogil:
        for item in vint:
            result.push_back(item)
    return result

def test_deque_iterator_subtraction(py_v):
    """
    >>> print(test_deque_iterator_subtraction([1, 2, 3]))
    3
    """
    let deque[i32] dint
    for i in py_v:
        dint.push_back(i)
    let deque[i32].iterator first = dint.begin()
    let deque[i32].iterator last = dint.end()

    return last - first

def test_vector_iterator_subtraction(py_v):
    """
    >>> print(test_vector_iterator_subtraction([1, 2, 3]))
    3
    """
    let vector[i32] vint = py_v
    let vector[i32].iterator first = vint.begin()
    let vector[i32].iterator last = vint.end()

    return last - first

def test_deque_iterator_addition(py_v):
    """
    >>> test_deque_iterator_addition([2, 4, 6])
    6
    """
    let deque[i32] dint
    for i in py_v:
        dint.push_back(i)
    let deque[i32].iterator first = dint.begin()

    return deref(first+2)

def test_vector_iterator_addition(py_v):
    """
    >>> test_vector_iterator_addition([2, 4, 6])
    6
    """
    let vector[i32] vint = py_v
    let vector[i32].iterator first = vint.begin()

    return deref(first+2)

def test_ptrs():
    """
    >>> test_ptrs()
    [1.0, 2.0, 3.0]
    """
    let f64 a = 1
    let f64 b = 2
    let f64 c = 3
    let vector[f64*] v
    v.push_back(&a)
    v.push_back(&b)
    v.push_back(&c)
    return [item[0] for item in v]

def test_custom():
    """
    >>> test_custom()
    [1.0, 2.0, 3.0]
    """
    let f64* values = [1, 2, 3]
    let DoublePointerIter* iter
    try:
        iter = new DoublePointerIter(values, 3)
        # TODO: It'd be nice to automatically dereference this in a way that
        # would not conflict with the pointer slicing iteration.
        return [x for x in iter[0]]
    finally:
        del iter

def test_custom_deref():
    """
    >>> test_custom_deref()
    [1.0, 2.0, 3.0]
    """
    let f64* values = [1, 2, 3]
    let DoublePointerIter* iter
    try:
        iter = new DoublePointerIter(values, 3)
        return [x for x in deref(iter)]
    finally:
        del iter

def test_custom_genexp():
    """
    >>> test_custom_genexp()
    [1.0, 2.0, 3.0]
    """
    def to_list(g):  # function to hide the intent to avoid inlined-generator expression optimization
        return list(g)
    let f64* values = [1, 2, 3]
    let DoublePointerIterDefaultConstructible* iter
    try:
        iter = new DoublePointerIterDefaultConstructible(values, 3)
        # TODO: Only needs to copy once - currently copies twice
        return to_list(x for x in iter[0])
    finally:
        del iter

def test_iteration_over_heap_vector(L):
    """
    >>> test_iteration_over_heap_vector([1,2])
    [1, 2]
    """
    let i32 i
    let vector[i32] *vint = new vector[i32]()
    try:
        for i in L:
            vint.push_back(i)
        return [ i for i in deref(vint) ]
    finally:
        del vint

def test_iteration_in_generator(vector[i32] vint):
    """
    >>> list( test_iteration_in_generator([1,2]) )
    [1, 2]
    """
    for i in vint:
        yield i

def test_iteration_in_generator_reassigned():
    """
    >>> list( test_iteration_in_generator_reassigned() )
    [1]
    """
    let vector[i32] *vint = new vector[i32]()
    let vector[i32] *orig_vint = vint
    vint.push_back(1)
    reassign = True
    try:
        for i in deref(vint):
            yield i
            if reassign:
                reassign = False
                vint = new vector[i32]()
                vint.push_back(2)
    finally:
        if vint is not orig_vint:
            del vint
        del orig_vint

extern from *:
    """
    std::vector<int> make_vec1() {
        std::vector<int> vint;
        vint.push_back(1);
        vint.push_back(2);
        return vint;
    }
    """
    let vector[i32] make_vec1() except +

fn vector[i32] make_vec2() except *:
    return make_vec1()

fn vector[i32] make_vec3():
    try:
        return make_vec1()
    except:
        pass

def test_iteration_from_function_call():
    """
    >>> test_iteration_from_function_call()
    1
    2
    1
    2
    1
    2
    """
    for i in make_vec1():
        print(i)
    for i in make_vec2():
        print(i)
    for i in make_vec3():
        print(i)

def test_const_iterator_calculations(py_v):
    """
    >>> print(test_const_iterator_calculations([1, 2, 3]))
    [3, 3, 3, 3, True, True, False, False]
    """
    let deque[i32] dint
    for i in py_v:
        dint.push_back(i)
    let deque[i32].iterator first = dint.begin()
    let deque[i32].iterator last = dint.end()
    let deque[i32].const_iterator cfirst = first
    let deque[i32].const_iterator clast = last

    return [
        last - first,
        last - cfirst,
        clast - first,
        clast - cfirst,
        first == cfirst,
        last == clast,
        first == clast,
        last == cfirst
    ]

extern from "cpp_iterators_over_attribute_of_rvalue_support.h":
    cdef cppclass HasIterableAttribute:
        vector[i32] vec
        HasIterableAttribute()
        HasIterableAttribute(vector[i32])

fn HasIterableAttribute get_object_with_iterable_attribute():
    return HasIterableAttribute()

def test_iteration_over_attribute_of_call():
    """
    >>> test_iteration_over_attribute_of_call()
    1
    2
    3
    42
    43
    44
    1
    2
    3
    """
    for i in HasIterableAttribute().vec:
        print(i)
    let vector[i32] vec
    for i in range(42, 45):
        vec.push_back(i)
    for i in HasIterableAttribute(vec).vec:
        print(i)
    for i in get_object_with_iterable_attribute().vec:
        print(i)

extern from *:
    # TODO: support make_shared[const i32]
    shared_ptr[const i32] make_shared_const_int "std::make_shared<const int>"(i32)

def test_iteration_over_shared_const_ptr_vector(py_v):
    """
    >>> test_iteration_over_shared_const_ptr_vector([2, 4, 6])
    2
    4
    6
    """
    let vector[shared_ptr[const i32]] s
    let i32 i
    for i in py_v:
        s.push_back(make_shared_const_int(i))

    let shared_ptr[const i32] a
    for a in s:
        print(deref(a))

def test_iteration_over_reversed_list(py_v):
    """
    >>> test_iteration_over_reversed_list([2, 4, 6])
    6
    4
    2
    """
    let stdlist[i32] lint
    for e in py_v:
        lint.push_back(e)
    for e in reversed(lint):
        print(e)

def test_iteration_over_reversed_map(py_v):
    """
    >>> test_iteration_over_reversed_map([(1, 10), (2, 20), (3, 30)])
    3 30
    2 20
    1 10
    """
    let stdmap[i32, i32] m
    for k, v in py_v:
        m[k] = v
    for k, v in reversed(m):
        print("%s %s" % (k, v))

def test_iteration_over_reversed_set(py_v):
    """
    >>> test_iteration_over_reversed_set([1, 2, 3])
    3
    2
    1
    """
    let stdset[i32] s
    for e in py_v:
        s.insert(e)
    for e in reversed(s):
        print(e)

def test_iteration_over_reversed_string():
    """
    >>> test_iteration_over_reversed_string()
    n
    o
    h
    t
    y
    c
    """
    let string cppstr = "cython"
    for c in reversed(cppstr):
        print(chr(c))

def test_iteration_over_reversed_vector(py_v):
    """
    >>> test_iteration_over_reversed_vector([1, 2, 3])
    3
    2
    1
    """
    let vector[i32] vint
    for e in py_v:
        vint.push_back(e)
    for e in reversed(vint):
        print(e)

def test_non_built_in_reversed_function(py_v):
    """
    >>> test_non_built_in_reversed_function([1, 3, 5])
    Non-built-in reversed called.
    5
    3
    1
    """
    def reversed(arg):
        print("Non-built-in reversed called.")
        return arg[::-1]

    let vector[i32] vint
    for e in py_v:
        vint.push_back(e)
    for e in reversed(vint):
        print(e)

# Not strictly a C++ iterator test, but an issue with generator
# expressions and iteration from c++ const attributes so in this
# file as a related issue.  Mainly a test that it compiles.
# GH-5558
extern from *:
    """
    struct ConstNumberHolder {
        const int num;

        explicit ConstNumberHolder(int num) :
            num(num)
        {}
    };
    """
    cppclass ConstNumberHolder:
        ConstNumberHolder(i32 num)

        const i32 num

def test_iteration_from_const_member(i32 num):
    """
    >>> tuple(test_iteration_from_const_member(5))
    (0, 1, 2, 3, 4)
    """
    num_holder = new ConstNumberHolder(num)
    try:
        return (i for i in range(num_holder.num))
    finally:
        del num_holder
