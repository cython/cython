#
#   Pyrex - Darwin system interface
#

verbose = 0
gcc_pendantic = True
gcc_warnings_are_errors = True
gcc_all_warnings = True
gcc_optimize = False

import os, sys
from Cython.Utils import replace_suffix
from Cython.Compiler.Errors import PyrexError

version_string = "%s.%s" % sys.version_info[:2]

py_include_dirs = [
    "/Library/Frameworks/Python.framework/Versions/%s/Headers" % version_string
]

# MACOSX_DEPLOYMENT_TARGET can be set to 10.3 in most cases.
# But for the built-in Python 2.5.1 on Leopard, it needs to be set for 10.5.
# This looks like a bug that will be fixed in 2.5.2.  If Apple updates their
# Python to 2.5.2, this fix should be OK.
import distutils.sysconfig as sc
python_prefix = sc.get_config_var('prefix')
leopard_python_prefix = '/System/Library/Frameworks/Python.framework/Versions/2.5'
full_version = "%s.%s.%s" % sys.version_info[:3]
if python_prefix == leopard_python_prefix and full_version == '2.5.1':
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.5"
else:
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.3"

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
if gcc_optimize:
    compiler_options.append("-O")

linkers = ["gcc", "g++"]
linker_options = \
    "-Wl,-F.,-w -bundle -undefined dynamic_lookup" \
    .split()
#linker_options = \
#	"-Wl,-F.,-w -bundle -framework Python" \
#	.split()

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
        print(" ".join(args))
    #print compiler, args ###
    status = os.spawnvp(os.P_WAIT, compiler, args)
    if status != 0:
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
        print(" ".join(args))
    status = os.spawnvp(os.P_WAIT, linker, args)
    if status != 0:
        raise CCompilerError("Linker returned status %s" % status)
    return out_file
