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

# set up the PyxArgs global variable in pyximport (why is that a global :)
importers = pyximport.install(pyimport=True)
pyximport.uninstall(*importers)

def _import_normal(modulename):
    # __import__ does not take keyword arguments under 2.4
    return __import__(modulename, None, None, [''])

def _import_compile(modulename):
    if '.' in modulename:
        packagename, modulename = modulename.rsplit('.', 1)
        __path__ = _import_normal(packagename).__path__
    else:
        __path__ = None

    file, filename, description = imp.find_module(modulename, __path__)

    if file:
        file.close()
    else:
        raise ImportError(modulename)

    return pyximport.load_module(modulename, filename)

def importer(modulename, compile=False, version=None):
    """
    Import a module. If compile is true, always try to compile the .py file.
    Otherwise, try a regular import and if that fails (i.e. there is a
    syntax error, try to compile it.
    """
    if version is not None and sys.version_info[:2] >= version and not compile:
        return _import_normal(modulename)

    if compile:
        return _import_compile(modulename)
    else:
        try:
            return _import_normal(modulename)
        except SyntaxError:
            return _import_compile(modulename)

def importer(modulename):
    try:
        # Check for an already compiled module
        return __import__(modulename, None, None, [''])
    except ImportError:
        pass

    dirname = os.path.dirname
    root = dirname(dirname(dirname(os.path.abspath(__file__))))
    filename = os.path.join(root, *modulename.split('.')) + ".pyx"
    return pyximport.load_module(modulename, filename)