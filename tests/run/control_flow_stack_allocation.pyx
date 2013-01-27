# mode: run
# tag: werror, control-flow
# cython: warn.unused=True, warn.unused_arg=True, warn.unused_result=True

cdef struct S:
    int x
    float y


cdef stack_alloc_test(int[2] array_arg, S struct_arg):
    cdef int[2] array_var
    cdef S struct_var, struct_var_by_value

    for i in range(2):
        array_var[i] = array_arg[i]
    struct_var.x, struct_var.y = struct_arg.x, struct_arg.y
    struct_var_by_value = struct_var

    return [ i for i in array_var ], struct_var_by_value


def test():
    """
    >>> a,d = test()
    >>> a
    [0, 1]
    >>> sorted(d.items())
    [('x', 1), ('y', 2.0)]
    """
    cdef int[2] array_var
    cdef S struct_var
    for i in range(2):
        array_var[i] = i
    struct_var = [1, 2.0]

    return stack_alloc_test(array_var, struct_var)
