# mode: run
# tag: cpp, werror, cpp17, cppexecpolicies, no-cpp-locals

from libcpp.numeric cimport reduce, exclusive_scan, inclusive_scan, 
                            transform_reduce, transform_exclusive_scan, 
                            transform_inclusive_scan
from libcpp.execution cimport seq
from libcpp.vector cimport vector

# Subtracts two integers.
cdef int subtract_integers(int lhs, int rhs):
    return lhs - rhs

# Adds two integers.
cdef int add_integers(int lhs, int rhs):
    return lhs + rhs

# Multiplies two integers.
cdef int multiply_integers(int lhs, int rhs):
    return lhs * rhs

# Multiplies a integer with 2
cdef int multiply_with_2(int val):
    return 2*val

def test_reduce(vector[int] v, int init):
    """
    Test reduce.
     0 + 1 = 1
     1 + 2 = 3
     3 + 3 = 6
    >>> test_reduce([1, 2, 3], 0)
    6
    """
    return reduce(v.begin(), v.end(), init)

def test_reduce_with_bin_op(vector[int] v, int init):
    """
    Test reduce with a binary operation (subtraction). 
     0 - 1 = -1
    -1 - 2 = -3
    -3 - 3 = -6
    >>> test_reduce_with_bin_op([1, 2, 3], 0)
    -6
    """
    return reduce(v.begin(), v.end(), init, subtract_integers)

def test_reduce_with_execpolicy(vector[int] v, int init):
    """
    Test reduce with execution policy. 
     0 + 1 = 1
     1 + 2 = 3
     3 + 3 = 6
    >>> test_reduce_with_execpolicy([1, 2, 3], 0)
    6
    """
    return reduce(seq, v.begin(), v.end(), init)

def test_reduce_with_bin_op_and_execpolicy(vector[int] v, int init):
    """
    Test reduce with execution policy and a binary operation (subtraction). 
     0 - 1 = -1
    -1 - 2 = -3
    -3 - 3 = -6
    >>> test_reduce_with_bin_op_and_execpolicy([1, 2, 3], 0)
    -6
    """
    return reduce(seq, v.begin(), v.end(), init, subtract_integers)

def test_transform_reduce(vector[int] v1, vector[int] v2, int init):
    """
    Test transform_reduce
    >>> test_transform_reduce([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(v1.begin(), v2.begin(), v1.end(), 0)

def test_transform_reduce_with_bin_red_op_and_bin_tran_op(vector[int] v1, vector[int] v2, int init):
    """
    Test transform_reduce with a binary reduce and transform operations
    >>> test_transform_reduce_with_bin_red_op_and_bin_tran_op([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(v1.begin(), v2.begin(), v1.end(), 0, add_integers, multiply_integers)

def test_transform_reduce_with_bin_op_and_unary_op(vector[int] v1, int init):
    """
    Test transform_reduce with a binary reduction and a unary transform operation
    >>> test_transform_reduce_with_bin_op_and_unary_op([1, 2, 3], 0)
    12
    """
    return transform_reduce(v1.begin(), v2.begin(), 0, add_integers, multiply_with_2)

def test_transform_reduce_with_execpolicy(vector[int] v1, vector[int] v2, int init):
    """
    Test transform_reduce with a execution policy
    >>> test_transform_reduce_with_execpolicy([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(seq, v1.begin(), v2.begin(), v1.end(), 0)

def test_transform_reduce_with_execpolicy_bin_red_op_and_bin_tran_op(vector[int] v1, vector[int] v2, int init):
    """
    Test transform_reduce with a execution policy and binary reduce and transform operations
    >>> test_transform_reduce_with_execpolicy_bin_red_op_and_bin_tran_op([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(seq, v1.begin(), v2.begin(), v1.end(), 0, add_integers, multiply_integers)

def test_transform_reduce_with_execpolicy_bin_op_and_unary_op(vector[int] v1, int init):
    """
    Test transform_reduce with a execution policy and binary reduction and a unary transform operation
    >>> test_transform_reduce_with_execpolicy_bin_op_and_unary_op([1, 2, 3], 0)
    12
    """
    return transform_reduce(seq, v1.begin(), v2.begin(), 0, add_integers, multiply_with_2)

def test_inclusive_scan(vector[int] v):
    """
    Test inclusive_scan
    >>> test_inclusive_scan([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(v.begin(), v.end(), out.begin())
    return out

def test_inclusive_scan_with_execpolicy(vector[int] v):
    """
    Test inclusive_scan with a execution policy
    >>> test_inclusive_scan_with_execpolicy([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(seq, v.begin(), v.end(), out.begin())
    return out

def test_inclusive_scan_with_bin_op(vector[int] v):
    """
    Test inclusive_scan with a binary operation
    >>> test_inclusive_scan_with_bin_op([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(v.begin(), v.end(), out.begin(), add_integers)
    return out

def test_inclusive_scan_with_execpolicy_and_bin_op(vector[int] v):
    """
    Test inclusive_scan with a execution policy and a binary operation
    >>> test_inclusive_scan_with_execpolicy_and_bin_op([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers)
    return out

def test_inclusive_scan_with_bin_op_and_init(vector[int] v, int init):
    """
    Test inclusive_scan with a binary operation and a initial value
    >>> test_inclusive_scan_with_bin_op_and_init([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(v.begin(), v.end(), out.begin(), add_integers, 0)
    return out

def test_inclusive_scan_with_execpolicy_bin_op_and_init(vector[int] v, int init):
    """
    Test inclusive_scan with a execution policy, a binary operation and a initial value
    >>> test_inclusive_scan_with_execpolicy_bin_op_and_init([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    cdef vector[int] out
    inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers, 0)
    return out










