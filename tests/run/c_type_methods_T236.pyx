# ticket: t236


def float_is_integer(float f):
    """
    >>> float_is_integer(1.0)
    True
    >>> float_is_integer(1.1)
    False
    """
    return f.is_integer()

def int_bit_length(int i):
    """
    >>> int_bit_length(1) == (1).bit_length()
    True
    >>> int_bit_length(1234) == (1234).bit_length()
    True
    """
    return i.bit_length()


def float__add__(float f):
    """
    >>> float__add__(5.0)
    7.0
    """
    return f.__add__(2)


def float_const__add__(float f):
    """
    >>> float_const__add__(5.0)
    7.0
    """
    return 2. .__add__(f)


def int__add__(int i):
    """
    >>> int__add__(5)
    7
    """
    return i.__add__(2)


def int_const__add__(int i):
    """
    >>> int_const__add__(5)
    7
    """
    return 2 .__add__(i)
