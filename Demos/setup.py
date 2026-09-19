# Run as:
#    python setup.py build_ext --inplace

import os
import sys
import sysconfig

sys.path.insert(0, "..")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize(
    "**/*.pyx", exclude=["numpy_*.pyx", "callback/*.pyx", "libraries/*.pyx"]
)

# Compile a mix of custom c code and cython .pyx
ext_def = [Extension("*", sources=["callback/*.pyx", "callback/cheesefinder.c"])]
ext_modules.extend(cythonize(ext_def))

# Only compile the following if numpy is installed.
try:
    from numpy import get_include
except ImportError:
    pass
else:
    ext_def = [Extension("*", sources=["numpy_*.pyx"], include_dirs=get_include().split(os.path.pathsep))]
    ext_modules.extend(cythonize(ext_def))

# For demo purposes, we build our own tiny library.
libname_no_ext = "mymath"
libname = f"lib{libname_no_ext}.a"  # gcc is default
# referebce Python language native platform Python.h header include directory
py_include = sysconfig.get_path("include")
source_dir = "libraries"
c_sources = f"{source_dir}/mymath.c"  # space separated list of source files
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
        sources=[f"{source_dir}/*.pyx"],
        include_dirs=[os.path.join(os.getcwd(), source_dir)],  # path to .h file(s)
        library_dirs=[os.getcwd()],  # path to .a or .so file(s)
        libraries=[libname_no_ext],
    )
]
ext_modules.extend(cythonize(ext_def))

setup(
    name="Demos",
    ext_modules=ext_modules,
)
