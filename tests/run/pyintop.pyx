# mode: run


def bigint(x):
    # avoid 'L' postfix in Py2.x
    print(str(x).rstrip('L'))


def or_obj(obj2, obj3):
    """
    >>> or_obj(2, 3)
    3
    """
    obj1 = obj2 | obj3
    return obj1


def or_int(obj2):
    """
    >>> or_int(1)
    17
    >>> or_int(16)
    16
    """
    obj1 = obj2 | 0x10
    return obj1


def xor_obj(obj2, obj3):
    """
    >>> xor_obj(2, 3)
    1
    """
    obj1 = obj2 ^ obj3
    return obj1


def xor_int(obj2):
    """
    >>> xor_int(2)
    18
    >>> xor_int(16)
    0
    """
    obj1 = obj2 ^ 0x10
    return obj1


def and_obj(obj2, obj3):
    """
    >>> and_obj(2, 3)
    2
    """
    obj1 = obj2 & obj3
    return obj1


def and_int(obj2):
    """
    >>> and_int(1)
    0
    >>> and_int(18)
    16
    """
    obj1 = obj2 & 0x10
    return obj1


def lshift_obj(obj2, obj3):
    """
    >>> lshift_obj(2, 3)
    16
    """
    obj1 = obj2 << obj3
    return obj1


def rshift_obj(obj2, obj3):
    """
    >>> rshift_obj(2, 3)
    0
    """
    obj1 = obj2 >> obj3
    return obj1


def rshift_int(obj2):
    """
    >>> rshift_int(2)
    0

    >>> rshift_int(27)
    3
    >>> (-27) >> 3
    -4
    >>> rshift_int(-27)
    -4

    >>> rshift_int(32)
    4
    >>> (-32) >> 3
    -4
    >>> rshift_int(-32)
    -4

    >>> (2**28) >> 3
    33554432
    >>> rshift_int(2**28)
    33554432
    >>> (-2**28) >> 3
    -33554432
    >>> rshift_int(-2**28)
    -33554432

    >>> (2**30) >> 3
    134217728
    >>> rshift_int(2**30)
    134217728
    >>> rshift_int(-2**30)
    -134217728

    >>> bigint((2**60) >> 3)
    144115188075855872
    >>> bigint(rshift_int(2**60))
    144115188075855872
    >>> bigint(rshift_int(-2**60))
    -144115188075855872
    """
    obj1 = obj2 >> 3
    return obj1


def mixed_obj(obj2, obj3):
    """
    >>> mixed_obj(2, 3)
    16
    """
    obj1 = obj2 << obj3 | obj2 >> obj3
    return obj1


def mixed_int(obj2):
    """
    >>> mixed_int(2)
    18
    >>> mixed_int(16)
    0
    >>> mixed_int(17)
    1
    """
    obj1 = (obj2 ^ 0x10) | (obj2 & 0x01)
    return obj1
