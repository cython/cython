from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib
import os, os.path
import sys
from Cython.Compiler.Version import version

compiler_dir = os.path.join(get_python_lib(prefix=''), 'Cython/Compiler')
if sys.platform == "win32":
    compiler_dir = compiler_dir[len(sys.prefix)+1:]

setup_args = {}

if sys.version_info < (2,4):
    import glob
    cython_dir = os.path.join(get_python_lib(prefix=''), 'Cython')
    compiler_dir = os.path.join(cython_dir, 'Compiler')
    setup_args['data_files'] = [
        (compiler_dir, ['Cython/Compiler/Lexicon.pickle']),
        (cython_dir, [ f for pattern in
                       ['Cython/Includes/*.pxd',
                        'Cython/Plex/*.pxd',
                        'Cython/Compiler/*.pxd',
                        'Cython/Runtime/*.pyx']
                       for f in glob.glob(pattern) ])]
else:
    setup_args['package_data'] = {'Cython.Compiler' : ['Lexicon.pickle'],
                                  'Cython' : ['Includes/*.pxd',
                                              'Plex/*.pxd',
                                              'Compiler/*.pxd',
                                              'Runtime/*.pyx']}

if os.name == "posix":
    scripts = ["bin/cython"]
else:
    scripts = ["cython.py"]

try:
    sys.argv.remove("--no-cython-compile")
except ValueError:
    try:
        from distutils.command.build_ext import build_ext as build_ext_orig
        class build_ext(build_ext_orig):
            def build_extension(self, ext, *args, **kargs):
                try:
                    build_ext_orig.build_extension(self, ext, *args, **kargs)
                except StandardError:
                    print("Compilation of '%s' failed" % ext.sources[0])
        from Cython.Compiler.Main import compile
        source_root = os.path.dirname(__file__)
        compiled_modules = ["Cython.Plex.Scanners",
                            "Cython.Compiler.Scanning",
                            "Cython.Compiler.Parsing",
                            "Cython.Compiler.Visitor",
                            "Cython.Runtime.refnanny"]
        extensions = []
        for module in compiled_modules:
            source_file = os.path.join(source_root, *module.split('.'))
            if os.path.exists(source_file + ".py"):
                source_file = source_file + ".py"
            else:
                source_file = source_file + ".pyx"
            print("Compiling module %s ..." % module)
            result = compile(source_file)
            if result.c_file:
                extensions.append(
                    Extension(module, sources = [result.c_file])
                    )
            else:
                print("Compilation failed")
        if extensions:
            setup_args['ext_modules'] = extensions
            setup_args['cmdclass'] = {"build_ext" : build_ext}
    except Exception:
        print("ERROR: %s" % sys.exc_info()[1])
        print("Extension module compilation failed, using plain Python implementation")


setup(
  name = 'Cython',
  version = version,
  url = 'http://www.cython.org',
  author = 'Greg Ewing, Robert Bradshaw, Stefan Behnel, Dag Seljebotn, et al.',
  author_email = 'cython-dev@codespeak.net',
  description = "The Cython compiler for writing C extensions for the Python language.",
  long_description = """\
  The Cython language makes writing C extensions for the Python language as
  easy as Python itself.  Cython is a source code translator based on the
  well-known Pyrex_, but supports more cutting edge functionality and
  optimizations.

  The Cython language is very close to the Python language (and most Python
  code is also valid Cython code), but Cython additionally supports calling C
  functions and declaring C types on variables and class attributes. This
  allows the compiler to generate very efficient C code from Cython code.

  This makes Cython the ideal language for writing glue code for external C
  libraries, and for fast C modules that speed up the execution of Python
  code.

  .. _Pyrex: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/
  """,
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: C",
    "Programming Language :: Cython",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],

  scripts = scripts,
  packages=[
    'Cython',
    'Cython.Compiler',
    'Cython.Runtime',
    'Cython.Distutils',
    'Cython.Mac',
    'Cython.Unix',
    'Cython.Plex',

    'Cython.Tests',
    'Cython.Compiler.Tests',
    ],

  # pyximport
  py_modules = ["pyximport/__init__",
                "pyximport/pyximport",
                "pyximport/pyxbuild",

                "cython"],

  **setup_args
  )
