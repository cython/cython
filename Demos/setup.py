# Run as:
#    python setup.py build_ext --inplace

import os
import sys
import sysconfig
sys.path.insert(0, "..")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize("**/*.pyx",
                            exclude=["numpy_*.pyx",
                                     "callback/*.pyx",
                                     "libraries/*.pyx"])

# Compile a mix of custom c code and cython .pyx
ext_def = [Extension("*",
                sources=["callback/*.pyx",
                         "callback/cheesefinder.c"])]
ext_modules.extend(cythonize(ext_def))

# Only compile the following if numpy is installed.
try:
    from numpy import get_include
except ImportError:
    pass
else:
    ext_def = [Extension("*",
                    sources=["numpy_*.pyx"],
                    include_dirs=[get_include()])]
    ext_modules.extend(cythonize(ext_def))

# Compile and link custom library
try:
    if not sys.platform.startswith("win"):
        print("building libmymath.a")
        assert os.system(f"gcc -I{sysconfig.get_path("include")} -shared -fPIC -c libraries/mymath.c -o mymath.o") == 0
        assert os.system("ar rcs libmymath.a mymath.o") == 0
    elif sys.platform.startswith("win"):
        print(f"building mymath.lib")
        from distutils import ccompiler
        cc = ccompiler.new_compiler(os.name)
        cc.initialize()
        obj_list = cc.compile(sources = ["libraries/mymath.c"], include_dirs = [sysconfig.get_path("include")])
        cc.create_static_lib(objects = obj_list, output_libname = "mymath", output_dir = ".")
except Exception as ex:
    print(ex)
    print("Error building external library, please create libmymath.lib manually.")
    exit(1)

ext_def = [Extension("*",
                sources=["libraries/*.pyx"],
                include_dirs=[os.path.join(os.getcwd(), "libraries")],  # path to .h file(s)
                library_dirs=[os.getcwd()],  # path to .a or .so file(s)
                libraries=['mymath'])]
ext_modules.extend(cythonize(ext_def))

setup(
    name = 'Demos',
    ext_modules = ext_modules,
)
