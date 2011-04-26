# cython: language_level=3
import sys
# fool Python we are in distutils
if sys.version_info >= (3,):
    __name__='distutils.cytest_relativeimport_T542'
else:
    __name__=b'distutils.cytest_relativeimport_T542'
from distutils import cmd, core, version

from .core import *
def test_relative():
    """
    >>> test_relative() == (cmd, core, 'distutils.version')
    True
    """
    from . import cmd, core
    from . import (version, core)
    from .version import __name__
    return cmd, core, __name__

def test_absolute():
    """
    >>> test_absolute()   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ImportError: No module named ...debug...
    """
    import debug
    return

__doc__ = """
>>> setup == core.setup
True
"""
