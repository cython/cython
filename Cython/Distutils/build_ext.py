# Subclasses disutils.command.build_ext,
# replacing it with a Pyrex version that compiles pyx->c
# before calling the original build_ext command.
# July 2002, Graham Fawcett
# Modified by Darrell Gallion <dgallion1@yahoo.com>
# to allow inclusion of .c files along with .pyx files.
# Pyrex is (c) Greg Ewing.

import distutils.command.build_ext
#import Cython.Compiler.Main
from Cython.Compiler.Main import CompilationOptions, default_options, compile
from Cython.Compiler.Errors import PyrexError
from distutils.dep_util import newer
import os
import sys

def replace_suffix(path, new_suffix):
    return os.path.splitext(path)[0] + new_suffix

class build_ext (distutils.command.build_ext.build_ext):

    description = "compile Cython scripts, then build C/C++ extensions (compile/link to build directory)"

    def finalize_options (self):
        distutils.command.build_ext.build_ext.finalize_options(self)

        # The following hack should no longer be needed.
        if 0:
            # compiling with mingw32 gets an "initializer not a constant" error
            # doesn't appear to happen with MSVC!
            # so if we are compiling with mingw32,
            # switch to C++ mode, to avoid the problem
            if self.compiler == 'mingw32':
                self.swig_cpp = 1

    def swig_sources (self, sources, extension = None):
        if not self.extensions:
            return

        #suffix = self.swig_cpp and '.cpp' or '.c'
        suffix = '.c'
        cplus  = 0
        include_dirs = []
        if extension is not None:
            module_name = extension.name
            include_dirs = extension.include_dirs or []
            if extension.language == "c++":
                cplus = 1
                suffix = ".cpp"
        else:
            module_name = None

        # collect the names of the source (.pyx) files
        pyx_sources = [source for source in sources if source.endswith('.pyx')]
        other_sources = [source for source in sources if not source.endswith('.pyx')]

        for pyx in pyx_sources:
            # should I raise an exception if it doesn't exist?
            if os.path.exists(pyx):
                source = pyx
                target = replace_suffix(source, suffix)
                if newer(source, target) or self.force:
                    self.cython_compile(source, module_name, include_dirs, cplus)

        return [replace_suffix(src, suffix) for src in pyx_sources] + other_sources

    def cython_compile(self, source, module_name, include_dirs, cplus):
        options = CompilationOptions(
            default_options,
            include_path = include_dirs + self.include_dirs,
            cplus=cplus)
        result = compile(source, options, full_module_name=module_name)
        if result.num_errors <> 0:
            sys.exit(1)
