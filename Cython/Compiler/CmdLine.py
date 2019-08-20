#
#   Cython - Command Line Parsing
#

from __future__ import absolute_import

import os
from argparse import ArgumentParser, Action, SUPPRESS
from . import Options


GLOBAL_OPTIONS = 'global_options'
DEBUG_FLAGS = 'debug_flags'
LOCAL_OPTIONS = 'options'


def set_values_to_subargument(namespace, subargument_name, value_map):
        subarguments = getattr(namespace, subargument_name, {})
        for key, val in value_map.items():
            subarguments[key] = val
        setattr(namespace, subargument_name, subarguments)


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
        namespace.compiler_directives = directives


class SetLenientAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value_map = {'error_on_unknown_names': False,
                     'error_on_uninitialized': False}
        set_values_to_subargument(namespace, GLOBAL_OPTIONS, value_map)


class SetGDBDebugAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        namespace.gdb_debug = True
        namespace.output_dir = os.curdir


class SetGDBDebugOutputAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        namespace.gdb_debug = True
        namespace.output_dir = values


class SetAnnotateCoverageAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value_map = {'annotate': True,
                     'annotate_coverage_xml': values}
        set_values_to_subargument(namespace, GLOBAL_OPTIONS, value_map)


def StoreToSubargument(subargument_name, default_value=None):
    class StoreToSubargumentClass(Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if default_value is None:
                opt_value = values[0]
            else:
                opt_value = default_value
            set_values_to_subargument(namespace, subargument_name, {self.dest: opt_value})
    return StoreToSubargumentClass


def create_cython_argparser():
    description = "Cython (https://cython.org/) is a compiler for code written in the "\
                  "Cython language.  Cython is based on Pyrex by Greg Ewing."

    parser = ArgumentParser(description=description, argument_default=SUPPRESS)

    parser.add_argument("-V", "--version", dest='show_version',
                      action=StoreToSubargument(LOCAL_OPTIONS, 1), nargs=0,
                      help='Display version number of cython compiler')
    parser.add_argument("-l", "--create-listing", dest='use_listing_file',
                      action=StoreToSubargument(LOCAL_OPTIONS, 1), nargs=0,
                      help='Write error messages to a listing file')
    parser.add_argument("-I", "--include-dir", dest='include_path', action='append',
                      help='Search for include files in named directory '
                           '(multiple include directories are allowed).')
    parser.add_argument("-o", "--output-file", dest='output_file',
                      action=StoreToSubargument(LOCAL_OPTIONS), nargs=1, type=str,
                      help='Specify name of generated C file')
    parser.add_argument("-t", "--timestamps", dest='timestamps',
                      action=StoreToSubargument(LOCAL_OPTIONS, 1), nargs=0,
                      help='Only compile newer source files')
    parser.add_argument("-f", "--force", dest='timestamps',
                      action=StoreToSubargument(LOCAL_OPTIONS, 0), nargs=0,
                      help='Compile all source files (overrides implied -t)')
    parser.add_argument("-v", "--verbose", dest='verbose', action='count',
                      help='Be verbose, print file names on multiple compilation')
    parser.add_argument("-p", "--embed-positions", dest='embed_pos_in_docstring',
                      action=StoreToSubargument(GLOBAL_OPTIONS, 1), nargs=0,
                      help='If specified, the positions in Cython files of each '
                           'function definition is embedded in its docstring.')
    parser.add_argument("--cleanup", dest='generate_cleanup_code',
                      action=StoreToSubargument(GLOBAL_OPTIONS), nargs=1, type=int,
                      help='Release interned objects on python exit, for memory debugging. '
                           'Level indicates aggressiveness, default 0 releases nothing.')
    parser.add_argument("-w", "--working", dest='working_path',
                      action=StoreToSubargument(LOCAL_OPTIONS), nargs=1, type=str,
                      help='Sets the working directory for Cython (the directory modules are searched from)')
    parser.add_argument("--gdb", action=SetGDBDebugAction, nargs=0,
                      help='Output debug information for cygdb')
    parser.add_argument("--gdb-outdir", action=SetGDBDebugOutputAction, type=str,
                      help='Specify gdb debug information output directory. Implies --gdb.')
    parser.add_argument("-D", "--no-docstrings", dest='docstrings',
                      action=StoreToSubargument(GLOBAL_OPTIONS, False), nargs=0,
                      help='Strip docstrings from the compiled module.')
    parser.add_argument('-a', '--annotate', action=StoreToSubargument(GLOBAL_OPTIONS, 'default'), nargs=0, dest='annotate',
                      help='Produce a colorized HTML version of the source.')
    parser.add_argument('--annotate-fullc', action=StoreToSubargument(GLOBAL_OPTIONS, 'fullc'), nargs=0, dest='annotate',
                      help='Produce a colorized HTML version of the source '
                           'which includes entire generated C/C++-code.')
    parser.add_argument("--annotate-coverage", dest='annotate_coverage_xml', action=SetAnnotateCoverageAction, type=str,
                      help='Annotate and include coverage information from cov.xml.')
    parser.add_argument("--line-directives", dest='emit_linenums',
                      action=StoreToSubargument(LOCAL_OPTIONS, True), nargs=0,
                      help='Produce #line directives pointing to the .pyx source')
    parser.add_argument("-+", "--cplus", dest='cplus',
                      action=StoreToSubargument(LOCAL_OPTIONS, 1), nargs=0,
                      help='Output a C++ rather than C file.')
    parser.add_argument('--embed', action='store_const', const='main',
                      help='Generate a main() function that embeds the Python interpreter. '
                           'Pass --embed=<method_name> for a name other than main().')
    parser.add_argument('-2', dest='language_level',
                      action=StoreToSubargument(LOCAL_OPTIONS, 2), nargs=0,
                      help='Compile based on Python-2 syntax and code semantics.')
    parser.add_argument('-3', dest='language_level',
                      action=StoreToSubargument(LOCAL_OPTIONS, 3), nargs=0,
                      help='Compile based on Python-3 syntax and code semantics.')
    parser.add_argument('--3str', dest='language_level',
                      action=StoreToSubargument(LOCAL_OPTIONS, '3str'), nargs=0,
                      help='Compile based on Python-3 syntax and code semantics without '
                           'assuming unicode by default for string literals under Python 2.')
    parser.add_argument("--lenient", action=SetLenientAction, nargs=0,
                      help='Change some compile time errors to runtime errors to '
                           'improve Python compatibility')
    parser.add_argument("--capi-reexport-cincludes", dest='capi_reexport_cincludes',
                      action=StoreToSubargument(LOCAL_OPTIONS, True), nargs=0,
                      help='Add cincluded headers to any auto-generated header files.')
    parser.add_argument("--fast-fail", dest='fast_fail',
                      action=StoreToSubargument(GLOBAL_OPTIONS, True), nargs=0,
                      help='Abort the compilation on the first error')
    parser.add_argument("-Werror", "--warning-errors", dest='warning_errors',
                      action=StoreToSubargument(GLOBAL_OPTIONS, True), nargs=0,
                      help='Make all warnings into errors')
    parser.add_argument("-Wextra", "--warning-extra", action=ActivateAllWarningsAction, nargs=0,
                      help='Enable extra warnings')

    parser.add_argument('-X', '--directive', metavar='NAME=VALUE,...',
                      dest='compiler_directives', type=str,
                      action=ParseDirectivesAction,
                      help='Overrides a compiler directive')
    parser.add_argument('-E', '--compile-time-env', metavar='NAME=VALUE,...',
                      dest='compile_time_env', type=str,
                      action=ParseCompileTimeEnvAction,
                      help='Provides compile time env like DEF would do.')
    parser.add_argument('sources', nargs='*', default=[])

    # TODO: add help
    parser.add_argument("-z", "--pre-import", dest='pre_import', action=StoreToSubargument(GLOBAL_OPTIONS), nargs=1, help=SUPPRESS)
    parser.add_argument("--convert-range", dest='convert_range', action=StoreToSubargument(GLOBAL_OPTIONS, True), nargs=0, help=SUPPRESS)
    parser.add_argument("--no-c-in-traceback", dest='c_line_in_traceback', action=StoreToSubargument(LOCAL_OPTIONS, False), nargs=0, help=SUPPRESS)
    parser.add_argument("--cimport-from-pyx", dest='cimport_from_pyx', action=StoreToSubargument(GLOBAL_OPTIONS, True), nargs=0, help=SUPPRESS)
    parser.add_argument("--old-style-globals", dest='old_style_globals', action=StoreToSubargument(GLOBAL_OPTIONS, True), nargs=0, help=SUPPRESS)

    # debug stuff:
    from . import DebugFlags
    for name in vars(DebugFlags):
        if name.startswith("debug"):
            option_name = name.replace('_', '-')
            parser.add_argument("--" + option_name, action=StoreToSubargument(DEBUG_FLAGS, True), nargs=0, help=SUPPRESS)

    return parser


def parse_command_line_raw(parser, args):
    # special handling for --embed and --embed=xxxx as they aren't correctly parsed
    def filter_out_embed_options(args):
        with_embed, without_embed = [], []
        for x in args:
            if x == '--embed' or x.startswith('--embed='):
                with_embed.append(x)
            else:
                without_embed.append(x)
        return with_embed, without_embed

    with_embed, args_without_embed = filter_out_embed_options(args)

    arguments, unknown = parser.parse_known_args(args_without_embed)

    sources = arguments.sources
    del arguments.sources

    # unknown can be either debug, embed or input files or really unknown
    for option in unknown:
        if option.startswith('-'):
            parser.error("unknown option " + option)
        else:
            sources.append(option)

    # embed-stuff must be handled extra:
    for x in with_embed:
        if x == '--embed':
            name = 'main'  # default value
        else:
            name = x[len('--embed='):]
        set_values_to_subargument(arguments, GLOBAL_OPTIONS, {'embed': name})

    return arguments, sources


def parse_command_line(args):
    parser = create_cython_argparser()
    arguments, sources = parse_command_line_raw(parser, args)

    options = Options.CompilationOptions(Options.default_options)
    for name, value in vars(arguments).items():
        if name in (DEBUG_FLAGS, GLOBAL_OPTIONS, LOCAL_OPTIONS):
            continue
        else:
            setattr(options, name, value)

    # handle local_options:
    local_options = getattr(arguments, LOCAL_OPTIONS, {})
    for name, value in local_options.items():
        setattr(options, name, value)

    # handle global_options:
    global_options = getattr(arguments, GLOBAL_OPTIONS, {})
    for name, value in global_options.items():
        setattr(Options, name, value)

    # handle debug flags
    debug_flags = getattr(arguments, DEBUG_FLAGS, {})
    for name, value in debug_flags.items():
        from . import DebugFlags
        setattr(DebugFlags, name, value)

    if options.use_listing_file and len(sources) > 1:
        parser.error("cython: Only one source file allowed when using -o\n")
    if len(sources) == 0 and not options.show_version:
        parser.error("cython: Need at least one source file\n")
    if Options.embed and len(sources) > 1:
        parser.error("cython: Only one source file allowed when using -embed\n")
    return options, sources
