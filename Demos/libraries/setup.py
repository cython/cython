# Run as:
#    python setup.py build_ext --inplace

import os
import sys
import sysconfig

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


# For demo purposes, we build our own tiny library.
libname_no_ext = "mymath"
libname = f"lib{libname_no_ext}.a"  # gcc is default
# referebce Python language native platform Python.h header include directory
py_include = sysconfig.get_path("include")
c_sources = f"mymath.c"  # space separated list of source files
try:
    if not sys.platform.startswith("win"):
        print(f"building {libname}")
        assert (
            os.system(
                f"gcc -I\"{"\" -I\"".join(py_include.split(os.path.pathsep))}\" -shared -fPIC -c {c_sources} -o mymath.o"
            )
            == 0
        )
        assert os.system(f"ar rcs {libname} mymath.o") == 0
    elif sys.platform.startswith("win"):
        libname = f"{libname_no_ext}.lib"
        print(f"building {libname}")
        from distutils import ccompiler

        cc = ccompiler.new_compiler(os.name)
        cc.initialize()
        obj_list = cc.compile(sources=c_sources.split(), include_dirs=py_include.split(os.path.pathsep))
        cc.create_static_lib(
            objects=obj_list, output_libname=libname_no_ext, output_dir="."
        )
except Exception as ex:
    print(ex)
    print(f"Error building external library, please create {libname} manually")
    exit(1)

# define extension and use libraries parameter to pass a list of custom built / 3rd party libraries
ext_def = [
    Extension(
        "*",
        sources=["*.pyx"],
        include_dirs=[os.getcwd()],  # path to .h file(s)
        library_dirs=[os.getcwd()],  # path to .a or .so file(s)
        libraries=[libname_no_ext],
    )
]
ext_modules = cythonize(ext_def)

setup(
    name="Demos",
    ext_modules=ext_modules,
)
