import glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

try:
    from numpy.distutils.misc_util import get_numpy_include_dirs
    numpy_include_dirs = get_numpy_include_dirs()
except:
    numpy_include_dirs = []

ext_modules=[ 
    Extension("primes",       ["primes.pyx"]),
    Extension("spam",         ["spam.pyx"]),
]

for file in glob.glob("*.pyx"):
    if file != "numeric_demo.pyx":
        ext_modules.append(Extension(file[:-4], [file], include_dirs = numpy_include_dirs))

setup(
  name = 'Demos',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
