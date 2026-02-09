# mode: run
# tag: bool, bint, builtin

def cast_to_bool(x):
    """
    >>> cast_to_bool(0)
    (0, 0)
    >>> cast_to_bool(1)
    (1, 1)
    >>> cast_to_bool(2)
    (1, 1)
    >>> cast_to_bool(-1)
    (1, 1)
    """
    cdef int int_x = x
    cdef signed char schar_x = x

    int_bool_int_x = <int> <bool> int_x
    int_bool_schar_x = <int> <bool> schar_x

    return (int_bool_int_x, int_bool_schar_x)


def cast_bint_to_char(x):
    """
    >>> cast_bint_to_char(0)
    0
    >>> cast_bint_to_char(1)
    1
    >>> cast_bint_to_char(2)
    1
    >>> cast_bint_to_char(256)
    1
    """
    return <char> <bint> x


def cast_bool_call_to_char(x):
    """
    >>> cast_bool_call_to_char(0)
    0
    >>> cast_bool_call_to_char(1)
    1
    >>> cast_bool_call_to_char(256)
    1
    """
    return <char> bool(x)


def call_arg_typing(x: bool):
    """
    >>> call_arg_typing(0)
    (False, 0, 0)
    >>> call_arg_typing(1)
    (True, 1, 1)
    >>> call_arg_typing(2)
    (True, 1, 1)
    >>> call_arg_typing(2000)
    (True, 1, 1)
    """
    return (x, <char> x, <int> x)
