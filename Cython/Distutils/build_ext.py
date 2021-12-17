import os

try:
    from setuptools.command.build_ext import build_ext as _build_ext
except ImportError:
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
        ])

    boolean_options.extend([
        'cython-cplus', 'cython-create-listing', 'cython-line-directives',
        'cython-c-in-temp', 'cython-gdb',
    ])

    def initialize_options(self):
        super(build_ext, self).initialize_options()
        self.cython_cplus = 0
        self.cython_create_listing = 0
        self.cython_line_directives = 0
        self.cython_include_dirs = None
        self.cython_directives = None
        self.cython_c_in_temp = 0
        self.cython_gen_pxi = 0
        self.cython_gdb = False
        self.cython_compile_time_env = None

    def finalize_options(self):
        super(build_ext, self).finalize_options()
        if self.cython_include_dirs is None:
            self.cython_include_dirs = []
        elif isinstance(self.cython_include_dirs, basestring):
            self.cython_include_dirs = \
                self.cython_include_dirs.split(os.pathsep)
        if self.cython_directives is None:
            self.cython_directives = {}

    def get_extension_attr(self, extension, option_name, default=False):
        return getattr(self, option_name) or getattr(extension, option_name, default)

    def build_extension(self, ext):
        from Cython.Build.Dependencies import cythonize

        # Set up the include_path for the Cython compiler:
        #    1.    Start with the command line option.
        #    2.    Add in any (unique) paths from the extension
        #        cython_include_dirs (if Cython.Distutils.extension is used).
        #    3.    Add in any (unique) paths from the extension include_dirs
        includes = list(self.cython_include_dirs)
        for include_dir in getattr(ext, 'cython_include_dirs', []):
            if include_dir not in includes:
                includes.append(include_dir)

        # In case extension.include_dirs is a generator, evaluate it and keep
        # result
        ext.include_dirs = list(ext.include_dirs)
        for include_dir in ext.include_dirs:
            if include_dir not in includes:
                includes.append(include_dir)

        # Set up Cython compiler directives:
        #    1. Start with the command line option.
        #    2. Add in any (unique) entries from the extension
        #         cython_directives (if Cython.Distutils.extension is used).
        directives = dict(self.cython_directives)
        if hasattr(ext, "cython_directives"):
            directives.update(ext.cython_directives)

        if self.get_extension_attr(ext, 'cython_cplus'):
            ext.language = 'c++'

        options = {
            'use_listing_file': self.get_extension_attr(ext, 'cython_create_listing'),
            'emit_linenums': self.get_extension_attr(ext, 'cython_line_directives'),
            'include_path': includes,
            'compiler_directives': directives,
            'build_dir': self.build_temp if self.get_extension_attr(ext, 'cython_c_in_temp') else None,
            'generate_pxi': self.get_extension_attr(ext, 'cython_gen_pxi'),
            'gdb_debug': self.get_extension_attr(ext, 'cython_gdb'),
            'c_line_in_traceback': not getattr(ext, 'no_c_in_traceback', 0),
            'compile_time_env': self.get_extension_attr(ext, 'cython_compile_time_env', default=None),
        }

        new_ext = cythonize(
            ext,force=self.force, quiet=self.verbose == 0, **options
        )[0]

        ext.sources = new_ext.sources
        super(build_ext, self).build_extension(ext)

# backward compatibility
new_build_ext = build_ext
