# cython: language_level=3
__name__='distutils.baregg' # fool Python we are in distutils
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
    >>> test_absolute()
    Traceback (most recent call last):
    ...
    ImportError: No module named debug
    """
    import debug
    return

__doc__ = """
>>> setup == core.setup
True
"""
