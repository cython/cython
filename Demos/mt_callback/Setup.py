from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
  name = 'mt_callback',
  ext_modules=cythonize([
    Extension("mt_cheeses", ["mt_cheeses.pyx", "mt_cheesefinder.c"],
               libraries=["pthread"] )
    ]),
)
