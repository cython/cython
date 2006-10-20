# Subclasses disutils.command.build_ext,
# replacing it with a Pyrex version that compiles pyx->c
# before calling the original build_ext command.
# July 2002, Graham Fawcett
# Modified by Darrell Gallion <dgallion1@yahoo.com>
# to allow inclusion of .c files along with .pyx files.
# Pyrex is (c) Greg Ewing.

import distutils.command.build_ext
#import Pyrex.Compiler.Main
from Pyrex.Compiler.Main import CompilationOptions, default_options, compile
from Pyrex.Compiler.Errors import PyrexError
from distutils.dep_util import newer
import os
import sys

def replace_suffix(path, new_suffix):
    return os.path.splitext(path)[0] + new_suffix

class build_ext (distutils.command.build_ext.build_ext):

    description = "compile Pyrex scripts, then build C/C++ extensions (compile/link to build directory)"

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

        # collect the names of the source (.pyx) files
        pyx_sources = []
        pyx_sources = [source for source in sources if source.endswith('.pyx')]
        other_sources = [source for source in sources if not source.endswith('.pyx')]

        #suffix = self.swig_cpp and '.cpp' or '.c'
        suffix = '.c'
        for pyx in pyx_sources:
            # should I raise an exception if it doesn't exist?
            if os.path.exists(pyx):
                source = pyx
                target = replace_suffix(source, suffix)
                if newer(source, target) or self.force:
                    self.pyrex_compile(source)

        return [replace_suffix(src, suffix) for src in pyx_sources] + other_sources

    def pyrex_compile(self, source):
        options = CompilationOptions(default_options,
            include_path = self.include_dirs)
        result = compile(source, options)
        if result.num_errors <> 0:
            sys.exit(1)

