# Run as:
#    python setup.py build_ext --inplace

import sys
sys.path.insert(0, "..")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize("**/*.pyx",
                            exclude=["numpy_*.pyx",
                                     "callback/*.pyx",
                                     "libraries/*.pyx"])

# Only compile the following if numpy is installed.
try:
    from numpy import get_include
except ImportError:
    pass
else:
    ext_def = [Extension("*",
                            sources=["callback/*.pyx",
                                     "callback/cheesefinder.c"]),
               Extension("*",
                            sources=["libraries/*.pyx",
                                     "libraries/mymath.c"]),
               Extension("*",
                            ["numpy_*.pyx"],
                            include_dirs=[get_include()])]
    ext_modules.extend(cythonize(ext_def))

setup(
    name = 'Demos',
    ext_modules = ext_modules,
)
