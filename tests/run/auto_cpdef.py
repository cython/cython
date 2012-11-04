# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef

import cython

def str(arg):
    """
    This is a bit evil - str gets mapped to a C-API function and is
    being redefined here.

    >>> print(str('TEST'))
    STR
    """
    return 'STR'

@cython.test_assert_path_exists('//SimpleCallNode[@function.type.is_cfunction = True]')
@cython.test_fail_if_path_exists('//SimpleCallNode[@function.type.is_builtin_type = True]')
def call_str(arg):
    """
    >>> print(call_str('TEST'))
    STR
    """
    return str(arg)


def stararg_func(*args):
    """
    >>> stararg_func(1, 2)
    (1, 2)
    """
    return args

def starstararg_func(**kwargs):
    """
    >>> starstararg_func(a=1)
    1
    """
    return kwargs['a']

l = lambda x: 1

def test_lambda():
    """
    >>> l(1)
    1
    """
