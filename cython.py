#!/usr/bin/env python

#
#   Cython -- Main Program, generic
#

if __name__ == '__main__':

    import os
    import sys

    try:
        # Make sure we import the right Cython
        cythonpath, _ = os.path.split(os.path.realpath(__file__))
        sys.path.insert(0, cythonpath)
    except NameError:
        # In pdb in python 2.4, __file__ is not defined...
        pass

    from Cython.Compiler.Main import main
    main(command_line = 1)

else:
    # Void cython.* directives.
    from Cython.Shadow import *
