from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'callback',
  ext_modules=[ 
    Extension("cheese", ["cheese.pyx", "cheesefinder.c"]),
    ],
  cmdclass = {'build_ext': build_ext}
)
