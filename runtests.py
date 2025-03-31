#!/usr/bin/env python

import atexit
import base64
import doctest
import gc
import glob
import heapq
import locale
import math
import operator
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import unittest
import warnings
import zlib
from collections import defaultdict
from contextlib import contextmanager

try:
    import platform
    IS_PYPY = platform.python_implementation() == 'PyPy'
    IS_CPYTHON = platform.python_implementation() == 'CPython'
    IS_GRAAL = platform.python_implementation() == 'GraalVM'
except (ImportError, AttributeError):
    IS_CPYTHON = True
    IS_PYPY = False
    IS_GRAAL = False

CAN_SYMLINK = sys.platform != 'win32' and hasattr(os, 'symlink')

from io import open as io_open
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO  # doesn't accept 'str' in Py2

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import threading
except ImportError: # No threads, no problems
    threading = None

try:
    from unittest import SkipTest
except ImportError:
    class SkipTest(Exception):  # don't raise, only provided to allow except-ing it!
        pass
    def skip_test(reason):
        sys.stderr.write("Skipping test: %s\n" % reason)
else:
    def skip_test(reason):
        raise SkipTest(reason)

try:
    basestring
except NameError:
    basestring = str

WITH_CYTHON = True

try:
    # Py3.12+ doesn't have distutils any more and requires setuptools to provide it.
    import setuptools
except ImportError:
    pass

from distutils.command.build_ext import build_ext as _build_ext
from distutils import sysconfig
_to_clean = []

@atexit.register
def _cleanup_files():
    """
    This is only used on Cygwin to clean up shared libraries that are unsafe
    to delete while the test suite is running.
    """

    for filename in _to_clean:
        if os.path.isdir(filename):
            shutil.rmtree(filename, ignore_errors=True)
        else:
            try:
                os.remove(filename)
            except OSError:
                pass


def get_distutils_distro(_cache=[]):
    if _cache:
        return _cache[0]
    # late import to accommodate for setuptools override
    from distutils.dist import Distribution
    distutils_distro = Distribution()

    if sys.platform == 'win32':
        # TODO: Figure out why this hackery (see https://thread.gmane.org/gmane.comp.python.cython.devel/8280/).
        config_files = distutils_distro.find_config_files()
        try:
            config_files.remove('setup.cfg')
        except ValueError:
            pass
        distutils_distro.parse_config_files(config_files)

        cfgfiles = distutils_distro.find_config_files()
        try:
            cfgfiles.remove('setup.cfg')
        except ValueError:
            pass
        distutils_distro.parse_config_files(cfgfiles)
    _cache.append(distutils_distro)
    return distutils_distro


def import_refnanny():
    try:
        # try test copy first
        import refnanny
        return refnanny
    except ImportError:
        pass
    import Cython.Runtime.refnanny
    return Cython.Runtime.refnanny


EXT_DEP_MODULES = {
    'tag:numpy':     'numpy',
    'tag:pythran':  'pythran',
    'tag:setuptools':  'setuptools.sandbox',
    'tag:asyncio':  'asyncio',
    'tag:pstats':   'pstats',
    'tag:posix':    'posix',
    'tag:array':    'array',
    'tag:coverage': 'Cython.Coverage',
    'Coverage':     'Cython.Coverage',
    'tag:ipython':  'IPython.testing.globalipapp',
    'tag:jedi':     'jedi_BROKEN_AND_DISABLED',
    'tag:test.support': 'test.support',  # support module for CPython unit tests
}

def patch_inspect_isfunction():
    import inspect
    orig_isfunction = inspect.isfunction
    def isfunction(obj):
        return orig_isfunction(obj) or type(obj).__name__ == 'cython_function_or_method'
    isfunction._orig_isfunction = orig_isfunction
    inspect.isfunction = isfunction

def unpatch_inspect_isfunction():
    import inspect
    try:
        orig_isfunction = inspect.isfunction._orig_isfunction
    except AttributeError:
        pass
    else:
        inspect.isfunction = orig_isfunction

def def_to_cdef(source):
    '''
    Converts the module-level def methods into cdef methods, i.e.

        @decorator
        def foo([args]):
            """
            [tests]
            """
            [body]

    becomes

        def foo([args]):
            """
            [tests]
            """
            return foo_c([args])

        cdef foo_c([args]):
            [body]
    '''
    output = []
    skip = False
    def_node = re.compile(r'def (\w+)\(([^()*]*)\):').match
    lines = iter(source.split('\n'))
    for line in lines:
        if not line.strip():
            output.append(line)
            continue

        if skip:
            if line[0] != ' ':
                skip = False
            else:
                continue

        if line[0] == '@':
            skip = True
            continue

        m = def_node(line)
        if m:
            name = m.group(1)
            args = m.group(2)
            if args:
                args_no_types = ", ".join(arg.split()[-1] for arg in args.split(','))
            else:
                args_no_types = ""
            output.append("def %s(%s):" % (name, args_no_types))
            line = next(lines)
            if '"""' in line:
                has_docstring = True
                output.append(line)
                for line in lines:
                    output.append(line)
                    if '"""' in line:
                        break
            else:
                has_docstring = False
            output.append("    return %s_c(%s)" % (name, args_no_types))
            output.append('')
            output.append("cdef %s_c(%s):" % (name, args))
            if not has_docstring:
                output.append(line)

        else:
            output.append(line)

    return '\n'.join(output)


def exclude_test_in_pyver(*versions):
    return sys.version_info[:2] in versions


def exclude_test_on_platform(*platforms):
    return sys.platform in platforms


def update_linetrace_extension(ext):
    if sys.version_info[:2] == (3, 12):
        # Line tracing is generally fragile in Py3.12.
        return EXCLUDE_EXT
    if not IS_CPYTHON and sys.version_info[:2] < (3, 13):
        # Tracing/profiling requires PEP-669 monitoring or old CPython tracing.
        return EXCLUDE_EXT
    ext.define_macros.append(('CYTHON_TRACE', 1))
    return ext


def update_numpy_extension(ext, set_api17_macro=True):
    import numpy as np
    # Add paths for npyrandom and npymath libraries:
    lib_path = [
        os.path.abspath(os.path.join(np.get_include(), '..', '..', 'random', 'lib')),
        os.path.abspath(os.path.join(np.get_include(), '..', 'lib'))
    ]
    ext.library_dirs += lib_path
    if sys.platform == "win32":
        ext.libraries += ["npymath"]
    else:
        ext.libraries += ["npymath", "m"]
    ext.include_dirs.append(np.get_include())

    if set_api17_macro and getattr(np, '__version__', '') not in ('1.19.0', '1.19.1'):
        ext.define_macros.append(('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'))
    del np

def update_gdb_extension(ext, _has_gdb=[None]):
    # We should probably also check for Python support.
    if not include_debugger:
        _has_gdb[0] = False
    if _has_gdb[0] is None:
        try:
            subprocess.check_call(["gdb", "--version"])
        except (IOError, subprocess.CalledProcessError):
            _has_gdb[0] = False
        else:
            _has_gdb[0] = True
    if not _has_gdb[0]:
        return EXCLUDE_EXT
    return ext


def update_openmp_extension(ext):
    ext.openmp = True
    language = ext.language

    if sys.platform == 'win32' and sys.version_info[:2] == (3,4):
        # OpenMP tests fail in appveyor in Py3.4 -> just ignore them, EoL of Py3.4 is early 2019...
        return EXCLUDE_EXT

    if language == 'cpp':
        flags = OPENMP_CPP_COMPILER_FLAGS
    else:
        flags = OPENMP_C_COMPILER_FLAGS

    if flags:
        compile_flags, link_flags = flags
        ext.extra_compile_args.extend(compile_flags.split())
        ext.extra_link_args.extend(link_flags.split())
        return ext
    elif sys.platform == 'win32':
        return ext

    return EXCLUDE_EXT


def update_language_extension(language, std, min_gcc_version=None, min_clang_version=None, min_macos_version=None):
    def _update_language_extension(ext):
        # If the extension provides a -std=... option, and it's greater than the one
        # we're about to give, assume that whatever C compiler we use will probably be ok with it.
        extra_compile_args = []
        already_has_std = False
        if ext.extra_compile_args:
            std_regex = re.compile(r"-std(?!lib).*?(?P<number>[0-9]+)")
            for ca in ext.extra_compile_args:
                match = std_regex.search(ca)
                if match:
                    number = int(match.group("number"))
                    if number < std:
                        continue  # and drop the argument
                    already_has_std = True
                extra_compile_args.append(ca)
            ext.extra_compile_args = extra_compile_args

        use_gcc = use_clang = already_has_std

        # check for a usable gcc version
        gcc_version = get_gcc_version(ext.language)
        if gcc_version:
            if not already_has_std:
                compiler_version = gcc_version.group(1)
                if not min_gcc_version or float(compiler_version) >= float(min_gcc_version):
                    use_gcc = True
                    ext.extra_compile_args.append(f"-std={language}{std}")

            if use_gcc:
                return ext

        # check for a usable clang version
        clang_version = get_clang_version(ext.language)
        if clang_version:
            if not already_has_std:
                compiler_version = clang_version.group(1)
                if not min_clang_version or float(compiler_version) >= float(min_clang_version):
                    use_clang = True
                    ext.extra_compile_args.append(f"-std={language}{std}")
            if sys.platform == "darwin":
                if language == "c++":
                    ext.extra_compile_args.append("-stdlib=libc++")
                if min_macos_version is not None:
                    ext.extra_compile_args.append("-mmacosx-version-min=" + min_macos_version)

            if use_clang:
                return ext

        # no usable C compiler found => exclude the extension
        return EXCLUDE_EXT
    return _update_language_extension

def update_c_extension(c_std, min_gcc_version=None, min_clang_version=None, min_macos_version=None):
    return update_language_extension("c", c_std, min_gcc_version, min_clang_version, min_macos_version)

def update_cpp_extension(cpp_std, min_gcc_version=None, min_clang_version=None, min_macos_version=None):
    return update_language_extension("c++", cpp_std, min_gcc_version, min_clang_version, min_macos_version)


update_cpp11_extension = update_cpp_extension(11, min_gcc_version="4.9", min_macos_version="10.7")
update_cpp17_extension = update_cpp_extension(17, min_gcc_version="5.0", min_macos_version="10.13")
update_cpp20_extension = update_cpp_extension(20, min_gcc_version="11.0", min_clang_version="13.0", min_macos_version="10.13")
update_c11_extension = update_c_extension(11, min_gcc_version="4.7", min_clang_version="3.3")


def require_gcc(version):
    def check(ext):
        gcc_version = get_gcc_version(ext.language)
        if gcc_version:
            if float(gcc_version.group(1)) >= float(version):
                return ext
        return EXCLUDE_EXT
    return check

def get_cc_version(language):
    """
        finds gcc version using Popen
    """
    cc = ''
    if language == 'cpp':
        cc = os.environ.get('CXX') or sysconfig.get_config_var('CXX')
    if not cc:
        cc = os.environ.get('CC') or sysconfig.get_config_var('CC')
    if not cc:
        from distutils import ccompiler
        cc = ccompiler.get_default_compiler()
    if not cc:
        return ''

    # For some reason, cc can be e.g. 'gcc -pthread'
    cc = cc.split()[0]

    # Force english output
    env = os.environ.copy()
    env['LC_MESSAGES'] = 'C'
    try:
        p = subprocess.Popen([cc, "-v"], stderr=subprocess.PIPE, env=env)
    except EnvironmentError as exc:
        warnings.warn("Unable to find the %s compiler: %s: %s" %
                      (language, os.strerror(exc.errno), cc))
        return ''
    _, output = p.communicate()
    return output.decode(locale.getpreferredencoding() or 'ASCII', 'replace')


def get_gcc_version(language):
    matcher = re.compile(r"gcc version (\d+\.\d+)").search
    return matcher(get_cc_version(language))


def get_clang_version(language):
    matcher = re.compile(r"clang(?:-|\s+version\s+)(\d+\.\d+)").search
    return matcher(get_cc_version(language))


def get_openmp_compiler_flags(language):
    """
    As of gcc 4.2, it supports OpenMP 2.5. Gcc 4.4 implements 3.0. We don't
    (currently) check for other compilers.

    returns a two-tuple of (CFLAGS, LDFLAGS) to build the OpenMP extension
    """
    gcc_version = get_gcc_version(language)

    if not gcc_version:
        if sys.platform == 'win32':
            return '/openmp', ''
        else:
            return None # not gcc - FIXME: do something about other compilers

    # gcc defines "__int128_t", assume that at least all 64 bit architectures have it
    global COMPILER_HAS_INT128
    COMPILER_HAS_INT128 = getattr(sys, 'maxsize', getattr(sys, 'maxint', 0)) > 2**60

    compiler_version = gcc_version.group(1)
    if compiler_version:
        compiler_version = [int(num) for num in compiler_version.split('.')]
        if compiler_version >= [4, 2]:
            return '-fopenmp', '-fopenmp'

try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    pass

COMPILER = None
COMPILER_HAS_INT128 = False
OPENMP_C_COMPILER_FLAGS = get_openmp_compiler_flags('c')
OPENMP_CPP_COMPILER_FLAGS = get_openmp_compiler_flags('cpp')

# Return this from the EXT_EXTRAS matcher callback to exclude the extension
EXCLUDE_EXT = object()

EXT_EXTRAS = {
    'tag:numpy' : update_numpy_extension,
    'tag:openmp': update_openmp_extension,
    'tag:gdb': update_gdb_extension,
    'tag:cpp11': update_cpp11_extension,
    'tag:cpp17': update_cpp17_extension,
    'tag:cpp20': update_cpp20_extension,
    'tag:c11': update_c11_extension,
    'tag:trace' : update_linetrace_extension,
    'tag:cppexecpolicies': require_gcc("9.1"),
}

TAG_EXCLUDERS = sorted({
    'no-macos':  exclude_test_on_platform('darwin'),
    'pstats': exclude_test_in_pyver((3,12)),
    'trace': not IS_CPYTHON,
}.items())

# TODO: use tags
VER_DEP_MODULES = {
    # tests are excluded if 'CurrentPythonVersion OP VersionTuple', i.e.
    # (2,4) : (operator.lt, ...) excludes ... when PyVer < 2.4.x

    # FIXME: fix? delete?
    (3,4,999): (operator.gt, lambda x: x in ['run.initial_file_path',
                                             ]),

    (3,8): (operator.lt, lambda x: x in ['run.special_methods_T561_py38',
                                         ]),
    (3,12): (operator.ge, lambda x: x in [
        'run.py_unicode_strings',  # Py_UNICODE was removed
        'compile.pylong',  # PyLongObject changed its structure
        'run.longintrepr',  # PyLongObject changed its structure
        'run.line_trace',  # sys.monitoring broke sys.set_trace() line tracing
    ]),
}

INCLUDE_DIRS = [ d for d in os.getenv('INCLUDE', '').split(os.pathsep) if d ]
CFLAGS = os.getenv('CFLAGS', '').split()
CCACHE = os.getenv('CYTHON_RUNTESTS_CCACHE', '').split()
CDEFS = []
TEST_SUPPORT_DIR = 'testsupport'

BACKENDS = ['c', 'cpp']

UTF8_BOM_BYTES = r'\xef\xbb\xbf'.encode('ISO-8859-1').decode('unicode_escape')


def memoize(f):
    uncomputed = object()
    f._cache = {}
    get = f._cache.get
    def func(*args):
        res = get(args, uncomputed)
        if res is uncomputed:
            res = f._cache[args] = f(*args)
        return res
    return func


@memoize
def parse_tags(filepath):
    tags = defaultdict(list)
    parse_tag = re.compile(r'#\s*(\w+)\s*:(.*)$').match
    with io_open(filepath, encoding='ISO-8859-1', errors='ignore') as f:
        for line in f:
            if line[0] != '#':
                # ignore BOM-like bytes and whitespace
                line = line.lstrip(UTF8_BOM_BYTES).strip()
                if not line:
                    if tags:
                        break  # assume all tags are in one block
                    continue
                if line[0] != '#':
                    break
            parsed = parse_tag(line)
            if parsed is not None:
                tag, values = parsed.groups()
                if tag not in ('mode', 'tag', 'ticket', 'cython', 'distutils', 'preparse'):
                    if tag in ('coding', 'encoding'):
                        continue
                    if tag == 'tags':
                        raise RuntimeError("test tags use the 'tag' directive, not 'tags' (%s)" % filepath)
                    print("WARNING: unknown test directive '%s' found (%s)" % (tag, filepath))
                values = values.split(',')
                tags[tag].extend(filter(None, [value.strip() for value in values]))
            elif tags:
                break  # assume all tags are in one block
    return tags


list_unchanging_dir = memoize(lambda x: os.listdir(x))  # needs lambda to set function attribute


@memoize
def _list_pyregr_data_files(test_directory):
    is_data_file = re.compile('(?:[.](txt|pem|db|html)|^bad.*[.]py)$').search
    return ['__init__.py'] + [
        filename for filename in list_unchanging_dir(test_directory)
        if is_data_file(filename)]


def import_module_from_file(module_name, file_path, execute=True):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    m = importlib.util.module_from_spec(spec)
    if execute:
        sys.modules[module_name] = m
        spec.loader.exec_module(m)
    return m


def import_ext(module_name, file_path=None):
    if file_path:
        return import_module_from_file(module_name, file_path)
    else:
        try:
            from importlib import invalidate_caches
        except ImportError:
            pass
        else:
            invalidate_caches()
        return __import__(module_name, globals(), locals(), ['*'])


class build_ext(_build_ext):
    def build_extension(self, ext):
        try:
            try: # Py2.7+ & Py3.2+
                compiler_obj = self.compiler_obj
            except AttributeError:
                compiler_obj = self.compiler
            if ext.language == 'c++':
                compiler_obj.compiler_so.remove('-Wstrict-prototypes')
            if CCACHE:
                compiler_obj.compiler_so = CCACHE + compiler_obj.compiler_so
            if getattr(ext, 'openmp', None) and compiler_obj.compiler_type == 'msvc':
                ext.extra_compile_args.append('/openmp')
        except Exception:
            pass
        _build_ext.build_extension(self, ext)


class ErrorWriter(object):
    match_error = re.compile(
        r'(?:(warning|performance hint):)?(?:.*:)?\s*([-0-9]+)\s*:\s*([-0-9]+)\s*:\s*(.*)').match

    def __init__(self, encoding=None):
        self.output = []
        self.encoding = encoding

    def write(self, value):
        if self.encoding:
            value = value.encode('ISO-8859-1').decode(self.encoding)
        self.output.append(value)

    def _collect(self):
        s = ''.join(self.output)
        results = {'error': [], 'warning': [], 'performance hint': []}
        for line in s.splitlines():
            match = self.match_error(line)
            if match:
                message_type, line, column, message = match.groups()
                results[message_type or 'error'].append((int(line), int(column), message.strip()))

        return [
            ["%d:%d: %s" % values for values in sorted(results[key])]
            for key in ('error', 'warning', 'performance hint')
        ]

    def geterrors(self):
        return self._collect()[0]

    def getall(self):
        return self._collect()

    def close(self):
        pass  # ignore, only to match file-like interface


class Stats(object):
    def __init__(self, top_n=8):
        self.top_n = top_n
        self.test_counts = defaultdict(int)
        self.test_times = defaultdict(float)
        self.top_tests = defaultdict(list)

    def add_time(self, name, language, metric, t, count=1):
        self.test_counts[metric] += count
        self.test_times[metric] += t
        top = self.top_tests[metric]
        push = heapq.heappushpop if len(top) >= self.top_n else heapq.heappush
        # min-heap => pop smallest/shortest until longest times remain
        push(top, (t, name, language))

    @contextmanager
    def time(self, name, language, metric):
        t = time.time()
        yield
        t = time.time() - t
        self.add_time(name, language, metric, t)

    def update(self, stats):
        # type: (Stats) -> None
        for metric, t in stats.test_times.items():
            self.test_times[metric] += t
            self.test_counts[metric] += stats.test_counts[metric]
            top = self.top_tests[metric]
            for entry in stats.top_tests[metric]:
                push = heapq.heappushpop if len(top) >= self.top_n else heapq.heappush
                push(top, entry)

    def print_stats(self, out=sys.stderr):
        if not self.test_times:
            return
        lines = ['Times:\n']
        for metric, t in sorted(self.test_times.items(), key=operator.itemgetter(1), reverse=True):
            count = self.test_counts[metric]
            top = self.top_tests[metric]
            lines.append("%-12s: %8.2f sec  (%4d, %6.3f / run) - slowest: %s\n" % (
                metric, t, count, t / count,
                ', '.join("'{2}:{1}' ({0:.2f}s)".format(*item) for item in heapq.nlargest(self.top_n, top))))
        out.write(''.join(lines))


class TestBuilder(object):
    def __init__(self, rootdir, workdir, selectors, exclude_selectors, options,
                 with_pyregr, languages, test_bugs, language_level,
                 common_utility_dir, pythran_dir=None,
                 default_mode='run', stats=None,
                 add_embedded_test=False, add_cython_import=False,
                 add_cpp_locals_extra_tests=False):
        self.rootdir = rootdir
        self.workdir = workdir
        self.selectors = selectors
        self.exclude_selectors = exclude_selectors
        self.shard_num = options.shard_num
        self.annotate = options.annotate_source
        self.evaluate_tree_assertions = options.evaluate_tree_assertions
        self.cleanup_workdir = options.cleanup_workdir
        self.cleanup_sharedlibs = options.cleanup_sharedlibs
        self.cleanup_failures = options.cleanup_failures
        self.with_pyregr = with_pyregr
        self.cython_only = options.cython_only
        self.test_selector = re.compile(options.only_pattern).search if options.only_pattern else None
        self.languages = languages
        self.test_bugs = test_bugs
        self.fork = options.fork
        self.language_level = language_level
        self.test_determinism = options.test_determinism
        self.common_utility_dir = common_utility_dir
        self.pythran_dir = pythran_dir
        self.default_mode = default_mode
        self.stats = stats
        self.add_embedded_test = add_embedded_test
        self.add_cython_import = add_cython_import
        self.capture = options.capture
        self.add_cpp_locals_extra_tests = add_cpp_locals_extra_tests

    def build_suite(self):
        suite = unittest.TestSuite()
        filenames = os.listdir(self.rootdir)
        filenames.sort()
        # TODO: parallelise I/O with a thread pool for the different directories once we drop Py2 support
        for filename in filenames:
            path = os.path.join(self.rootdir, filename)
            if os.path.isdir(path) and filename != TEST_SUPPORT_DIR:
                if filename == 'pyregr' and not self.with_pyregr:
                    continue
                if filename == 'broken' and not self.test_bugs:
                    continue
                suite.addTest(
                    self.handle_directory(path, filename))
        if (sys.platform not in ['win32'] and self.add_embedded_test
                # the embedding test is currently broken in Py3.8+ and Py2.7, except on Linux.
                and ((3, 0) <= sys.version_info < (3, 8) or sys.platform != 'darwin')
                # broken on graal too
                and not IS_GRAAL):
            # Non-Windows makefile.
            if [1 for selector in self.selectors if selector("embedded")] \
                    and not [1 for selector in self.exclude_selectors if selector("embedded")]:
                suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EmbedTest))
        return suite

    def handle_directory(self, path, context):
        workdir = os.path.join(self.workdir, context)
        if not os.path.exists(workdir):
            os.makedirs(workdir)

        suite = unittest.TestSuite()
        filenames = list_unchanging_dir(path)
        filenames.sort()
        for filename in filenames:
            filepath = os.path.join(path, filename)
            module, ext = os.path.splitext(filename)
            if ext not in ('.py', '.pyx', '.srctree'):
                continue
            if filename.startswith('.'):
                continue # certain emacs backup files
            if context == 'pyregr':
                tags = defaultdict(list)
            else:
                tags = parse_tags(filepath)
            fqmodule = "%s.%s" % (context, module)
            if not [ 1 for match in self.selectors
                     if match(fqmodule, tags) ]:
                continue
            if self.exclude_selectors:
                if [1 for match in self.exclude_selectors
                        if match(fqmodule, tags)]:
                    continue

            mode = self.default_mode
            if tags['mode']:
                mode = tags['mode'][0]
            elif context == 'pyregr':
                mode = 'pyregr'

            if ext == '.srctree':
                if self.cython_only:
                    # EndToEnd tests always execute arbitrary build and test code
                    continue
                if skip_limited(tags):
                    continue
                if 'cpp' not in tags['tag'] or 'cpp' in self.languages:
                    suite.addTest(EndToEndTest(filepath, workdir,
                             self.cleanup_workdir, stats=self.stats,
                             capture=self.capture, shard_num=self.shard_num))
                continue

            # Choose the test suite.
            if mode == 'pyregr':
                if not filename.startswith('test_'):
                    continue
                test_class = CythonPyregrTestCase
            elif mode == 'run':
                if module.startswith("test_"):
                    test_class = CythonUnitTestCase
                else:
                    test_class = CythonRunTestCase
            elif mode in ['compile', 'error']:
                test_class = CythonCompileTestCase
            else:
                raise KeyError('Invalid test mode: ' + mode)

            for test in self.build_tests(test_class, path, workdir,
                                         module, filepath, mode == 'error', tags):
                suite.addTest(test)

            if mode == 'run' and ext == '.py' and not self.cython_only and not filename.startswith('test_'):
                # additionally test file in real Python
                min_py_ver = [
                    (int(pyver.group(1)), int(pyver.group(2)))
                    for pyver in map(re.compile(r'pure([0-9]+)[.]([0-9]+)').match, tags['tag'])
                    if pyver
                ]
                if not min_py_ver or any(sys.version_info >= min_ver for min_ver in min_py_ver):
                    suite.addTest(PureDoctestTestCase(
                        module, filepath, tags, stats=self.stats, shard_num=self.shard_num))

        return suite

    def build_tests(self, test_class, path, workdir, module, module_path, expect_errors, tags):
        warning_errors = 'werror' in tags['tag']
        expect_log = ("errors",) if expect_errors else ()
        if 'warnings' in tags['tag']:
            expect_log += ("warnings",)
        if "perf_hints" in tags['tag']:
            expect_log += ("perf_hints",)

        extra_directives_list = [{}]

        if expect_errors:
            if skip_c(tags) and 'cpp' in self.languages:
                languages = ['cpp']
            else:
                languages = self.languages[:1]
        else:
            languages = self.languages
            if (self.add_cpp_locals_extra_tests and 'cpp' in languages and
                    'cpp' in tags['tag'] and not 'no-cpp-locals' in tags['tag']):
                extra_directives_list.append({'cpp_locals': True})

        if 'c' in languages and skip_c(tags):
            languages = list(languages)
            languages.remove('c')
        if 'cpp' in languages and 'no-cpp' in tags['tag']:
            languages = list(languages)
            languages.remove('cpp')
        if not languages:
            return []
        if skip_limited(tags):
            return []

        language_levels = [2, 3] if 'all_language_levels' in tags['tag'] else [None]

        pythran_dir = self.pythran_dir
        if 'pythran' in tags['tag'] and not pythran_dir and 'cpp' in languages:
            import pythran.config
            try:
                pythran_ext = pythran.config.make_extension(python=True)
            except TypeError:  # old pythran version syntax
                pythran_ext = pythran.config.make_extension()
            pythran_dir = pythran_ext['include_dirs'][0]

        add_cython_import = self.add_cython_import and module_path.endswith('.py')

        preparse_list = tags.get('preparse', ['id'])
        tests = [ self.build_test(test_class, path, workdir, module, module_path,
                                  tags, language, language_level,
                                  expect_log,
                                  warning_errors, preparse,
                                  pythran_dir if language == "cpp" else None,
                                  add_cython_import=add_cython_import,
                                  extra_directives=extra_directives)
                  for language in languages
                  for preparse in preparse_list
                  for language_level in language_levels
                  for extra_directives in extra_directives_list
        ]
        return tests

    def build_test(self, test_class, path, workdir, module, module_path, tags, language, language_level,
                   expect_log, warning_errors, preparse, pythran_dir, add_cython_import,
                   extra_directives):
        language_workdir = os.path.join(workdir, language)
        if not os.path.exists(language_workdir):
            os.makedirs(language_workdir)
        workdir = os.path.join(language_workdir, module)
        if preparse != 'id':
            workdir += '_%s' % (preparse,)
        if language_level:
            workdir += '_cy%d' % (language_level,)
        if extra_directives:
            workdir += ('_directives_'+ '_'.join('%s_%s' % (k, v) for k,v in extra_directives.items()))
        return test_class(path, workdir, module, module_path, tags,
                          language=language,
                          preparse=preparse,
                          expect_log=expect_log,
                          annotate=self.annotate,
                          cleanup_workdir=self.cleanup_workdir,
                          cleanup_sharedlibs=self.cleanup_sharedlibs,
                          cleanup_failures=self.cleanup_failures,
                          cython_only=self.cython_only,
                          test_selector=self.test_selector,
                          shard_num=self.shard_num,
                          fork=self.fork,
                          language_level=language_level or self.language_level,
                          warning_errors=warning_errors,
                          evaluate_tree_assertions=self.evaluate_tree_assertions,
                          test_determinism=self.test_determinism,
                          common_utility_dir=self.common_utility_dir,
                          pythran_dir=pythran_dir,
                          stats=self.stats,
                          add_cython_import=add_cython_import,
                          extra_directives=extra_directives,
                          )


def skip_c(tags):
    if 'cpp' in tags['tag']:
        return True

    # We don't want to create a distutils key in the
    # dictionary so we check before looping.
    if 'distutils' in tags:
        for option in tags['distutils']:
            split = option.split('=')
            if len(split) == 2:
                argument, value = split
                if argument.strip() == 'language' and value.strip() == 'c++':
                    return True
    return False


def skip_limited(tags):
    if 'limited-api' in tags['tag']:
        # Run limited-api tests only on CPython.
        if sys.implementation.name != 'cpython':
            return True
    return False


def filter_stderr(stderr_bytes):
    """
    Filter annoying warnings from output.
    """
    if b"Command line warning D9025" in stderr_bytes:
        # MSCV: cl : Command line warning D9025 : overriding '/Ox' with '/Od'
        stderr_bytes = b'\n'.join(
            line for line in stderr_bytes.splitlines()
            if b"Command line warning D9025" not in line)
    return stderr_bytes


def filter_test_suite(test_suite, selector):
    filtered_tests = []
    for test in test_suite._tests:
        if isinstance(test, unittest.TestSuite):
            filter_test_suite(test, selector)
        elif not selector(test.id()):
            continue
        filtered_tests.append(test)
    test_suite._tests[:] = filtered_tests


class CythonCompileTestCase(unittest.TestCase):
    def __init__(self, test_directory, workdir, module, module_path, tags, language='c', preparse='id',
                 expect_log=(),
                 annotate=False, cleanup_workdir=True,
                 cleanup_sharedlibs=True, cleanup_failures=True, cython_only=False, test_selector=None,
                 fork=True, language_level=2, warning_errors=False,
                 test_determinism=False, shard_num=0,
                 common_utility_dir=None, pythran_dir=None, stats=None, add_cython_import=False,
                 extra_directives=None, evaluate_tree_assertions=True):
        self.test_directory = test_directory
        self.tags = tags
        self.workdir = workdir
        self.module = module
        self.module_path = module_path
        self.language = language
        self.preparse = preparse
        self.name = module if self.preparse == "id" else "%s_%s" % (module, preparse)
        self.expect_log = expect_log
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir
        self.cleanup_sharedlibs = cleanup_sharedlibs
        self.cleanup_failures = cleanup_failures
        self.cython_only = cython_only
        self.test_selector = test_selector
        self.shard_num = shard_num
        self.fork = fork
        self.language_level = language_level
        self.warning_errors = warning_errors
        self.evaluate_tree_assertions = evaluate_tree_assertions
        self.test_determinism = test_determinism
        self.common_utility_dir = common_utility_dir
        self.pythran_dir = pythran_dir
        self.stats = stats
        self.add_cython_import = add_cython_import
        self.extra_directives = extra_directives if extra_directives is not None else {}
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        extra_directives = ''
        if self.extra_directives:
            extra_directives = '/'.join(
                name if value is True else f"{name}={value!r}"
                for name, value in sorted(self.extra_directives.items())
            )

        return (
            f"[{self.shard_num}] compiling ("
            f"{self.language}"
            f"{'/cy2' if self.language_level == 2 else '/cy3' if self.language_level == 3 else ''}"
            f"{'/pythran' if self.pythran_dir is not None else ''}"
            f"/{os.path.splitext(self.module_path)[1][1:]}"
            f"{'/' if extra_directives else ''}{extra_directives}"
            f") {self.description_name()}"
        )

    def description_name(self):
        return self.name

    def setUp(self):
        from Cython.Compiler import Options
        self._saved_options = [
            (name, getattr(Options, name))
            for name in (
                'warning_errors',
                'clear_to_none',
                'error_on_unknown_names',
                'error_on_uninitialized',
                # 'cache_builtins',  # not currently supported due to incorrect global caching
            )
        ]
        Options.warning_errors = self.warning_errors

        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        if self.workdir not in sys.path:
            sys.path.insert(0, self.workdir)

        if self.add_cython_import:
            with open(self.module_path, 'rb') as f:
                source = f.read()
                if b'cython.cimports.' in source:
                    from Cython.Shadow import CythonCImports
                    for name in set(re.findall(br"(cython\.cimports(?:\.\w+)+)", source)):
                        name = name.decode()
                        sys.modules[name] = CythonCImports(name)

    def tearDown(self):
        from Cython.Compiler import Options
        for name, value in self._saved_options:
            setattr(Options, name, value)
        unpatch_inspect_isfunction()

        try:
            sys.path.remove(self.workdir)
        except ValueError:
            pass
        try:
            del sys.modules[self.module]
        except KeyError:
            pass

        # remove any stubs of cimported modules in pure Python mode
        if self.add_cython_import:
            for name in list(sys.modules):
                if name.startswith('cython.cimports.'):
                    del sys.modules[name]

        cleanup = self.cleanup_failures or self.success
        cleanup_c_files = WITH_CYTHON and self.cleanup_workdir and cleanup
        cleanup_lib_files = self.cleanup_sharedlibs and cleanup
        is_cygwin = sys.platform == 'cygwin'

        if os.path.exists(self.workdir):
            if cleanup_c_files and cleanup_lib_files and not is_cygwin:
                shutil.rmtree(self.workdir, ignore_errors=True)
            else:
                for rmfile in os.listdir(self.workdir):
                    ext = os.path.splitext(rmfile)[1]
                    if not cleanup_c_files:
                        # Keep C, C++ files, header files, preprocessed sources
                        # and assembly sources (typically the .i and .s files
                        # are intentionally generated when -save-temps is given)
                        if ext in (".c", ".cpp", ".h", ".i", ".ii", ".s"):
                            continue
                        if ext == ".html" and rmfile.startswith(self.module):
                            continue

                    is_shared_obj = ext in (".so", ".dll")

                    if not cleanup_lib_files and is_shared_obj:
                        continue

                    try:
                        rmfile = os.path.join(self.workdir, rmfile)
                        if os.path.isdir(rmfile):
                            shutil.rmtree(rmfile, ignore_errors=True)
                        elif is_cygwin and is_shared_obj:
                            # Delete later
                            _to_clean.append(rmfile)
                        else:
                            os.remove(rmfile)
                    except IOError:
                        pass

                if cleanup_c_files and cleanup_lib_files and is_cygwin:
                    # Finally, remove the work dir itself
                    _to_clean.append(self.workdir)

        if cleanup_c_files and os.path.exists(self.workdir + '-again'):
            shutil.rmtree(self.workdir + '-again', ignore_errors=True)

    def runTest(self):
        self.success = False
        self.runCompileTest()
        self.success = True

    def runCompileTest(self):
        return self.compile(
            self.test_directory, self.module, self.module_path, self.workdir,
            self.test_directory, self.expect_log,
            self.annotate, self.add_cython_import, self.evaluate_tree_assertions)

    def find_module_source_file(self, source_file):
        if not os.path.exists(source_file):
            source_file = source_file[:-1]
        return source_file

    def build_target_filename(self, module_name):
        target = '%s.%s' % (module_name, self.language)
        return target

    def related_files(self, test_directory, module_name):
        is_related = re.compile('%s_.*[.].*' % module_name).match
        return [filename for filename in list_unchanging_dir(test_directory)
                if is_related(filename)]

    def copy_files(self, test_directory, target_directory, file_list):
        if self.preparse and self.preparse != 'id':
            preparse_func = globals()[self.preparse]
            def copy(src, dest):
                with open(src) as fin:
                    with open(dest, 'w') as fout:
                        fout.write(preparse_func(fin.read()))
        else:
            # use symlink on Unix, copy on Windows
            copy = os.symlink if CAN_SYMLINK else shutil.copy

        join = os.path.join
        for filename in file_list:
            file_path = join(test_directory, filename)
            if os.path.exists(file_path):
                copy(file_path, join(target_directory, filename))

    def source_files(self, workdir, module_name, file_list):
        return ([self.build_target_filename(module_name)] +
            [filename for filename in file_list
             if not os.path.isfile(os.path.join(workdir, filename))])

    def split_source_and_output(self, source_file, workdir, add_cython_import=False):
        from Cython.Utils import detect_opened_file_encoding
        with io_open(source_file, 'rb') as f:
            # encoding is passed to ErrorWriter but not used on the source
            # since it is sometimes deliberately wrong
            encoding = detect_opened_file_encoding(f, default=None)

        with io_open(source_file, 'r', encoding='ISO-8859-1') as source_and_output:
            error_writer = warnings_writer = perf_hint_writer = None
            out = io_open(os.path.join(workdir, os.path.basename(source_file)),
                          'w', encoding='ISO-8859-1')
            try:
                for line in source_and_output:
                    if line.startswith(u"_ERRORS"):
                        out.close()
                        out = error_writer = ErrorWriter(encoding=encoding)
                    elif line.startswith(u"_WARNINGS"):
                        out.close()
                        out = warnings_writer = ErrorWriter(encoding=encoding)
                    elif line.startswith(u"_PERFORMANCE_HINTS"):
                        out.close()
                        out = perf_hint_writer = ErrorWriter(encoding=encoding)
                    else:
                        if add_cython_import and line.strip() and not (
                                line.startswith(u'#') or line.startswith(u"from __future__ import ")):
                            # insert "import cython" statement after any directives or future imports
                            if line !=  u"import cython\n":
                                out.write(u"import cython\n")
                            add_cython_import = False
                        out.write(line)
            finally:
                out.close()

        return (error_writer.geterrors() if error_writer else [],
                warnings_writer.geterrors() if warnings_writer else [],
                perf_hint_writer.geterrors() if perf_hint_writer else [])

    def run_cython(self, test_directory, module, module_path, targetdir, incdir, annotate,
                   extra_compile_options=None, evaluate_tree_assertions=True):
        include_dirs = INCLUDE_DIRS + [os.path.join(test_directory, '..', TEST_SUPPORT_DIR)]
        if incdir:
            include_dirs.append(incdir)

        if self.preparse != 'id' and test_directory != targetdir:
            file_name = os.path.basename(module_path)
            self.copy_files(test_directory, targetdir, [file_name])
            module_path = os.path.join(targetdir, file_name)
        target = os.path.join(targetdir, self.build_target_filename(module))

        if extra_compile_options is None:
            extra_compile_options = {}

        if 'allow_unknown_names' in self.tags['tag']:
            from Cython.Compiler import Options
            Options.error_on_unknown_names = False

        try:
            # see configure_cython()
            CompilationOptions, cython_compile, pyrex_default_options
        except NameError:
            from Cython.Compiler.Options import (
                CompilationOptions,
                default_options as pyrex_default_options,
            )
            from Cython.Compiler.Main import compile as cython_compile
        common_utility_include_dir = self.common_utility_dir

        compiler_directives = {
            'autotestdict': False,
            **self.extra_directives,
        }
        options = CompilationOptions(
            pyrex_default_options,
            include_path = include_dirs,
            output_file = target,
            annotate = annotate,
            use_listing_file = False,
            cplus = self.language == 'cpp',
            np_pythran = self.pythran_dir is not None,
            language_level = self.language_level,
            generate_pxi = False,
            evaluate_tree_assertions = evaluate_tree_assertions,
            common_utility_include_dir = common_utility_include_dir,
            c_line_in_traceback = True,
            compiler_directives = compiler_directives,
            **extra_compile_options
            )
        cython_compile(module_path, options=options, full_module_name=module)

    def run_distutils(self, test_directory, module, workdir, incdir,
                      extra_extension_args=None):
        cwd = os.getcwd()
        os.chdir(workdir)
        try:
            build_extension = build_ext(get_distutils_distro())
            build_extension.include_dirs = INCLUDE_DIRS[:]
            if incdir:
                build_extension.include_dirs.append(incdir)
            build_extension.finalize_options()
            if COMPILER:
                build_extension.compiler = COMPILER

            ext_compile_flags = CFLAGS[:]
            ext_compile_defines = CDEFS[:]

            if  build_extension.compiler == 'mingw32':
                ext_compile_flags.append('-Wno-format')
            if extra_extension_args is None:
                extra_extension_args = {}

            related_files = self.related_files(test_directory, module)
            self.copy_files(test_directory, workdir, related_files)

            from distutils.core import Extension
            extension = Extension(
                module,
                sources=self.source_files(workdir, module, related_files),
                extra_compile_args=ext_compile_flags,
                define_macros=ext_compile_defines,
                **extra_extension_args
                )

            if self.language == 'cpp':
                # Set the language now as the fixer might need it
                extension.language = 'c++'
                if self.extra_directives.get('cpp_locals'):
                    extension = update_cpp17_extension(extension)
                    if extension is EXCLUDE_EXT:
                        return

            if 'distutils' in self.tags:
                from Cython.Build.Dependencies import DistutilsInfo
                from Cython.Utils import open_source_file
                pyx_path = self.find_module_source_file(
                    os.path.join(self.test_directory, self.module + ".pyx"))
                with open_source_file(pyx_path) as f:
                    DistutilsInfo(f).apply(extension)

            if self.pythran_dir:
                from Cython.Build.Dependencies import update_pythran_extension
                update_pythran_extension(extension)

            # Compile with -DCYTHON_CLINE_IN_TRACEBACK=1 unless we have
            # the "traceback" tag
            if 'traceback' not in self.tags['tag']:
                extension.define_macros.append(("CYTHON_CLINE_IN_TRACEBACK", 1))

            for matcher, fixer in list(EXT_EXTRAS.items()):
                if isinstance(matcher, str):
                    # lazy init
                    del EXT_EXTRAS[matcher]
                    matcher = string_selector(matcher)
                    EXT_EXTRAS[matcher] = fixer
                if matcher(module, self.tags):
                    newext = fixer(extension)
                    if newext is EXCLUDE_EXT:
                        return skip_test("Test '%s' excluded due to tags '%s'" % (
                            self.name, ', '.join(self.tags.get('tag', ''))))
                    extension = newext or extension
            if self.language == 'cpp':
                extension.language = 'c++'

            build_extension.extensions = [extension]
            build_extension.build_temp = workdir
            build_extension.build_lib  = workdir

            from Cython.Utils import captured_fd, prepare_captured
            from distutils.errors import CCompilerError

            error = None
            with captured_fd(2) as get_stderr:
                try:
                    build_extension.run()
                except CCompilerError as exc:
                    error = str(exc)
            stderr = get_stderr()
            if stderr and b"Command line warning D9025" in stderr:
                # Manually suppress annoying MSVC warnings about overridden CLI arguments.
                stderr = b''.join([
                    line for line in stderr.splitlines(keepends=True)
                    if b"Command line warning D9025" not in line
                ])
            if stderr:
                # The test module name should always be ASCII, but let's not risk encoding failures.
                output = b"Compiler output for module " + module.encode('utf-8') + b":\n" + stderr + b"\n"
                sys.stdout.buffer.write(output)
            if error is not None:
                raise CCompilerError(u"%s\nCompiler output:\n%s" % (error, prepare_captured(stderr)))
        finally:
            os.chdir(cwd)

        try:
            get_ext_fullpath = build_extension.get_ext_fullpath
        except AttributeError:
            def get_ext_fullpath(ext_name, self=build_extension):
                # copied from distutils.command.build_ext (missing in Py2.[45])
                fullname = self.get_ext_fullname(ext_name)
                modpath = fullname.split('.')
                filename = self.get_ext_filename(modpath[-1])
                if not self.inplace:
                    filename = os.path.join(*modpath[:-1]+[filename])
                    return os.path.join(self.build_lib, filename)
                package = '.'.join(modpath[0:-1])
                build_py = self.get_finalized_command('build_py')
                package_dir = os.path.abspath(build_py.get_package_dir(package))
                return os.path.join(package_dir, filename)

        return get_ext_fullpath(module)

    def compile(self, test_directory, module, module_path, workdir, incdir,
                expect_log, annotate, add_cython_import, evaluate_tree_assertions):
        expected_errors = expected_warnings = expected_perf_hints = errors = warnings = perf_hints = ()
        expect_errors = "errors" in expect_log
        expect_warnings = "warnings" in expect_log
        expect_perf_hints = "perf_hints" in expect_log
        if expect_errors or expect_warnings or expect_perf_hints or add_cython_import:
            expected_errors, expected_warnings, expected_perf_hints = self.split_source_and_output(
                module_path, workdir, add_cython_import)
            test_directory = workdir
            module_path = os.path.join(workdir, os.path.basename(module_path))

        if WITH_CYTHON:
            old_stderr = sys.stderr
            try:
                sys.stderr = ErrorWriter()
                with self.stats.time(self.name, self.language, 'cython'):
                    self.run_cython(
                        test_directory, module, module_path, workdir, incdir, annotate,
                        evaluate_tree_assertions=evaluate_tree_assertions)
                errors, warnings, perf_hints = sys.stderr.getall()
            finally:
                sys.stderr = old_stderr
            if self.test_determinism and not expect_errors:
                workdir2 = workdir + '-again'
                os.mkdir(workdir2)
                self.run_cython(test_directory, module, module_path, workdir2, incdir, annotate)
                diffs = []
                for file in os.listdir(workdir2):
                    with open(os.path.join(workdir, file)) as fid:
                        txt1 = fid.read()
                    with open(os.path.join(workdir2, file)) as fid:
                        txt2 = fid.read()
                    if txt1 != txt2:
                        diffs.append(file)
                        os.system('diff -u %s/%s %s/%s > %s/%s.diff' % (
                            workdir, file,
                            workdir2, file,
                            workdir2, file))
                if diffs:
                    self.fail('Nondeterministic file generation: %s' % ', '.join(diffs))

        tostderr = sys.__stderr__.write
        if 'cerror' in self.tags['tag']:
            if errors:
                tostderr("\n=== Expected C compile error ===\n")
                tostderr("\n=== Got Cython errors: ===\n")
                tostderr('\n'.join(errors))
                tostderr('\n\n')
                raise RuntimeError('should have generated extension code')
        elif errors or expected_errors:
            self._match_output(expected_errors, errors, tostderr)
            return None
        if expected_warnings or (expect_warnings and warnings):
            self._match_output(expected_warnings, warnings, tostderr)
        if expected_perf_hints or (expect_perf_hints and perf_hints):
            self._match_output(expected_perf_hints, perf_hints, tostderr)

        so_path = None
        if not self.cython_only:
            from Cython.Utils import captured_fd, print_bytes
            from distutils.errors import CCompilerError
            show_output = True
            get_stderr = get_stdout = None
            try:
                with captured_fd(1) as get_stdout:
                    with captured_fd(2) as get_stderr:
                        with self.stats.time(self.name, self.language, 'compile-%s' % self.language):
                            so_path = self.run_distutils(test_directory, module, workdir, incdir)
            except Exception as exc:
                if ('cerror' in self.tags['tag'] and
                    ((get_stderr and get_stderr()) or
                     isinstance(exc, CCompilerError))):
                    show_output = False  # expected C compiler failure
                else:
                    raise
            else:
                if 'cerror' in self.tags['tag']:
                    raise RuntimeError('should have failed C compile')
            finally:
                if show_output:
                    stdout = get_stdout and get_stdout().strip()
                    stderr = get_stderr and filter_stderr(get_stderr()).strip()
                    if so_path and not stderr:
                        # normal success case => ignore non-error compiler output
                        stdout = None
                    if stdout:
                        print_bytes(
                            stdout, header_text="\n=== C/C++ compiler output: =========\n",
                            end=None, file=sys.__stderr__)
                    if stderr:
                        print_bytes(
                            stderr, header_text="\n=== C/C++ compiler error output: ===\n",
                            end=None, file=sys.__stderr__)
                    if stdout or stderr:
                        tostderr("\n====================================\n")
        return so_path

    def _match_output(self, expected_output, actual_output, write):
        try:
            for expected, actual in zip(expected_output, actual_output):
                if expected != actual and '\\' in actual and os.sep == '\\' and '/' in expected and '\\' not in expected:
                    expected = expected.replace('/', '\\')
                self.assertEqual(expected, actual)
            if len(actual_output) < len(expected_output):
                expected = expected_output[len(actual_output)]
                self.assertEqual(expected, None)
            elif len(actual_output) > len(expected_output):
                unexpected = actual_output[len(expected_output)]
                self.assertEqual(None, unexpected)
        except AssertionError:
            write("\n=== Expected: ===\n")
            write('\n'.join(expected_output))
            write("\n\n=== Got: ===\n")
            write('\n'.join(actual_output))
            write('\n\n')
            raise


class CythonRunTestCase(CythonCompileTestCase):
    def setUp(self):
        CythonCompileTestCase.setUp(self)
        from Cython.Compiler import Options
        Options.clear_to_none = False

    def description_name(self):
        return self.name if self.cython_only else "and running %s" % self.name

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        try:
            self.setUp()
            try:
                self.success = False
                ext_so_path = self.runCompileTest()
                failures, errors, skipped = len(result.failures), len(result.errors), len(result.skipped)
                if not self.cython_only and ext_so_path is not None:
                    self.run_tests(result, ext_so_path)
                if failures == len(result.failures) and errors == len(result.errors):
                    # No new errors...
                    self.success = True
            finally:
                check_thread_termination()
        except SkipTest as exc:
            result.addSkip(self, str(exc))
            result.stopTest(self)
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

    def run_tests(self, result, ext_so_path):
        self.run_doctests(self.module, result, ext_so_path)

    def run_doctests(self, module_or_name, result, ext_so_path):
        def run_test(result):
            if isinstance(module_or_name, basestring):
                with self.stats.time(self.name, self.language, 'import'):
                    module = import_ext(module_or_name, ext_so_path)
            else:
                module = module_or_name
            tests = doctest.DocTestSuite(module)
            if self.test_selector:
                filter_test_suite(tests, self.test_selector)
            with self.stats.time(self.name, self.language, 'run'):
                tests.run(result)
        run_forked_test(result, run_test, self.shortDescription(), self.fork)


def run_forked_test(result, run_func, test_name, fork=True):
    if not fork or sys.version_info[0] >= 3 or not hasattr(os, 'fork'):
        run_func(result)
        sys.stdout.flush()
        sys.stderr.flush()
        gc.collect()
        return

    # fork to make sure we do not keep the tested module loaded
    result_handle, result_file = tempfile.mkstemp()
    os.close(result_handle)
    child_id = os.fork()
    if not child_id:
        result_code = 0
        try:
            try:
                tests = partial_result = None
                try:
                    partial_result = PartialTestResult(result)
                    run_func(partial_result)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    gc.collect()
                except Exception:
                    result_code = 1
                    if partial_result is not None:
                        if tests is None:
                            # importing failed, try to fake a test class
                            tests = _FakeClass(
                                failureException=sys.exc_info()[1],
                                _shortDescription=test_name,
                                module_name=None)
                        partial_result.addError(tests, sys.exc_info())
                if partial_result is not None:
                    with open(result_file, 'wb') as output:
                        pickle.dump(partial_result.data(), output)
            except:
                traceback.print_exc()
        finally:
            try: sys.stderr.flush()
            except: pass
            try: sys.stdout.flush()
            except: pass
            os._exit(result_code)

    try:
        cid, result_code = os.waitpid(child_id, 0)
        module_name = test_name.split()[-1]
        # os.waitpid returns the child's result code in the
        # upper byte of result_code, and the signal it was
        # killed by in the lower byte
        if result_code & 255:
            raise Exception(
                "Tests in module '%s' were unexpectedly killed by signal %d, see test output for details." % (
                    module_name, result_code & 255))
        result_code >>= 8
        if result_code in (0,1):
            try:
                with open(result_file, 'rb') as f:
                    PartialTestResult.join_results(result, pickle.load(f))
            except Exception:
                raise Exception(
                    "Failed to load test result from test in module '%s' after exit status %d,"
                    " see test output for details." % (module_name, result_code))
        if result_code:
            raise Exception(
                "Tests in module '%s' exited with status %d, see test output for details." % (
                    module_name, result_code))
    finally:
        try:
            os.unlink(result_file)
        except:
            pass


class PureDoctestTestCase(unittest.TestCase):
    def __init__(self, module_name, module_path, tags, stats=None, shard_num=0):
        self.tags = tags
        self.module_name = self.name = module_name
        self.module_path = module_path
        self.stats = stats
        self.shard_num = shard_num
        unittest.TestCase.__init__(self, 'run')

    def shortDescription(self):
        return "[%d] running pure doctests in %s" % (
            self.shard_num, self.module_name)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        loaded_module_name = 'pure_doctest__' + self.module_name
        result.startTest(self)
        try:
            self.setUp()

            with self.stats.time(self.name, 'py', 'pyimport'):
                m = import_module_from_file(self.module_name, self.module_path)

            try:
                with self.stats.time(self.name, 'py', 'pyrun'):
                    doctest.DocTestSuite(m).run(result)
            finally:
                del m
                if loaded_module_name in sys.modules:
                    del sys.modules[loaded_module_name]
                check_thread_termination()
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

        if 'mypy' in self.tags['tag']:
            try:
                from mypy import api as mypy_api
            except ImportError:
                pass
            else:
                with self.stats.time(self.name, 'py', 'mypy'):
                    mypy_result = mypy_api.run([
                        self.module_path,
                        #'--ignore-missing-imports',
                        #'--follow-imports', 'skip',
                        '--python-version', '3.10',
                    ])
                if mypy_result[2]:
                    self.fail(mypy_result[0])


is_private_field = re.compile('^_[^_]').match

class _FakeClass(object):
    def __init__(self, **kwargs):
        self._shortDescription = kwargs.get('module_name')
        self.__dict__.update(kwargs)
    def shortDescription(self):
        return self._shortDescription

from unittest import TextTestResult

class PartialTestResult(TextTestResult):
    def __init__(self, base_result):
        TextTestResult.__init__(
            self, self._StringIO(), True,
            base_result.dots + base_result.showAll*2)

    def strip_error_results(self, results):
        for test_case, error in results:
            for attr_name in filter(is_private_field, dir(test_case)):
                if attr_name == '_dt_test':
                    test_case._dt_test = _FakeClass(
                        name=test_case._dt_test.name)
                elif attr_name != '_shortDescription':
                    setattr(test_case, attr_name, None)

    def data(self):
        self.strip_error_results(self.failures)
        self.strip_error_results(self.errors)
        return (self.failures, self.errors, self.skipped, self.testsRun,
                self.stream.getvalue())

    def join_results(result, data):
        """Static method for merging the result back into the main
        result object.
        """
        failures, errors, skipped, tests_run, output = data
        if output:
            result.stream.write(output)
        result.errors.extend(errors)
        result.skipped.extend(skipped)
        result.failures.extend(failures)
        result.testsRun += tests_run

    join_results = staticmethod(join_results)

    class _StringIO(StringIO):
        def writeln(self, line):
            self.write("%s\n" % line)


class CythonUnitTestCase(CythonRunTestCase):
    def shortDescription(self):
        return "[%d] compiling (%s) tests in %s" % (
            self.shard_num, self.language, self.description_name())

    def run_tests(self, result, ext_so_path):
        with self.stats.time(self.name, self.language, 'import'):
            module = import_ext(self.module, ext_so_path)
        tests = unittest.defaultTestLoader.loadTestsFromModule(module)
        if self.test_selector:
            filter_test_suite(tests, self.test_selector)
        with self.stats.time(self.name, self.language, 'run'):
            tests.run(result)


class CythonPyregrTestCase(CythonRunTestCase):
    def setUp(self):
        CythonRunTestCase.setUp(self)
        from Cython.Compiler import Options
        Options.error_on_unknown_names = False
        Options.error_on_uninitialized = False
        Options._directive_defaults.update(dict(
            binding=True, always_allow_keywords=True,
            set_initial_path="SOURCEFILE"))
        patch_inspect_isfunction()

    def related_files(self, test_directory, module_name):
        return _list_pyregr_data_files(test_directory)

    def _run_unittest(self, result, *classes):
        """Run tests from unittest.TestCase-derived classes."""
        valid_types = (unittest.TestSuite, unittest.TestCase)
        suite = unittest.TestSuite()
        load_tests = unittest.TestLoader().loadTestsFromTestCase
        for cls in classes:
            if isinstance(cls, str):
                if cls in sys.modules:
                    suite.addTest(unittest.TestLoader().loadTestsFromModule(sys.modules[cls]))
                else:
                    raise ValueError("str arguments must be keys in sys.modules")
            elif isinstance(cls, valid_types):
                suite.addTest(cls)
            else:
                suite.addTest(load_tests(cls))
        with self.stats.time(self.name, self.language, 'run'):
            suite.run(result)

    def _run_doctest(self, result, module):
        self.run_doctests(module, result, None)

    def run_tests(self, result, ext_so_path):
        try:
            from test import support
        except ImportError: # Python2.x
            from test import test_support as support

        def run_test(result):
            def run_unittest(*classes):
                return self._run_unittest(result, *classes)
            def run_doctest(module, verbosity=None):
                return self._run_doctest(result, module)

            backup = (support.run_unittest, support.run_doctest)
            support.run_unittest = run_unittest
            support.run_doctest = run_doctest

            try:
                try:
                    sys.stdout.flush() # helps in case of crashes
                    with self.stats.time(self.name, self.language, 'import'):
                        module = import_ext(self.module, ext_so_path)
                    sys.stdout.flush() # helps in case of crashes
                    if hasattr(module, 'test_main'):
                        # help 'doctest.DocFileTest' find the module path through frame inspection
                        fake_caller_module_globals = {
                            'module': module,
                            '__name__': module.__name__,
                        }
                        call_tests = eval(
                            'lambda: module.test_main()',
                            fake_caller_module_globals, fake_caller_module_globals)
                        call_tests()
                        sys.stdout.flush() # helps in case of crashes
                except (unittest.SkipTest, support.ResourceDenied):
                    result.addSkip(self, 'ok')
            finally:
                support.run_unittest, support.run_doctest = backup

        run_forked_test(result, run_test, self.shortDescription(), self.fork)


class TestCodeFormat(unittest.TestCase):

    def __init__(self, cython_dir):
        self.cython_dir = cython_dir
        unittest.TestCase.__init__(self)

    def runTest(self):
        source_dirs = ['Cython', 'Demos', 'docs', 'pyximport', 'tests']

        import pycodestyle
        config_file = os.path.join(self.cython_dir, "setup.cfg")
        if not os.path.exists(config_file):
            config_file = os.path.join(os.path.dirname(__file__), "setup.cfg")
        total_errors = 0

        # checks for .py files
        paths = []
        for codedir in source_dirs:
            paths += glob.glob(os.path.join(self.cython_dir, codedir + "/**/*.py"), recursive=True)
        style = pycodestyle.StyleGuide(config_file=config_file)
        print("")  # Fix the first line of the report.
        result = style.check_files(paths)
        total_errors += result.total_errors

        # checks for non-Python source files
        paths = []
        for codedir in ['Cython', 'Demos', 'pyximport']:  # source_dirs:
            paths += glob.glob(os.path.join(self.cython_dir, codedir + "/**/*.p[yx][xdi]"), recursive=True)
        style = pycodestyle.StyleGuide(config_file=config_file, select=[
            # whitespace
            "W1", "W2", "W3",
            # indentation
            "E101", "E111",
        ])
        print("")  # Fix the first line of the report.
        result = style.check_files(paths)
        total_errors += result.total_errors

        """
        # checks for non-Python test files
        paths = []
        for codedir in ['tests']:
            paths += glob.glob(os.path.join(self.cython_dir, codedir + "/**/*.p[yx][xdi]"), recursive=True)
        style = pycodestyle.StyleGuide(select=[
            # whitespace
            "W1", "W2", "W3",
        ])
        result = style.check_files(paths)
        total_errors += result.total_errors
        """

        self.assertEqual(total_errors, 0, "Found code style errors.")


include_debugger = IS_CPYTHON


def collect_unittests(path, module_prefix, suite, selectors, exclude_selectors):
    def file_matches(filename):
        return filename.startswith("Test") and filename.endswith(".py")

    def package_matches(dirname):
        return dirname == "Tests"

    loader = unittest.TestLoader()
    from importlib import import_module

    if include_debugger:
        skipped_dirs = []
    else:
        skipped_dirs = ['Cython' + os.path.sep + 'Debugger' + os.path.sep]

    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath != path and "__init__.py" not in filenames:
            skipped_dirs.append(dirpath + os.path.sep)
            continue
        skip = False
        for dir in skipped_dirs:
            if dirpath.startswith(dir):
                skip = True
        if skip:
            continue
        parentname = os.path.split(dirpath)[-1]
        if package_matches(parentname):
            for f in filenames:
                if file_matches(f):
                    filepath = os.path.join(dirpath, f)[:-len(".py")]
                    modulename = module_prefix + filepath[len(path)+1:].replace(os.path.sep, '.')
                    if not any(1 for match in selectors if match(modulename)):
                        continue
                    if any(1 for match in exclude_selectors if match(modulename)):
                        continue
                    module = import_module(modulename)
                    suite.addTests([loader.loadTestsFromModule(module)])


def collect_doctests(path, module_prefix, suite, selectors, exclude_selectors):
    def package_matches(dirname):
        if dirname == 'Debugger' and not include_debugger:
            return False
        return dirname not in ("Mac", "Distutils", "Plex", "Tempita")

    def file_matches(filename):
        filename, ext = os.path.splitext(filename)
        excludelist = ['libcython', 'libpython', 'test_libcython_in_gdb',
                       'TestLibCython']
        return (ext == '.py' and not
                '~' in filename and not
                '#' in filename and not
                filename.startswith('.') and not
                filename in excludelist)

    import doctest
    from importlib import import_module

    for dirpath, dirnames, filenames in os.walk(path):
        for dir in list(dirnames):
            if not package_matches(dir):
                dirnames.remove(dir)
        for f in filenames:
            if file_matches(f):
                if not f.endswith('.py'): continue
                filepath = os.path.join(dirpath, f)
                if os.path.getsize(filepath) == 0: continue
                filepath = filepath[:-len(".py")]
                modulename = module_prefix + filepath[len(path)+1:].replace(os.path.sep, '.')
                if not [ 1 for match in selectors if match(modulename) ]:
                    continue
                if [ 1 for match in exclude_selectors if match(modulename) ]:
                    continue
                if 'in_gdb' in modulename:
                    # These should only be imported from gdb.
                    continue
                module = import_module(modulename)
                if hasattr(module, "__doc__") or hasattr(module, "__test__"):
                    try:
                        suite.addTest(doctest.DocTestSuite(module))
                    except ValueError: # no tests
                        pass


class EndToEndTest(unittest.TestCase):
    """
    This is a test of build/*.srctree files, where srctree defines a full
    directory structure and its header gives a list of commands to run.
    """
    cython_root = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, treefile, workdir, cleanup_workdir=True, stats=None, capture=True, shard_num=0):
        self.name = os.path.splitext(os.path.basename(treefile))[0]
        self.treefile = treefile
        self.workdir = os.path.join(workdir, self.name)
        self.cleanup_workdir = cleanup_workdir
        self.stats = stats
        self.capture = capture
        self.shard_num = shard_num
        cython_syspath = [self.cython_root]
        for path in sys.path:
            if path.startswith(self.cython_root) and path not in cython_syspath:
                # Py3 installation and refnanny build prepend their
                # fixed paths to sys.path => prefer that over the
                # generic one (cython_root itself goes last)
                cython_syspath.append(path)
        self.cython_syspath = os.pathsep.join(cython_syspath[::-1])
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "[%d] End-to-end %s" % (
            self.shard_num, self.name)

    def setUp(self):
        from Cython.TestUtils import unpack_source_tree
        _, self.commands = unpack_source_tree(self.treefile, self.workdir, self.cython_root)

    def tearDown(self):
        if self.cleanup_workdir:
            for trial in range(5):
                try:
                    shutil.rmtree(self.workdir)
                except OSError:
                    time.sleep(0.1)
                else:
                    break

    def runTest(self):
        self.success = False
        old_path = os.environ.get('PYTHONPATH')
        new_path = self.cython_syspath
        if old_path:
            new_path = new_path + os.pathsep + self.workdir + os.pathsep + old_path
        env_cflags = list(CFLAGS) + [f'"-D{macro}={definition}"' for macro, definition in CDEFS]
        env_cflags = " ".join(env_cflags)
        env = dict(os.environ, PYTHONPATH=new_path, PYTHONIOENCODING='utf8',
                   CFLAGS=env_cflags)
        cmd = []
        out = []
        err = []
        workdir = self.workdir
        for command_no, command in enumerate(self.commands, 1):
            if command[0] == "UNSET":
                try:
                    envvar = command[1]
                except KeyError:
                    envvar = None
                env.pop(envvar, None)
                continue
            elif command[0] == "CD":
                if len(command) == 1:
                    workdir = self.workdir
                else:
                    workdir = os.path.normpath(os.path.join(workdir, command[1]))
                continue
            time_category = 'etoe-build' if (
                'setup.py' in command or 'cythonize.py' in command or 'cython.py' in command) else 'etoe-run'
            with self.stats.time('%s(%d)' % (self.name, command_no), 'c', time_category):
                if self.capture:
                    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, cwd=workdir)
                    _out, _err = p.communicate()
                    res = p.returncode
                else:
                    p = subprocess.call(command, env=env, cwd=workdir)
                    _out, _err = b'', b''
                    res = p
            cmd.append(command)
            out.append(_out.decode('utf-8'))
            err.append(_err.decode('utf-8'))

            if res == 0 and b'REFNANNY: ' in _out:
                res = -1
            if res != 0:
                for c, o, e in zip(cmd, out, err):
                    sys.stderr.write("[%d] %s\n%s\n%s\n\n" % (
                        self.shard_num, c, o, e))
                sys.stderr.write("Final directory layout of '%s':\n%s\n\n" % (
                    self.name,
                    '\n'.join(os.path.join(dirpath, filename) for dirpath, dirs, files in os.walk(self.workdir) for filename in files),
                ))
                self.assertEqual(0, res, "non-zero exit status, last output was:\n%r\n-- stdout:%s\n-- stderr:%s\n" % (
                    ' '.join(command), out[-1], err[-1]))
        self.success = True


# TODO: Support cython_freeze needed here as well.
# TODO: Windows support.

class EmbedTest(unittest.TestCase):

    working_dir = "Demos/embed"

    def setUp(self):
        self.old_dir = os.getcwd()
        os.chdir(self.working_dir)
        os.system(
            "make PYTHON='%s' clean > /dev/null" % sys.executable)

    def tearDown(self):
        try:
            os.system(
                "make PYTHON='%s' clean > /dev/null" % sys.executable)
        except:
            pass
        os.chdir(self.old_dir)

    def test_embed(self):
        libname = sysconfig.get_config_var('LIBRARY')
        libdir = sysconfig.get_config_var('LIBDIR')
        if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
            libdir = os.path.join(os.path.dirname(sys.executable), '..', 'lib')
            if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
                libdir = os.path.join(libdir, 'python%d.%d' % sys.version_info[:2], 'config')
                if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
                    # report the error for the original directory
                    libdir = sysconfig.get_config_var('LIBDIR')
        cython = os.path.abspath(os.path.join('..', '..', 'cython.py'))

        try:
            subprocess.check_output([
                    "make",
                    "PYTHON='%s'" % sys.executable,
                    "CYTHON='%s'" % cython,
                    "LIBDIR1='%s'" % libdir,
                    "paths", "test",
                ],
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as err:
            if err.output:
                self.fail("EmbedTest failed: " + err.output.decode().strip())
            raise
        self.assertTrue(True)  # :)


def load_listfile(filename):
    # just reuse the FileListExclude implementation
    return list(FileListExcluder(filename))

class MissingDependencyExcluder(object):
    def __init__(self, deps):
        # deps: { matcher func : module name }
        self.exclude_matchers = []
        for matcher, module_name in deps.items():
            try:
                module = __import__(module_name)
            except ImportError:
                self.exclude_matchers.append(string_selector(matcher))
                print("Test dependency not found: '%s'" % module_name)
            else:
                version = self.find_dep_version(module_name, module)
                print("Test dependency found: '%s' version %s" % (module_name, version))
        self.tests_missing_deps = []

    def find_dep_version(self, name, module):
        try:
            version = module.__version__
        except AttributeError:
            stdlib_dir = os.path.dirname(shutil.__file__) + os.sep
            module_path = getattr(module, '__file__', stdlib_dir)  # no __file__? => builtin stdlib module
            # GraalPython seems to return None for some unknown reason
            if module_path and module_path.startswith(stdlib_dir):
                # stdlib module
                version = sys.version.partition(' ')[0]
            elif '.' in name:
                # incrementally look for a parent package with version
                name = name.rpartition('.')[0]
                return self.find_dep_version(name, __import__(name))
            else:
                version = '?.?'
        return version

    def __call__(self, testname, tags=None):
        for matcher in self.exclude_matchers:
            if matcher(testname, tags):
                self.tests_missing_deps.append(testname)
                return True
        return False


class VersionDependencyExcluder(object):
    def __init__(self, deps):
        # deps: { version : matcher func }
        from sys import version_info
        self.exclude_matchers = []
        for ver, (compare, matcher) in deps.items():
            if compare(version_info, ver):
                self.exclude_matchers.append(matcher)
        self.tests_missing_deps = []
    def __call__(self, testname, tags=None):
        for matcher in self.exclude_matchers:
            if matcher(testname):
                self.tests_missing_deps.append(testname)
                return True
        return False


class FileListExcluder(object):
    def __init__(self, list_file, verbose=False):
        self.verbose = verbose
        self.excludes = {}
        self._list_file = os.path.relpath(list_file)
        with open(list_file) as f:
            for line in f:
                line = line.strip()
                if line and line[0] != '#':
                    self.excludes[line.split()[0]] = True

    def __call__(self, testname, tags=None):
        exclude = any(string_selector(ex)(testname) for ex in self.excludes)
        if exclude and self.verbose:
            print("Excluding %s because it's listed in %s"
                  % (testname, self._list_file))
        return exclude


class TagsSelector(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __call__(self, testname, tags=None):
        if tags is None:
            return False
        else:
            return self.value in tags[self.tag]


class RegExSelector(object):
    def __init__(self, pattern_string):
        try:
            self.regex_matches = re.compile(pattern_string, re.I|re.U).search
        except re.error:
            print('Invalid pattern: %r' % pattern_string)
            raise

    def __call__(self, testname, tags=None):
        return self.regex_matches(testname)


def string_selector(s):
    if ':' in s:
        return TagsSelector(*s.split(':', 1))
    else:
        return RegExSelector(s)


class ShardExcludeSelector(object):
    # This is an exclude selector so it can override the (include) selectors.
    # It may not provide uniform distribution (in time or count), but is a
    # determanistic partition of the tests which is important.

    # Random seed to improve the hash distribution.
    _seed = base64.b64decode(b'2ged1EtsGz/GkisJr22UcLeP6n9XIaA5Vby2wM49Wvg=')

    def __init__(self, shard_num, shard_count):
        self.shard_num = shard_num
        self.shard_count = shard_count

    def __call__(self, testname, tags=None, _hash=zlib.crc32):
        # Cannot use simple hash() here as shard processes might use different hash seeds.
        # CRC32 is fast and simple.
        return _hash(self._seed + testname.encode()) % self.shard_count != self.shard_num


class PendingThreadsError(RuntimeError):
    pass

threads_seen = []

def check_thread_termination(ignore_seen=True):
    if threading is None: # no threading enabled in CPython
        return
    current = threading.current_thread()
    blocking_threads = []
    for t in threading.enumerate():
        if not t.is_alive() or t == current or t.name == 'time_stamper':
            continue
        t.join(timeout=2)
        if t.is_alive():
            if not ignore_seen:
                blocking_threads.append(t)
                continue
            for seen in threads_seen:
                if t is seen:
                    break
            else:
                threads_seen.append(t)
                blocking_threads.append(t)
    if not blocking_threads:
        return
    sys.stderr.write("warning: left-over threads found after running test:\n")
    for t in blocking_threads:
        sys.stderr.write('...%s\n'  % repr(t))
    raise PendingThreadsError("left-over threads found after running test")

def subprocess_output(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.communicate()[0].decode('UTF-8')
    except OSError:
        return ''

def get_version():
    from Cython.Compiler.Version import version as cython_version
    full_version = cython_version
    top = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(top, '.git')):
        old_dir = os.getcwd()
        try:
            os.chdir(top)
            head_commit = subprocess_output(['git', 'rev-parse', 'HEAD']).strip()
            version_commit = subprocess_output(['git', 'rev-parse', cython_version]).strip()
            diff = subprocess_output(['git', 'diff', '--stat']).strip()
            if head_commit != version_commit:
                full_version += " " + head_commit
            if diff:
                full_version += ' + uncommitted changes'
        finally:
            os.chdir(old_dir)
    return full_version

_orig_stdout, _orig_stderr = sys.stdout, sys.stderr
def flush_and_terminate(status):
    try:
        _orig_stdout.flush()
        _orig_stderr.flush()
    finally:
        os._exit(status)

def main():

    global DISTDIR, WITH_CYTHON

    # Set an environment variable to the top directory
    os.environ['CYTHON_PROJECT_DIR'] = os.path.abspath(os.path.dirname(__file__))

    DISTDIR = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))

    from Cython.Compiler import DebugFlags
    args = []
    for arg in sys.argv[1:]:
        if arg.startswith('--debug') and arg[2:].replace('-', '_') in dir(DebugFlags):
            setattr(DebugFlags, arg[2:].replace('-', '_'), True)
        else:
            args.append(arg)

    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] [selector ...]")
    parser.add_option("--no-cleanup", dest="cleanup_workdir",
                      action="store_false", default=True,
                      help="do not delete the generated C files (allows passing --no-cython on next run)")
    parser.add_option("--no-cleanup-sharedlibs", dest="cleanup_sharedlibs",
                      action="store_false", default=True,
                      help="do not delete the generated shared library files (allows manual module experimentation)")
    parser.add_option("--no-cleanup-failures", dest="cleanup_failures",
                      action="store_false", default=True,
                      help="enable --no-cleanup and --no-cleanup-sharedlibs for failed tests only")
    parser.add_option("--no-cython", dest="with_cython",
                      action="store_false", default=True,
                      help="do not run the Cython compiler, only the C compiler")
    parser.add_option("--compiler", dest="compiler", default=None,
                      help="C compiler type")
    backend_list = ','.join(BACKENDS)
    parser.add_option("--backends", dest="backends", default=backend_list,
                      help="select backends to test (default: %s)" % backend_list)
    parser.add_option("--no-c", dest="use_c",
                      action="store_false", default=True,
                      help="do not test C compilation backend")
    parser.add_option("--no-cpp", dest="use_cpp",
                      action="store_false", default=True,
                      help="do not test C++ compilation backend")
    parser.add_option("--no-cpp-locals", dest="use_cpp_locals",
                      action="store_false", default=True,
                      help="do not rerun select C++ tests with cpp_locals directive")
    parser.add_option("--no-unit", dest="unittests",
                      action="store_false", default=True,
                      help="do not run the unit tests")
    parser.add_option("--no-doctest", dest="doctests",
                      action="store_false", default=True,
                      help="do not run the doctests")
    parser.add_option("--no-file", dest="filetests",
                      action="store_false", default=True,
                      help="do not run the file based tests")
    parser.add_option("--no-pyregr", dest="pyregr",
                      action="store_false", default=True,
                      help="do not run the regression tests of CPython in tests/pyregr/")
    parser.add_option("--no-examples", dest="examples",
                      action="store_false", default=True,
                      help="Do not run the documentation tests in the examples directory.")
    parser.add_option("--no-code-style", dest="code_style",
                      action="store_false", default=True,
                      help="Do not run the code style (PEP8) checks.")
    parser.add_option("--no-tree-asserts", dest="evaluate_tree_assertions",
                      action="store_false", default=True,
                      help="Do not evaluation tree path assertions (which prevents C code generation in tests)")
    parser.add_option("--cython-only", dest="cython_only",
                      action="store_true", default=False,
                      help="only compile pyx to c, do not run C compiler or run the tests")
    parser.add_option("--no-refnanny", dest="with_refnanny",
                      action="store_false", default=True,
                      help="do not regression test reference counting")
    parser.add_option("--no-fork", dest="fork",
                      action="store_false", default=True,
                      help="do not fork to run tests")
    parser.add_option("--sys-pyregr", dest="system_pyregr",
                      action="store_true", default=False,
                      help="run the regression tests of the CPython installation")
    parser.add_option("-x", "--exclude", dest="exclude",
                      action="append", metavar="PATTERN",
                      help="exclude tests matching the PATTERN")
    parser.add_option("--listfile", dest="listfile",
                      action="append",
                      help="specify a file containing a list of tests to run")
    parser.add_option("-j", "--shard_count", dest="shard_count", metavar="N",
                      type=int, default=1,
                      help="shard this run into several parallel runs")
    parser.add_option("--shard_num", dest="shard_num", metavar="K",
                      type=int, default=-1,
                      help="test only this single shard")
    parser.add_option("--profile", dest="profile",
                      action="store_true", default=False,
                      help="enable profiling of the tests")
    parser.add_option("-C", "--coverage", dest="coverage",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler")
    parser.add_option("--coverage-xml", dest="coverage_xml",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler in XML format")
    parser.add_option("--coverage-html", dest="coverage_html",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler in HTML format")
    parser.add_option("--tracemalloc", dest="tracemalloc",
                      action="store_true", default=False,
                      help="enable tracemalloc for the tests")
    parser.add_option("-A", "--annotate", dest="annotate_source",
                      action="store_true", default=True,
                      help="generate annotated HTML versions of the test source files")
    parser.add_option("--no-annotate", dest="annotate_source",
                      action="store_false",
                      help="do not generate annotated HTML versions of the test source files")
    parser.add_option("-v", "--verbose", dest="verbosity",
                      action="count", default=0,
                      help="display test progress, pass twice to print test names")
    parser.add_option("-T", "--ticket", dest="tickets",
                      action="append",
                      help="a bug ticket number to run the respective test in 'tests/*'")
    parser.add_option("-k", dest="only_pattern",
                      help="a regex pattern for selecting doctests and test functions in the test modules")
    parser.add_option("-3", dest="language_level",
                      action="store_const", const=3, default=2,
                      help="set language level to Python 3 (useful for running the CPython regression tests)'")
    parser.add_option("--xml-output", dest="xml_output_dir", metavar="DIR",
                      help="write test results in XML to directory DIR")
    parser.add_option("--exit-ok", dest="exit_ok", default=False,
                      action="store_true",
                      help="exit without error code even on test failures")
    parser.add_option("--failfast", dest="failfast", default=False,
                      action="store_true",
                      help="stop on first failure or error")
    parser.add_option("--root-dir", dest="root_dir", default=os.path.join(DISTDIR, 'tests'),
                      help=("Directory to look for the file based "
                            "tests (the ones which are deactivated with '--no-file'."))
    parser.add_option("--examples-dir", dest="examples_dir",
                      default=os.path.join(DISTDIR, 'docs', 'examples'),
                      help="Directory to look for documentation example tests")
    parser.add_option("--work-dir", dest="work_dir", default=os.path.join(os.getcwd(), 'TEST_TMP'),
                      help="working directory")
    parser.add_option("--cython-dir", dest="cython_dir", default=os.getcwd(),
                      help="Cython installation directory (default: use local source version)")
    parser.add_option("--debug", dest="for_debugging", default=False, action="store_true",
                      help="configure for easier use with a debugger (e.g. gdb)")
    parser.add_option("--pyximport-py", dest="pyximport_py", default=False, action="store_true",
                      help="use pyximport to automatically compile imported .pyx and .py files")
    parser.add_option("--watermark", dest="watermark", default=None,
                      help="deterministic generated by string")
    parser.add_option("--use_common_utility_dir", default=False, action="store_true")
    parser.add_option("--use_formal_grammar", default=False, action="store_true")
    parser.add_option("--test_determinism", default=False, action="store_true",
                      help="test whether Cython's output is deterministic")
    parser.add_option("--pythran-dir", dest="pythran_dir", default=None,
                      help="specify Pythran include directory. This will run the C++ tests using Pythran backend for Numpy")
    parser.add_option("--no-capture", dest="capture", default=True, action="store_false",
                      help="do not capture stdout, stderr in srctree tests. Makes pdb.set_trace interactive")
    parser.add_option("--limited-api", dest="limited_api", default=False, action="store_true",
                      help="Compiles Cython using CPython's LIMITED_API")

    options, cmd_args = parser.parse_args(args)

    if options.with_cython:
        sys.path.insert(0, options.cython_dir)

    # requires glob with the wildcard.
    if cmd_args:
        options.code_style = False

    WITH_CYTHON = options.with_cython

    coverage = None
    if options.coverage or options.coverage_xml or options.coverage_html:
        if not WITH_CYTHON:
            options.coverage = options.coverage_xml = options.coverage_html = False
        elif options.shard_num == -1:
            print("Enabling coverage analysis")
            from coverage import coverage as _coverage
            coverage = _coverage(branch=True)
            coverage.erase()
            coverage.start()

    if options.xml_output_dir:
        shutil.rmtree(options.xml_output_dir, ignore_errors=True)

    if options.listfile:
        for listfile in options.listfile:
            cmd_args.extend(load_listfile(listfile))

    if options.capture and not options.for_debugging:
        keep_alive_interval = 10
    else:
        keep_alive_interval = None
    if options.shard_count > 1 and options.shard_num == -1:
        if "PYTHONIOENCODING" not in os.environ:
            # Make sure subprocesses can print() Unicode text.
            os.environ["PYTHONIOENCODING"] = sys.stdout.encoding or sys.getdefaultencoding()
        import multiprocessing
        pool = multiprocessing.Pool(options.shard_count)
        tasks = [(options, cmd_args, shard_num) for shard_num in range(options.shard_count)]
        open_shards = list(range(options.shard_count))
        error_shards = []
        failure_outputs = []
        # NOTE: create process pool before time stamper thread to avoid forking issues.
        total_time = time.time()
        stats = Stats()
        merged_pipeline_stats = defaultdict(lambda: (0, 0))
        with time_stamper_thread(interval=keep_alive_interval, open_shards=open_shards):
            for shard_num, shard_stats, pipeline_stats, return_code, failure_output in pool.imap_unordered(runtests_callback, tasks):
                open_shards.remove(shard_num)
                if return_code != 0:
                    error_shards.append(shard_num)
                    failure_outputs.append(failure_output)
                    sys.stderr.write("FAILED (%s/%s)\n" % (shard_num, options.shard_count))
                sys.stderr.write("ALL DONE (%s/%s)\n" % (shard_num, options.shard_count))

                stats.update(shard_stats)
                for stage_name, (stage_time, stage_count) in pipeline_stats.items():
                    old_time, old_count = merged_pipeline_stats[stage_name]
                    merged_pipeline_stats[stage_name] = (old_time + stage_time, old_count + stage_count)

        pool.close()
        pool.join()
        pool.terminate()  # graalpy seems happier if we terminate now rather than leaving it to the gc

        total_time = time.time() - total_time
        sys.stderr.write("Sharded tests run in %d seconds (%.1f minutes)\n" % (round(total_time), total_time / 60.))
        if error_shards:
            sys.stderr.write("Errors found in shards %s\n" % ", ".join([str(e) for e in error_shards]))
            for failure_output in zip(error_shards, failure_outputs):
                sys.stderr.write("\nErrors from shard %s:\n%s" % failure_output)
            return_code = 1
        else:
            return_code = 0
    else:
        with time_stamper_thread(interval=keep_alive_interval):
            _, stats, merged_pipeline_stats, return_code, _ = runtests(options, cmd_args, coverage)

    if coverage:
        if options.shard_count > 1 and options.shard_num == -1:
            coverage.combine()
        coverage.stop()

    def as_msecs(t, unit=1000000):
        # pipeline times are in msecs
        return t // unit + float(t % unit) / unit

    pipeline_stats = [
        (as_msecs(stage_time), as_msecs(stage_time) / stage_count, stage_count, stage_name)
        for stage_name, (stage_time, stage_count) in merged_pipeline_stats.items()
    ]
    total_pipeline_time_percent = math.fsum(stats[0] for stats in pipeline_stats) / 100.0
    pipeline_stats.sort(reverse=True)
    sys.stderr.write("Most expensive pipeline stages: %s\n" % ", ".join(
        "%r: %.2f / %d (%.3f / run, %.1f%%)" % (
            stage_name, total_stage_time, stage_count, stage_time, total_stage_time / total_pipeline_time_percent)
        for total_stage_time, stage_time, stage_count, stage_name in pipeline_stats[:10]
    ))

    stats.print_stats(sys.stderr)

    if coverage:
        save_coverage(coverage, options)

    sys.stderr.write("ALL DONE\n")
    sys.stderr.flush()

    try:
        check_thread_termination(ignore_seen=False)
    except PendingThreadsError:
        # normal program exit won't kill the threads, do it the hard way here
        flush_and_terminate(return_code)
    else:
        sys.exit(return_code)


@contextmanager
def time_stamper_thread(interval=10, open_shards=None):
    """
    Print regular time stamps into the build logs to find slow tests.
    @param interval: time interval in seconds
    """
    if not interval or interval < 0:
        # Do nothing
        yield
        return

    import threading
    import datetime
    from time import sleep

    interval = range(interval * 4)
    now = datetime.datetime.now
    stop = False

    # We capture stderr in some places.
    # => make sure we write to the real (original) stderr of the test runner.
    stderr = os.dup(2)
    def write(s):
        os.write(stderr, s if type(s) is bytes else s.encode('ascii'))

    def time_stamper():
        waiting_for_shards = ""
        while True:
            if stop:
                return
            for _ in interval:
                sleep(1./4)
                if stop:
                    return
            if open_shards is not None:
                waiting_for_shards = f" - waiting for {open_shards}"
            write(f'\n#### {now()}{waiting_for_shards}\n')

    thread = threading.Thread(target=time_stamper, name='time_stamper')
    thread.daemon = True
    thread.start()
    try:
        yield
    finally:
        stop = True
        thread.join()
        os.close(stderr)


def configure_cython(options):
    global CompilationOptions, pyrex_default_options, cython_compile
    from Cython.Compiler.Options import \
        CompilationOptions, \
        default_options as pyrex_default_options
    from Cython.Compiler.Options import _directive_defaults as directive_defaults

    from Cython.Compiler import Errors
    Errors.LEVEL = 0  # show all warnings

    from Cython.Compiler import Options
    Options.generate_cleanup_code = 3  # complete cleanup code

    from Cython.Compiler import DebugFlags
    DebugFlags.debug_temp_code_comments = 1
    DebugFlags.debug_no_exception_intercept = 1  # provide better crash output in CI runs

    pyrex_default_options['formal_grammar'] = options.use_formal_grammar
    if options.profile:
        directive_defaults['profile'] = True
    if options.watermark:
        import Cython.Compiler.Version
        Cython.Compiler.Version.watermark = options.watermark


def save_coverage(coverage, options):
    if options.coverage:
        coverage.report(show_missing=0)
    if options.coverage_xml:
        coverage.xml_report(outfile="coverage-report.xml")
    if options.coverage_html:
        coverage.html_report(directory="coverage-report-html")


def runtests_callback(args):
    options, cmd_args, shard_num = args
    options.shard_num = shard_num

    # Make the shard number visible in faulthandler stack traces in the case of process crashes.
    try:
        runtests.__code__ = runtests.__code__.replace(co_name=f"runtests_SHARD_{shard_num}")
    except (AttributeError, TypeError):
        # No .replace() in Py3.7, 'co_name' might not be replacible, whatever.
        pass

    return runtests(options, cmd_args)


def runtests(options, cmd_args, coverage=None):
    # faulthandler should be able to provide a limited traceback
    # in the event of a segmentation fault. Only available on Python 3.3+
    try:
        import faulthandler
    except ImportError:
        pass  # OK - not essential
    else:
        faulthandler.enable()

    WITH_CYTHON = options.with_cython
    ROOTDIR = os.path.abspath(options.root_dir)
    WORKDIR = os.path.abspath(options.work_dir)

    if WITH_CYTHON:
        configure_cython(options)

    xml_output_dir = options.xml_output_dir
    if options.shard_num > -1:
        WORKDIR = os.path.join(WORKDIR, str(options.shard_num))
        if xml_output_dir:
            xml_output_dir = os.path.join(xml_output_dir, 'shard-%03d' % options.shard_num)

    # RUN ALL TESTS!
    UNITTEST_MODULE = "Cython"
    UNITTEST_ROOT = os.path.join(os.path.dirname(__file__), UNITTEST_MODULE)
    if WITH_CYTHON:
        if os.path.exists(WORKDIR):
            for path in os.listdir(WORKDIR):
                if path in ("support", "Cy3"): continue
                shutil.rmtree(os.path.join(WORKDIR, path), ignore_errors=True)
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    if options.shard_num <= 0:
        sys.stderr.write("Python %s\n" % sys.version)
        sys.stderr.write("\n")
        if WITH_CYTHON:
            sys.stderr.write("Running tests against Cython %s\n" % get_version())
        else:
            sys.stderr.write("Running tests without Cython.\n")

    if options.for_debugging:
        options.cleanup_workdir = False
        options.cleanup_sharedlibs = False
        options.fork = False
        if WITH_CYTHON and include_debugger:
            from Cython.Compiler.Options import default_options as compiler_default_options
            compiler_default_options['gdb_debug'] = True
            compiler_default_options['output_dir'] = os.getcwd()

    if IS_PYPY:
        if options.with_refnanny:
            sys.stderr.write("Disabling refnanny in PyPy\n")
            options.with_refnanny = False

    refnanny = None
    if options.with_refnanny:
        try:
            refnanny = import_refnanny()
        except ImportError:
            from pyximport.pyxbuild import pyx_to_dll
            libpath = pyx_to_dll(os.path.join("Cython", "Runtime", "refnanny.pyx"),
                                build_in_temp=True,
                                pyxbuild_dir=os.path.join(WORKDIR, "support"))
            sys.path.insert(0, os.path.split(libpath)[0])
            refnanny = import_refnanny()
        CDEFS.append(('CYTHON_REFNANNY', '1'))

    if options.limited_api:
        CDEFS.append(('CYTHON_LIMITED_API', '1'))
        CDEFS.append(("Py_LIMITED_API", '(PY_VERSION_HEX & 0xffff0000)'))
        CFLAGS.append('-Wno-unused-function')

    if xml_output_dir and options.fork:
        # doesn't currently work together
        sys.stderr.write("Disabling forked testing to support XML test output\n")
        options.fork = False

    if WITH_CYTHON:
        sys.stderr.write("Using Cython language level %d.\n" % options.language_level)

    test_bugs = False
    if options.tickets:
        for ticket_number in options.tickets:
            test_bugs = True
            cmd_args.append('ticket:%s' % ticket_number)
    if not test_bugs:
        for selector in cmd_args:
            if selector.startswith('bugs'):
                test_bugs = True

    selectors = [ string_selector(r) for r in cmd_args ]
    verbose_excludes = selectors or options.verbosity >= 2
    if not selectors:
        selectors = [ lambda x, tags=None: True ]

    # Check which external modules are not present and exclude tests
    # which depends on them (by prefix)

    missing_dep_excluder = MissingDependencyExcluder(EXT_DEP_MODULES)
    version_dep_excluder = VersionDependencyExcluder(VER_DEP_MODULES)
    exclude_selectors = [missing_dep_excluder, version_dep_excluder] # want to print msg at exit

    try:
        import IPython.core.release
        if list(IPython.core.release._ver) < [1, 0, 0]:
            raise ImportError
    except (ImportError, AttributeError, TypeError):
        exclude_selectors.append(RegExSelector('IPython'))

    try:
        raise ImportError("Jedi typer is currently broken, see GH#1845")
        import jedi
        if not ([0, 9] <= list(map(int, re.findall('[0-9]+', jedi.__version__ or '0')))):
            raise ImportError
    except (ImportError, AttributeError, TypeError):
        exclude_selectors.append(RegExSelector('Jedi'))

    if options.exclude:
        exclude_selectors += [ string_selector(r) for r in options.exclude ]

    if not COMPILER_HAS_INT128:
        exclude_selectors += [RegExSelector('int128')]

    if options.shard_num > -1:
        exclude_selectors.append(ShardExcludeSelector(options.shard_num, options.shard_count))

    if not test_bugs:
        bug_files = [
            ('bugs.txt', True),
            ('pypy_bugs.txt', IS_PYPY),
            ('pypy_crash_bugs.txt', IS_PYPY),
            ('pypy_implementation_detail_bugs.txt', IS_PYPY),
            ('graal_bugs.txt', IS_GRAAL),
            ('limited_api_bugs.txt', options.limited_api),
            ('limited_api_bugs_38.txt', options.limited_api and sys.version_info < (3, 9)),
            ('windows_bugs.txt', sys.platform == 'win32'),
            ('cygwin_bugs.txt', sys.platform == 'cygwin'),
            ('windows_bugs_39.txt', sys.platform == 'win32' and sys.version_info[:2] == (3, 9)),
        ]

        exclude_selectors += [
            FileListExcluder(os.path.join(ROOTDIR, bugs_file_name),
                             verbose=verbose_excludes)
            for bugs_file_name, condition in bug_files if condition
        ]

    if sys.version_info < (3, 11) and options.limited_api:
        # exclude everything with memoryviews in since this is a big
        # missing feature from the limited API in these versions
        exclude_selectors += [
            TagsSelector('tag', 'memoryview'),
            FileListExcluder(os.path.join(ROOTDIR, "memoryview_tests.txt")),
        ]

    if not test_bugs and re.match("arm|aarch", platform.machine(), re.IGNORECASE):
        # Pythran is only excluded on arm because it fails to link with blas on the CI.
        # I don't think there's anything fundamentally wrong with it.
        exclude_selectors += [
            TagsSelector('tag', 'pythran')
        ]

    exclude_selectors += [TagsSelector('tag', tag) for tag, exclude in TAG_EXCLUDERS if exclude]

    global COMPILER
    if options.compiler:
        COMPILER = options.compiler

    selected_backends = [ name.strip() for name in options.backends.split(',') if name.strip() ]
    backends = []
    for backend in selected_backends:
        if backend == 'c' and not options.use_c:
            continue
        elif backend == 'cpp' and not options.use_cpp:
            continue
        elif backend not in BACKENDS:
            sys.stderr.write("Unknown backend requested: '%s' not one of [%s]\n" % (
                backend, ','.join(BACKENDS)))
            sys.exit(1)
        backends.append(backend)
    if options.shard_num <= 0:
        sys.stderr.write("Backends: %s\n" % ','.join(backends))
    languages = backends

    if 'CI' in os.environ and sys.platform == 'darwin' and 'cpp' in languages:
        bugs_file_name = 'macos_cpp_bugs.txt'
        exclude_selectors += [
            FileListExcluder(os.path.join(ROOTDIR, bugs_file_name),
                             verbose=verbose_excludes)
        ]

    if options.use_common_utility_dir:
        common_utility_dir = os.path.join(WORKDIR, 'utility_code')
        if not os.path.exists(common_utility_dir):
            os.makedirs(common_utility_dir)
    else:
        common_utility_dir = None

    sys.stderr.write("\n")

    test_suite = unittest.TestSuite()
    stats = Stats()

    if options.unittests:
        collect_unittests(UNITTEST_ROOT, UNITTEST_MODULE + ".", test_suite, selectors, exclude_selectors)

    if options.doctests:
        collect_doctests(UNITTEST_ROOT, UNITTEST_MODULE + ".", test_suite, selectors, exclude_selectors)

    if options.filetests and languages:
        filetests = TestBuilder(ROOTDIR, WORKDIR, selectors, exclude_selectors,
                                options, options.pyregr, languages, test_bugs,
                                options.language_level, common_utility_dir,
                                options.pythran_dir, add_embedded_test=True, stats=stats,
                                add_cpp_locals_extra_tests=options.use_cpp_locals)
        test_suite.addTest(filetests.build_suite())

    if options.examples and languages:
        examples_workdir = os.path.join(WORKDIR, 'examples')
        language_level = 3
        for subdirectory in glob.glob(os.path.join(options.examples_dir, "*/")):
            filetests = TestBuilder(subdirectory, examples_workdir, selectors, exclude_selectors,
                                    options, options.pyregr, languages, test_bugs,
                                    language_level, common_utility_dir,
                                    options.pythran_dir,
                                    default_mode='compile', stats=stats, add_cython_import=True)
            test_suite.addTest(filetests.build_suite())

    if options.system_pyregr and languages:
        sys_pyregr_dir = os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3], 'test')
        if not os.path.isdir(sys_pyregr_dir):
            sys_pyregr_dir = os.path.join(os.path.dirname(sys.executable), 'Lib', 'test')  # source build
        if os.path.isdir(sys_pyregr_dir):
            filetests = TestBuilder(ROOTDIR, WORKDIR, selectors, exclude_selectors,
                                    options, True, languages, test_bugs,
                                    sys.version_info[0], common_utility_dir, stats=stats)
            sys.stderr.write("Including CPython regression tests in %s\n" % sys_pyregr_dir)
            test_suite.addTest(filetests.handle_directory(sys_pyregr_dir, 'pyregr'))

    if options.code_style and options.shard_num <= 0:
        try:
            import pycodestyle
        except ImportError:
            # Hack to make the exclusion visible.
            missing_dep_excluder.tests_missing_deps.append('TestCodeFormat')
        else:
            test_suite.addTest(TestCodeFormat(options.cython_dir))

    if xml_output_dir:
        from Cython.Tests.xmlrunner import XMLTestRunner
        if not os.path.exists(xml_output_dir):
            try:
                os.makedirs(xml_output_dir)
            except OSError:
                pass  # concurrency issue?
        test_runner = XMLTestRunner(output=xml_output_dir,
                                    verbose=options.verbosity > 0)
        if options.failfast:
            sys.stderr.write("--failfast not supported with XML runner\n")
    else:
        text_runner_options = {}
        if options.failfast:
            text_runner_options['failfast'] = True
        test_runner = unittest.TextTestRunner(verbosity=options.verbosity, **text_runner_options)

    if options.pyximport_py:
        from pyximport import pyximport
        pyximport.install(pyimport=True, build_dir=os.path.join(WORKDIR, '_pyximport'),
                          load_py_module_on_import_failure=True, inplace=True)

    try:
        gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
    except AttributeError:
        pass  # not available on PyPy

    enable_faulthandler = False
    old_faulhandler_envvar = os.environ.get('PYTHONFAULTHANDLER')
    try:
        import faulthandler
    except ImportError:
        pass
    else:
        os.environ['PYTHONFAULTHANDLER'] = "1"
        enable_faulthandler = not faulthandler.is_enabled()
        if enable_faulthandler:
            faulthandler.enable()

    if options.tracemalloc:
        import tracemalloc
        tracemalloc.start()

    # Run the collected tests.
    try:
        if options.shard_num > -1:
            thread_id = f" (Thread ID 0x{threading.get_ident():x})" if threading is not None else ""
            sys.stderr.write(f"Tests in shard ({options.shard_num}/{options.shard_count}) starting{thread_id}\n")
        result = test_runner.run(test_suite)
    except Exception as exc:
        # Make sure we print exceptions also from shards.
        if options.shard_num > -1:
            sys.stderr.write(f"Tests in shard ({options.shard_num}/{options.shard_count}) crashed: {exc}\n")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if enable_faulthandler:
            faulthandler.disable()
        if os.environ.get('PYTHONFAULTHANDLER') != old_faulhandler_envvar:
            if old_faulhandler_envvar is None:
                del os.environ['PYTHONFAULTHANDLER']
            else:
                os.environ['PYTHONFAULTHANDLER'] = old_faulhandler_envvar

    if options.tracemalloc:
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        run_dir = os.curdir
        mallocs = '\n'.join(f"   {os.path.relpath(str(tm_stat), run_dir)}" for tm_stat in snapshot.statistics('lineno')[:20])
        del snapshot
        tracemalloc.stop()
        sys.stderr.write(f"Memory allocations:\n{mallocs}\n")

    if common_utility_dir and options.shard_num < 0 and options.cleanup_workdir:
        shutil.rmtree(common_utility_dir)

    from Cython.Compiler.Pipeline import get_timings
    pipeline_stats = get_timings()

    if missing_dep_excluder.tests_missing_deps:
        sys.stderr.write("Following tests excluded because of missing dependencies on your system:\n")
        for test in missing_dep_excluder.tests_missing_deps:
            sys.stderr.write("   %s\n" % test)

    if options.with_refnanny and refnanny is not None:
        sys.stderr.write("\n".join([repr(x) for x in refnanny.reflog]))

    result_code = 0 if options.exit_ok else not result.wasSuccessful()

    if xml_output_dir:
        failure_output = ""
    else:
        failure_output = "".join(collect_failure_output(result))

    return options.shard_num, stats, pipeline_stats, result_code, failure_output


def collect_failure_output(result):
    """Extract test error/failure output from a TextTestResult."""
    failure_output = []
    for flavour, errors in (("ERROR", result.errors), ("FAIL", result.failures)):
        for test, err in errors:
            failure_output.append("%s\n%s: %s\n%s\n%s\n" % (
                result.separator1,
                flavour, result.getDescription(test),
                result.separator2,
                err))
    return failure_output


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
        try:
            check_thread_termination(ignore_seen=False)
        except PendingThreadsError:
            # normal program exit won't kill the threads, do it the hard way here
            flush_and_terminate(1)
        sys.exit(1)
