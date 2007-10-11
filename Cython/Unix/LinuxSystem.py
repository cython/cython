#
#   Pyrex - Linux system interface
#

verbose = 0
gcc_pendantic = True
gcc_warnings_are_errors = True
gcc_all_warnings = True

import os, sys
from Pyrex.Utils import replace_suffix
from Pyrex.Compiler.Errors import PyrexError

version = "%s.%s" % sys.version[:2]
py_include_dirs = [
    "%s/include/python%s" % (sys.prefix, version)
]

compilers = ["gcc", "g++"]
compiler_options = \
    "-g -c -fno-strict-aliasing -Wno-long-double -no-cpp-precomp " \
    "-mno-fused-madd -fno-common -dynamic " \
    .split()
if gcc_pendantic:
    compiler_options.extend(["-pedantic", "-Wno-long-long"])
if gcc_warnings_are_errors:
    compiler_options.append("-Werror")
if gcc_all_warnings:
    compiler_options.append("-Wall")
    compiler_options.append("-Wno-unused-function")

linkers = ["gcc", "g++"]
linker_options = \
    "-shared" \
    .split()

class CCompilerError(PyrexError):
    pass

def c_compile(c_file, verbose_flag = 0, cplus = 0, obj_suffix = ".o"):
    #  Compile the given C source file to produce
    #  an object file. Returns the pathname of the
    #  resulting file.
    c_file = os.path.join(os.getcwd(), c_file)
    o_file = replace_suffix(c_file, obj_suffix)
    include_options = []
    for dir in py_include_dirs:
        include_options.append("-I%s" % dir)
    compiler = compilers[bool(cplus)]
    args = [compiler] + compiler_options + include_options + [c_file, "-o", o_file]
    if verbose_flag or verbose:
        print " ".join(args)
    #print compiler, args ###
    status = os.spawnvp(os.P_WAIT, compiler, args)
    if status <> 0:
        raise CCompilerError("C compiler returned status %s" % status)
    return o_file

def c_link(obj_file, verbose_flag = 0, extra_objects = [], cplus = 0):
    return c_link_list([obj_file] + extra_objects, verbose_flag, cplus)

def c_link_list(obj_files, verbose_flag = 0, cplus = 0):
    #  Link the given object files into a dynamically
    #  loadable extension file. Returns the pathname
    #  of the resulting file.
    out_file = replace_suffix(obj_files[0], ".so")
    linker = linkers[bool(cplus)]
    args = [linker] + linker_options + obj_files + ["-o", out_file]
    if verbose_flag or verbose:
        print " ".join(args)
    status = os.spawnvp(os.P_WAIT, linker, args)
    if status <> 0:
        raise CCompilerError("Linker returned status %s" % status)
    return out_file
