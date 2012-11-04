"""
Highly experimental script that compiles the CPython standard library using Cython.

Execute the script either in the CPython 'Lib' directory or pass the
option '--current-python' to compile the standard library of the running
Python interpreter.

Pass '--parallel' to get a parallel build.

Usage example::

    $ python cystdlib.py --current-python build_ext -i
"""

import sys
from distutils.core import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

# improve Python compatibility by allowing some broken code
Options.error_on_unknown_names = False

excludes = ['**/test/**/*.py', '**/tests/**/*.py', '**/__init__.py']
broken = [
    'idlelib/MultiCall.py',
    'email/utils.py',
    'multiprocessing/reduction.py',
    'multiprocessing/util.py',
    'threading.py',      # interrupt handling
]

default_directives = dict(
    auto_cpdef=True,
    set_initial_path='SOURCEFILE')

special_directives = [
    (['pkgutil.py',
      'datetime.py',
      'optparse.py',
      'sndhdr.py',
      'opcode.py',
      'ntpath.py',
      'urllib/request.py',
      'plat-linux/TYPES.py',
      'tkinter/_fix.py',
      'lib2to3/refactor.py'
     ], dict(auto_cpdef=False)),
]

#del special_directives[:]

def build_extensions(includes='**/*.py',
                     excludes=excludes+broken,
                     special_directives=special_directives,
                     parallel=None):
    if isinstance(includes, str):
        includes = [includes]

    all_groups = (special_directives or []) + [(includes, {})]
    extensions = []
    for modules, directives in all_groups:
        exclude_now = excludes[:]
        for other_modules, _ in special_directives:
            if other_modules != modules:
                exclude_now.extend(other_modules)

        d = dict(default_directives)
        d.update(directives)

        extensions.extend(
            cythonize(modules,
                exclude=exclude_now,
                exclude_failures=True,
                language_level=pyver,
                compiler_directives=d,
                nthreads=parallel,
                ))
    return extensions

def build(extensions):
    try:
        setup(name = 'stuff', ext_modules = extensions)
        return extensions, True
    except:
        import traceback
        print('error building extensions %s' % (extensions,))
        traceback.print_exc()
        return extensions, False

def _build(args):
    sys_args, ext = args
    sys.argv[1:] = sys_args
    return build([ext])


if __name__ == '__main__':
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
        print("Building in %d parallel processes" % parallel_compiles)
    except (ValueError, ImportError):
        parallel_compiles = None

    extensions = build_extensions(parallel=parallel_compiles)
    if parallel_compiles:
        pool = multiprocessing.Pool(parallel_compiles)
        sys_args = sys.argv[1:]
        results = pool.map(_build, [ (sys_args, ext) for ext in extensions ])
        pool.close()
        pool.join()
        for ext, result in results:
            if not result:
                print("building extension %s failed" % (ext[0].name,))
    else:
        build(extensions)
