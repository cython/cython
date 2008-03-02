#!/usr/bin/python

import os, sys, unittest, doctest

from Cython.Distutils.build_ext import build_ext
from Cython.Distutils.extension import Extension

from distutils.dist import Distribution
distutils_distro = Distribution()

TEST_DIRS = ['compile', 'run']
TEST_RUN_DIRS = ['run']

INCLUDE_DIRS = os.getenv('INCLUDE', '').split(os.pathsep)
CFLAGS = os.getenv('CFLAGS', '').split()

class TestBuilder(object):
    def __init__(self, rootdir, workdir, selectors):
        self.rootdir = rootdir
        self.workdir = workdir
        self.selectors = selectors

    def build_suite(self):
        suite = unittest.TestSuite()
        for filename in os.listdir(self.rootdir):
            path = os.path.join(self.rootdir, filename)
            if os.path.isdir(path) and filename in TEST_DIRS:
                suite.addTest(
                    self.handle_directory(path, filename))
        return suite

    def handle_directory(self, path, context):
        suite = unittest.TestSuite()
        for filename in os.listdir(path):
            if not filename.endswith(".pyx"):
                continue
            module = filename[:-4]
            fqmodule = "%s.%s" % (context, module)
            if not [ 1 for match in self.selectors
                     if match(fqmodule) ]:
                continue
            suite.addTest(
                CythonCompileTestCase(path, self.workdir, module))
            if context in TEST_RUN_DIRS:
                suite.addTest(
                    CythonRunTestCase(self.workdir, module))
        return suite

class CythonCompileTestCase(unittest.TestCase):
    def __init__(self, directory, workdir, module):
        self.directory = directory
        self.workdir = workdir
        self.module = module
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "compiling " + self.module

    def runTest(self):
        self.compile(self.directory, self.module, self.workdir)

    def compile(self, directory, module, workdir):
        build_extension = build_ext(distutils_distro)
        build_extension.include_dirs = INCLUDE_DIRS[:]
        build_extension.include_dirs.append(directory)
        build_extension.finalize_options()

        extension = Extension(
            module,
            sources = [os.path.join(directory, module + '.pyx')],
            extra_compile_args = CFLAGS,
            pyrex_c_in_temp = 1
            )
        build_extension.extensions = [extension]
        build_extension.build_temp = workdir
        build_extension.build_lib  = workdir
        build_extension.pyrex_c_in_temp = 1
        build_extension.run()

class CythonRunTestCase(unittest.TestCase):
    def __init__(self, rootdir, module):
        self.rootdir, self.module = rootdir, module
        unittest.TestCase.__init__(self)

    def shortDescription(self):
        return "running " + self.module

    def runTest(self):
        self.run(self)

    def run(self, result=None):
        sys.path.insert(0, self.rootdir)
        if result is None: result = self.defaultTestResult()
        try:
            try:
                doctest.DocTestSuite(self.module).run(result)
            except ImportError:
                result.startTest(self)
                result.addFailure(self, sys.exc_info())
                result.stopTest(self)
        except Exception:
            result.startTest(self)
            result.addError(self, sys.exc_info())
            result.stopTest(self)

if __name__ == '__main__':
    # RUN ALL TESTS!
    ROOTDIR = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]), 'tests')
    WORKDIR = os.path.join(os.getcwd(), 'BUILD')
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    try:
        sys.argv.remove("-C")
    except ValueError:
        coverage = None
    else:
        import coverage
        coverage.erase()

    import re
    selectors = [ re.compile(r, re.I).search for r in sys.argv[1:] ]
    if not selectors:
        selectors = [ lambda x:True ]

    tests = TestBuilder(ROOTDIR, WORKDIR, selectors)
    test_suite = tests.build_suite()

    if coverage is not None:
        coverage.start()

    unittest.TextTestRunner(verbosity=2).run(test_suite)

    if coverage is not None:
        coverage.stop()
        ignored_modules = ('Options', 'Version', 'DebugFlags')
        modules = [ module for name, module in sys.modules.items()
                    if module is not None and
                    name.startswith('Cython.Compiler.') and 
                    name[len('Cython.Compiler.'):] not in ignored_modules ]
        coverage.report(modules, show_missing=0)
