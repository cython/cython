
def simple_values(obj1, obj2, obj3, obj4):
    """
    >>> simple_values(True, False, 23, 'test')
    (0.0, 1.0, False, False)
    """
    cdef int bool1, bool2
    cdef float bool3, bool4
    cdef char *ptr1, *ptr2, *ptr0
    cdef float f
    bool1 = 1
    bool2 = 0
    ptr1 = ptr2 = NULL
    f = 0.0

    bool3 = bool1 and bool2
    bool3 = bool1 or bool2
    bool3 = obj1 and obj2
    ptr0 = ptr1 and ptr2
    bool3 = bool1 and f
    bool4 = bool1 and bool2 and bool3
    bool4 = bool1 or bool2 and bool3
    obj4 = obj1 and obj2 and obj3
    obj5 = (obj1 + obj2 + obj3) and obj4
    return bool3, bool4, obj4, obj5


def non_simple_values(obj1, obj2, obj3, obj4):
    """
    >>> non_simple_values(1, 2, 3, 4)
    (7, 3, 7, 3, 7, 7, 5, 5)
    >>> non_simple_values(0, 0, 3, 4)
    (0, 7, 4, 4, 4, 4, 4, 4)
    >>> non_simple_values(0, 0, 1, -1)
    (0, 0, -1, 0, -1, -1, 0, 0)
    >>> non_simple_values(1, -1, 1, -1)
    (0, 0, 0, 0, 0, 0, 0, 0)
    >>> non_simple_values(1, 2, 1, -1)
    (0, 3, 0, 3, 0, 0, 1, 1)
    >>> non_simple_values(2, 1, 1, -1)
    (0, 3, 1, 3, 0, 0, 1, 1)
    """
    and1 = obj1 + obj2 and obj3 + obj4
    or1 = obj1 + obj2 or obj3 + obj4
    and_or = obj1 + obj2 and obj3 + obj4 or obj1 + obj4
    or_and = obj1 + obj2 or obj3 + obj4 and obj1 + obj4
    and_or_and = obj1 + obj2 and obj3 + obj4 or obj1 + obj4 and obj2 + obj4
    and1_or_and = (and1 or (obj1 + obj4 and obj2 + obj4))
    or_and_or = (obj1 + obj2 or obj3 + obj4) and (obj1 + obj4 or obj2 + obj4)
    or1_and_or = (or1 and (obj1 + obj4 or obj2 + obj4))
    return (and1, or1, and_or, or_and, and_or_and, and1_or_and, or_and_or, or1_and_or)


def nested_c_values_condexpr_GH7472(int i, int j, int k, bint c):
    """
    >>> nested_c_values_condexpr_GH7472(1, 0, 5, True)
    5
    >>> nested_c_values_condexpr_GH7472(1, 0, 0, True)
    0
    >>> nested_c_values_condexpr_GH7472(0, 3, 5, True)
    False
    >>> nested_c_values_condexpr_GH7472(1, 3, 5, False) is None
    True
    """
    # "j or k" is a C int and/or nested inside a Python object and/or.
    return (i > 0 and (j or k)) if c else None


def nested_pointers_bool_context(obj, bint use_null):
    """
    >>> nested_pointers_bool_context(0, False)
    (1, 0)
    >>> nested_pointers_bool_context(0, True)
    (0, 0)
    >>> nested_pointers_bool_context(1, True)
    (1, 0)
    >>> nested_pointers_bool_context(1, False)
    (1, 1)
    """
    # Nested pointer operands cannot become Python objects,
    # but they are fine when the whole expression is only tested for truth.
    cdef int value = 1
    cdef int *ptr1 = &value
    cdef int *ptr2 = NULL
    if use_null:
        ptr1 = NULL
    or_result = and_result = 0
    if obj or (ptr2 or ptr1):
        or_result = 1
    if obj and (ptr1 and ptr1[0]):
        and_result = 1
    return or_result, and_result


def nested_null_pointer_bool_context(obj, bint use_string):
    """
    >>> nested_null_pointer_bool_context(0, True)
    (1, 0)
    >>> nested_null_pointer_bool_context(0, False)
    (0, 0)
    >>> nested_null_pointer_bool_context(1, False)
    (1, 0)
    """
    # "s or NULL" spans to char*, but its NULL operand cannot become a Python object.
    cdef char *s = NULL
    if use_string:
        s = b"abc"
    or_result = and_result = 0
    if obj or (s or NULL):
        or_result = 1
    if obj and (s and NULL):
        and_result = 1
    return or_result, and_result


cdef enum _NestedMode:
    NESTED_OFF = 0
    NESTED_ON = 1


def nested_enum_in_float_context(double ratio, bint on, int count):
    """
    >>> nested_enum_in_float_context(0.5, True, 4)
    True
    >>> nested_enum_in_float_context(0.0, True, 0)
    False
    >>> nested_enum_in_float_context(0.0, False, 3)
    False
    >>> nested_enum_in_float_context(1.5, False, 0)
    True
    """
    # "mode and count" spans to a C int and the whole expression to a C double,
    # but the enum operand cannot be assigned to a double directly.
    cdef _NestedMode mode = NESTED_ON if on else NESTED_OFF
    if mode and count or ratio:
        return True
    return False
