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

import Cython.Distutils.extension
from Cython.Debugger import Cygdb as cygdb


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
        
        code = textwrap.dedent("""
            cdef extern from "stdio.h":
                int puts(char *s)
                
            cdef int c_var = 0
            python_var = 0
            
            def spam(a=0):
                cdef:
                    int b, c, d
                
                b = c = d = 0
                
                b = 1
                c = 2
                d = 3
                int(10)
                puts("spam")
                
            cdef ham():
                pass
                
            cpdef eggs():
                pass
            
            cdef class SomeClass(object):
                def spam(self):
                    pass
            
            spam()
        """)
        
        self.cwd = os.getcwd()
        os.chdir(self.tempdir)
        
        open(self.destfile, 'w').write(code)
        
        ext = Cython.Distutils.extension.Extension(
            'codefile',
            ['codefile.pyx'], 
            pyrex_debug=True)
            
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
        
        self.gdb_command_file = cygdb.make_command_file(self.tempdir)
        with open(self.gdb_command_file, 'a') as f:
            f.write('python '
                'from Cython.Debugger.Tests import test_libcython_in_gdb;'
                'test_libcython_in_gdb.main()\n')
                
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