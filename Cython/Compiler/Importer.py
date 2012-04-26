"""
Transparently import a module from the compiler on which the compiler
does not depend for its bootstrapping. This way one can write code
that is not supported in certain Python versions but which is supported
by Cython.
"""

import os
import sys
import imp

import pyximport

def importer(modulename, version=None):
    try:
        # Check for an already compiled module
        return __import__(modulename, None, None, [''])
    except ImportError:
        pass

    dirname = os.path.dirname
    root = dirname(dirname(dirname(os.path.abspath(__file__))))
    filename = os.path.join(root, *modulename.split('.')) + ".pyx"

    if version and version < sys.version_info[:2]:
        return pyximport.load_module(modulename, filename)
    else:
        mod = imp.new_module(modulename)
        exec open(filename).read() in mod.__dict__, mod.__dict__
        sys.modules[modulename] = mod
        return mod
