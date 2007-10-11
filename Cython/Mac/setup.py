#
#   Setup file for compiling _Filemodule_patched.c
#

from distutils.core import setup
from distutils.extension import Extension

setup(
    ext_modules = [
        Extension("_File", ["_Filemodule_patched.c"])
    ]
)
