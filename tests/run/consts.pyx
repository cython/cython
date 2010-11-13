import sys
IS_PY3 = sys.version_info[0] >= 3

cimport cython

DEF INT_VAL = 1

def _func(a,b,c):
    return a+b+c

@cython.test_fail_if_path_exists("//BinopNode")
def add():
    """
    >>> add() == 1+2+3+4
    True
    """
    return 1+2+3+4

@cython.test_fail_if_path_exists("//BinopNode")
def add_var(a):
    """
    >>> add_var(10) == 1+2+10+3+4
    True
    """
    return 1+2 +a+ 3+4

@cython.test_fail_if_path_exists("//BinopNode")
def neg():
    """
    >>> neg() == -1 -2 - (-3+4)
    True
    """
    return -1 -2 - (-3+4)

@cython.test_fail_if_path_exists("//BinopNode")
def long_int_mix():
    """
    >>> long_int_mix() == 1 + (2 * 3) // 2
    True
    >>> if IS_PY3: type(long_int_mix()) is int  or type(long_int_mix())
    ... else:      type(long_int_mix()) is long or type(long_int_mix())
    True
    """
    return 1L + (2 * 3L) // 2

@cython.test_fail_if_path_exists("//BinopNode")
def char_int_mix():
    """
    >>> char_int_mix() == 1 + (ord(' ') * 3) // 2 + ord('A')
    True
    """
    return 1L + (c' ' * 3L) // 2 + c'A'

@cython.test_fail_if_path_exists("//BinopNode")
def int_cast():
    """
    >>> int_cast() == 1 + 2 * 6000
    True
    """
    return <int>(1 + 2 * 6000)

@cython.test_fail_if_path_exists("//BinopNode")
def mul():
    """
    >>> mul() == 1*60*1000
    True
    """
    return 1*60*1000

@cython.test_fail_if_path_exists("//BinopNode")
def arithm():
    """
    >>> arithm() == 9*2+3*8//6-10
    True
    """
    return 9*2+3*8//6-10

@cython.test_fail_if_path_exists("//BinopNode")
def parameters():
    """
    >>> parameters() == _func(-1 -2, - (-3+4), 1*2*3)
    True
    """
    return _func(-1 -2, - (-3+4), 1*2*3)

@cython.test_fail_if_path_exists("//BinopNode")
def lists():
    """
    >>> lists() == [1,2,3] + [4,5,6]
    True
    """
    return [1,2,3] + [4,5,6]

@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def compile_time_DEF():
    """
    >>> compile_time_DEF()
    (1, False, True, True, False)
    """
    return INT_VAL, INT_VAL == 0, INT_VAL != 0, INT_VAL == 1, INT_VAL != 1

@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def cascaded_compare():
    """
    >>> cascaded_compare()
    True
    """
    return 1 < 2 < 3 < 4
