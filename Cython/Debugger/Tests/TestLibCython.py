import os
import re
import sys
import uuid
import shutil
import textwrap
import unittest
import tempfile
import subprocess
import distutils.core
from distutils import sysconfig
from distutils import ccompiler

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
        compiler.compile(['cfuncs.c'], debug=True)
        
        ext = Cython.Distutils.extension.Extension(
            'codefile',
            ['codefile.pyx'], 
            pyrex_debug=True,
            extra_objects=['cfuncs.o'])
            
        distutils.core.setup(
            script_args=['build_ext', '--inplace'],
            ext_modules=[ext],
            cmdclass=dict(build_ext=Cython.Distutils.build_ext)
        )
    
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
            test_libcython_in_gdb.main()
            
            end
            ''')
        
        self.gdb_command_file = cygdb.make_command_file(self.tempdir, 
                                                        prefix_code)
        open(self.gdb_command_file, 'a').write(code)
        
        args = ['gdb', '-batch', '-x', self.gdb_command_file, '-n', '--args',
                sys.executable, '-c', 'import codefile']
        
        paths = []
        path = os.environ.get('PYTHONPATH')
        if path:
            paths.append(path)
        paths.append(os.path.dirname(os.path.dirname(
            os.path.abspath(Cython.__file__))))
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(paths))

        self.p = subprocess.Popen(
            args,
            stdout=open(os.devnull, 'w'),
            stderr=subprocess.PIPE,
            env=env)
        
    def tearDown(self):
        super(GdbDebuggerTestCase, self).tearDown()
        self.p.stderr.close()
        self.p.wait()
        os.remove(self.gdb_command_file)
        
   
class TestAll(GdbDebuggerTestCase):
    
    def test_all(self):
        out, err = self.p.communicate()
        border = '*' * 30
        start = '%s   v INSIDE GDB v   %s' % (border, border)
        end   = '%s   ^ INSIDE GDB ^   %s' % (border, border)
        errmsg = '\n%s\n%s%s' % (start, err, end)
        self.assertEquals(0, self.p.wait(), errmsg)
        sys.stderr.write(err)

if __name__ == '__main__':
    unittest.main()