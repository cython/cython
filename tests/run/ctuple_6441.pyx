# mode: run

cimport cython

cdef int b = 0

cdef int has_side_effects() noexcept:
    global b

    b += 1
    return b

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_ctuple_var((int, int, int) a):
    return len(a)

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_ctuple_const():
    return len(<(int, int, int)>(<int>1, <int>2, <int>3))

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_ctuple_const_side_effects():
    return len(<(int, int, int)>(<int>1, <int>2, has_side_effects()))

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_tuple_const():
    return len((1, 2, str()))

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_tuple_const_side_effects():
    return len((1, 2, has_side_effects()))

@cython.test_fail_if_path_exists("//IntNode[@value='3']")
cdef int test_len_tuple_const_starred(list args):
    return len((1, 2, *args))

ctypedef fused ab:
    (int, int, int)
    (int, int, int, int)

@cython.test_assert_path_exists("//IntNode")
cdef int test_len_ctuple_var_fused(ab a):
    return len(a)

cdef int test_index_ctuple_var((int, int, int) a, int i):
    return a[i]

cdef int test_index_ctuple_var_py_index((int, int, int) a, i):
    return a[i]

cdef int test_index_ctuple_var_fused(ab a, int i):
    return a[i]

cdef int *test_index_ctuple_var_addrof((int, int, int) *a, int i):
    return &a[0][i]

cdef void test_index_ctuple_var_assign((int, int, int) *a, int i):
    a[0][i] = -1

cdef void test_index_ctuple_var_assign_fused(ab *a, int i):
    a[0][i] = -1

cdef int test_index_ctuple_var_const_index((int, int, int) a):
    return a[0]

cdef int test_index_ctuple_var_const_index_fused(ab a):
    return a[0]

cdef int test_index_ctuple_const(int i):
    return (<(int, int, int)>(<int>1, <int>2, <int>3))[i]

cdef int test_index_ctuple_const_const_index():
    return (<(int, int, int)>(<int>1, <int>2, <int>3))[0]

cdef int test_index_tuple_const(int i):
    return (1, 2, 3)[i]

cdef int test_index_tuple_const_const_index():
    return (1, 2, 3)[0]


cdef int pointer_read(int *ptr):
    return ptr[0]

cdef (int, int, int) a3 = (1, 2, 3)
cdef (int, int, int, int) a4 = (1, 2, 3, 4)

assert test_len_ctuple_var(a3) == 3

assert test_len_ctuple_const() == 3

assert test_len_ctuple_const_side_effects() == 3
assert b == 1

assert test_len_tuple_const() == 3

assert test_len_tuple_const_side_effects() == 3
assert b == 2

assert test_len_tuple_const_starred([3, 4, 5, 6]) == 6

assert test_len_ctuple_var_fused(a3) == 3
assert test_len_ctuple_var_fused(a4) == 4

assert test_index_ctuple_var(a3, 2) == 3

assert test_index_ctuple_var_py_index(a3, 2) == 3

assert test_index_ctuple_var_fused(a3, 2) == 3
assert test_index_ctuple_var_fused(a4, 3) == 4

assert pointer_read(test_index_ctuple_var_addrof(&a3, 2)) == 3

test_index_ctuple_var_assign(&a3, 2)
assert a3[2] == -1

test_index_ctuple_var_assign_fused(&a3, 2)
assert a3[2] == -1
test_index_ctuple_var_assign_fused(&a4, 3)
assert a4[3] == -1

assert test_index_ctuple_var_const_index(a3) == 1

assert test_index_ctuple_var_const_index_fused(a3) == 1
assert test_index_ctuple_var_const_index_fused(a4) == 1

assert test_index_ctuple_const(2) == 3

assert test_index_ctuple_const_const_index() == 1

assert test_index_tuple_const(2) == 3

assert test_index_tuple_const_const_index() == 1
