"""Pyrex.Distutils.extension

Provides a modified Extension class, that understands hou to describe
Pyrex extension modules in setup scripts."""

__revision__ = "$Id:$"

import os, string, sys
from types import *
import distutils.extension as _Extension

try:
    import warnings
except ImportError:
    warnings = None

class Extension(_Extension.Extension):
    _Extension.Extension.__doc__ + \
    """pyrex_include_dirs : [string]
        list of directories to search for Pyrex header files (.pxd) (in
        Unix form for portability)
    pyrex_create_listing_file : boolean
        write pyrex error messages to a listing (.lis) file.
    pyrex_cplus : boolean
        use the C++ compiler for compiling and linking.
    pyrex_c_in_temp : boolean
        put generated C files in temp directory.
    pyrex_gen_pxi : boolean
        generate .pxi file for public declarations
    """

    # When adding arguments to this constructor, be sure to update
    # user_options.extend in build_ext.py.
    def __init__ (self, name, sources,
            include_dirs = None,
            define_macros = None,
            undef_macros = None,
            library_dirs = None,
            libraries = None,
            runtime_library_dirs = None,
            extra_objects = None,
            extra_compile_args = None,
            extra_link_args = None,
            export_symbols = None,
            #swig_opts = None,
            depends = None,
            language = None,
            pyrex_include_dirs = None,
            pyrex_create_listing = 0,
            pyrex_cplus = 0,
            pyrex_c_in_temp = 0,
            pyrex_gen_pxi = 0,
            **kw):

        _Extension.Extension.__init__(self, name, sources,
            include_dirs = include_dirs,
            define_macros = define_macros,
            undef_macros = undef_macros,
            library_dirs = library_dirs,
            libraries = libraries,
            runtime_library_dirs = runtime_library_dirs,
            extra_objects = extra_objects,
            extra_compile_args = extra_compile_args,
            extra_link_args = extra_link_args,
            export_symbols = export_symbols,
            #swig_opts = swig_opts,
            depends = depends,
            language = language,
            **kw)

        self.pyrex_include_dirs = pyrex_include_dirs or []
        self.pyrex_create_listing = pyrex_create_listing
        self.pyrex_cplus = pyrex_cplus
        self.pyrex_c_in_temp = pyrex_c_in_temp
        self.pyrex_gen_pxi = pyrex_gen_pxi

# class Extension

read_setup_file = _Extension.read_setup_file
