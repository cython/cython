from __future__ import with_statement

import os
import re
import sys
import uuid
import shutil
import warnings
import textwrap
import unittest
import tempfile
import subprocess
import distutils.core
from distutils import sysconfig
from distutils import ccompiler

import runtests
import Cython.Distutils.extension
from Cython.Debugger import Cygdb as cygdb

root = os.path.dirname(os.path.abspath(__file__))
codefile = os.path.join(root, 'codefile')
cfuncs_file = os.path.join(root, 'cfuncs.c')
with open(codefile) as f:
    source_to_lineno = dict((line.strip(), i + 1) for i, line in enumerate(f))

class DebuggerTestCase(unittest.TestCase):

    def setUp(self):
        """
        Run gdb and have cygdb import the debug information from the code
        defined in TestParseTreeTransforms's setUp method
        """
        self.tempdir = tempfile.mkdtemp()
        self.destfile = os.path.join(self.tempdir, 'codefile.pyx')
        self.debug_dest = os.path.join(self.tempdir,
                                      'cython_debug',
                                      'cython_debug_info_codefile')
        self.cfuncs_destfile = os.path.join(self.tempdir, 'cfuncs')

        self.cwd = os.getcwd()
        os.chdir(self.tempdir)

        shutil.copy(codefile, self.destfile)
        shutil.copy(cfuncs_file, self.cfuncs_destfile + '.c')

        compiler = ccompiler.new_compiler()
        compiler.compile(['cfuncs.c'], debug=True, extra_postargs=['-fPIC'])

        opts = dict(
            test_directory=self.tempdir,
            module='codefile',
        )

        cython_compile_testcase = runtests.CythonCompileTestCase(
            workdir=self.tempdir,
            # we clean up everything (not only compiled files)
            cleanup_workdir=False,
            **opts
        )

        cython_compile_testcase.run_cython(
            targetdir=self.tempdir,
            incdir=None,
            annotate=False,
            extra_compile_options={
                'gdb_debug':True,
                'output_dir':self.tempdir,
            },
            **opts
        )

        cython_compile_testcase.run_distutils(
            incdir=None,
            workdir=self.tempdir,
            extra_extension_args={'extra_objects':['cfuncs.o']},
            **opts
        )

        # ext = Cython.Distutils.extension.Extension(
            # 'codefile',
            # ['codefile.pyx'],
            # pyrex_gdb=True,
            # extra_objects=['cfuncs.o'])
        #
        # distutils.core.setup(
            # script_args=['build_ext', '--inplace'],
            # ext_modules=[ext],
            # cmdclass=dict(build_ext=Cython.Distutils.build_ext)
        # )

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tempdir)


class GdbDebuggerTestCase(DebuggerTestCase):
    def setUp(self):
        super(GdbDebuggerTestCase, self).setUp()

        prefix_code = textwrap.dedent('''\
            python

            import os
            import sys
            import traceback

            def excepthook(type, value, tb):
                traceback.print_exception(type, value, tb)
                os._exit(1)

            sys.excepthook = excepthook

            # Have tracebacks end up on sys.stderr (gdb replaces sys.stderr
            # with an object that calls gdb.write())
            sys.stderr = sys.__stderr__

            end
            ''')

        code = textwrap.dedent('''\
            python

            from Cython.Debugger.Tests import test_libcython_in_gdb
            test_libcython_in_gdb.main(version=%r)

            end
            ''' % (sys.version_info[:2],))

        self.gdb_command_file = cygdb.make_command_file(self.tempdir,
                                                        prefix_code)

        with open(self.gdb_command_file, 'a') as f:
            f.write(code)

        args = ['gdb', '-batch', '-x', self.gdb_command_file, '-n', '--args',
                sys.executable, '-c', 'import codefile']

        paths = []
        path = os.environ.get('PYTHONPATH')
        if path:
            paths.append(path)
        paths.append(os.path.dirname(os.path.dirname(
            os.path.abspath(Cython.__file__))))
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(paths))

        try:
            p = subprocess.Popen(['gdb', '-v'], stdout=subprocess.PIPE)
            have_gdb = True
        except OSError:
            # gdb was not installed
            have_gdb = False
        else:
            gdb_version = p.stdout.read().decode('ascii')
            p.wait()
            p.stdout.close()

        if have_gdb:
            # Based on Lib/test/test_gdb.py
            regex = "^GNU gdb [^\d]*(\d+)\.(\d+)"
            gdb_version_number = re.search(regex, gdb_version).groups()

        # Be Python 3 compatible
        if not have_gdb or list(map(int, gdb_version_number)) < [7, 2]:
            self.p = None
            warnings.warn('Skipping gdb tests, need gdb >= 7.2')
        else:
            self.p = subprocess.Popen(
                args,
                stdout=open(os.devnull, 'w'),
                stderr=subprocess.PIPE,
                env=env)

    def tearDown(self):
        super(GdbDebuggerTestCase, self).tearDown()
        if self.p:
            self.p.stderr.close()
            self.p.wait()
        os.remove(self.gdb_command_file)


class TestAll(GdbDebuggerTestCase):

    def test_all(self):
        if self.p is None:
            return

        out, err = self.p.communicate()
        border = '*' * 30
        start = '%s   v INSIDE GDB v   %s' % (border, border)
        end   = '%s   ^ INSIDE GDB ^   %s' % (border, border)
        errmsg = '\n%s\n%s%s' % (start, err.decode('UTF-8'), end)
        self.assertEquals(0, self.p.wait(), errmsg)
        sys.stderr.write(err)

if __name__ == '__main__':
    unittest.main()
