from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os, sys
import sys
from Cython.Compiler.Version import version

compiler_dir = os.path.join(get_python_lib(prefix=''), 'Cython/Compiler')
if sys.platform == "win32":
    compiler_dir = compiler_dir[len(sys.prefix)+1:]

setup_args = {}

if sys.version_info < (2,4):
    compiler_dir = os.path.join(get_python_lib(prefix=''), 'Cython/Compiler')
    setup_args['data_files'] = [
        {compiler_dir : ['Cython/Compiler/Lexicon.pickle']}]
else:
    setup_args['package_data'] = {'Cython.Compiler' : ['Lexicon.pickle']}

if os.name == "posix":
    scripts = ["bin/cython"]
else:
    scripts = ["cython.py"]

setup(
  name = 'Cython', 
  version = version,
  url = 'http://www.cython.org',
  author = 'Greg Ewing, William Stein, Robert Bradshaw, Stefan Behnel, et al.',
  author_email = 'wstein@gmail.com',
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
    "License :: OSI Approved :: Python Software Foundation License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: C",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],

  scripts = scripts,
  packages=[
    'Cython',
    'Cython.Compiler',
    'Cython.Distutils',
    'Cython.Mac',
    'Cython.Plex'
    ],
  **setup_args
  )

