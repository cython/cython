#!/usr/bin/env python

from __future__ import absolute_import

import os
import shutil
import tempfile
from distutils.core import setup

from .Dependencies import cythonize, extended_iglob
from ..Utils import is_package_dir
from ..Compiler import Options

from ..Compiler.CmdLine import (
    create_cythonize_argparser, parse_args_raw, multiprocessing
)


class _FakePool(object):
    def map_async(self, func, args):
        try:
            from itertools import imap
        except ImportError:
            imap=map
        for _ in imap(func, args):
            pass

    def close(self):
        pass

    def terminate(self):
        pass

    def join(self):
        pass


def find_package_base(path):
    base_dir, package_path = os.path.split(path)
    while is_package_dir(base_dir):
        base_dir, parent = os.path.split(base_dir)
        package_path = '%s/%s' % (parent, package_path)
    return base_dir, package_path


def cython_compile(path_pattern, options):
    pool = None
    all_paths = map(os.path.abspath, extended_iglob(path_pattern))
    try:
        for path in all_paths:
            if options.build_inplace:
                base_dir = path
                while not os.path.isdir(base_dir) or is_package_dir(base_dir):
                    base_dir = os.path.dirname(base_dir)
            else:
                base_dir = None

            if os.path.isdir(path):
                # recursively compiling a package
                paths = [os.path.join(path, '**', '*.{py,pyx}')]
            else:
                # assume it's a file(-like thing)
                paths = [path]

            ext_modules = cythonize(
                paths,
                nthreads=options.parallel,
                exclude_failures=options.keep_going,
                exclude=options.excludes,
                force=options.force,
                quiet=options.quiet,
                **options.options)

            if ext_modules and options.build:
                if len(ext_modules) > 1 and options.parallel > 1:
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
            pool.join()


def run_distutils(args):
    base_dir, ext_modules = args
    script_args = ['build_ext', '-i']
    cwd = os.getcwd()
    temp_dir = None
    try:
        if base_dir:
            os.chdir(base_dir)
            temp_dir = tempfile.mkdtemp(dir=base_dir)
            script_args.extend(['--build-temp', temp_dir])
        setup(
            script_name='setup.py',
            script_args=script_args,
            ext_modules=ext_modules,
        )
    finally:
        if base_dir:
            os.chdir(cwd)
            if temp_dir and os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)


def parse_args(args):
    parser = create_cythonize_argparser()
    options, args = parse_args_raw(parser, args)

    if not args:
        parser.error("no source files provided")
    if multiprocessing is None:
        options.parallel = 0

    # handle global_options:
    from ..Compiler.CmdLine import GLOBAL_OPTIONS
    global_options = getattr(options, GLOBAL_OPTIONS, {})
    for name, value in global_options.items():
        if value is not None:
            setattr(Options, name, value)

    return options, args


def main(args=None):
    options, paths = parse_args(args)

    for path in paths:
        cython_compile(path, options)


if __name__ == '__main__':
    main()
