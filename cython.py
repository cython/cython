#!/usr/bin/env python

#
#   Cython -- Main Program, generic
#

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if not TYPE_CHECKING and __name__ == '__main__':

    import os
    import sys

    # Make sure we import the right Cython
    cythonpath, _ = os.path.split(os.path.realpath(__file__))
    sys.path.insert(0, cythonpath)

    from Cython.Compiler.Main import main
    main(command_line = 1)

else:
    # Void cython.* directives.
    from Cython.Shadow import *
    # Dynamic importing in Python 3.7+
    from Cython.Shadow import __getattr__
    import functools
    __getattr__ = functools.partial(__getattr__, module='cython')
    del functools
    ## and bring in the __version__
    from Cython import __version__
    from Cython import load_ipython_extension
