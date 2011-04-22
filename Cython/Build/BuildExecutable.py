"""
Compile a Python script into an executable that embeds CPython and run it.
Requires CPython to be built as a shared library ('libpythonX.Y').

Basic usage:

    python cythonrun somefile.py [ARGS]
"""

DEBUG = True

import sys
import os
from distutils import sysconfig

def get_config_var(name):
    return sysconfig.get_config_var(name) or ''

INCDIR = sysconfig.get_python_inc()
LIBDIR1 = get_config_var('LIBDIR')
LIBDIR2 = get_config_var('LIBPL')
PYLIB = get_config_var('LIBRARY')
if PYLIB:
    PYLIB = '-l%s' % PYLIB[3:-2]

CC = get_config_var('CC')
CFLAGS = get_config_var('CFLAGS') + ' ' + os.environ.get('CFLAGS', '')
LINKCC = get_config_var('LINKCC')
LINKFORSHARED = get_config_var('LINKFORSHARED')
LIBS = get_config_var('LIBS')
SYSLIBS = get_config_var('SYSLIBS')

def _debug(msg, *args):
    if DEBUG:
        if args:
            msg = msg % args
        sys.stderr.write(msg + '\n')

def dump_config():
    _debug('INCDIR: %s', INCDIR)
    _debug('LIBDIR1: %s', LIBDIR1)
    _debug('LIBDIR2: %s', LIBDIR2)
    _debug('PYLIB: %s', PYLIB)
    _debug('CC: %s', CC)
    _debug('CFLAGS: %s', CFLAGS)
    _debug('LINKCC: %s', LINKCC)
    _debug('LINKFORSHARED: %s', LINKFORSHARED)
    _debug('LIBS: %s', LIBS)
    _debug('SYSLIBS: %s', SYSLIBS)

def runcmd(cmd, shell=True):
    if shell:
        cmd = ' '.join(cmd)
        _debug(cmd)
    else:
        _debug(' '.join(cmd))

    try:
        import subprocess
    except ImportError: # Python 2.3 ...
        returncode = os.system(cmd)
    else:
        returncode = subprocess.call(cmd, shell=shell)
    
    if returncode:
        sys.exit(returncode)

def clink(basename):
    runcmd([LINKCC, '-o', basename, basename+'.o', '-L'+LIBDIR1, '-L'+LIBDIR2, PYLIB]
           + LIBS.split() + SYSLIBS.split() + LINKFORSHARED.split())

def ccompile(basename):
    runcmd([CC, '-c', '-o', basename+'.o', basename+'.c', '-I' + INCDIR] + CFLAGS.split())

def cycompile(input_file, options=()):
    from Cython.Compiler import Version, CmdLine, Main
    options, sources = CmdLine.parse_command_line(list(options or ()) + ['--embed', input_file])
    _debug('Using Cython %s to compile %s', Version.version, input_file)
    result = Main.compile(sources, options)
    if result.num_errors > 0:
        sys.exit(1)

def exec_file(basename, args=()):
    runcmd([os.path.abspath(basename)] + list(args), shell=False)

def build(input_file, compiler_args=()):
    """
    Build an executable program from a Cython module.

    Returns the name of the executable file.
    """
    basename = os.path.splitext(input_file)[0]
    cycompile(input_file, compiler_args)
    ccompile(basename)
    clink(basename)
    return basename

def build_and_run(args):
    """
    Build an executable program from a Cython module and runs it.

    Arguments after the module name will be passed verbatimely to the
    program.
    """
    cy_args = []
    last_arg = None
    for i, arg in enumerate(args):
        if arg.startswith('-'):
            cy_args.append(arg)
        elif last_arg in ('-X', '--directive'):
            cy_args.append(arg)
        else:
            input_file = arg
            args = args[i+1:]
            break
        last_arg = arg
    else:
        raise ValueError('no input file provided')

    program_name = build(input_file, cy_args)
    exec_file(program_name, args)

if __name__ == '__main__':
    build_and_run(sys.argv[1:])
