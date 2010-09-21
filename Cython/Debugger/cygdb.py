#!/usr/bin/env python

"""
The Cython debugger

The current directory should contain a directory named 'cython_debug', or a
path to the cython project directory should be given (the parent directory of
cython_debug).
"""

import os
import sys
import glob
import tempfile
import subprocess

def main(import_libpython=False, path_to_debug_info=os.curdir):
    """
    Start the Cython debugger. This tells gdb to import the Cython and Python
    extensions (libpython.py and libcython.py) and it enables gdb's pending 
    breakpoints
    
    import_libpython indicates whether we should just 'import libpython',
    or import it from Cython.Debugger
    
    path_to_debug_info is the path to the cython_debug directory
    """
    debug_files = glob.glob(
        os.path.join(path_to_debug_info, 'cython_debug/cython_debug_info_*'))

    if not debug_files:
        sys.exit('No debug files were found in %s. Aborting.' % (
                 os.path.abspath(path_to_debug_info))) 
        
    fd, tempfilename = tempfile.mkstemp()
    f = os.fdopen(fd, 'w')
    f.write('set breakpoint pending on\n')
    f.write('python from Cython.Debugger import libcython\n')
    if import_libpython:
        f.write('python import libpython')
    else:
        f.write('python from Cython.Debugger import libpython\n')
    f.write('\n'.join('cy import %s\n' % fn for fn in debug_files))
    f.close()
    
    p = subprocess.Popen(['gdb', '-command', tempfilename])
    while True:
        try:
            p.wait()
        except KeyboardInterrupt:
            pass
        else:
            break
    os.remove(tempfilename)