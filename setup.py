from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib
import os, os.path
import sys

if 'sdist' in sys.argv and sys.platform != "win32":
    assert os.system("git show-ref -s HEAD > .gitrev") == 0

if sys.platform == "darwin":
    # Don't create resource files on OS X tar.
    os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
    os.environ['COPYFILE_DISABLE'] = 'true'

setup_args = {}

def add_command_class(name, cls):
    cmdclasses = setup_args.get('cmdclass', {})
    cmdclasses[name] = cls
    setup_args['cmdclass'] = cmdclasses

if sys.version_info[0] >= 3:
    import lib2to3.refactor
    from distutils.command.build_py \
         import build_py_2to3 as build_py
    # need to convert sources to Py3 on installation
    fixers = [ fix for fix in lib2to3.refactor.get_fixers_from_package("lib2to3.fixes")
               if fix.split('fix_')[-1] not in ('next',)
               ]
    build_py.fixer_names = fixers
    add_command_class("build_py", build_py)

pxd_include_dirs = [
    directory for directory, dirs, files in os.walk('Cython/Includes')
    if '__init__.pyx' in files or '__init__.pxd' in files
    or directory == 'Cython/Includes' or directory == 'Cython/Includes/Deprecated']

pxd_include_patterns = [
    p+'/*.pxd' for p in pxd_include_dirs ] + [
    p+'/*.pyx' for p in pxd_include_dirs ]

if sys.version_info < (2,4):
    install_base_dir = get_python_lib(prefix='')
    import glob
    patterns = pxd_include_patterns + [
        'Cython/Plex/*.pxd',
        'Cython/Compiler/*.pxd',
        'Cython/Runtime/*.pyx'
        ]
    setup_args['data_files'] = [
        (os.path.dirname(os.path.join(install_base_dir, pattern)),
         [ f for f in glob.glob(pattern) ])
        for pattern in patterns
        ]
else:
    setup_args['package_data'] = {
        'Cython.Plex'     : ['*.pxd'],
        'Cython.Compiler' : ['*.pxd'],
        'Cython.Runtime'  : ['*.pyx', '*.pxd'],
        'Cython'          : [ p[7:] for p in pxd_include_patterns ],
        }

# This dict is used for passing extra arguments that are setuptools
# specific to setup
setuptools_extra_args = {}

# tells whether to include cygdb (the script and the Cython.Debugger package
include_debugger = sys.version_info[:2] > (2, 5)

if 'setuptools' in sys.modules:
    setuptools_extra_args['zip_safe'] = False
    setuptools_extra_args['entry_points'] = {
        'console_scripts': [
            'cython = Cython.Compiler.Main:setuptools_main',
        ]
    }
    scripts = []
else:
    if os.name == "posix":
        scripts = ["bin/cython"]
        if include_debugger:
            scripts.append('bin/cygdb')
    else:
        scripts = ["cython.py"]
        if include_debugger:
            scripts.append('cygdb.py')

def compile_cython_modules(profile=False, compile_more=False, cython_with_refnanny=False):
    source_root = os.path.abspath(os.path.dirname(__file__))
    compiled_modules = ["Cython.Plex.Scanners",
                        "Cython.Plex.Actions",
                        "Cython.Compiler.Lexicon",
                        "Cython.Compiler.Scanning",
                        "Cython.Compiler.Parsing",
                        "Cython.Compiler.Visitor",
                        "Cython.Compiler.Code",
                        "Cython.Runtime.refnanny",]
    if compile_more:
        compiled_modules.extend([
            "Cython.Compiler.ParseTreeTransforms",
            "Cython.Compiler.Nodes",
            "Cython.Compiler.ExprNodes",
            "Cython.Compiler.ModuleNode",
            "Cython.Compiler.Optimize",
            ])

    defines = []
    if cython_with_refnanny:
        defines.append(('CYTHON_REFNANNY', '1'))

    extensions = []
    if sys.version_info[0] >= 3:
        from Cython.Distutils import build_ext as build_ext_orig
        for module in compiled_modules:
            source_file = os.path.join(source_root, *module.split('.'))
            if os.path.exists(source_file + ".py"):
                pyx_source_file = source_file + ".py"
            else:
                pyx_source_file = source_file + ".pyx"
            dep_files = []
            if os.path.exists(source_file + '.pxd'):
                dep_files.append(source_file + '.pxd')
            if '.refnanny' in module:
                defines_for_module = []
            else:
                defines_for_module = defines
            extensions.append(
                Extension(module, sources = [pyx_source_file],
                          define_macros = defines_for_module,
                          depends = dep_files)
                )

        class build_ext(build_ext_orig):
            # we must keep the original modules alive to make sure
            # their code keeps working when we remove them from
            # sys.modules
            dead_modules = []

            def build_extensions(self):
                # add path where 2to3 installed the transformed sources
                # and make sure Python (re-)imports them from there
                already_imported = [ module for module in sys.modules
                                     if module == 'Cython' or module.startswith('Cython.') ]
                keep_alive = self.dead_modules.append
                for module in already_imported:
                    keep_alive(sys.modules[module])
                    del sys.modules[module]
                sys.path.insert(0, os.path.join(source_root, self.build_lib))

                if profile:
                    from Cython.Compiler.Options import directive_defaults
                    directive_defaults['profile'] = True
                    print("Enabled profiling for the Cython binary modules")
                build_ext_orig.build_extensions(self)

        setup_args['ext_modules'] = extensions
        add_command_class("build_ext", build_ext)

    else: # Python 2.x
        from distutils.command.build_ext import build_ext as build_ext_orig
        try:
            class build_ext(build_ext_orig):
                def build_extension(self, ext, *args, **kargs):
                    try:
                        build_ext_orig.build_extension(self, ext, *args, **kargs)
                    except StandardError:
                        print("Compilation of '%s' failed" % ext.sources[0])
            from Cython.Compiler.Main import compile
            from Cython import Utils
            if profile:
                from Cython.Compiler.Options import directive_defaults
                directive_defaults['profile'] = True
                print("Enabled profiling for the Cython binary modules")
            source_root = os.path.dirname(__file__)
            for module in compiled_modules:
                source_file = os.path.join(source_root, *module.split('.'))
                if os.path.exists(source_file + ".py"):
                    pyx_source_file = source_file + ".py"
                else:
                    pyx_source_file = source_file + ".pyx"
                c_source_file = source_file + ".c"
                source_is_newer = False
                if not os.path.exists(c_source_file):
                    source_is_newer = True
                else:
                    c_last_modified = Utils.modification_time(c_source_file)
                    if Utils.file_newer_than(pyx_source_file, c_last_modified):
                        source_is_newer = True
                    else:
                        pxd_source_file = source_file + ".pxd"
                        if os.path.exists(pxd_source_file) and Utils.file_newer_than(pxd_source_file, c_last_modified):
                            source_is_newer = True
                if source_is_newer:
                    print("Compiling module %s ..." % module)
                    result = compile(pyx_source_file)
                    c_source_file = result.c_file
                if c_source_file:
                    # Py2 distutils can't handle unicode file paths
                    if isinstance(c_source_file, unicode):
                        filename_encoding = sys.getfilesystemencoding()
                        if filename_encoding is None:
                            filename_encoding = sys.getdefaultencoding()
                        c_source_file = c_source_file.encode(filename_encoding)
                    if '.refnanny' in module:
                        defines_for_module = []
                    else:
                        defines_for_module = defines
                    extensions.append(
                        Extension(module, sources = [c_source_file],
                                  define_macros = defines_for_module)
                        )
                else:
                    print("Compilation failed")
            if extensions:
                setup_args['ext_modules'] = extensions
                add_command_class("build_ext", build_ext)
        except Exception:
            print('''
ERROR: %s

Extension module compilation failed, looks like Cython cannot run
properly on this system.  To work around this, pass the option
"--no-cython-compile".  This will install a pure Python version of
Cython without compiling its own sources.
''' % sys.exc_info()[1])
            raise

cython_profile = '--cython-profile' in sys.argv
if cython_profile:
    sys.argv.remove('--cython-profile')

try:
    sys.argv.remove("--cython-compile-all")
    cython_compile_more = True
except ValueError:
    cython_compile_more = False

try:
    sys.argv.remove("--cython-with-refnanny")
    cython_with_refnanny = True
except ValueError:
    cython_with_refnanny = False

try:
    sys.argv.remove("--no-cython-compile")
except ValueError:
    compile_cython_modules(cython_profile, cython_compile_more, cython_with_refnanny)

setup_args.update(setuptools_extra_args)

from Cython import __version__ as version

packages = [
    'Cython',
    'Cython.Build',
    'Cython.Compiler',
    'Cython.Runtime',
    'Cython.Distutils',
    'Cython.Plex',
    'Cython.Tests',
    'Cython.Build.Tests',
    'Cython.Compiler.Tests',
]

if include_debugger:
    packages.append('Cython.Debugger')
    packages.append('Cython.Debugger.Tests')
    # it's enough to do this for Py2.5+:
    setup_args['package_data']['Cython.Debugger.Tests'] = ['codefile', 'cfuncs.c']


setup(
  name = 'Cython',
  version = version,
  url = 'http://www.cython.org',
  author = 'Greg Ewing, Robert Bradshaw, Stefan Behnel, Dag Seljebotn, et al.',
  author_email = 'cython-dev@codespeak.net',
  description = "The Cython compiler for writing C extensions for the Python language.",
  long_description = """\
  The Cython language makes writing C extensions for the Python language as
  easy as Python itself.  Cython is a source code translator based on the
  well-known Pyrex_, but supports more cutting edge functionality and
  optimizations.

  The Cython language is very close to the Python language (and most Python
  code is also valid Cython code), but Cython additionally supports calling C
  functions and declaring C types on variables and class attributes. This
  allows the compiler to generate very efficient C code from Cython code.

  This makes Cython the ideal language for writing glue code for external C
  libraries, and for fast C modules that speed up the execution of Python
  code.

  .. _Pyrex: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/
  """,
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: C",
    "Programming Language :: Cython",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],

  scripts = scripts,
  packages=packages,

  # pyximport
  py_modules = ["pyximport/__init__",
                "pyximport/pyximport",
                "pyximport/pyxbuild",

                "cython"],

  **setup_args
  )
