#
#   Cython - Command Line Parsing
#

from __future__ import absolute_import

import os
import sys
from argparse import ArgumentParser, Action, SUPPRESS
from . import Options


class ParseDirectivesAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        old_directives = dict(getattr(namespace, self.dest,
                                      Options.get_directive_defaults()))
        directives = Options.parse_directive_list(
            values, relaxed_bool=True, current_settings=old_directives)
        setattr(namespace, self.dest, directives)


class ParseOptionsAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        options = dict(getattr(namespace, self.dest, {}))
        for opt in values.split(','):
            if '=' in opt:
                n, v = opt.split('=', 1)
                v = v.lower() not in ('false', 'f', '0', 'no')
            else:
                n, v = opt, True
            options[n] = v
        setattr(namespace, self.dest, options)


class ParseCompileTimeEnvAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        old_env = dict(getattr(namespace, self.dest, {}))
        new_env = Options.parse_compile_time_env(values, current_settings=old_env)
        setattr(namespace, self.dest, new_env)


class ActivateAllWarningsAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        directives = getattr(namespace, 'compiler_directives', {})
        directives.update(Options.extra_warnings)
        setattr(namespace, 'compiler_directives', directives)


class SetLenientAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'error_on_unknown_names', False)
        setattr(namespace, 'error_on_uninitialized', False)


class SetGDBDebugAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'gdb_debug', True)
        setattr(namespace, 'output_dir', os.curdir)


class SetGDBDebugOutputAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'gdb_debug', True)
        setattr(namespace, 'output_dir', values)


class SetAnnotateCoverageAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'annotate', True)
        setattr(namespace, 'annotate_coverage_xml', values)


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


def parse_command_line_raw(args):
    description = "Cython (https://cython.org/) is a compiler for code written in the "\
                  "Cython language.  Cython is based on Pyrex by Greg Ewing."

    parser = ArgumentParser(description=description)

    parser.add_argument("-V", "--version", dest='show_version', action='store_const', const=1,
                      help='Display version number of cython compiler')
    parser.add_argument("-l", "--create-listing", dest='use_listing_file', action='store_const', const=1,
                      help='Write error messages to a listing file')
    parser.add_argument("-I", "--include-dir", dest='include_path', action='append',
                      help='Search for include files in named directory '
                           '(multiple include directories are allowed).')
    parser.add_argument("-o", "--output-file", dest='output_file', action='store', type=str,
                      help='Specify name of generated C file')
    parser.add_argument("-t", "--timestamps", dest='timestamps', action='store_const', const=1,
                      help='Only compile newer source files')
    parser.add_argument("-f", "--force", dest='timestamps', action='store_const', const=0,
                      help='Compile all source files (overrides implied -t)')
    parser.add_argument("-v", "--verbose", dest='verbose', action='count',
                      help='Be verbose, print file names on multiple compilation')
    parser.add_argument("-p", "--embed-positions", dest='embed_pos_in_docstring', action='store_const', const=1,
                      help='If specified, the positions in Cython files of each '
                           'function definition is embedded in its docstring.')
    parser.add_argument("--cleanup", dest='generate_cleanup_code', action='store', type=int,
                      help='Release interned objects on python exit, for memory debugging. '
                           'Level indicates aggressiveness, default 0 releases nothing.')
    parser.add_argument("-w", "--working", dest='working_path', action='store', type=str,
                      help='Sets the working directory for Cython (the directory modules are searched from)')
    parser.add_argument("--gdb", action=SetGDBDebugAction, nargs=0,
                      help='Output debug information for cygdb')
    parser.add_argument("--gdb-outdir", action=SetGDBDebugOutputAction, type=str,
                      help='Specify gdb debug information output directory. Implies --gdb.')
    parser.add_argument("-D", "--no-docstrings", dest='docstrings', action='store_false', default=None,
                      help='Strip docstrings from the compiled module.')
    parser.add_argument('-a', '--annotate', action='store_const', const='default', dest='annotate',
                      help='Produce a colorized HTML version of the source.')
    parser.add_argument('--annotate-fullc', action='store_const', const='fullc', dest='annotate',
                      help='Produce a colorized HTML version of the source '
                           'which includes entire generated C/C++-code.')
    parser.add_argument("--annotate-coverage", dest='annotate_coverage_xml', action=SetAnnotateCoverageAction, type=str,
                      help='Annotate and include coverage information from cov.xml.')
    parser.add_argument("--line-directives", dest='emit_linenums', action='store_true', default=None,
                      help='Produce #line directives pointing to the .pyx source')
    parser.add_argument("-+", "--cplus", dest='cplus', action='store_const', const=1,
                      help='Output a C++ rather than C file.')
    parser.add_argument('--embed', nargs='?', const='main', type=str,
                      help='Generate a main() function that embeds the Python interpreter.')
    parser.add_argument('-2', dest='language_level', action='store_const', const=2,
                      help='Compile based on Python-2 syntax and code semantics.')
    parser.add_argument('-3', dest='language_level', action='store_const', const=3,
                      help='Compile based on Python-3 syntax and code semantics.')
    parser.add_argument('--3str', dest='language_level', action='store_const', const='3str',
                      help='Compile based on Python-3 syntax and code semantics without '
                           'assuming unicode by default for string literals under Python 2.')
    parser.add_argument("--lenient", action=SetLenientAction, nargs=0,
                      help='Change some compile time errors to runtime errors to '
                           'improve Python compatibility')
    parser.add_argument("--capi-reexport-cincludes", dest='capi_reexport_cincludes', action='store_true', default=None,
                      help='Add cincluded headers to any auto-generated header files.')
    parser.add_argument("--fast-fail", dest='fast_fail', action='store_true',
                      help='Abort the compilation on the first error')
    parser.add_argument("-Werror", "--warning-errors", dest='warning_errors', action='store_true', default=None,
                      help='Make all warnings into errors')
    parser.add_argument("-Wextra", "--warning-extra", action=ActivateAllWarningsAction, nargs=0,
                      help='Enable extra warnings')

    parser.add_argument('-X', '--directive', metavar='NAME=VALUE,...',
                      dest='compiler_directives', default={}, type=str,
                      action=ParseDirectivesAction,
                      help='Overrides a compiler directive')
    parser.add_argument('-E', '--compile-time-env', metavar='NAME=VALUE,...',
                      dest='compile_time_env', default={}, type=str,
                      action=ParseCompileTimeEnvAction,
                      help='Provides compile time env like DEF would do.')
    parser.add_argument('sources', nargs='*')

    # TODO: add help
    parser.add_argument("-z", "--pre-import", dest='pre_import', action='store', type=str, help=SUPPRESS)
    parser.add_argument("--convert-range", dest='convert_range', action='store_true', default=None, help=SUPPRESS)
    parser.add_argument("--no-c-in-traceback", dest='c_line_in_traceback', action='store_false', default=None, help=SUPPRESS)
    parser.add_argument("--cimport-from-pyx", dest='cimport_from_pyx', action='store_true', default=None, help=SUPPRESS)
    parser.add_argument("--old-style-globals", dest='old_style_globals', action='store_true', default=None, help=SUPPRESS)

    arguments, unknown = parser.parse_known_args(args)

    sources = arguments.sources
    del arguments.sources

    # unknown can be either debug or input files or really unknown
    for option in unknown:
        if option.startswith('--debug'):
            option = option[2:].replace('-', '_')
            setattr(arguments, option, True)
        elif option.startswith('-'):
            parser.error("unknown option " + option)
        else:
            sources.append(option)

    return arguments, sources


def parse_command_line(args):
    arguments, sources = parse_command_line_raw(args)

    options = Options.CompilationOptions(Options.default_options)
    for name, value in vars(arguments).items():
        if value is None or value == {}:
            continue
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

