import sys
import os

if 'setuptools' in sys.modules:
    try:
        from setuptools.command.build_ext import build_ext as _build_ext
    except ImportError:
        # We may be in the process of importing setuptools, which tries
        # to import this.
        from distutils.command.build_ext import build_ext as _build_ext
else:
    from distutils.command.build_ext import build_ext as _build_ext

try:
    from __builtin__ import basestring
except ImportError:
    basestring = str


class build_ext(_build_ext, object):

    sep_by = _build_ext.sep_by
    user_options = _build_ext.user_options[:]
    boolean_options = _build_ext.boolean_options[:]

    user_options.extend([
        ('cython-cplus', None,
         "generate C++ source files"),
        ('cython-create-listing', None,
         "write errors to a listing file"),
        ('cython-line-directives', None,
         "emit source line directives"),
        ('cython-include-dirs=', None,
         "path to the Cython include files" + sep_by),
        ('cython-c-in-temp', None,
         "put generated C files in temp directory"),
        ('cython-gen-pxi', None,
            "generate .pxi file for public declarations"),
        ('cython-directives=', None,
            "compiler directive overrides"),
        ('cython-gdb', None,
         "generate debug information for cygdb"),
        ('cython-compile-time-env', None,
            "cython compile time environment"),

        # For backwards compatibility.
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
        'cython-cplus', 'cython-create-listing', 'cython-line-directives',
        'cython-c-in-temp', 'cython-gdb',

        # For backwards compatibility.
        'pyrex-cplus', 'pyrex-create-listing', 'pyrex-line-directives',
        'pyrex-c-in-temp', 'pyrex-gdb',
    ])

    def initialize_options(self):
        _build_ext.initialize_options(self)
        self.cython_cplus = 0
        self.cython_create_listing = 0
        self.cython_line_directives = 0
        self.cython_include_dirs = None
        self.cython_directives = None
        self.cython_c_in_temp = 0
        self.cython_gen_pxi = 0
        self.cython_gdb = False
        self.no_c_in_traceback = 0
        self.cython_compile_time_env = None

    def __getattr__(self, name):
        if name[:6] == 'pyrex_':
            return getattr(self, 'cython_' + name[6:])
        else:
            return _build_ext.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name[:6] == 'pyrex_':
            return setattr(self, 'cython_' + name[6:], value)
        else:
            self.__dict__[name] = value

    def finalize_options(self):
        _build_ext.finalize_options(self)
        if self.cython_include_dirs is None:
            self.cython_include_dirs = []
        elif isinstance(self.cython_include_dirs, basestring):
            self.cython_include_dirs = \
                self.cython_include_dirs.split(os.pathsep)
        if self.cython_directives is None:
            self.cython_directives = {}

    def build_extension(self, ext):
        from Cython.Build.Dependencies import cythonize

        # Set up the include_path for the Cython compiler:
        #    1.    Start with the command line option.
        #    2.    Add in any (unique) paths from the extension
        #        cython_include_dirs (if Cython.Distutils.extension is used).
        #    3.    Add in any (unique) paths from the extension include_dirs
        includes = list(self.cython_include_dirs)
        try:
            for i in ext.cython_include_dirs:
                if i not in includes:
                    includes.append(i)
        except AttributeError:
            pass

        # In case extension.include_dirs is a generator, evaluate it and keep
        # result
        ext.include_dirs = list(ext.include_dirs)
        for i in ext.include_dirs:
            if i not in includes:
                includes.append(i)

        # Set up Cython compiler directives:
        #    1. Start with the command line option.
        #    2. Add in any (unique) entries from the extension
        #         cython_directives (if Cython.Distutils.extension is used).
        directives = dict(self.cython_directives)
        if hasattr(ext, "cython_directives"):
            directives.update(ext.cython_directives)

        no_c_in_traceback = not self.no_c_in_traceback or \
                getattr(ext, 'no_c_in_traceback', 0)

        options = {
            'cplus': self.cython_cplus or getattr(ext, 'cython_cplus', 0) or \
                (ext.language and ext.language.lower() == 'c++'),
            'use_listing_file': self.cython_create_listing or \
                getattr(ext, 'cython_create_listing', 0),
            'emit_linenums': self.cython_line_directives or \
                getattr(ext, 'cython_line_directives', 0),
            'include_path': includes,
            'compiler_directives': directives,
            'build_dir': self.build_temp if self.cython_c_in_temp else None,
            'generate_pxi': self.cython_gen_pxi or getattr(ext, 'cython_gen_pxi', 0),
            'gdb_debug': self.cython_gdb or getattr(ext, 'cython_gdb', False),
            'c_line_in_traceback': no_c_in_traceback,
            'compile_time_env': self.cython_compile_time_env or \
                getattr(ext, 'cython_compile_time_env', None),
        }

        new_ext = cythonize(
            ext,force=self.force, quiet=self.verbose == 0, **options
        )[0]

        ext.sources = new_ext.sources
        super(build_ext, self).build_extension(ext)

# backward compatibility
new_build_ext = build_ext
