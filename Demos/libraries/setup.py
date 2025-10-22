from __future__ import absolute_import, print_function

import os
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


# For demo purposes, we build our own tiny library.
try:
    if not sys.platform.startswith("win"):
        print("building libmymath.a")
        assert os.system("gcc -shared -fPIC -c mymath.c -o mymath.o") == 0
        assert os.system("ar rcs libmymath.a mymath.o") == 0
    else:
        print("this platform does not support gcc compiler, using cython to build module")
except:
    if not os.path.exists("libmymath.a"):
        print("Error building external library, please create libmymath.a manually.")
        sys.exit(1)

# Here is how to use the library built above.
if os.path.exists("libmymath.a"):
    ext_modules = cythonize([
        Extension("call_mymath",
                  sources=["call_mymath.pyx"],
                  include_dirs=[os.getcwd()],  # path to .h file(s)
                  library_dirs=[os.getcwd()],  # path to .a or .so file(s)
                  libraries=['mymath'])
    ])
else:
    ext_modules = cythonize([
        Extension("call_mymath",
                  sources=["call_mymath.pyx", "mymath.c"],
                  include_dirs=[os.getcwd()])  # path to .h file(s)
    ])
setup(
    name='Demos',
    ext_modules=ext_modules,
)
