"""
Import hooks; when installed with the install() function, these hooks 
allow importing .pyx files as if they were Python modules.

If you want the hook installed every time you run Python
you can add it to your Python version by adding these lines to
sitecustomize.py (which you can create from scratch in site-packages 
if it doesn't exist there or somewhere else on your python path)::

    import pyximport
    pyximport.install()

For instance on the Mac with a non-system Python 2.3, you could create
sitecustomize.py with only those two lines at
/usr/local/lib/python2.3/site-packages/sitecustomize.py .

A custom distutils.core.Extension instance and setup() args
(Distribution) for for the build can be defined by a <modulename>.pyxbld
file like:

# examplemod.pyxbdl
def make_ext(modname, pyxfilename):
    from distutils.extension import Extension
    return Extension(name = modname,
                     sources=[pyxfilename, 'hello.c'],
                     include_dirs=['/myinclude'] )
def make_setup_args():
    return dict(script_args=["--compiler=mingw32"])

Extra dependencies can be defined by a <modulename>.pyxdep .
See README.

Since Cython 0.11, the :mod:`pyximport` module also has experimental
compilation support for normal Python modules.  This allows you to
automatically run Cython on every .pyx and .py module that Python
imports, including parts of the standard library and installed
packages.  Cython will still fail to compile a lot of Python modules,
in which case the import mechanism will fall back to loading the
Python source modules instead.  The .py import mechanism is installed
like this::

    pyximport.install(pyimport = True)

Running this module as a top-level script will run a test and then print
the documentation.

This code is based on the Py2.3+ import protocol as described in PEP 302.
"""
from pyximport import *

# replicate docstring
from pyximport import __doc__
