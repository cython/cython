# mode: run
# tag: cpp, werror, cpp17, cppexecpolicies

from libcpp.numeric cimport (reduce, transform_reduce, inclusive_scan, 
                             exclusive_scan, transform_inclusive_scan, 
                             transform_exclusive_scan, gcd, lcm)
from libcpp.execution cimport seq
from libcpp.vector cimport vector

# Subtracts two integers.
fn i32 subtract_integers(i32 lhs, i32 rhs):
    return lhs - rhs

# Adds two integers.
fn i32 add_integers(i32 lhs, i32 rhs):
    return lhs + rhs

# Multiplies two integers.
fn i32 multiply_integers(i32 lhs, i32 rhs):
    return lhs * rhs

# Multiplies a integer with 2
fn i32 multiply_with_2(i32 val):
    return 2*val

def test_reduce(vector[i32] v, i32 init):
    """
    Test reduce.
     0 + 1 = 1
     1 + 2 = 3
     3 + 3 = 6
    >>> test_reduce([1, 2, 3], 0)
    6
    """
    return reduce(v.begin(), v.end(), init)

def test_reduce_with_bin_op(vector[i32] v, i32 init):
    """
    Test reduce with a binary operation (subtraction). 
     0 - 1 = -1
    -1 - 2 = -3
    -3 - 3 = -6
    >>> test_reduce_with_bin_op([1, 2, 3], 0)
    -6
    """
    return reduce(v.begin(), v.end(), init, subtract_integers)

# def test_reduce_with_execpolicy(vector[i32] v, i32 init):
#     """
#     Test reduce with execution policy. 
#      0 + 1 = 1
#      1 + 2 = 3
#      3 + 3 = 6
#     >>> test_reduce_with_execpolicy([1, 2, 3], 0)
#     6
#     """
#     return reduce(seq, v.begin(), v.end(), init)

def test_reduce_with_bin_op_and_execpolicy(vector[i32] v, i32 init):
    """
    Test reduce with execution policy and a binary operation (subtraction). 
     0 - 1 = -1
    -1 - 2 = -3
    -3 - 3 = -6
    >>> test_reduce_with_bin_op_and_execpolicy([1, 2, 3], 0)
    -6
    """
    return reduce(seq, v.begin(), v.end(), init, subtract_integers)

def test_transform_reduce(vector[i32] v1, vector[i32] v2, i32 init):
    """
    Test transform_reduce
    >>> test_transform_reduce([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(v1.begin(), v1.end(), v2.begin(), init)

def test_transform_reduce_with_bin_red_op_and_bin_tran_op(vector[i32] v1, vector[i32] v2, i32 init):
    """
    Test transform_reduce with a binary reduce and transform operations
    >>> test_transform_reduce_with_bin_red_op_and_bin_tran_op([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(v1.begin(), v1.end(), v2.begin(), init, add_integers, multiply_integers)

def test_transform_reduce_with_bin_op_and_unary_op(vector[i32] v1, vector[i32] v2, i32 init):
    """
    Test transform_reduce with a binary reduction and a unary transform operation
    >>> test_transform_reduce_with_bin_op_and_unary_op([1, 2, 3], [1, 2, 3], 0)
    12
    """
    return transform_reduce(v1.begin(), v1.end(), init, add_integers, multiply_with_2)

# def test_transform_reduce_with_execpolicy(vector[i32] v1, vector[i32] v2, i32 init):
#     """
#     Test transform_reduce with a execution policy
#     >>> test_transform_reduce_with_execpolicy([1, 2, 3], [1, 2, 3], 0)
#     14
#     """
#     return transform_reduce(seq, v1.begin(), v1.end(), v2.begin(), init)

def test_transform_reduce_with_execpolicy_bin_red_op_and_bin_tran_op(vector[i32] v1, vector[i32] v2, i32 init):
    """
    Test transform_reduce with a execution policy and binary reduce and transform operations
    >>> test_transform_reduce_with_execpolicy_bin_red_op_and_bin_tran_op([1, 2, 3], [1, 2, 3], 0)
    14
    """
    return transform_reduce(seq, v1.begin(), v1.end(), v2.begin(), init, add_integers, multiply_integers)

# def test_transform_reduce_with_execpolicy_bin_op_and_unary_op(vector[i32] v1, vector[i32] v2, i32 init):
#     """
#     Test transform_reduce with a execution policy and binary reduction and a unary transform operation
#     >>> test_transform_reduce_with_execpolicy_bin_op_and_unary_op([1, 2, 3], [1, 2, 3], 0)
#     12
#     """
#     return transform_reduce(seq, v1.begin(), v1.end(), v2.begin(), init, add_integers, multiply_with_2)

def test_inclusive_scan(vector[i32] v):
    """
    Test inclusive_scan
    >>> test_inclusive_scan([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    let vector[i32] out = vector[i32](v.size())
    inclusive_scan(v.begin(), v.end(), out.begin())
    return out

# def test_inclusive_scan_with_execpolicy(vector[i32] v):
#     """
#     Test inclusive_scan with a execution policy
#     >>> test_inclusive_scan_with_execpolicy([1, 2, 3, 4])
#     [1, 3, 6, 10]
#     """
#     cdef vector[i32] out
#     inclusive_scan(seq, v.begin(), v.end(), out.begin())
#     return out

def test_inclusive_scan_with_bin_op(vector[i32] v):
    """
    Test inclusive_scan with a binary operation
    >>> test_inclusive_scan_with_bin_op([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    let vector[i32] out = vector[i32](v.size())
    inclusive_scan(v.begin(), v.end(), out.begin(), add_integers)
    return out

# def test_inclusive_scan_with_execpolicy_and_bin_op(vector[i32] v):
#     """
#     Test inclusive_scan with a execution policy and a binary operation
#     >>> test_inclusive_scan_with_execpolicy_and_bin_op([1, 2, 3, 4])
#     [1, 3, 6, 10]
#     """
#     cdef vector[i32] out
#     inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers)
#     return out

def test_inclusive_scan_with_bin_op_and_init(vector[i32] v, i32 init):
    """
    Test inclusive_scan with a binary operation and a initial value
    >>> test_inclusive_scan_with_bin_op_and_init([1, 2, 3, 4], 0)
    [1, 3, 6, 10]
    """
    let vector[i32] out = vector[i32](v.size())
    inclusive_scan(v.begin(), v.end(), out.begin(), add_integers, init)
    return out

# def test_inclusive_scan_with_execpolicy_bin_op_and_init(vector[i32] v, i32 init):
#     """
#     Test inclusive_scan with a execution policy, a binary operation and a initial value
#     >>> test_inclusive_scan_with_execpolicy_bin_op_and_init([1, 2, 3, 4], 0)
#     [1, 3, 6, 10]
#     """
#     cdef vector[i32] out = vector[i32](v.size())
#     inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers, init)
#     return out

def test_transform_inclusive_scan(vector[i32] v):
    """
    Test transform inclusive_scan
    >>> test_transform_inclusive_scan([1, 2, 3, 4])
    [2, 6, 12, 20]
    """
    let vector[i32] out = vector[i32](v.size())
    transform_inclusive_scan(v.begin(), v.end(), out.begin(), add_integers, multiply_with_2)
    return out

# def test_transform_inclusive_scan_with_execpolicy(vector[i32] v):
#     """
#     Test transform inclusive_scan with a execution policy
#     >>> test_transform_inclusive_scan_with_execpolicy([1, 2, 3, 4])
#     [2, 6, 12, 20 ]
#     """
#     cdef vector[i32] out
#     transform_inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers, multiply_with_2)
#     return out

def test_transform_inclusive_scan_with_init(vector[i32] v, i32 init):
    """
    Test transform inclusive_scan with an initial value
    >>> test_transform_inclusive_scan_with_init([1, 2, 3, 4], 0)
    [2, 6, 12, 20]
    """
    let vector[i32] out = vector[i32](v.size())
    transform_inclusive_scan(v.begin(), v.end(), out.begin(), add_integers, multiply_with_2, init)
    return out

def test_transform_inclusive_scan_with_execpolicy_and_init(vector[i32] v, i32 init):
    """
    Test transform inclusive_scan with an initial value
    >>> test_transform_inclusive_scan_with_execpolicy_and_init([1, 2, 3, 4], 0)
    [2, 6, 12, 20]
    """
    let vector[i32] out = vector[i32](v.size())
    transform_inclusive_scan(seq, v.begin(), v.end(), out.begin(), add_integers, multiply_with_2, init)
    return out

def test_exclusive_scan(vector[i32] v, i32 init):
    """
    Test exclusive_scan
    >>> test_exclusive_scan([1, 2, 3, 4], 0)
    [0, 1, 3, 6]
    """
    let vector[i32] out = vector[i32](v.size())
    exclusive_scan(v.begin(), v.end(), out.begin(), init)
    return out

# def test_exclusive_scan_with_execpolicy(vector[i32] v, i32 init):
#     """
#     Test exclusive_scan with a execution policy
#     >>> test_exclusive_scan_with_execpolicy([1, 2, 3, 4], 0)
#     [0, 1, 3, 6]
#     """
#     cdef vector[i32] out
#     exclusive_scan(seq, v.begin(), v.end(), out.begin(), init)
#     return out

def test_exclusive_scan_with_bin_op(vector[i32] v, i32 init):
    """
    Test exclusive_scan with a binary operation
    >>> test_exclusive_scan_with_bin_op([1, 2, 3, 4], 0)
    [0, 1, 3, 6]
    """
    let vector[i32] out = vector[i32](v.size())
    exclusive_scan(v.begin(), v.end(), out.begin(), init, add_integers)
    return out

def test_exclusive_scan_with_execpolicy_and_bin_op(vector[i32] v, i32 init):
    """
    Test exclusive_scan with a execution policy and a binary operation
    >>> test_exclusive_scan_with_execpolicy_and_bin_op([1, 2, 3, 4], 0)
    [0, 1, 3, 6]
    """
    let vector[i32] out = vector[i32](v.size())
    exclusive_scan(seq, v.begin(), v.end(), out.begin(), init, add_integers)
    return out


def test_transform_exclusive_scan_with_execpolicy(vector[i32] v, i32 init):
    """
    Test transform_exclusive_scan
    >>> test_transform_exclusive_scan_with_execpolicy([1, 2, 3, 4], 0)
    [0, 2, 6, 12]
    """
    let vector[i32] out = vector[i32](v.size())
    transform_exclusive_scan(seq, v.begin(), v.end(), out.begin(), init, add_integers, multiply_with_2)
    return out

def test_transform_exclusive_scan_with_execpolicy(vector[i32] v, i32 init):
    """
    Test transform_exclusive_scan with a execution policy
    >>> test_transform_exclusive_scan_with_execpolicy([1, 2, 3, 4], 0)
    [0, 2, 6, 12]
    """
    let vector[i32] out = vector[i32](v.size())
    transform_exclusive_scan(seq, v.begin(), v.end(), out.begin(), init, add_integers, multiply_with_2)
    return out

def test_gcd(i32 a, i32 b):
    """
    Test gcd
    >>> test_gcd(12, 18)
    6
    """
    return gcd[int](a, b)

def test_lcm(i32 a, i32 b):
    """
    Test lcm
    >>> test_lcm(45, 75)
    225
    """
    return lcm[int](a, b)
