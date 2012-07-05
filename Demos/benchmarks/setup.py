from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'benchmarks',
  ext_modules = cythonize("*.py", language_level=3, annotate=True),
)
