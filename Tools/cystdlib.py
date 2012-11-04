from distutils.core import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

import sys
pyver = sys.version_info[0]
try:
    sys.argv.remove('--current-python')
except ValueError:
    pass
else:
    # assume that the stdlib is where the "os" module lives
    import os
    os.chdir(os.path.dirname(os.__file__))

try:
    sys.argv.remove('--parallel')
    import multiprocessing
    parallel_compiles = multiprocessing.cpu_count() * 2
except (ValueError, ImportError):
    parallel_compiles = None

# improve Python compatibility by allowing some broken code
Options.error_on_unknown_names = False

excludes = ['**/test/**/*.py', '**/tests/**/*.py', '**/__init__.py']

default_directives = dict(auto_cpdef=True)

setup(
  name = 'stuff',
  ext_modules = cythonize(["**/*.py"],
                          exclude=excludes,
                          exclude_failures=True,
                          language_level=pyver,
#                          compiler_directives=dict(auto_cpdef=True),
                          nthreads=parallel_compiles,
                          ),
)
