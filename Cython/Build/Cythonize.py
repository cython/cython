#!/usr/bin/env python

import os
import sys
import glob

from distutils.core import setup
from Cython.Build import cythonize
from Cython.Utils import find_root_package_dir, is_package_dir
from Cython.Compiler import Options

try:
    import multiprocessing
    parallel_compiles = int(multiprocessing.cpu_count() * 1.5)
except ImportError:
    multiprocessing = None
    parallel_compiles = 0


class _FakePool(object):
    def map_async(self, func, args):
        from itertools import imap
        for _ in imap(func, args):
            pass

    def close(self): pass
    def terminate(self): pass
    def join(self): pass


def parse_directives(option, name, value, parser):
    dest = option.dest
    old_directives = dict(getattr(parser.values, dest,
                                  Options.directive_defaults))
    directives = Options.parse_directive_list(
        value, relaxed_bool=True, current_settings=old_directives)
    setattr(parser.values, dest, directives)


def parse_options(option, name, value, parser):
    dest = option.dest
    options = dict(getattr(parser.values, dest, {}))
    for opt in value.split(','):
        if '=' in opt:
            n, v = opt.split('=', 1)
            v = v.lower() not in ('false', 'f', '0', 'no')
        else:
            n, v = opt, True
        options[n] = v
    setattr(parser.values, dest, options)


def find_package_base(path):
    base_dir, package_path = os.path.split(path)
    while os.path.isfile(os.path.join(base_dir, '__init__.py')):
        base_dir, parent = os.path.split(base_dir)
        package_path = '%s/%s' % (parent, package_path)
    return base_dir, package_path


def cython_compile(path_pattern, options):
    pool = None
    try:
        for path in glob.iglob(path_pattern):
            path = os.path.abspath(path)
            if options.build_inplace:
                if is_package_dir(path):
                    base_dir = find_root_package_dir(path)
                else:
                    base_dir = path
            else:
                base_dir = None

            if os.path.isdir(path):
                # recursively compiling a package
                paths = [os.path.join(path, '**', '*.%s' % ext)
                         for ext in ('py', 'pyx')]
            else:
                # assume it's a file(-like thing)
                paths = [path]

            cwd = os.getcwd()
            try:
                if base_dir:
                    os.chdir(base_dir)
                ext_modules = cythonize(
                    paths,
                    nthreads=options.parallel,
                    exclude_failures=options.keep_going,
                    exclude=options.excludes,
                    compiler_directives=options.directives,
                    **options.options)
            finally:
                if base_dir:
                    os.chdir(cwd)

            if ext_modules and options.build:
                if len(ext_modules) > 1 and options.parallel:
                    if pool is None:
                        try:
                            pool = multiprocessing.Pool(options.parallel)
                        except OSError:
                            pool = _FakePool()
                    pool.map_async(run_distutils, [
                        (base_dir, [ext]) for ext in ext_modules])
                else:
                    run_distutils((base_dir, ext_modules))
    except:
        if pool is not None:
            pool.terminate()
        raise
    else:
        if pool is not None:
            pool.close()
    finally:
        if pool is not None:
            pool.join()


def run_distutils(args):
    base_dir, ext_modules = args
    sys.argv[1:] = ['build_ext', '-i']
    cwd = os.getcwd()
    try:
        if base_dir:
            os.chdir(base_dir)
        setup(ext_modules=ext_modules)
    finally:
        if base_dir:
            os.chdir(cwd)


def parse_args(args):
    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] [sources and packages]+')

    parser.add_option('-X', '--directive', metavar='NAME=VALUE,...', dest='directives',
                      action='callback', callback=parse_directives, default={},
                      help='set a compiler directive')
    parser.add_option('-s', '--option', metavar='NAME=VALUE', dest='options',
                      action='callback', callback=parse_options, default={},
                      help='set a cythonize option')

    parser.add_option('-x', '--exclude', metavar='PATTERN', dest='excludes',
                      action='append', default=[],
                      help='exclude certain file patterns from the compilation')

    parser.add_option('-b', '--build', dest='build', action='store_true',
                      help='build extension modules using distutils')
    parser.add_option('-i', '--inplace', dest='build_inplace', action='store_true',
                      help='build extension modules in place using distutils (implies -b)')
    parser.add_option('-j', '--parallel', dest='parallel', metavar='N',
                      type=int, default=parallel_compiles,
                      help=('run builds in N parallel jobs (default: %d)' %
                            parallel_compiles or 1))

    parser.add_option('--lenient', dest='lenient', action='store_true',
                      help='increase Python compatibility by ignoring some compile time errors')
    parser.add_option('-k', '--keep-going', dest='keep_going', action='store_true',
                      help='compile as much as possible, ignore compilation failures')

    options, args = parser.parse_args(args)
    if not args:
        parser.error("no source files provided")
    if options.build_inplace:
        options.build = True
    if multiprocessing is None:
        options.parallel = 0
    return options, args


def main(args=None):
    options, paths = parse_args(args)

    if options.lenient:
        # increase Python compatibility by ignoring compile time errors
        Options.error_on_unknown_names = False
        Options.error_on_uninitialized = False

    for path in paths:
        cython_compile(path, options)


if __name__ == '__main__':
    main()
