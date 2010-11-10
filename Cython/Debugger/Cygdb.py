#!/usr/bin/env python

"""
The Cython debugger

The current directory should contain a directory named 'cython_debug', or a
path to the cython project directory should be given (the parent directory of
cython_debug).

Additional gdb args can be provided only if a path to the project directory is 
given.
"""

import os
import sys
import glob
import tempfile
import subprocess

def usage():
    print("Usage: cygdb [PATH GDB_ARGUMENTS]")

def make_command_file(path_to_debug_info, prefix_code='', no_import=False):
    if not no_import:
        pattern = os.path.join(path_to_debug_info, 
                               'cython_debug',
                               'cython_debug_info_*')
        debug_files = glob.glob(pattern)

        if not debug_files:
            usage()
            sys.exit('No debug files were found in %s. Aborting.' % (
                    os.path.abspath(path_to_debug_info)))
    
    
    
    fd, tempfilename = tempfile.mkstemp()
    f = os.fdopen(fd, 'w')
    f.write(prefix_code)
    f.write('set breakpoint pending on\n')
    f.write("set print pretty on\n")
    f.write('python from Cython.Debugger import libcython\n')
    
    if no_import:
        f.write("file %s\n" % sys.executable)
    else:
        path = os.path.join(path_to_debug_info, "cython_debug", "interpreter")
        interpreter = open(path).read()
        f.write("file %s\n" % interpreter)
        f.write('\n'.join('cy import %s\n' % fn for fn in debug_files))
    
    f.close()
    
    return tempfilename

def main(path_to_debug_info=os.curdir, gdb_argv=[], no_import=False):
    """
    Start the Cython debugger. This tells gdb to import the Cython and Python
    extensions (libpython.py and libcython.py) and it enables gdb's pending 
    breakpoints
    
    path_to_debug_info is the path to the cython_debug directory
    """
    tempfilename = make_command_file(path_to_debug_info, no_import=no_import)
    p = subprocess.Popen(['gdb', '-command', tempfilename] + gdb_argv)
    while True:
        try:
            p.wait()
        except KeyboardInterrupt:
            pass
        else:
            break
    os.remove(tempfilename)