#
#   Pyrex -- Mac system interface
#

import os, sys, string
import aetools
from aetools import TalkTo
from StdSuites.Standard_Suite import Standard_Suite_Events as Standard_Suite
from Pyrex.Utils import replace_suffix
from Pyrex.Compiler.Errors import PyrexError

c_compiler = "MWCPPC"
c_optimizations = "off"
#c_linker = "PPCLink"
c_linker = "MWLinkPPC"
shared_lib_suffix = ".slb"

#py_home = "Python2.2:Home:"
py_home = sys.exec_prefix

py_include_dirs = (
    py_home + "Include:",
    py_home + "Mac:Include:"
)

pythoncore = py_home + "PythonCore"

mwlibdir = "MPW:Interfaces&Libraries:Libraries:MWPPCLibraries:"

libraries = (
    #mwlibdir + "'MSL C.PPC.Lib'",
    #mwlibdir + "'MSL RuntimePPC.Lib'",
    mwlibdir + "'MSL ShLibRuntime.Lib'",
    mwlibdir + "InterfaceLib",
    #mwlibdir + "MathLib",
    )

class CCompilerError(PyrexError):
    pass

#---------------- ToolServer ---------------------------

from TS_Misc_Suite import TS_Misc_Suite

class ToolServer(Standard_Suite, TS_Misc_Suite, TalkTo):
    pass

def send_toolserver_command(cmd):
    ts = ToolServer('MPSX', start = 1)
    return ts.DoScript(cmd)

def do_toolserver_command(command):
    try:
        result = send_toolserver_command(command)
    except aetools.Error, e:
        raise CCompilerError("Apple Event error: %s" % e)
    errn, stat, stdout, stderr = result
    if errn:
        raise CCompilerError("ToolServer error: %s" % errn)
    stdout = string.replace(stdout, "\r", "\n")
    stderr = string.replace(stderr, "\r", "\n")
    if stdout:
        #print "<<< Begin ToolServer StdOut >>>"
        sys.stderr.write(stdout)
        #print "<<< End ToolServer StdOut >>>"
    if stderr:
        #print "<<< Begin ToolServer StdErr >>>"
        sys.stderr.write(stderr)
        #print "<<< End ToolServer StdErr >>>"
    return stat

#-------------------------------------------------------

def c_compile(c_file):
    #  Compile the given C source file to produce
    #  an object file. Returns the pathname of the
    #  resulting file.
    c_file = os.path.join(os.getcwd(), c_file)
    #print "c_compile: c_file =", repr(c_file) ###
    c_file_dir = os.path.dirname(c_file)
    o_file = replace_suffix(c_file, ".o")
    include_options = ["-i %s" % c_file_dir]
    for dir in py_include_dirs:
        include_options.append("-i %s" % dir)
    command = "%s -opt %s -nomapcr -w off -r %s %s -o %s" % (
        c_compiler, 
        c_optimizations,
        string.join(include_options),
        c_file, 
        o_file, 
        #e_file
        )
    #print "...command =", repr(command) ###
    stat = do_toolserver_command(command)
    if stat:
        raise CCompilerError("C compiler returned status %s" % stat)
    return o_file

def c_link(obj_file):
    return c_link_list([obj_file])

def c_link_list(obj_files):
    #  Link the given object files into a dynamically
    #  loadable extension file. Returns the pathname
    #  of the resulting file.
    out_file = replace_suffix(obj_files[0], shared_lib_suffix)
    command = "%s -xm s -export all %s %s %s -o %s" % (
        c_linker, 
        string.join(obj_files), 
        pythoncore,
        string.join(libraries),
        out_file)
    stat = do_toolserver_command(command)
    if stat:
        raise CCompilerError("Linker returned status %s" % stat)
    return out_file

def test_c_compile(link = 0):
    objs = []
    for arg in sys.argv[1:]:
        if arg.endswith(".c"):
            try:
                obj = c_compile(arg)
            except PyrexError, e:
                #print "Caught a PyrexError:" ###
                #print repr(e) ###
                print "%s.%s:" % (e.__class__.__module__,
                    e.__class__.__name__), e
                sys.exit(1)
        else:
            obj = arg
        objs.append(obj)
    if link:
        c_link_list(objs)

