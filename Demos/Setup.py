from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'Demos',
  ext_modules=[ 
    Extension("primes",       ["primes.pyx"]),
    Extension("spam",         ["spam.pyx"]),
#    Extension("numeric_demo", ["numeric_demo.pyx"]),
    Extension("test", ["test.pyx"]),
    ],
  cmdclass = {'build_ext': build_ext},
#  include_dirs = "/System/Library/Frameworks/Python.framework/Versions/2.3/include/python2.3/"
)
