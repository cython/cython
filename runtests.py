#!/usr/bin/python

import os
import sys
import re
import gc
import codecs
import shutil
import unittest
import doctest
import operator
import tempfile
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import cPickle as pickle
except ImportError:
    import pickle


WITH_CYTHON = True

from distutils.dist import Distribution
from distutils.core import Extension
from distutils.command.build_ext import build_ext as _build_ext
distutils_distro = Distribution()

TEST_DIRS = ['compile', 'errors', 'run', 'pyregr']
TEST_RUN_DIRS = ['run', 'pyregr']

# Lists external modules, and a matcher matching tests
# which should be excluded if the module is not present.
EXT_DEP_MODULES = {
    'numpy' : re.compile('.*\.numpy_.*').match
}

def get_numpy_include_dirs():
    import numpy
    return [numpy.get_include()]

EXT_DEP_INCLUDES = [
    # test name matcher , callable returning list
    (re.compile('numpy_.*').match, get_numpy_include_dirs),
]

VER_DEP_MODULES = {
# such as:
#    (2,4) : (operator.le, lambda x: x in ['run.set']),
    (3,): (operator.ge, lambda x: x in ['run.non_future_division',
                                        'compile.extsetslice',
                                        'compile.extdelslice']),
}

INCLUDE_DIRS = [ d for d in os.getenv('INCLUDE', '').split(os.pathsep) if d ]
CFLAGS = os.getenv('CFLAGS', '').split()

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
                 languages, test_bugs, fork):
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

    def build_suite(self):
        suite = unittest.TestSuite()
        test_dirs = TEST_DIRS
        filenames = os.listdir(self.rootdir)
        filenames.sort()
        for filename in filenames:
            if not WITH_CYTHON and filename == "errors":
                # we won't get any errors without running Cython
                continue
            path = os.path.join(self.rootdir, filename)
            if os.path.isdir(path) and filename in test_dirs:
                if filename == 'pyregr' and not self.with_pyregr:
                    continue
                suite.addTest(
                    self.handle_directory(path, filename))
        if sys.platform not in ['win32'] and sys.version_info[0] < 3:
            # Non-Windows makefile, can't run Cython under Py3.
            if [1 for selector in self.selectors if selector("embedded")]:
                suite.addTest(unittest.makeSuite(EmbedTest))
        return suite

    def handle_directory(self, path, context):
        workdir = os.path.join(self.workdir, context)
        if not os.path.exists(workdir):
            os.makedirs(workdir)

        expect_errors = (context == 'errors')
        suite = unittest.TestSuite()
        filenames = os.listdir(path)
        filenames.sort()
        for filename in filenames:
            if not (filename.endswith(".pyx") or filename.endswith(".py")):
                continue
            if filename.startswith('.'): continue # certain emacs backup files
            if context == 'pyregr' and not filename.startswith('test_'):
                continue
            module = os.path.splitext(filename)[0]
            fqmodule = "%s.%s" % (context, module)
            if not [ 1 for match in self.selectors
                     if match(fqmodule) ]:
                continue
            if self.exclude_selectors:
                if [1 for match in self.exclude_selectors if match(fqmodule)]:
                    continue
            if context in TEST_RUN_DIRS:
                if module.startswith("test_"):
                    test_class = CythonUnitTestCase
                else:
                    test_class = CythonRunTestCase
            else:
                test_class = CythonCompileTestCase
            for test in self.build_tests(test_class, path, workdir,
                                         module, expect_errors):
                suite.addTest(test)
        return suite

    def build_tests(self, test_class, path, workdir, module, expect_errors):
        if expect_errors:
            languages = self.languages[:1]
        else:
            languages = self.languages
        if 'cpp' in module and 'c' in languages:
            languages = list(languages)
            languages.remove('c')
        tests = [ self.build_test(test_class, path, workdir, module,
                                  language, expect_errors)
                  for language in languages ]
        return tests

    def build_test(self, test_class, path, workdir, module,
                   language, expect_errors):
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
                          fork=self.fork)

class CythonCompileTestCase(unittest.TestCase):
    def __init__(self, directory, workdir, module, language='c',
                 expect_errors=False, annotate=False, cleanup_workdir=True,
                 cleanup_sharedlibs=True, cython_only=False, fork=True):
        self.directory = directory
        self.workdir = workdir
        self.module = module
        self.language = language
        self.expect_errors = expect_errors
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir
        self.cleanup_sharedlibs = cleanup_sharedlibs
        self.cython_only = cython_only
        self.fork = fork
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "compiling (%s) %s" % (self.language, self.module)

    def setUp(self):
        if self.workdir not in sys.path:
            sys.path.insert(0, self.workdir)

    def tearDown(self):
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
        self.compile(self.directory, self.module, self.workdir,
                     self.directory, self.expect_errors, self.annotate)

    def find_module_source_file(self, source_file):
        if not os.path.exists(source_file):
            source_file = source_file[:-1]
        return source_file

    def build_target_filename(self, module_name):
        target = '%s.%s' % (module_name, self.language)
        return target

    def split_source_and_output(self, directory, module, workdir):
        source_file = os.path.join(directory, module) + '.pyx'
        source_and_output = codecs.open(
            self.find_module_source_file(source_file), 'rU', 'ISO-8859-1')
        out = codecs.open(os.path.join(workdir, module + '.pyx'),
                          'w', 'ISO-8859-1')
        for line in source_and_output:
            last_line = line
            if line.startswith("_ERRORS"):
                out.close()
                out = ErrorWriter()
            else:
                out.write(line)
        try:
            geterrors = out.geterrors
        except AttributeError:
            return []
        else:
            return geterrors()

    def run_cython(self, directory, module, targetdir, incdir, annotate):
        include_dirs = INCLUDE_DIRS[:]
        if incdir:
            include_dirs.append(incdir)
        source = self.find_module_source_file(
            os.path.join(directory, module + '.pyx'))
        target = os.path.join(targetdir, self.build_target_filename(module))
        options = CompilationOptions(
            pyrex_default_options,
            include_path = include_dirs,
            output_file = target,
            annotate = annotate,
            use_listing_file = False,
            cplus = self.language == 'cpp',
            generate_pxi = False,
            evaluate_tree_assertions = True,
            )
        cython_compile(source, options=options,
                       full_module_name=module)

    def run_distutils(self, module, workdir, incdir):
        cwd = os.getcwd()
        os.chdir(workdir)
        try:
            build_extension = build_ext(distutils_distro)
            build_extension.include_dirs = INCLUDE_DIRS[:]
            if incdir:
                build_extension.include_dirs.append(incdir)
            build_extension.finalize_options()
            ext_include_dirs = []
            for match, get_additional_include_dirs in EXT_DEP_INCLUDES:
                if match(module):
                    ext_include_dirs += get_additional_include_dirs()
            extension = Extension(
                module,
                sources = [self.build_target_filename(module)],
                include_dirs = ext_include_dirs,
                extra_compile_args = CFLAGS,
                )
            if self.language == 'cpp':
                extension.language = 'c++'
            build_extension.extensions = [extension]
            build_extension.build_temp = workdir
            build_extension.build_lib  = workdir
            build_extension.run()
        finally:
            os.chdir(cwd)

    def compile(self, directory, module, workdir, incdir,
                expect_errors, annotate):
        expected_errors = errors = ()
        if expect_errors:
            expected_errors = self.split_source_and_output(
                directory, module, workdir)
            directory = workdir

        if WITH_CYTHON:
            old_stderr = sys.stderr
            try:
                sys.stderr = ErrorWriter()
                self.run_cython(directory, module, workdir, incdir, annotate)
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
                self.run_distutils(module, workdir, incdir)

class CythonRunTestCase(CythonCompileTestCase):
    def shortDescription(self):
        return "compiling (%s) and running %s" % (self.language, self.module)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        try:
            self.setUp()
            self.runCompileTest()
            if not self.cython_only:
                self.run_doctests(self.module, result)
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

    def run_doctests(self, module_name, result):
        if sys.version_info[0] >= 3 or not hasattr(os, 'fork') or not self.fork:
            doctest.DocTestSuite(module_name).run(result)
            gc.collect()
            return

        # fork to make sure we do not keep the tested module loaded
        result_handle, result_file = tempfile.mkstemp()
        child_id = os.fork()
        if not child_id:
            result_code = 0
            try:
                output = os.fdopen(result_handle, 'wb')
                tests = None
                try:
                    partial_result = PartialTestResult(result)
                    tests = doctest.DocTestSuite(module_name)
                    tests.run(partial_result)
                    gc.collect()
                except Exception:
                    if tests is None:
                        # importing failed, try to fake a test class
                        tests = _FakeClass(
                            failureException=None,
                            shortDescription = self.shortDescription,
                            **{module_name: None})
                    partial_result.addError(tests, sys.exc_info())
                    result_code = 1
                pickle.dump(partial_result.data(), output)
            except:
                import traceback
                traceback.print_exc()
            finally:
                try: output.close()
                except: pass
                os._exit(result_code)

        try:
            cid, result_code = os.waitpid(child_id, 0)
            if result_code in (0,1):
                input = open(result_file, 'rb')
                try:
                    PartialTestResult.join_results(result, pickle.load(input))
                finally:
                    input.close()
            if result_code:
                raise Exception("Tests in module '%s' exited with status %d" %
                                (module_name, result_code >> 8))
        finally:
            try: os.unlink(result_file)
            except: pass


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
                else:
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
        errors, failures, tests_run, output = data
        if output:
            result.stream.write(output)
        result.errors.extend(errors)
        result.failures.extend(failures)
        result.testsRun += tests_run

    join_results = staticmethod(join_results)

    class _StringIO(StringIO):
        def writeln(self, line):
            self.write("%s\n" % line)


class CythonUnitTestCase(CythonCompileTestCase):
    def shortDescription(self):
        return "compiling (%s) tests in %s" % (self.language, self.module)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        try:
            self.setUp()
            self.runCompileTest()
            unittest.defaultTestLoader.loadTestsFromName(self.module).run(result)
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

def collect_unittests(path, module_prefix, suite, selectors):
    def file_matches(filename):
        return filename.startswith("Test") and filename.endswith(".py")

    def package_matches(dirname):
        return dirname == "Tests"

    loader = unittest.TestLoader()

    skipped_dirs = []

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
        return dirname not in ("Mac", "Distutils", "Plex")
    def file_matches(filename):
        return (filename.endswith(".py") and not ('~' in filename
                or '#' in filename or filename.startswith('.')))
    import doctest, types
    for dirpath, dirnames, filenames in os.walk(path):
        parentname = os.path.split(dirpath)[-1]
        if package_matches(parentname):
            for f in filenames:
                if file_matches(f):
                    if not f.endswith('.py'): continue
                    filepath = os.path.join(dirpath, f)[:-len(".py")]
                    modulename = module_prefix + filepath[len(path)+1:].replace(os.path.sep, '.')
                    if not [ 1 for match in selectors if match(modulename) ]:
                        continue
                    module = __import__(modulename)
                    for x in modulename.split('.')[1:]:
                        module = getattr(module, x)
                    if hasattr(module, "__doc__") or hasattr(module, "__test__"):
                        try:
                            suite.addTest(doctest.DocTestSuite(module))
                        except ValueError: # no tests
                            pass

# TODO: Support cython_freeze needed here as well.
# TODO: Windows support.

class EmbedTest(unittest.TestCase):
    
    working_dir = "Demos/embed"
    
    def setUp(self):
        self.old_dir = os.getcwd()
        os.chdir(self.working_dir)
        os.system("make clean > /dev/null")
    
    def tearDown(self):
        try:
            os.system("make clean > /dev/null")
        except:
            pass
        os.chdir(self.old_dir)
        
    def test_embed(self):
        self.assert_(os.system("make test > make.output") == 0)

class MissingDependencyExcluder:
    def __init__(self, deps):
        # deps: { module name : matcher func }
        self.exclude_matchers = []
        for mod, matcher in deps.items():
            try:
                __import__(mod)
            except ImportError:
                self.exclude_matchers.append(matcher)
        self.tests_missing_deps = []
    def __call__(self, testname):
        for matcher in self.exclude_matchers:
            if matcher(testname):
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
    def __call__(self, testname):
        for matcher in self.exclude_matchers:
            if matcher(testname):
                self.tests_missing_deps.append(testname)
                return True
        return False

class FileListExcluder:

    def __init__(self, list_file):
        self.excludes = {}
        for line in open(list_file).readlines():
            line = line.strip()
            if line and line[0] != '#':
                self.excludes[line.split()[0]] = True
                
    def __call__(self, testname):
        return testname.split('.')[-1] in self.excludes

if __name__ == '__main__':
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
                      help="a bug ticket number to run the respective test in 'tests/bugs'")

    options, cmd_args = parser.parse_args()

    DISTDIR = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
    ROOTDIR = os.path.join(DISTDIR, 'tests')
    WORKDIR = os.path.join(os.getcwd(), 'BUILD')

    if sys.version_info >= (3,1):
        options.doctests    = False
        options.unittests   = False
        options.pyregr      = False
        if options.with_cython:
            # need to convert Cython sources first
            import lib2to3.refactor
            from distutils.util import copydir_run_2to3
            fixers = [ fix for fix in lib2to3.refactor.get_fixers_from_package("lib2to3.fixes")
                       if fix.split('fix_')[-1] not in ('next',)
                       ]
            cy3_dir = os.path.join(WORKDIR, 'Cy3')
            if not os.path.exists(cy3_dir):
                os.makedirs(cy3_dir)
            import distutils.log as dlog
            dlog.set_threshold(dlog.DEBUG)
            copydir_run_2to3(DISTDIR, cy3_dir, fixer_names=fixers,
                             template = '''
                             global-exclude *
                             graft Cython
                             recursive-exclude Cython *
                             recursive-include Cython *.py *.pyx *.pxd
                             ''')
            sys.path.insert(0, cy3_dir)
    elif sys.version_info[0] >= 3:
        # make sure we do not import (or run) Cython itself
        options.with_cython = False
        options.doctests    = False
        options.unittests   = False
        options.pyregr      = False

    if options.coverage:
        import coverage
        coverage.erase()
        coverage.start()

    WITH_CYTHON = options.with_cython

    if WITH_CYTHON:
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
    UNITTEST_ROOT = os.path.join(os.getcwd(), UNITTEST_MODULE)
    if WITH_CYTHON:
        if os.path.exists(WORKDIR):
            for path in os.listdir(WORKDIR):
                if path in ("support", "Cy3"): continue
                shutil.rmtree(os.path.join(WORKDIR, path), ignore_errors=True)
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    if WITH_CYTHON:
        from Cython.Compiler.Version import version
        sys.stderr.write("Running tests against Cython %s\n" % version)
    else:
        sys.stderr.write("Running tests without Cython.\n")
    sys.stderr.write("Python %s\n" % sys.version)
    sys.stderr.write("\n")

    if options.with_refnanny:
        from pyximport.pyxbuild import pyx_to_dll
        libpath = pyx_to_dll(os.path.join("Cython", "Runtime", "refnanny.pyx"),
                             build_in_temp=True,
                             pyxbuild_dir=os.path.join(WORKDIR, "support"))
        sys.path.insert(0, os.path.split(libpath)[0])
        CFLAGS.append("-DCYTHON_REFNANNY=1")

    test_bugs = False
    if options.tickets:
        for ticket_number in options.tickets:
            test_bugs = True
            cmd_args.append('.*T%s$' % ticket_number)
    if not test_bugs:
        for selector in cmd_args:
            if selector.startswith('bugs'):
                test_bugs = True

    import re
    selectors = [ re.compile(r, re.I|re.U).search for r in cmd_args ]
    if not selectors:
        selectors = [ lambda x:True ]

    # Chech which external modules are not present and exclude tests
    # which depends on them (by prefix)

    missing_dep_excluder = MissingDependencyExcluder(EXT_DEP_MODULES) 
    version_dep_excluder = VersionDependencyExcluder(VER_DEP_MODULES) 
    exclude_selectors = [missing_dep_excluder, version_dep_excluder] # want to pring msg at exit

    if options.exclude:
        exclude_selectors += [ re.compile(r, re.I|re.U).search for r in options.exclude ]
    
    if not test_bugs:
        exclude_selectors += [ FileListExcluder("tests/bugs.txt") ]
    
    if sys.platform in ['win32', 'cygwin'] and sys.version_info < (2,6):
        exclude_selectors += [ lambda x: x == "run.specialfloat" ]

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
                                options.fork)
        test_suite.addTest(filetests.build_suite())

    if options.system_pyregr and languages:
        filetests = TestBuilder(ROOTDIR, WORKDIR, selectors, exclude_selectors,
                                options.annotate_source, options.cleanup_workdir,
                                options.cleanup_sharedlibs, True,
                                options.cython_only, languages, test_bugs,
                                options.fork)
        test_suite.addTest(
            filetests.handle_directory(
                os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3], 'test'),
                'pyregr'))

    unittest.TextTestRunner(verbosity=options.verbosity).run(test_suite)

    if options.coverage:
        coverage.stop()
        ignored_modules = ('Options', 'Version', 'DebugFlags', 'CmdLine')
        modules = [ module for name, module in sys.modules.items()
                    if module is not None and
                    name.startswith('Cython.Compiler.') and 
                    name[len('Cython.Compiler.'):] not in ignored_modules ]
        coverage.report(modules, show_missing=0)

    if missing_dep_excluder.tests_missing_deps:
        sys.stderr.write("Following tests excluded because of missing dependencies on your system:\n")
        for test in missing_dep_excluder.tests_missing_deps:
            sys.stderr.write("   %s\n" % test)

    if options.with_refnanny:
        import refnanny
        sys.stderr.write("\n".join([repr(x) for x in refnanny.reflog]))
