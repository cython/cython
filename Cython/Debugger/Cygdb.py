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
import textwrap
import subprocess

usage = "Usage: cygdb [PATH [GDB_ARGUMENTS]]"

def make_command_file(path_to_debug_info, prefix_code='', no_import=False):
    if not no_import:
        pattern = os.path.join(path_to_debug_info,
                               'cython_debug',
                               'cython_debug_info_*')
        debug_files = glob.glob(pattern)

        if not debug_files:
            sys.exit('%s.\nNo debug files were found in %s. Aborting.' % (
                                   usage, os.path.abspath(path_to_debug_info)))

    fd, tempfilename = tempfile.mkstemp()
    f = os.fdopen(fd, 'w')
    f.write(prefix_code)
    f.write('set breakpoint pending on\n')
    f.write("set print pretty on\n")
    f.write('python from Cython.Debugger import libcython, libpython\n')

    if no_import:
        # don't do this, this overrides file command in .gdbinit
        # f.write("file %s\n" % sys.executable)
        pass
    else:
        path = os.path.join(path_to_debug_info, "cython_debug", "interpreter")
        interpreter = open(path).read()
        f.write("file %s\n" % interpreter)
        f.write('\n'.join('cy import %s\n' % fn for fn in debug_files))
        f.write(textwrap.dedent('''\
            python
            import sys
            try:
                gdb.lookup_type('PyModuleObject')
            except RuntimeError:
                sys.stderr.write(
                    'Python was not compiled with debug symbols (or it was '
                    'stripped). Some functionality may not work (properly).\\n')
            end
        '''))

    f.close()

    return tempfilename

def main(path_to_debug_info=None, gdb_argv=None, no_import=False):
    """
    Start the Cython debugger. This tells gdb to import the Cython and Python
    extensions (libcython.py and libpython.py) and it enables gdb's pending
    breakpoints.

    path_to_debug_info is the path to the Cython build directory
    gdb_argv is the list of options to gdb
    no_import tells cygdb whether it should import debug information
    """
    if path_to_debug_info is None:
        if len(sys.argv) > 1:
            path_to_debug_info = sys.argv[1]
        else:
            path_to_debug_info = os.curdir

    if gdb_argv is None:
        gdb_argv = sys.argv[2:]

    if path_to_debug_info == '--':
        no_import = True

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
