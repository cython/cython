"""
Tool to run Cython files (.pyx) into .c and .cpp.

TODO:
 - Add support for dynamically selecting in-process Cython
   through CYTHONINPROCESS variable.
 - Have a CYTHONCPP option which turns on C++ in flags and
   changes output extension at the same time

VARIABLES:
 - CYTHON - The path to the "cython" command line tool.
 - CYTHONFLAGS - Flags to pass to the "cython" command line tool.

AUTHORS:
 - David Cournapeau
 - Dag Sverre Seljebotn
 - Holger Rapp (HolgerRapp@gmx.net)

"""
import os.path

import SCons
from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Scanner import Scanner, FindPathDirs
from SCons.Tool import SourceFileScanner

from _cython_dependencies import CythonDependencyScanner

def cython_dependency_scanner(node, env, path, arg):
    cdir = os.path.dirname(str(node))
    scanner = CythonDependencyScanner([cdir] + map(str,path))

    return [os.path.relpath(f, cdir) for f in scanner(str(node))]

cythonAction = Action("$CYTHONCOM")

def create_builder(env):
    try:
        cython = env['BUILDERS']['Cython']
    except KeyError:
        cython = SCons.Builder.Builder(
                  action = cythonAction,
                  emitter = {},
                  suffix = cython_suffix_emitter,
                  source_scanner = SourceFileScanner,
                  single_source = 1)
        env['BUILDERS']['Cython'] = cython

    return cython

def cython_suffix_emitter(env, source):
    return "$CYTHONCFILESUFFIX"

def generate(env):
    env["CYTHON"] = "cython"
    env["CYTHONPATH"] = []
    env['CYTHONINCPREFIX']     = '-I'
    env['CYTHONINCSUFFIX']     = ''
    env['_CYTHONINCFLAGS']     = '$( ${_concat(CYTHONINCPREFIX, CYTHONPATH, CYTHONINCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
    env["CYTHONCOM"] = "$CYTHON ${_CYTHONINCFLAGS} $CYTHONFLAGS -o $TARGET $SOURCE"
    env["CYTHONCFILESUFFIX"] = ".c"

    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    c_file.suffix['.pyx'] = cython_suffix_emitter
    c_file.add_action('.pyx', cythonAction)

    c_file.suffix['.py'] = cython_suffix_emitter
    c_file.add_action('.py', cythonAction)

    create_builder(env)

    __scanner = Scanner(name = 'cython',
                    function = cython_dependency_scanner,
                    argument = None,
                    skeys = ['.pyx', '.pxd'],
                    path_function = FindPathDirs("CYTHONPATH"),
                    recursive = False) # CythonDependencyScanner recurses automatically

    env.Append(SCANNERS = __scanner)


def exists(env):
    try:
#        import Cython
        return True
    except ImportError:
        return False
