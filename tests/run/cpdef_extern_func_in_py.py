
"""
>>> pxd_sqrt(9)
3.0
"""

import cython

if not cython.compiled:
    from math import sqrt as pxd_sqrt


@cython.test_assert_path_exists('//SimpleCallNode/NameNode[@type.is_pyobject = False]')
def call_pxd_sqrt(x):
    """
    >>> call_pxd_sqrt(9)
    3.0
    """
    return pxd_sqrt(x)
