import sys
import os

# Always inherit from the "build_ext" in distutils since setuptools already imports
# it from Cython if available, and does the proper distutils fallback otherwise.
# https://github.com/pypa/setuptools/blob/9f1822ee910df3df930a98ab99f66d18bb70659b/setuptools/command/build_ext.py#L16

# setuptools imports Cython's "build_ext", so make sure we go first.
_build_ext_module = sys.modules.get('setuptools.command.build_ext')
if _build_ext_module is None:
    try:
        import distutils.command.build_ext as _build_ext_module
    except ImportError:
        # Python 3.12 no longer has distutils, but setuptools can replace it.
        try:
            import setuptools.command.build_ext as _build_ext_module
        except ImportError:
            raise ImportError("'distutils' cannot be imported. Please install setuptools.")


# setuptools remembers the original distutils "build_ext" as "_du_build_ext"
_build_ext = getattr(_build_ext_module, '_du_build_ext', None)
if _build_ext is None:
    _build_ext = getattr(_build_ext_module, 'build_ext', None)
if _build_ext is None:
    from distutils.command.build_ext import build_ext as _build_ext

PGO_CONFIG = {
    'gcc': {
        'gen': ['-fprofile-generate', '-fprofile-dir={TEMPDIR}'],
        'use': ['-fprofile-use', '-fprofile-correction', '-fprofile-dir={TEMPDIR}'],
    },
    # blind copy from 'configure' script in CPython 3.7
    'icc': {
        'gen': ['-prof-gen'],
        'use': ['-prof-use'],
    }
}
PGO_CONFIG['mingw32'] = PGO_CONFIG['gcc']

class build_ext(_build_ext):

    user_options = _build_ext.user_options + [
        ('cython-cplus', None,
             "generate C++ source files"),
        ('cython-create-listing', None,
             "write errors to a listing file"),
        ('cython-line-directives', None,
             "emit source line directives"),
        ('cython-include-dirs=', None,
             "path to the Cython include files" + _build_ext.sep_by),
        ('cython-c-in-temp', None,
             "put generated C files in temp directory"),
        ('cython-gen-pxi', None,
            "generate .pxi file for public declarations"),
        ('cython-gen-pgo', None,
            "generate PGO file"),
        ('cython-use-pgo', None,
            "use PGO file"),
        ('cython-directives=', None,
            "compiler directive overrides"),
        ('cython-gdb', None,
             "generate debug information for cygdb"),
        ('cython-compile-time-env', None,
            "cython compile time environment"),
        ]

    boolean_options = _build_ext.boolean_options + [
        'cython-cplus', 'cython-create-listing', 'cython-line-directives',
        'cython-c-in-temp', 'cython-gdb', 'cython-use-pgo', 'cython-gen-pgo'
    ]

    def initialize_options(self):
        super().initialize_options()
        self.cython_cplus = 0
        self.cython_create_listing = 0
        self.cython_line_directives = 0
        self.cython_include_dirs = None
        self.cython_directives = None
        self.cython_c_in_temp = 0
        self.cython_gen_pxi = 0
        self.cython_gen_pgo = 0
        self.cython_use_pgo = 0
        self.pgo_dir = None
        self.cython_gdb = False
        self.cython_compile_time_env = None
        self.shared_utility_qualified_name = None
        self.shared_utility_features_enabled = None
        self.shared_utility_features_disabled = None

    def finalize_options(self):
        super().finalize_options()
        if self.cython_include_dirs is None:
            self.cython_include_dirs = []
        elif isinstance(self.cython_include_dirs, str):
            self.cython_include_dirs = \
                self.cython_include_dirs.split(os.pathsep)
        if self.cython_directives is None:
            self.cython_directives = {}

    def get_extension_attr(self, extension, option_name, default=False):
        return getattr(self, option_name) or getattr(extension, option_name, default)

    def _add_pgo_flags(self, ext, step_name, temp_dir):
        compiler_type = self.compiler.compiler_type
        if compiler_type == 'unix':
            compiler_cmd = self.compiler.compiler_so
            if not compiler_cmd:
                pass
            elif 'clang' in compiler_cmd or 'clang' in compiler_cmd[0]:
                compiler_type = 'gcc'
            elif 'icc' in compiler_cmd or 'icc' in compiler_cmd[0]:
                compiler_type = 'icc'
            elif 'gcc' in compiler_cmd or 'gcc' in compiler_cmd[0]:
                compiler_type = 'gcc'
            elif 'g++' in compiler_cmd or 'g++' in compiler_cmd[0]:
                compiler_type = 'gcc'
            else:
                compiler_type = 'gcc'
        config = PGO_CONFIG.get(compiler_type)
        orig_flags = []
        if config and step_name in config:
            flags = [f.format(TEMPDIR=temp_dir) for f in config[step_name]]
            orig_flags.append((ext.extra_compile_args, ext.extra_link_args))
            ext.extra_compile_args = ext.extra_compile_args + flags
            ext.extra_link_args = ext.extra_link_args + flags
        else:
            print("No PGO %s configuration known for C compiler type '%s'" % (step_name, compiler_type),
                  file=sys.stderr)
        return orig_flags

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
        for include_dir in ext.include_dirs + list(self.include_dirs):
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

        pgo_dir = self.get_extension_attr(ext, 'pgo_dir', default=None)

        if self.cython_gen_pgo:
            self._add_pgo_flags(ext, 'gen', pgo_dir)
        if self.cython_use_pgo:
            self.force = 1
            self._add_pgo_flags(ext, 'use', pgo_dir)
            np_pythran = getattr(ext, 'np_pythran', False)
            c_sources = []
            for source in ext.sources:
                base, ex = os.path.splitext(source)
                if ex in ('.pyx', '.py'):
                   c_file = base + ('.cpp' if ext.language == 'c++' or np_pythran else '.c')
                   c_sources.append(c_file)
                else:
                    c_sources.append(source)
            ext.sources = c_sources
            return super().build_extension(ext)

        if hasattr(ext, 'no_c_in_traceback'):
            c_line_in_traceback = not ext.no_c_in_traceback
        else:
            c_line_in_traceback = None
        options = {
            'use_listing_file': self.get_extension_attr(ext, 'cython_create_listing'),
            'emit_linenums': self.get_extension_attr(ext, 'cython_line_directives'),
            'include_path': includes,
            'compiler_directives': directives,
            'build_dir': self.build_temp if self.get_extension_attr(ext, 'cython_c_in_temp') else None,
            'generate_pxi': self.get_extension_attr(ext, 'cython_gen_pxi'),
            'gdb_debug': self.get_extension_attr(ext, 'cython_gdb'),
            'c_line_in_traceback': c_line_in_traceback,
            'compile_time_env': self.get_extension_attr(ext, 'cython_compile_time_env', default=None),
            'shared_utility_qualified_name': self.get_extension_attr(ext, 'shared_utility_qualified_name', default=None),
            'shared_utility_features_enabled': self.get_extension_attr(ext, 'shared_utility_features_enabled', default=None),
            'shared_utility_features_disabled': self.get_extension_attr(ext, 'shared_utility_features_disabled', default=None),
        }

        new_ext = cythonize(
            ext,force=self.force, quiet=self.verbose == 0, **options
        )[0]

        ext.sources = new_ext.sources
        super().build_extension(ext)

# backward compatibility
new_build_ext = build_ext
