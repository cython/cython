"""Cython.Distutils.build_ext

Implements a version of the Distutils 'build_ext' command, for
building Cython extension modules."""

# This module should be kept compatible with Python 2.3.

__revision__ = "$Id:$"

import sys
import os
import re
from distutils.core import Command
from distutils.errors import DistutilsPlatformError
from distutils.sysconfig import customize_compiler, get_python_version
from distutils.dep_util import newer, newer_group
from distutils import log
from distutils.dir_util import mkpath
from distutils.command import build_ext as _build_ext
from distutils import sysconfig

extension_name_re = _build_ext.extension_name_re

show_compilers = _build_ext.show_compilers

class Optimization(object):
    def __init__(self):
        self.flags = (
            'OPT',
            'CFLAGS',
            'CPPFLAGS',
            'EXTRA_CFLAGS',
            'BASECFLAGS',
            'PY_CFLAGS',
        )
        self.state = sysconfig.get_config_vars(*self.flags)
        self.config_vars = sysconfig.get_config_vars()


    def disable_optimization(self):
        "disable optimization for the C or C++ compiler"
        badoptions = ('-O1', '-O2', '-O3')

        for flag, option in zip(self.flags, self.state):
            if option is not None:
                L = [opt for opt in option.split() if opt not in badoptions]
                self.config_vars[flag] = ' '.join(L)

    def restore_state(self):
        "restore the original state"
        for flag, option in zip(self.flags, self.state):
            if option is not None:
                self.config_vars[flag] = option


optimization = Optimization()


class build_ext(_build_ext.build_ext):

    description = "build C/C++ and Cython extensions (compile/link to build directory)"

    sep_by = _build_ext.build_ext.sep_by
    user_options = _build_ext.build_ext.user_options
    boolean_options = _build_ext.build_ext.boolean_options
    help_options = _build_ext.build_ext.help_options

    # Add the pyrex specific data.
    user_options.extend([
        ('pyrex-cplus', None,
         "generate C++ source files"),
        ('pyrex-create-listing', None,
         "write errors to a listing file"),
        ('pyrex-line-directives', None,
         "emit source line directives"),
        ('pyrex-include-dirs=', None,
         "path to the Cython include files" + sep_by),
        ('pyrex-c-in-temp', None,
         "put generated C files in temp directory"),
        ('pyrex-gen-pxi', None,
            "generate .pxi file for public declarations"),
        ('pyrex-directives=', None,
            "compiler directive overrides"),
        ('pyrex-gdb', None,
         "generate debug information for cygdb"),
        ])

    boolean_options.extend([
        'pyrex-cplus', 'pyrex-create-listing', 'pyrex-line-directives',
        'pyrex-c-in-temp', 'pyrex-gdb',
    ])

    def initialize_options(self):
        _build_ext.build_ext.initialize_options(self)
        self.pyrex_cplus = 0
        self.pyrex_create_listing = 0
        self.pyrex_line_directives = 0
        self.pyrex_include_dirs = None
        self.pyrex_directives = None
        self.pyrex_c_in_temp = 0
        self.pyrex_gen_pxi = 0
        self.pyrex_gdb = False
        self.no_c_in_traceback = 0

    def finalize_options (self):
        _build_ext.build_ext.finalize_options(self)
        if self.pyrex_include_dirs is None:
            self.pyrex_include_dirs = []
        elif isinstance(self.pyrex_include_dirs, basestring):
            self.pyrex_include_dirs = \
                self.pyrex_include_dirs.split(os.pathsep)
        if self.pyrex_directives is None:
            self.pyrex_directives = {}
    # finalize_options ()

    def run(self):
        # We have one shot at this before build_ext initializes the compiler.
        # If --pyrex-gdb is in effect as a command line option or as option
        # of any Extension module, disable optimization for the C or C++
        # compiler.
        if self.pyrex_gdb or [1 for ext in self.extensions
                                     if getattr(ext, 'pyrex_gdb', False)]:
            optimization.disable_optimization()

        _build_ext.build_ext.run(self)

    def build_extensions(self):
        # First, sanity-check the 'extensions' list
        self.check_extensions_list(self.extensions)

        for ext in self.extensions:
            ext.sources = self.cython_sources(ext.sources, ext)
            self.build_extension(ext)

    def cython_sources(self, sources, extension):
        """
        Walk the list of source files in 'sources', looking for Cython
        source files (.pyx and .py).  Run Cython on all that are
        found, and return a modified 'sources' list with Cython source
        files replaced by the generated C (or C++) files.
        """
        try:
            from Cython.Compiler.Main \
                import CompilationOptions, \
                       default_options as pyrex_default_options, \
                       compile as cython_compile
            from Cython.Compiler.Errors import PyrexError
        except ImportError:
            e = sys.exc_info()[1]
            print("failed to import Cython: %s" % e)
            raise DistutilsPlatformError("Cython does not appear to be installed")

        new_sources = []
        pyrex_sources = []
        pyrex_targets = {}

        # Setup create_list and cplus from the extension options if
        # Cython.Distutils.extension.Extension is used, otherwise just
        # use what was parsed from the command-line or the configuration file.
        # cplus will also be set to true is extension.language is equal to
        # 'C++' or 'c++'.
        #try:
        #    create_listing = self.pyrex_create_listing or \
        #                        extension.pyrex_create_listing
        #    cplus = self.pyrex_cplus or \
        #                extension.pyrex_cplus or \
        #                (extension.language != None and \
        #                    extension.language.lower() == 'c++')
        #except AttributeError:
        #    create_listing = self.pyrex_create_listing
        #    cplus = self.pyrex_cplus or \
        #                (extension.language != None and \
        #                    extension.language.lower() == 'c++')

        create_listing = self.pyrex_create_listing or \
            getattr(extension, 'pyrex_create_listing', 0)
        line_directives = self.pyrex_line_directives or \
            getattr(extension, 'pyrex_line_directives', 0)
        no_c_in_traceback = self.no_c_in_traceback or \
            getattr(extension, 'no_c_in_traceback', 0)
        cplus = self.pyrex_cplus or getattr(extension, 'pyrex_cplus', 0) or \
                (extension.language and extension.language.lower() == 'c++')
        pyrex_gen_pxi = self.pyrex_gen_pxi or getattr(extension, 'pyrex_gen_pxi', 0)
        pyrex_gdb = self.pyrex_gdb or getattr(extension, 'pyrex_gdb', False)
        # Set up the include_path for the Cython compiler:
        #    1.    Start with the command line option.
        #    2.    Add in any (unique) paths from the extension
        #        pyrex_include_dirs (if Cython.Distutils.extension is used).
        #    3.    Add in any (unique) paths from the extension include_dirs
        includes = self.pyrex_include_dirs
        try:
            for i in extension.pyrex_include_dirs:
                if not i in includes:
                    includes.append(i)
        except AttributeError:
            pass
        for i in extension.include_dirs:
            if not i in includes:
                includes.append(i)

        # Set up Cython compiler directives:
        #    1. Start with the command line option.
        #    2. Add in any (unique) entries from the extension
        #         pyrex_directives (if Cython.Distutils.extension is used).
        directives = self.pyrex_directives
        if hasattr(extension, "pyrex_directives"):
            directives.update(extension.pyrex_directives)

        # Set the target_ext to '.c'.  Cython will change this to '.cpp' if
        # needed.
        if cplus:
            target_ext = '.cpp'
        else:
            target_ext = '.c'

        # Decide whether to drop the generated C files into the temp dir
        # or the source tree.

        if not self.inplace and (self.pyrex_c_in_temp
                or getattr(extension, 'pyrex_c_in_temp', 0)):
            target_dir = os.path.join(self.build_temp, "pyrex")
            for package_name in extension.name.split('.')[:-1]:
                target_dir = os.path.join(target_dir, package_name)
        else:
            target_dir = None

        newest_dependency = None
        for source in sources:
            (base, ext) = os.path.splitext(os.path.basename(source))
            if ext == ".py":
                # FIXME: we might want to special case this some more
                ext = '.pyx'
            if ext == ".pyx":              # Cython source file
                output_dir = target_dir or os.path.dirname(source)
                new_sources.append(os.path.join(output_dir, base + target_ext))
                pyrex_sources.append(source)
                pyrex_targets[source] = new_sources[-1]
            elif ext == '.pxi' or ext == '.pxd':
                if newest_dependency is None \
                        or newer(source, newest_dependency):
                    newest_dependency = source
            else:
                new_sources.append(source)

        if not pyrex_sources:
            return new_sources

        module_name = extension.name

        for source in pyrex_sources:
            target = pyrex_targets[source]
            depends = [source] + list(extension.depends or ())
            rebuild = self.force or newer_group(depends, target, 'newer')
            if not rebuild and newest_dependency is not None:
                rebuild = newer(newest_dependency, target)
            if rebuild:
                log.info("cythoning %s to %s", source, target)
                self.mkpath(os.path.dirname(target))
                if self.inplace:
                    output_dir = os.curdir
                else:
                    output_dir = self.build_lib
                options = CompilationOptions(pyrex_default_options,
                    use_listing_file = create_listing,
                    include_path = includes,
                    compiler_directives = directives,
                    output_file = target,
                    cplus = cplus,
                    emit_linenums = line_directives,
                    c_line_in_traceback = not no_c_in_traceback,
                    generate_pxi = pyrex_gen_pxi,
                    output_dir = output_dir,
                    gdb_debug = pyrex_gdb)
                result = cython_compile(source, options=options,
                                        full_module_name=module_name)
            else:
                log.info("skipping '%s' Cython extension (up-to-date)", target)

        return new_sources

    # cython_sources ()

# class build_ext
