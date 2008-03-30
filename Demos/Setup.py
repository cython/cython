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
    Extension("func_pointers", ["func_pointers.pyx"]),
#    Extension("inplace", ["inplace.pyx"]),
#    Extension("withGIL", ["withGIL.pyx"]),
    Extension("class_members", ["class_members.pyx"]),
#    Extension("inherit_bug", ["inherit_bug.pyx"]),
    Extension("override", ["override.pyx"]),
    Extension("cond", ["cond.pyx"]),
#    Extension("submodule.test",       ["submodule/test.pyx"]),
    Extension("errors",       ["errors.pyx"]),
    Extension("cpdef",       ["cpdef.pyx"]),
    Extension("range",       ["range.pyx"]),
    Extension("early_temps",       ["early_temps.pyx"]),
    Extension("ints",       ["ints.pyx"]),
    Extension("clear",       ["clear.pyx"]),
    Extension("detect_override",       ["detect_override.pyx"]),
    Extension("fixes",       ["fixes.pyx"]),
    ],
  cmdclass = {'build_ext': build_ext},
#  include_dirs = "/System/Library/Frameworks/Python.framework/Versions/2.3/include/python2.3/"
)
