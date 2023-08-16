# Run as:
#    python setup.py build_ext --inplace

import sys
sys.path.insert(0, "..")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize("**/*.pyx", exclude="numpy_*.pyx")

# Only compile the following if numpy is installed.
try:
    from numpy import get_include
except ImportError:
    pass
else:
    numpy_demo = [Extension("*",
                            ["numpy_*.pyx"],
                            include_dirs=get_include())]
    ext_modules.extend(cythonize(numpy_demo))

setup(
  name = 'Demos',
  ext_modules = ext_modules,
)
