# mode: run

import cython


def check_int(s):
    """
    >>> check_int(5)
    True
    >>> check_int("Hello world!")
    False
    """
    return isinstance(s, cython.int)


# FIXME: broken, see #5521
# def check_str(s):
#     """
#     >>> check_str(5)
#     False
#     >>> check_str("Hello world!")
#     True
#     """
#     return isinstance(s, cython.str)
