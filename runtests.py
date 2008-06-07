#!/usr/bin/python

import os, sys, re, shutil, unittest, doctest

WITH_CYTHON = True

from distutils.dist import Distribution
from distutils.core import Extension
from distutils.command.build_ext import build_ext
distutils_distro = Distribution()

TEST_DIRS = ['compile', 'errors', 'run']
TEST_RUN_DIRS = ['run']

INCLUDE_DIRS = [ d for d in os.getenv('INCLUDE', '').split(os.pathsep) if d ]
CFLAGS = os.getenv('CFLAGS', '').split()


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
    def __init__(self, rootdir, workdir, selectors, annotate, cleanup_workdir):
        self.rootdir = rootdir
        self.workdir = workdir
        self.selectors = selectors
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir

    def build_suite(self):
        suite = unittest.TestSuite()
        filenames = os.listdir(self.rootdir)
        filenames.sort()
        for filename in filenames:
            if not WITH_CYTHON and filename == "errors":
                # we won't get any errors without running Cython
                continue
            path = os.path.join(self.rootdir, filename)
            if os.path.isdir(path) and filename in TEST_DIRS:
                suite.addTest(
                    self.handle_directory(path, filename))
        return suite

    def handle_directory(self, path, context):
        workdir = os.path.join(self.workdir, context)
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        if workdir not in sys.path:
            sys.path.insert(0, workdir)

        expect_errors = (context == 'errors')
        suite = unittest.TestSuite()
        filenames = os.listdir(path)
        filenames.sort()
        for filename in filenames:
            if not filename.endswith(".pyx"):
                continue
            module = filename[:-4]
            fqmodule = "%s.%s" % (context, module)
            if not [ 1 for match in self.selectors
                     if match(fqmodule) ]:
                continue
            if context in TEST_RUN_DIRS:
                test = CythonRunTestCase(
                    path, workdir, module,
                    annotate=self.annotate,
                    cleanup_workdir=self.cleanup_workdir)
            else:
                test = CythonCompileTestCase(
                    path, workdir, module,
                    expect_errors=expect_errors,
                    annotate=self.annotate,
                    cleanup_workdir=self.cleanup_workdir)
            suite.addTest(test)
        return suite

class CythonCompileTestCase(unittest.TestCase):
    def __init__(self, directory, workdir, module,
                 expect_errors=False, annotate=False, cleanup_workdir=True):
        self.directory = directory
        self.workdir = workdir
        self.module = module
        self.expect_errors = expect_errors
        self.annotate = annotate
        self.cleanup_workdir = cleanup_workdir
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "compiling " + self.module

    def tearDown(self):
        cleanup_c_files = WITH_CYTHON and self.cleanup_workdir
        if os.path.exists(self.workdir):
            for rmfile in os.listdir(self.workdir):
                if not cleanup_c_files and rmfile[-2:] in (".c", ".h"):
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
        self.compile(self.directory, self.module, self.workdir,
                     self.directory, self.expect_errors, self.annotate)

    def split_source_and_output(self, directory, module, workdir):
        source_and_output = open(os.path.join(directory, module + '.pyx'), 'rU')
        out = open(os.path.join(workdir, module + '.pyx'), 'w')
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
        source = os.path.join(directory, module + '.pyx')
        target = os.path.join(targetdir, module + '.c')
        options = CompilationOptions(
            pyrex_default_options,
            include_path = include_dirs,
            output_file = target,
            annotate = annotate,
            use_listing_file = False, cplus = False, generate_pxi = False)
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

            extension = Extension(
                module,
                sources = [module + '.c'],
                extra_compile_args = CFLAGS,
                )
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
            for expected, error in zip(expected_errors, errors):
                self.assertEquals(expected, error)
            if len(errors) < len(expected_errors):
                expected_error = expected_errors[len(errors)]
                self.assertEquals(expected_error, None)
            elif len(errors) > len(expected_errors):
                unexpected_error = errors[len(expected_errors)]
                self.assertEquals(None, unexpected_error)
        else:
            self.run_distutils(module, workdir, incdir)

class CythonRunTestCase(CythonCompileTestCase):
    def shortDescription(self):
        return "compiling and running " + self.module

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        try:
            self.runTest()
            doctest.DocTestSuite(self.module).run(result)
        except Exception:
            result.addError(self, sys.exc_info())
            result.stopTest(self)
        try:
            self.tearDown()
        except Exception:
            pass

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--no-cleanup", dest="cleanup_workdir",
                      action="store_false", default=True,
                      help="do not delete the generated C files (allows passing --no-cython on next run)")
    parser.add_option("--no-cython", dest="with_cython",
                      action="store_false", default=True,
                      help="do not run the Cython compiler, only the C compiler")
    parser.add_option("-C", "--coverage", dest="coverage",
                      action="store_true", default=False,
                      help="collect source coverage data for the Compiler")
    parser.add_option("-A", "--annotate", dest="annotate_source",
                      action="store_true", default=False,
                      help="generate annotated HTML versions of the test source files")
    parser.add_option("-v", "--verbose", dest="verbosity",
                      action="count", default=0,
                      help="display test progress, pass twice to print test names")

    options, cmd_args = parser.parse_args()

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

    # RUN ALL TESTS!
    ROOTDIR = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]), 'tests')
    WORKDIR = os.path.join(os.getcwd(), 'BUILD')
    if WITH_CYTHON:
        if os.path.exists(WORKDIR):
            shutil.rmtree(WORKDIR, ignore_errors=True)
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    if WITH_CYTHON:
        from Cython.Compiler.Version import version
        print("Running tests against Cython %s" % version)
    else:
        print("Running tests without Cython.")
    print("Python %s" % sys.version)
    print("")

    import re
    selectors = [ re.compile(r, re.I|re.U).search for r in cmd_args ]
    if not selectors:
        selectors = [ lambda x:True ]

    tests = TestBuilder(ROOTDIR, WORKDIR, selectors,
                        options.annotate_source, options.cleanup_workdir)
    test_suite = tests.build_suite()

    unittest.TextTestRunner(verbosity=options.verbosity).run(test_suite)

    if options.coverage:
        coverage.stop()
        ignored_modules = ('Options', 'Version', 'DebugFlags')
        modules = [ module for name, module in sys.modules.items()
                    if module is not None and
                    name.startswith('Cython.Compiler.') and 
                    name[len('Cython.Compiler.'):] not in ignored_modules ]
        coverage.report(modules, show_missing=0)
