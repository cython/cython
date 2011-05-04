#!/usr/bin/python

import os
import sys
import re
import gc
import locale
import codecs
import shutil
import time
import unittest
import doctest
import operator
import tempfile
import warnings
import traceback
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from io import open as io_open
except ImportError:
    from codecs import open as io_open

try:
    import threading
except ImportError: # No threads, no problems
    threading = None

try:
    from collections import defaultdict
except ImportError:
    class defaultdict(object):
        def __init__(self, default_factory=lambda : None):
            self._dict = {}
            self.default_factory = default_factory
        def __getitem__(self, key):
            if key not in self._dict:
                self._dict[key] = self.default_factory()
            return self._dict[key]
        def __setitem__(self, key, value):
            self._dict[key] = value
        def __repr__(self):
            return repr(self._dict)

WITH_CYTHON = True
CY3_DIR = None

from distutils.dist import Distribution
from distutils.core import Extension
from distutils.command.build_ext import build_ext as _build_ext
from distutils import sysconfig
distutils_distro = Distribution()

if sys.platform == 'win32':
    # TODO: Figure out why this hackery (see http://thread.gmane.org/gmane.comp.python.cython.devel/8280/).
    config_files = distutils_distro.find_config_files()
    try: config_files.remove('setup.cfg')
    except ValueError: pass
    distutils_distro.parse_config_files(config_files)

    cfgfiles = distutils_distro.find_config_files()
    try: cfgfiles.remove('setup.cfg')
    except ValueError: pass
    distutils_distro.parse_config_files(cfgfiles)

EXT_DEP_MODULES = {
    'tag:numpy' : 'numpy',
    'tag:pstats': 'pstats',
    'tag:posix' : 'posix',
}

def update_numpy_extension(ext):
    import numpy
    ext.include_dirs.append(numpy.get_include())

def update_openmp_extension(ext):
    language = ext.language

    if language == 'cpp':
        flags = OPENMP_CPP_COMPILER_FLAGS
    else:
        flags = OPENMP_C_COMPILER_FLAGS

    if flags:
        compile_flags, link_flags = flags

        ext.extra_compile_args.extend(compile_flags.split())
        ext.extra_link_args.extend(link_flags.split())
        return ext

    return EXCLUDE_EXT

def get_openmp_compiler_flags(language):
    """
    As of gcc 4.2, it supports OpenMP 2.5. Gcc 4.4 implements 3.0. We don't
    (currently) check for other compilers.

    returns a two-tuple of (CFLAGS, LDFLAGS) to build the OpenMP extension
    """
    if language == 'cpp':
        cc = sysconfig.get_config_var('CXX')
    else:
        cc = sysconfig.get_config_var('CC')

    # For some reason, cc can be e.g. 'gcc -pthread'
    cc = cc.split()[0]

    matcher = re.compile(r"gcc version (\d+\.\d+)").search
    try:
        import subprocess
    except ImportError:
        try:
            in_, out, err = os.popen(cc + " -v")
        except EnvironmentError:
            # Be compatible with Python 3
            _, e, _ = sys.exc_info()
            warnings.warn("Unable to find the %s compiler: %s: %s" %
                                        (language, os.strerror(e.errno), cc))
            return None

        output = out.read() or err.read()
    else:
        try:
            p = subprocess.Popen([cc, "-v"], stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)
        except EnvironmentError:
            # Be compatible with Python 3
            _, e, _ = sys.exc_info()
            warnings.warn("Unable to find the %s compiler: %s: %s" %
                                        (language, os.strerror(e.errno), cc))
            return None

        output = p.stdout.read()

    output = output.decode(locale.getpreferredencoding() or 'UTF-8')

    compiler_version = matcher(output).group(1)
    if compiler_version and compiler_version.split('.') >= ['4', '2']:
        return '-fopenmp', '-fopenmp'


locale.setlocale(locale.LC_ALL, '')

OPENMP_C_COMPILER_FLAGS = get_openmp_compiler_flags('c')
OPENMP_CPP_COMPILER_FLAGS = get_openmp_compiler_flags('cpp')

# Return this from the EXT_EXTRAS matcher callback to exclude the extension
EXCLUDE_EXT = object()

EXT_EXTRAS = {
    'tag:numpy' : update_numpy_extension,
    'tag:openmp': update_openmp_extension,
}

# TODO: use tags
VER_DEP_MODULES = {
    # tests are excluded if 'CurrentPythonVersion OP VersionTuple', i.e.
    # (2,4) : (operator.lt, ...) excludes ... when PyVer < 2.4.x
    (2,4) : (operator.lt, lambda x: x in ['run.extern_builtins_T258',
                                          'run.builtin_sorted'
                                          ]),
    (2,5) : (operator.lt, lambda x: x in ['run.any',
                                          'run.all',
                                          'run.relativeimport_T542',
                                          'run.relativeimport_star_T542',
                                          ]),
    (2,6) : (operator.lt, lambda x: x in ['run.print_function',
                                          'run.cython3',
                                          'run.generators_py', # generators, with statement
                                          'run.pure_py', # decorators, with statement
                                          ]),
    (2,7) : (operator.lt, lambda x: x in ['run.withstat_py', # multi context with statement
                                          ]),
    # The next line should start (3,); but this is a dictionary, so
    # we can only have one (3,) key.  Since 2.7 is supposed to be the
    # last 2.x release, things would have to change drastically for this
    # to be unsafe...
    (2,999): (operator.lt, lambda x: x in ['run.special_methods_T561_py3',
                                           'run.test_raisefrom',
                                           ]),
    (3,): (operator.ge, lambda x: x in ['run.non_future_division',
                                        'compile.extsetslice',
                                        'compile.extdelslice',
                                        'run.special_methods_T561_py2']),
}

# files that should not be converted to Python 3 code with 2to3
KEEP_2X_FILES = [
    os.path.join('Cython', 'Debugger', 'Tests', 'test_libcython_in_gdb.py'),
    os.path.join('Cython', 'Debugger', 'Tests', 'test_libpython_in_gdb.py'),
    os.path.join('Cython', 'Debugger', 'libcython.py'),
    os.path.join('Cython', 'Debugger', 'libpython.py'),
]

COMPILER = None
INCLUDE_DIRS = [ d for d in os.getenv('INCLUDE', '').split(os.pathsep) if d ]
CFLAGS = os.getenv('CFLAGS', '').split()

def memoize(f):
    uncomputed = object()
    f._cache = {}
    def func(*args):
        res = f._cache.get(args, uncomputed)
        if res is uncomputed:
            res = f._cache[args] = f(*args)
        return res
    return func

def parse_tags(filepath):
    tags = defaultdict(list)
    f = io_open(filepath, encoding='ISO-8859-1', errors='replace')
    try:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] != '#':
                break
            ix = line.find(':')
            if ix != -1:
                tag = line[1:ix].strip()
                values = line[ix+1:].split(',')
                tags[tag].extend([value.strip() for value in values])
    finally:
        f.close()
    return tags

parse_tags = memoize(parse_tags)

list_unchanging_dir = memoize(lambda x: os.listdir(x))


class build_ext(_build_ext):
    def build_extension(self, ext):
        if ext.language == 'c++':
            try:
                try: # Py2.7+ & Py3.2+
                    compiler_obj = self.compiler_obj
                except AttributeError:
                    compiler_obj = self.compiler
                compiler_obj.compiler_so.remove('-Wstrict-prototypes')
            except Exception:
                pass
        _build_ext.build_extension(self, ext)

class ErrorWriter(object):
    match_error = re.compile('(warning:)?(?:.*:)?\s*([-0-9]+)\s*:\s*([-0-9]+)\s*:\s*(.*)').match
    def __init__(self):
        self.output = []
        self.write = self.output.append

    def _collect(self, collect_errors, collect_warnings):
        s = ''.join(self.output)
        result = []
        for line in s.split('\n'):
            match = self.match_error(line)
            if match:
                is_warning, line, column, message = match.groups()
                if (is_warning and collect_warnings) or \
                        (not is_warning and collect_errors):
                    result.append( (int(line), int(column), message.strip()) )
        result.sort()
        return [ "%d:%d: %s" % values for values in result ]

    def geterrors(self):
        return self._collect(True, False)

    def getwarnings(self):
        return self._collect(False, True)

    def getall(self):
        return self._collect(True, True)

class TestBuilder(object):
    def __init__(self, rootdir, workdir, selectors, exclude_selectors, annotate,
                 cleanup_workdir, cleanup_sharedlibs, with_pyregr, cython_only,
                 languages, test_bugs, fork, language_level):
        self.rootdir = rootdir
        self.workdir = workdir
        self.selectors = selectors
        self.exclude_selectors = exclude_selectors
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir
        self.cleanup_sharedlibs = cleanup_sharedlibs
        self.with_pyregr = with_pyregr
        self.cython_only = cython_only
        self.languages = languages
        self.test_bugs = test_bugs
        self.fork = fork
        self.language_level = language_level

    def build_suite(self):
        suite = unittest.TestSuite()
        filenames = os.listdir(self.rootdir)
        filenames.sort()
        for filename in filenames:
            path = os.path.join(self.rootdir, filename)
            if os.path.isdir(path):
                if filename == 'pyregr' and not self.with_pyregr:
                    continue
                if filename == 'broken' and not self.test_bugs:
                    continue
                suite.addTest(
                    self.handle_directory(path, filename))
        if sys.platform not in ['win32']:
            # Non-Windows makefile.
            if [1 for selector in self.selectors if selector("embedded")] \
                and not [1 for selector in self.exclude_selectors if selector("embedded")]:
                suite.addTest(unittest.makeSuite(EmbedTest))
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
            tags = parse_tags(filepath)
            fqmodule = "%s.%s" % (context, module)
            if not [ 1 for match in self.selectors
                     if match(fqmodule, tags) ]:
                continue
            if self.exclude_selectors:
                if [1 for match in self.exclude_selectors 
                        if match(fqmodule, tags)]:
                    continue

            mode = 'run' # default
            if tags['mode']:
                mode = tags['mode'][0]
            elif context == 'pyregr':
                mode = 'pyregr'

            if ext == '.srctree':
                suite.addTest(EndToEndTest(filepath, workdir, self.cleanup_workdir))
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
            else:
                test_class = CythonCompileTestCase

            for test in self.build_tests(test_class, path, workdir,
                                         module, mode == 'error', tags):
                suite.addTest(test)
            if mode == 'run' and ext == '.py':
                # additionally test file in real Python
                suite.addTest(PureDoctestTestCase(module, os.path.join(path, filename)))
                
        return suite

    def build_tests(self, test_class, path, workdir, module, expect_errors, tags):
        if 'werror' in tags['tag']:
            warning_errors = True
        else:
            warning_errors = False

        if expect_errors:
            if 'cpp' in tags['tag'] and 'cpp' in self.languages:
                languages = ['cpp']
            else:
                languages = self.languages[:1]
        else:
            languages = self.languages
        if 'cpp' in tags['tag'] and 'c' in languages:
            languages = list(languages)
            languages.remove('c')
        tests = [ self.build_test(test_class, path, workdir, module,
                                  language, expect_errors, warning_errors)
                  for language in languages ]
        return tests

    def build_test(self, test_class, path, workdir, module,
                   language, expect_errors, warning_errors):
        workdir = os.path.join(workdir, language)
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        return test_class(path, workdir, module,
                          language=language,
                          expect_errors=expect_errors,
                          annotate=self.annotate,
                          cleanup_workdir=self.cleanup_workdir,
                          cleanup_sharedlibs=self.cleanup_sharedlibs,
                          cython_only=self.cython_only,
                          fork=self.fork,
                          language_level=self.language_level,
                          warning_errors=warning_errors)

class CythonCompileTestCase(unittest.TestCase):
    def __init__(self, test_directory, workdir, module, language='c',
                 expect_errors=False, annotate=False, cleanup_workdir=True,
                 cleanup_sharedlibs=True, cython_only=False, fork=True,
                 language_level=2, warning_errors=False):
        self.test_directory = test_directory
        self.workdir = workdir
        self.module = module
        self.language = language
        self.expect_errors = expect_errors
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir
        self.cleanup_sharedlibs = cleanup_sharedlibs
        self.cython_only = cython_only
        self.fork = fork
        self.language_level = language_level
        self.warning_errors = warning_errors
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "compiling (%s) %s" % (self.language, self.module)

    def setUp(self):
        from Cython.Compiler import Options
        self._saved_options = [ (name, getattr(Options, name))
                                for name in ('warning_errors', 'error_on_unknown_names') ]
        Options.warning_errors = self.warning_errors

        if self.workdir not in sys.path:
            sys.path.insert(0, self.workdir)

    def tearDown(self):
        from Cython.Compiler import Options
        for name, value in self._saved_options:
            setattr(Options, name, value)

        try:
            sys.path.remove(self.workdir)
        except ValueError:
            pass
        try:
            del sys.modules[self.module]
        except KeyError:
            pass
        cleanup_c_files = WITH_CYTHON and self.cleanup_workdir
        cleanup_lib_files = self.cleanup_sharedlibs
        if os.path.exists(self.workdir):
            for rmfile in os.listdir(self.workdir):
                if not cleanup_c_files:
                    if rmfile[-2:] in (".c", ".h") or rmfile[-4:] == ".cpp":
                        continue
                if not cleanup_lib_files and rmfile.endswith(".so") or rmfile.endswith(".dll"):
                    continue
                if self.annotate and rmfile.endswith(".html"):
                    continue
                try:
                    rmfile = os.path.join(self.workdir, rmfile)
                    if os.path.isdir(rmfile):
                        shutil.rmtree(rmfile, ignore_errors=True)
                    else:
                        os.remove(rmfile)
                except IOError:
                    pass
        else:
            os.makedirs(self.workdir)

    def runTest(self):
        self.runCompileTest()

    def runCompileTest(self):
        self.compile(self.test_directory, self.module, self.workdir,
                     self.test_directory, self.expect_errors, self.annotate)

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
        for filename in file_list:
            shutil.copy(os.path.join(test_directory, filename),
                        target_directory)

    def source_files(self, workdir, module_name, file_list):
        return ([self.build_target_filename(module_name)] +
            [filename for filename in file_list
                if not os.path.isfile(os.path.join(workdir, filename))])

    def split_source_and_output(self, test_directory, module, workdir):
        source_file = self.find_module_source_file(os.path.join(test_directory, module) + '.pyx')
        source_and_output = io_open(source_file, 'rU', encoding='ISO-8859-1')
        try:
            out = io_open(os.path.join(workdir, module + os.path.splitext(source_file)[1]),
                              'w', encoding='ISO-8859-1')
            for line in source_and_output:
                last_line = line
                if line.startswith("_ERRORS"):
                    out.close()
                    out = ErrorWriter()
                else:
                    out.write(line)
        finally:
            source_and_output.close()
        try:
            geterrors = out.geterrors
        except AttributeError:
            out.close()
            return []
        else:
            return geterrors()

    def run_cython(self, test_directory, module, targetdir, incdir, annotate,
                   extra_compile_options=None):
        include_dirs = INCLUDE_DIRS[:]
        if incdir:
            include_dirs.append(incdir)
        source = self.find_module_source_file(
            os.path.join(test_directory, module + '.pyx'))
        target = os.path.join(targetdir, self.build_target_filename(module))

        if extra_compile_options is None:
            extra_compile_options = {}

        try:
            CompilationOptions
        except NameError:
            from Cython.Compiler.Main import CompilationOptions
            from Cython.Compiler.Main import compile as cython_compile
            from Cython.Compiler.Main import default_options

        options = CompilationOptions(
            default_options,
            include_path = include_dirs,
            output_file = target,
            annotate = annotate,
            use_listing_file = False,
            cplus = self.language == 'cpp',
            language_level = self.language_level,
            generate_pxi = False,
            evaluate_tree_assertions = True,
            **extra_compile_options
            )
        cython_compile(source, options=options,
                       full_module_name=module)

    def run_distutils(self, test_directory, module, workdir, incdir,
                      extra_extension_args=None):
        original_source = self.find_module_source_file(
            os.path.join(test_directory, module + '.pyx'))
        try:
            tags = parse_tags(original_source)
        except IOError:
            tags = {}
        cwd = os.getcwd()
        os.chdir(workdir)
        try:
            build_extension = build_ext(distutils_distro)
            build_extension.include_dirs = INCLUDE_DIRS[:]
            if incdir:
                build_extension.include_dirs.append(incdir)
            build_extension.finalize_options()
            if COMPILER:
                build_extension.compiler = COMPILER
            ext_compile_flags = CFLAGS[:]
            if  build_extension.compiler == 'mingw32':
                ext_compile_flags.append('-Wno-format')
            if extra_extension_args is None:
                extra_extension_args = {}

            related_files = self.related_files(test_directory, module)
            self.copy_files(test_directory, workdir, related_files)
            extension = Extension(
                module,
                sources = self.source_files(workdir, module, related_files),
                extra_compile_args = ext_compile_flags,
                **extra_extension_args
                )

            if self.language == 'cpp':
                # Set the language now as the fixer might need it
                extension.language = 'c++'

            for matcher, fixer in EXT_EXTRAS.items():
                if isinstance(matcher, str):
                    del EXT_EXTRAS[matcher]
                    matcher = string_selector(matcher)
                    EXT_EXTRAS[matcher] = fixer
                if matcher(module, tags):
                    newext = fixer(extension)
                    if newext is EXCLUDE_EXT:
                        return
                    extension = newext or extension
            if self.language == 'cpp':
                extension.language = 'c++'
            build_extension.extensions = [extension]
            build_extension.build_temp = workdir
            build_extension.build_lib  = workdir
            build_extension.run()
        finally:
            os.chdir(cwd)

    def compile(self, test_directory, module, workdir, incdir,
                expect_errors, annotate):
        expected_errors = errors = ()
        if expect_errors:
            expected_errors = self.split_source_and_output(
                test_directory, module, workdir)
            test_directory = workdir

        if WITH_CYTHON:
            old_stderr = sys.stderr
            try:
                sys.stderr = ErrorWriter()
                self.run_cython(test_directory, module, workdir, incdir, annotate)
                errors = sys.stderr.geterrors()
            finally:
                sys.stderr = old_stderr

        if errors or expected_errors:
            try:
                for expected, error in zip(expected_errors, errors):
                    self.assertEquals(expected, error)
                if len(errors) < len(expected_errors):
                    expected_error = expected_errors[len(errors)]
                    self.assertEquals(expected_error, None)
                elif len(errors) > len(expected_errors):
                    unexpected_error = errors[len(expected_errors)]
                    self.assertEquals(None, unexpected_error)
            except AssertionError:
                print("\n=== Expected errors: ===")
                print('\n'.join(expected_errors))
                print("\n\n=== Got errors: ===")
                print('\n'.join(errors))
                print('\n')
                raise
        else:
            if not self.cython_only:
                self.run_distutils(test_directory, module, workdir, incdir)

class CythonRunTestCase(CythonCompileTestCase):
    def shortDescription(self):
        return "compiling (%s) and running %s" % (self.language, self.module)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        try:
            self.setUp()
            try:
                self.runCompileTest()
                self.run_tests(result)
            finally:
                check_thread_termination()
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

    def run_tests(self, result):
        if not self.cython_only:
            self.run_doctests(self.module, result)

    def run_doctests(self, module_name, result):
        def run_test(result):
            tests = doctest.DocTestSuite(module_name)
            tests.run(result)
        run_forked_test(result, run_test, self.shortDescription(), self.fork)


def run_forked_test(result, run_func, test_name, fork=True):
    if not fork or sys.version_info[0] >= 3 or not hasattr(os, 'fork'):
        run_func(result)
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
                tests = None
                try:
                    partial_result = PartialTestResult(result)
                    run_func(partial_result)
                    gc.collect()
                except Exception:
                    if tests is None:
                        # importing failed, try to fake a test class
                        tests = _FakeClass(
                            failureException=sys.exc_info()[1],
                            _shortDescription=test_name,
                            module_name=None)
                    partial_result.addError(tests, sys.exc_info())
                    result_code = 1
                output = open(result_file, 'wb')
                pickle.dump(partial_result.data(), output)
            except:
                traceback.print_exc()
        finally:
            try: output.close()
            except: pass
            os._exit(result_code)

    try:
        cid, result_code = os.waitpid(child_id, 0)
        module_name = test_name.split()[-1]
        # os.waitpid returns the child's result code in the
        # upper byte of result_code, and the signal it was
        # killed by in the lower byte
        if result_code & 255:
            raise Exception("Tests in module '%s' were unexpectedly killed by signal %d"%
                            (module_name, result_code & 255))
        result_code = result_code >> 8
        if result_code in (0,1):
            input = open(result_file, 'rb')
            try:
                PartialTestResult.join_results(result, pickle.load(input))
            finally:
                input.close()
        if result_code:
            raise Exception("Tests in module '%s' exited with status %d" %
                            (module_name, result_code))
    finally:
        try: os.unlink(result_file)
        except: pass

class PureDoctestTestCase(unittest.TestCase):
    def __init__(self, module_name, module_path):
        self.module_name = module_name
        self.module_path = module_path
        unittest.TestCase.__init__(self, 'run')

    def shortDescription(self):
        return "running pure doctests in %s" % self.module_name

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        loaded_module_name = 'pure_doctest__' + self.module_name
        result.startTest(self)
        try:
            self.setUp()

            import imp
            m = imp.load_source(loaded_module_name, self.module_path)
            try:
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

is_private_field = re.compile('^_[^_]').match

class _FakeClass(object):
    def __init__(self, **kwargs):
        self._shortDescription = kwargs.get('module_name')
        self.__dict__.update(kwargs)
    def shortDescription(self):
        return self._shortDescription

try: # Py2.7+ and Py3.2+
    from unittest.runner import _TextTestResult
except ImportError:
    from unittest import _TextTestResult

class PartialTestResult(_TextTestResult):
    def __init__(self, base_result):
        _TextTestResult.__init__(
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
        return (self.failures, self.errors, self.testsRun,
                self.stream.getvalue())

    def join_results(result, data):
        """Static method for merging the result back into the main
        result object.
        """
        failures, errors, tests_run, output = data
        if output:
            result.stream.write(output)
        result.errors.extend(errors)
        result.failures.extend(failures)
        result.testsRun += tests_run

    join_results = staticmethod(join_results)

    class _StringIO(StringIO):
        def writeln(self, line):
            self.write("%s\n" % line)


class CythonUnitTestCase(CythonRunTestCase):
    def shortDescription(self):
        return "compiling (%s) tests in %s" % (self.language, self.module)

    def run_tests(self, result):
        unittest.defaultTestLoader.loadTestsFromName(self.module).run(result)


class CythonPyregrTestCase(CythonRunTestCase):
    def setUp(self):
        CythonRunTestCase.setUp(self)
        from Cython.Compiler import Options
        Options.error_on_unknown_names = False

    def _run_unittest(self, result, *classes):
        """Run tests from unittest.TestCase-derived classes."""
        valid_types = (unittest.TestSuite, unittest.TestCase)
        suite = unittest.TestSuite()
        for cls in classes:
            if isinstance(cls, str):
                if cls in sys.modules:
                    suite.addTest(unittest.findTestCases(sys.modules[cls]))
                else:
                    raise ValueError("str arguments must be keys in sys.modules")
            elif isinstance(cls, valid_types):
                suite.addTest(cls)
            else:
                suite.addTest(unittest.makeSuite(cls))
        suite.run(result)

    def _run_doctest(self, result, module):
        self.run_doctests(module, result)

    def run_tests(self, result):
        try:
            from test import test_support as support
        except ImportError: # Py3k
            from test import support

        def run_test(result):
            def run_unittest(*classes):
                return self._run_unittest(result, *classes)
            def run_doctest(module, verbosity=None):
                return self._run_doctest(result, module)

            support.run_unittest = run_unittest
            support.run_doctest = run_doctest

            try:
                module = __import__(self.module)
                if hasattr(module, 'test_main'):
                    module.test_main()
            except (unittest.SkipTest, support.ResourceDenied):
                result.addSkip(self, 'ok')

        run_forked_test(result, run_test, self.shortDescription(), self.fork)

include_debugger = sys.version_info[:2] > (2, 5)

def collect_unittests(path, module_prefix, suite, selectors):
    def file_matches(filename):
        return filename.startswith("Test") and filename.endswith(".py")

    def package_matches(dirname):
        return dirname == "Tests"

    loader = unittest.TestLoader()

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
                    if not [ 1 for match in selectors if match(modulename) ]:
                        continue
                    module = __import__(modulename)
                    for x in modulename.split('.')[1:]:
                        module = getattr(module, x)
                    suite.addTests([loader.loadTestsFromModule(module)])



def collect_doctests(path, module_prefix, suite, selectors):
    def package_matches(dirname):
        if dirname == 'Debugger' and not include_debugger:
            return False
        return dirname not in ("Mac", "Distutils", "Plex")
    def file_matches(filename):
        filename, ext = os.path.splitext(filename)
        blacklist = ['libcython', 'libpython', 'test_libcython_in_gdb',
                     'TestLibCython']
        return (ext == '.py' and not
                '~' in filename and not
                '#' in filename and not
                filename.startswith('.') and not
                filename in blacklist)
    import doctest, types
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
                if 'in_gdb' in modulename:
                    # These should only be imported from gdb.
                    continue
                module = __import__(modulename)
                for x in modulename.split('.')[1:]:
                    module = getattr(module, x)
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

    def __init__(self, treefile, workdir, cleanup_workdir=True):
        self.name = os.path.splitext(os.path.basename(treefile))[0]
        self.treefile = treefile
        self.workdir = os.path.join(workdir, self.name)
        self.cleanup_workdir = cleanup_workdir
        cython_syspath = self.cython_root
        for path in sys.path[::-1]:
            if path.startswith(self.cython_root):
                # Py3 installation and refnanny build prepend their
                # fixed paths to sys.path => prefer that over the
                # generic one
                cython_syspath = path + os.pathsep + cython_syspath
        self.cython_syspath = cython_syspath
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "End-to-end %s" % self.name

    def setUp(self):
        from Cython.TestUtils import unpack_source_tree
        _, self.commands = unpack_source_tree(self.treefile, self.workdir)
        self.old_dir = os.getcwd()
        os.chdir(self.workdir)
        if self.workdir not in sys.path:
            sys.path.insert(0, self.workdir)

    def tearDown(self):
        if self.cleanup_workdir:
            for trial in range(5):
                try:
                    shutil.rmtree(self.workdir)
                except OSError:
                    time.sleep(0.1)
                else:
                    break
        os.chdir(self.old_dir)

    def runTest(self):
        commands = (self.commands
            .replace("CYTHON", "PYTHON %s" % os.path.join(self.cython_root, 'cython.py'))
            .replace("PYTHON", sys.executable))
        try:
            old_path = os.environ.get('PYTHONPATH')
            os.environ['PYTHONPATH'] = self.cython_syspath + os.pathsep + os.path.join(self.cython_syspath, (old_path or ''))
            for command in commands.split('\n'):
                if sys.version_info[:2] >= (2,4):
                    import subprocess
                    p = subprocess.Popen(commands,
                                         stderr=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         shell=True)
                    out, err = p.communicate()
                    res = p.returncode
                    if res != 0:
                        print(command)
                        print(out)
                        print(err)
                else:
                    res = os.system(command)
                self.assertEqual(0, res, "non-zero exit status")
        finally:
            if old_path:
                os.environ['PYTHONPATH'] = old_path
            else:
                del os.environ['PYTHONPATH']


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
        from distutils import sysconfig
        libname = sysconfig.get_config_var('LIBRARY')
        libdir = sysconfig.get_config_var('LIBDIR')
        if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
            libdir = os.path.join(os.path.dirname(sys.executable), '..', 'lib')
            if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
                libdir = os.path.join(libdir, 'python%d.%d' % sys.version_info[:2], 'config')
                if not os.path.isdir(libdir) or libname not in os.listdir(libdir):
                    # report the error for the original directory
                    libdir = sysconfig.get_config_var('LIBDIR')
        cython = 'cython.py'
        if sys.version_info[0] >=3 and CY3_DIR:
            cython = os.path.join(CY3_DIR, cython)
        cython = os.path.abspath(os.path.join('..', '..', cython))
        self.assert_(os.system(
            "make PYTHON='%s' CYTHON='%s' LIBDIR1='%s' test > make.output" % (sys.executable, cython, libdir)) == 0)
        try:
            os.remove('make.output')
        except OSError:
            pass

class MissingDependencyExcluder:
    def __init__(self, deps):
        # deps: { matcher func : module name }
        self.exclude_matchers = []
        for matcher, mod in deps.items():
            try:
                __import__(mod)
            except ImportError:
                self.exclude_matchers.append(string_selector(matcher))
        self.tests_missing_deps = []
    def __call__(self, testname, tags=None):
        for matcher in self.exclude_matchers:
            if matcher(testname, tags):
                self.tests_missing_deps.append(testname)
                return True
        return False

class VersionDependencyExcluder:
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

class FileListExcluder:

    def __init__(self, list_file):
        self.excludes = {}
        f = open(list_file)
        try:
            for line in f.readlines():
                line = line.strip()
                if line and line[0] != '#':
                    self.excludes[line.split()[0]] = True
        finally:
            f.close()

    def __call__(self, testname, tags=None):
        return testname in self.excludes or testname.split('.')[-1] in self.excludes

class TagsSelector:

    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
    
    def __call__(self, testname, tags=None):
        if tags is None:
            return False
        else:
            return self.value in tags[self.tag]

class RegExSelector:
    
    def __init__(self, pattern_string):
        self.pattern = re.compile(pattern_string, re.I|re.U)

    def __call__(self, testname, tags=None):
        return self.pattern.search(testname)

def string_selector(s):
    ix = s.find(':')
    if ix == -1:
        return RegExSelector(s)
    else:
        return TagsSelector(s[:ix], s[ix+1:])
        

def refactor_for_py3(distdir, cy3_dir):
    # need to convert Cython sources first
    import lib2to3.refactor
    from distutils.util import copydir_run_2to3
    fixers = [ fix for fix in lib2to3.refactor.get_fixers_from_package("lib2to3.fixes")
               if fix.split('fix_')[-1] not in ('next',)
               ]
    if not os.path.exists(cy3_dir):
        os.makedirs(cy3_dir)
    import distutils.log as dlog
    dlog.set_threshold(dlog.INFO)
    copydir_run_2to3(distdir, cy3_dir, fixer_names=fixers,
                     template = '''
                     global-exclude *
                     graft Cython
                     recursive-exclude Cython *
                     recursive-include Cython *.py *.pyx *.pxd
                     recursive-include Cython/Debugger/Tests *
                     include runtests.py
                     include cython.py
                     ''')
    sys.path.insert(0, cy3_dir)

    for keep_2x_file in KEEP_2X_FILES:
        destfile = os.path.join(cy3_dir, keep_2x_file)
        shutil.copy(keep_2x_file, destfile)

class PendingThreadsError(RuntimeError):
    pass

threads_seen = []

def check_thread_termination(ignore_seen=True):
    if threading is None: # no threading enabled in CPython
        return
    current = threading.currentThread()
    blocking_threads = []
    for t in threading.enumerate():
        if not t.isAlive() or t == current:
            continue
        t.join(timeout=2)
        if t.isAlive():
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

def main():

    DISTDIR = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--no-cleanup", dest="cleanup_workdir",
                      action="store_false", default=True,
                      help="do not delete the generated C files (allows passing --no-cython on next run)")
    parser.add_option("--no-cleanup-sharedlibs", dest="cleanup_sharedlibs",
                      action="store_false", default=True,
                      help="do not delete the generated shared libary files (allows manual module experimentation)")
    parser.add_option("--no-cython", dest="with_cython",
                      action="store_false", default=True,
                      help="do not run the Cython compiler, only the C compiler")
    parser.add_option("--compiler", dest="compiler", default=None,
                      help="C compiler type")
    parser.add_option("--no-c", dest="use_c",
                      action="store_false", default=True,
                      help="do not test C compilation")
    parser.add_option("--no-cpp", dest="use_cpp",
                      action="store_false", default=True,
                      help="do not test C++ compilation")
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
    parser.add_option("-C", "--coverage", dest="coverage",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler")
    parser.add_option("--coverage-xml", dest="coverage_xml",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler in XML format")
    parser.add_option("--coverage-html", dest="coverage_html",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler in HTML format")
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
    parser.add_option("-3", dest="language_level",
                      action="store_const", const=3, default=2,
                      help="set language level to Python 3 (useful for running the CPython regression tests)'")
    parser.add_option("--xml-output", dest="xml_output_dir", metavar="DIR",
                      help="write test results in XML to directory DIR")
    parser.add_option("--exit-ok", dest="exit_ok", default=False,
                      action="store_true",
                      help="exit without error code even on test failures")
    parser.add_option("--root-dir", dest="root_dir", default=os.path.join(DISTDIR, 'tests'),
                      help="working directory")
    parser.add_option("--work-dir", dest="work_dir", default=os.path.join(os.getcwd(), 'BUILD'),
                      help="working directory")

    options, cmd_args = parser.parse_args()

    ROOTDIR = os.path.abspath(options.root_dir)
    WORKDIR = os.path.abspath(options.work_dir)

    if sys.version_info[0] >= 3:
        options.doctests = False
        if options.with_cython:
            try:
                # try if Cython is installed in a Py3 version
                import Cython.Compiler.Main
            except Exception:
                # back out anything the import process loaded, then
                # 2to3 the Cython sources to make them re-importable
                cy_modules = [ name for name in sys.modules
                               if name == 'Cython' or name.startswith('Cython.') ]
                for name in cy_modules:
                    del sys.modules[name]
                # hasn't been refactored yet - do it now
                global CY3_DIR
                CY3_DIR = cy3_dir = os.path.join(WORKDIR, 'Cy3')
                if sys.version_info >= (3,1):
                    refactor_for_py3(DISTDIR, cy3_dir)
                elif os.path.isdir(cy3_dir):
                    sys.path.insert(0, cy3_dir)
                else:
                    options.with_cython = False

    WITH_CYTHON = options.with_cython

    if options.coverage or options.coverage_xml or options.coverage_html:
        if not WITH_CYTHON:
            options.coverage = options.coverage_xml = options.coverage_html = False
        else:
            from coverage import coverage as _coverage
            coverage = _coverage(branch=True)
            coverage.erase()
            coverage.start()

    if WITH_CYTHON:
        global CompilationOptions, pyrex_default_options, cython_compile
        from Cython.Compiler.Main import \
            CompilationOptions, \
            default_options as pyrex_default_options, \
            compile as cython_compile
        from Cython.Compiler import Errors
        Errors.LEVEL = 0 # show all warnings
        from Cython.Compiler import Options
        Options.generate_cleanup_code = 3   # complete cleanup code
        from Cython.Compiler import DebugFlags
        DebugFlags.debug_temp_code_comments = 1

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

    sys.stderr.write("Python %s\n" % sys.version)
    sys.stderr.write("\n")
    if WITH_CYTHON:
        from Cython.Compiler.Version import version
        sys.stderr.write("Running tests against Cython %s\n" % version)
    else:
        sys.stderr.write("Running tests without Cython.\n")

    if options.with_refnanny:
        from pyximport.pyxbuild import pyx_to_dll
        libpath = pyx_to_dll(os.path.join("Cython", "Runtime", "refnanny.pyx"),
                             build_in_temp=True,
                             pyxbuild_dir=os.path.join(WORKDIR, "support"))
        sys.path.insert(0, os.path.split(libpath)[0])
        CFLAGS.append("-DCYTHON_REFNANNY=1")

    if options.xml_output_dir and options.fork:
        # doesn't currently work together
        sys.stderr.write("Disabling forked testing to support XML test output\n")
        options.fork = False

    if WITH_CYTHON and options.language_level == 3:
        sys.stderr.write("Using Cython language level 3.\n")

    sys.stderr.write("\n")

    test_bugs = False
    if options.tickets:
        for ticket_number in options.tickets:
            test_bugs = True
            cmd_args.append('ticket:%s' % ticket_number)
    if not test_bugs:
        for selector in cmd_args:
            if selector.startswith('bugs'):
                test_bugs = True

    import re
    selectors = [ string_selector(r) for r in cmd_args ]
    if not selectors:
        selectors = [ lambda x, tags=None: True ]

    # Chech which external modules are not present and exclude tests
    # which depends on them (by prefix)

    missing_dep_excluder = MissingDependencyExcluder(EXT_DEP_MODULES)
    version_dep_excluder = VersionDependencyExcluder(VER_DEP_MODULES)
    exclude_selectors = [missing_dep_excluder, version_dep_excluder] # want to pring msg at exit

    if options.exclude:
        exclude_selectors += [ string_selector(r) for r in options.exclude ]

    if not test_bugs:
        exclude_selectors += [ FileListExcluder(os.path.join(ROOTDIR, "bugs.txt")) ]

    if sys.platform in ['win32', 'cygwin'] and sys.version_info < (2,6):
        exclude_selectors += [ lambda x: x == "run.specialfloat" ]

    global COMPILER
    if options.compiler:
        COMPILER = options.compiler
    languages = []
    if options.use_c:
        languages.append('c')
    if options.use_cpp:
        languages.append('cpp')

    test_suite = unittest.TestSuite()

    if options.unittests:
        collect_unittests(UNITTEST_ROOT, UNITTEST_MODULE + ".", test_suite, selectors)

    if options.doctests:
        collect_doctests(UNITTEST_ROOT, UNITTEST_MODULE + ".", test_suite, selectors)

    if options.filetests and languages:
        filetests = TestBuilder(ROOTDIR, WORKDIR, selectors, exclude_selectors,
                                options.annotate_source, options.cleanup_workdir,
                                options.cleanup_sharedlibs, options.pyregr,
                                options.cython_only, languages, test_bugs,
                                options.fork, options.language_level)
        test_suite.addTest(filetests.build_suite())

    if options.system_pyregr and languages:
        sys_pyregr_dir = os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3], 'test')
        if os.path.isdir(sys_pyregr_dir):
            filetests = TestBuilder(ROOTDIR, WORKDIR, selectors, exclude_selectors,
                                    options.annotate_source, options.cleanup_workdir,
                                    options.cleanup_sharedlibs, True,
                                    options.cython_only, languages, test_bugs,
                                    options.fork, sys.version_info[0])
            sys.stderr.write("Including CPython regression tests in %s\n" % sys_pyregr_dir)
            test_suite.addTest(filetests.handle_directory(sys_pyregr_dir, 'pyregr'))

    if options.xml_output_dir:
        from Cython.Tests.xmlrunner import XMLTestRunner
        test_runner = XMLTestRunner(output=options.xml_output_dir,
                                    verbose=options.verbosity > 0)
    else:
        test_runner = unittest.TextTestRunner(verbosity=options.verbosity)

    result = test_runner.run(test_suite)

    if options.coverage or options.coverage_xml or options.coverage_html:
        coverage.stop()
        ignored_modules = ('Options', 'Version', 'DebugFlags', 'CmdLine')
        modules = [ module for name, module in sys.modules.items()
                    if module is not None and
                    name.startswith('Cython.Compiler.') and
                    name[len('Cython.Compiler.'):] not in ignored_modules ]
        if options.coverage:
            coverage.report(modules, show_missing=0)
        if options.coverage_xml:
            coverage.xml_report(modules, outfile="coverage-report.xml")
        if options.coverage_html:
            coverage.html_report(modules, directory="coverage-report-html")

    if missing_dep_excluder.tests_missing_deps:
        sys.stderr.write("Following tests excluded because of missing dependencies on your system:\n")
        for test in missing_dep_excluder.tests_missing_deps:
            sys.stderr.write("   %s\n" % test)

    if options.with_refnanny:
        import refnanny
        sys.stderr.write("\n".join([repr(x) for x in refnanny.reflog]))

    print("ALL DONE")

    if options.exit_ok:
        return_code = 0
    else:
        return_code = not result.wasSuccessful()

    try:
        check_thread_termination(ignore_seen=False)
        sys.exit(return_code)
    except PendingThreadsError:
        # normal program exit won't kill the threads, do it the hard way here
        os._exit(return_code)

if __name__ == '__main__':
    try:
        main()
    except SystemExit: # <= Py2.4 ...
        raise
    except Exception:
        traceback.print_exc()
        try:
            check_thread_termination(ignore_seen=False)
        except PendingThreadsError:
            # normal program exit won't kill the threads, do it the hard way here
            os._exit(1)
