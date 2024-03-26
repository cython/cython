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
import optparse
import logging

logger = logging.getLogger(__name__)


def make_command_file(path_to_debug_info, prefix_code='',
                      no_import=False, skip_interpreter=False):
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
    try:
        f.write(prefix_code)
        f.write(textwrap.dedent('''\
            # This is a gdb command file
            # See https://sourceware.org/gdb/onlinedocs/gdb/Command-Files.html

            set breakpoint pending on
            set print pretty on

            python
            try:
                # Activate virtualenv, if we were launched from one
                import os
                virtualenv = os.getenv('VIRTUAL_ENV')
                if virtualenv:
                    path_to_activate_this_py = os.path.join(virtualenv, 'bin', 'activate_this.py')
                    print("gdb command file: Activating virtualenv: %s; path_to_activate_this_py: %s" % (
                        virtualenv, path_to_activate_this_py))
                    with open(path_to_activate_this_py) as f:
                        exec(f.read(), dict(__file__=path_to_activate_this_py))
                from Cython.Debugger import libcython, libpython
            except Exception as ex:
                from traceback import print_exc
                print("There was an error in Python code originating from the file ''' + str(__file__) + '''")
                print("It used the Python interpreter " + str(sys.executable))
                print_exc()
                exit(1)
            end
            '''))

        if no_import:
            # don't do this, this overrides file command in .gdbinit
            # f.write("file %s\n" % sys.executable)
            pass
        else:
            if not skip_interpreter:
                # Point Cygdb to the interpreter that was used to generate
                # the debugging information.
                path = os.path.join(path_to_debug_info, "cython_debug", "interpreter")
                interpreter_file = open(path)
                try:
                    interpreter = interpreter_file.read()
                finally:
                    interpreter_file.close()
                f.write("file %s\n" % interpreter)

            f.write('\n'.join('cy import %s\n' % fn for fn in debug_files))

            if not skip_interpreter:
                # The following `f.write` stuff is a bit tricky:

                # How this is supposed to work:
                # If you launch gdb and enter these commands:
                # (gdb) file someexe
                # (gdb) explore MyStruct
                # or these commands
                # (gdb) file someexe
                # (gdb) python
                # gdb.lookup_type('MyStruct')
                # end
                # You get an error, unless the source code of `someexe` contains
                # `struct MyStruct {...};`, and debugging symbols for that are
                # loaded into gdb. Thus, we use
                # `gdb.lookup_type('PyModuleObject')` to detect whether debug
                # symbols for the python interpreter are loaded into gdb. Some
                # functionality of cygdb requires these debug symbols. For example
                # `cy list` will print c code if these debug symbols are missing,
                # but it will print cython code if these debug symbols exist.

                # Two reasons why this does not work properly:
                # 1. If I build python with `--with-pydebug` the debug symbol
                # for `PyModuleObject` is not in the python binary, but in a
                # shared library called `libpython3.so`. Thus, if do this:
                # (gdb) file python
                # (gdb) explore PyModuleObject
                # I get an error. If I however do this
                # (gdb) file python
                # (gdb) break main
                # (gdb) run
                # (gdb) explore PyModuleObject
                # I don't get an error. Therefore, the code below this long
                # comment always prints a warning, but `cy list` works fine, since
                # the code below is executed before `libpython3.so` is loaded, but
                # `cy list` is executed after `libpython3.so` is loaded.
                # 2. I installed python from the official Arch Linux package,
                # and the code below this long comment prints the warning, but `cy
                # list` works fine anyway. Why? Because `libpython3.so` contains
                # no debug symbols, but debuginfod exists. As soon as
                # `libpython3.so` is loaded, gdb downloads debug symbols for
                # `libpython3.so` and `cy list` works properly. Since the code
                # below runs before `libpython3.so` is loaded, it runs before the
                # debug symbols are downloaded.

                # How to fix this:
                # The check below should probably removed and instead executed
                # everytime e.g. `cy list` is executed.

                # Hint: If you want a python interpreter that was compiled with
                # `--with-pydebug` and thus contains debug symbols, and another
                # python interpreter thas was not, run e.g. `pyenv install 3.8.1`
                # and `pyenv install 3.8.1-debug`.

                f.write(textwrap.dedent('''\
                    python
                    import sys
                    # Check if the Python executable provides a symbol table.
                    if not hasattr(gdb.selected_inferior().progspace, "symbol_file"):
                        sys.stderr.write(
                            "''' + interpreter + ''' was not compiled with debug symbols (or it was "
                            "stripped). Some functionality may not work (properly).\\n")
                    end
                '''))

            f.write("source .cygdbinit\n")
    finally:
        f.close()

    return tempfilename

usage = "Usage: cygdb [options] [PATH [-- GDB_ARGUMENTS]]"

def main(path_to_debug_info=None, gdb_argv=None, no_import=False):
    """
    Start the Cython debugger. This tells gdb to import the Cython and Python
    extensions (libcython.py and libpython.py) and it enables gdb's pending
    breakpoints.

    path_to_debug_info is the path to the Cython build directory
    gdb_argv is the list of options to gdb
    no_import tells cygdb whether it should import debug information
    """
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--gdb-executable",
        dest="gdb", default='gdb',
        help="gdb executable to use [default: gdb]")
    parser.add_option("--verbose", "-v",
        dest="verbosity", action="count", default=0,
        help="Verbose mode. Multiple -v options increase the verbosity")
    parser.add_option("--skip-interpreter",
                      dest="skip_interpreter", default=False, action="store_true",
                      help="Do not automatically point GDB to the same interpreter "
                           "used to generate debugging information")

    (options, args) = parser.parse_args()
    if path_to_debug_info is None:
        if len(args) > 1:
            path_to_debug_info = args[0]
        else:
            path_to_debug_info = os.curdir

    if gdb_argv is None:
        gdb_argv = args[1:]

    if path_to_debug_info == '--':
        no_import = True

    logging_level = logging.WARN
    if options.verbosity == 1:
        logging_level = logging.INFO
    if options.verbosity >= 2:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level)

    skip_interpreter = options.skip_interpreter

    logger.info("verbosity = %r", options.verbosity)
    logger.debug("options = %r; args = %r", options, args)
    logger.debug("Done parsing command-line options. path_to_debug_info = %r, gdb_argv = %r",
        path_to_debug_info, gdb_argv)

    tempfilename = make_command_file(path_to_debug_info,
                                     no_import=no_import,
                                     skip_interpreter=skip_interpreter)
    logger.info("Launching %s with command file: %s and gdb_argv: %s",
        options.gdb, tempfilename, gdb_argv)
    with open(tempfilename) as tempfile:
        logger.debug('Command file (%s) contains: """\n%s"""', tempfilename, tempfile.read())
        logger.info("Spawning %s...", options.gdb)
        p = subprocess.Popen([options.gdb, '-command', tempfilename] + gdb_argv)
        logger.info("Spawned %s (pid %d)", options.gdb, p.pid)
        while True:
            try:
                logger.debug("Waiting for gdb (pid %d) to exit...", p.pid)
                ret = p.wait()
                logger.debug("Wait for gdb (pid %d) to exit is done. Returned: %r", p.pid, ret)
            except KeyboardInterrupt:
                pass
            else:
                break
        logger.debug("Closing temp command file with fd: %s", tempfile.fileno())
    logger.debug("Removing temp command file: %s", tempfilename)
    os.remove(tempfilename)
    logger.debug("Removed temp command file: %s", tempfilename)
