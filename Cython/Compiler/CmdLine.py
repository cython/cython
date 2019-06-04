#
#   Cython - Command Line Parsing
#

from __future__ import absolute_import

import os
import sys
from . import Options

usage = """\
Cython (https://cython.org/) is a compiler for code written in the
Cython language.  Cython is based on Pyrex by Greg Ewing.

Usage: cython [options] sourcefile.{pyx,py} ...

Options:
  -V, --version                  Display version number of cython compiler
  -l, --create-listing           Write error messages to a listing file
  -I, --include-dir <directory>  Search for include files in named directory
                                 (multiple include directories are allowed).
  -o, --output-file <filename>   Specify name of generated C file
  -t, --timestamps               Only compile newer source files
  -f, --force                    Compile all source files (overrides implied -t)
  -v, --verbose                  Be verbose, print file names on multiple compilation
  -p, --embed-positions          If specified, the positions in Cython files of each
                                 function definition is embedded in its docstring.
  --cleanup <level>              Release interned objects on python exit, for memory debugging.
                                 Level indicates aggressiveness, default 0 releases nothing.
  -w, --working <directory>      Sets the working directory for Cython (the directory modules
                                 are searched from)
  --gdb                          Output debug information for cygdb
  --gdb-outdir <directory>       Specify gdb debug information output directory. Implies --gdb.

  -D, --no-docstrings            Strip docstrings from the compiled module.
  -a, --annotate                 Produce a colorized HTML version of the source.
  --annotate-fullc               Produce a colorized HTML version of the source which
                                 includes entire generated C/C++-code.
  --annotate-coverage <cov.xml>  Annotate and include coverage information from cov.xml.
  --line-directives              Produce #line directives pointing to the .pyx source
  --cplus                        Output a C++ rather than C file.
  --embed[=<method_name>]        Generate a main() function that embeds the Python interpreter.
  -2                             Compile based on Python-2 syntax and code semantics.
  -3                             Compile based on Python-3 syntax and code semantics.
  --3str                         Compile based on Python-3 syntax and code semantics without
                                 assuming unicode by default for string literals under Python 2.
  --lenient                      Change some compile time errors to runtime errors to
                                 improve Python compatibility
  --capi-reexport-cincludes      Add cincluded headers to any auto-generated header files.
  --fast-fail                    Abort the compilation on the first error
  --warning-errors, -Werror      Make all warnings into errors
  --warning-extra, -Wextra       Enable extra warnings
  -X, --directive <name>=<value>[,<name=value,...] Overrides a compiler directive
  -E, --compile-time-env name=value[,<name=value,...] Provides compile time env like DEF would do.
"""


# The following experimental options are supported only on MacOSX:
#  -C, --compile    Compile generated .c file to .o file
#  --link           Link .o file to produce extension module (implies -C)
#  -+, --cplus      Use C++ compiler for compiling and linking
#  Additional .o files to link may be supplied when using -X."""

def bad_usage():
    sys.stderr.write(usage)
    sys.exit(1)


def parse_command_line(args):
    pending_arg = []

    def pop_arg():
        if not args or pending_arg:
            bad_usage()
        if '=' in args[0] and args[0].startswith('--'):  # allow "--long-option=xyz"
            name, value = args.pop(0).split('=', 1)
            pending_arg.append(value)
            return name
        return args.pop(0)

    def pop_value(default=None):
        if pending_arg:
            return pending_arg.pop()
        elif default is not None:
            return default
        elif not args:
            bad_usage()
        return args.pop(0)

    def get_param(option):
        tail = option[2:]
        if tail:
            return tail
        else:
            return pop_arg()

    sources = []
    arguments = {}
    while args:
        if args[0].startswith("-"):
            option = pop_arg()
            if option in ("-V", "--version"):
                arguments['show_version'] = 1
            elif option in ("-l", "--create-listing"):
                arguments['use_listing_file'] = 1
            elif option in ("-+", "--cplus"):
                arguments['cplus'] = 1
            elif option == "--embed":
                arguments['embed'] = pop_value("main")
            elif option.startswith("-I"):
                i_path = arguments.get('include_path', [])
                i_path.append(get_param(option))
                arguments['include_path'] = i_path
            elif option == "--include-dir":
                i_path = arguments.get('include_path', [])
                i_path.append(pop_value())
                arguments['include_path'] = i_path
            elif option in ("-w", "--working"):
                arguments['working_path'] = pop_value()
            elif option in ("-o", "--output-file"):
                arguments['output_file'] = pop_value()
            elif option in ("-t", "--timestamps"):
                arguments['timestamps'] = 1
            elif option in ("-f", "--force"):
                arguments['timestamps'] = 0
            elif option in ("-v", "--verbose"):
                arguments['verbose'] = arguments.get('verbose', 0) + 1
            elif option in ("-p", "--embed-positions"):
                arguments['embed_pos_in_docstring'] = 1
            elif option in ("-z", "--pre-import"):
                arguments['pre_import'] = pop_value()
            elif option == "--cleanup":
                arguments['generate_cleanup_code'] = int(pop_value())
            elif option in ("-D", "--no-docstrings"):
                arguments['docstrings'] = False
            elif option in ("-a", "--annotate"):
                arguments['annotate'] = "default"
            elif option == "--annotate-fullc":
                arguments['annotate'] = "fullc"
            elif option == "--annotate-coverage":
                arguments['annotate'] = True
                arguments['annotate_coverage_xml'] = pop_value()
            elif option == "--convert-range":
                arguments['convert_range'] = True
            elif option == "--line-directives":
                arguments['emit_linenums'] = True
            elif option == "--no-c-in-traceback":
                arguments['c_line_in_traceback'] = False
            elif option == "--gdb":
                arguments['gdb_debug'] = True
                arguments['output_dir'] = os.curdir
            elif option == "--gdb-outdir":
                arguments['gdb_debug'] = True
                arguments['output_dir'] = pop_value()
            elif option == "--lenient":
                arguments['error_on_unknown_names'] = False
                arguments['error_on_uninitialized'] = False
            elif option == '-2':
                arguments['language_level'] = 2
            elif option == '-3':
                arguments['language_level'] = 3
            elif option == '--3str':
                arguments['language_level'] = '3str'
            elif option == "--capi-reexport-cincludes":
                arguments['capi_reexport_cincludes'] = True
            elif option == "--fast-fail":
                arguments['fast_fail'] = True
            elif option == "--cimport-from-pyx":
                arguments['cimport_from_pyx'] = True
            elif option in ('-Werror', '--warning-errors'):
                arguments['warning_errors'] = True
            elif option in ('-Wextra', '--warning-extra'):
                directives = arguments.get('compiler_directives', {})
                directives.update(Options.extra_warnings)
                arguments['compiler_directives'] = directives
            elif option == "--old-style-globals":
                arguments['old_style_globals'] = True
            elif option == "--directive" or option.startswith('-X'):
                if option.startswith('-X') and option[2:].strip():
                    x_args = option[2:]
                else:
                    x_args = pop_value()
                try:
                    directives = arguments.get('compiler_directives', {})
                    directives = Options.parse_directive_list(
                        x_args, relaxed_bool=True,
                        current_settings=directives)
                    arguments['compiler_directives'] = directives
                except ValueError as e:
                    sys.stderr.write("Error in compiler directive: %s\n" % e.args[0])
                    sys.exit(1)
            elif option == "--compile-time-env" or option.startswith('-E'):
                if option.startswith('-E') and option[2:].strip():
                    x_args = option[2:]
                else:
                    x_args = pop_value()
                try:
                    envs = arguments.get('compile_time_env', {})
                    envs = Options.parse_compile_time_env(
                        x_args, current_settings=envs)
                    arguments['compile_time_env'] = envs
                except ValueError as e:
                    sys.stderr.write("Error in compile-time-env: %s\n" % e.args[0])
                    sys.exit(1)
            elif option.startswith('--debug'):
                option = option[2:].replace('-', '_')
                arguments[option] = True
            elif option in ('-h', '--help'):
                sys.stdout.write(usage)
                sys.exit(0)
            else:
                sys.stderr.write("Unknown compiler flag: %s\n" % option)
                sys.exit(1)
        else:
            sources.append(pop_arg())

    if pending_arg:
        bad_usage()

    options = Options.CompilationOptions(Options.default_options)
    for name, value in arguments.items():
        if name.startswith('debug'):
            from . import DebugFlags
            if name in dir(DebugFlags):
                setattr(DebugFlags, name, value)
            else:
                sys.stderr.write("Unknown debug flag: %s\n" % name)
                bad_usage()
        elif hasattr(Options, name):
            setattr(Options, name, value)
        else:
            setattr(options, name, value)

    if options.use_listing_file and len(sources) > 1:
        sys.stderr.write(
            "cython: Only one source file allowed when using -o\n")
        sys.exit(1)
    if len(sources) == 0 and not options.show_version:
        bad_usage()
    if Options.embed and len(sources) > 1:
        sys.stderr.write(
            "cython: Only one source file allowed when using -embed\n")
        sys.exit(1)
    return options, sources

