#
#   Cython - Command Line Parsing
#

import argparse

from Cython.Compiler.Main import CompilationOptions, default_options
import Options

import os
import sys

parser = argparse.ArgumentParser(epilog=
    '''Cython (http://cython.org) is a compiler for code written in the
    Cython language.  Cython is based on Pyrex by Greg Ewing.''')

# General options
parser.add_argument('-V', '--version', dest='show_version', const=1,
    action='store_const', help='Display version number of cython compiler')

# Environment setup: include dirs, working directory &co.
working = parser.add_argument_group(title='Environment setup')

working.add_argument('-l', '--create-listing', dest='use_listing_file',
    const=1, action='store_const', help='Write error messages to a listing file')
working.add_argument('-I', '--include-dir', dest='include_path', action='append',
    help='Search for include files in named directory (multiple include directories are allowed).')
working.add_argument('-o', '--output-file', dest='output_file',
    help='Specify name of generated C file')
working.add_argument('-w', '--working', dest='working_path',
    help='Sets the working directory for Cython (the directory modules are searched from)')

# Compilation: what files to compile, based on timestamp
compilation = parser.add_argument_group(title='Compilation')

compilation.add_argument('-t', '--timestamps', dest='timestamps', const=1,
    action='store_const', help='Only compile newer source files (implied)')
compilation.add_argument('-f', '--force', dest='timestamps', const=0,
    action='store_const', help='Compile all source files (overrides -t)')

# Debugging options (both for compiler and generated files)
debug = parser.add_argument_group(title='Debugging')

# CLEANUP
debug.add_argument('--gdb', dest='gdb_debug', action='store_true',
    help='Output debug information for cygdb')

# Recursion options
recurse = parser.add_argument_group(title='Recursive compilation')

recurse.add_argument('-r', '--recursive', dest='recursive', const=1,
    action='store_const', help='Recursively find and compile dependencies (implies -t) BROKEN!!!') #FIXME
recurse.add_argument('-q', '--quiet', dest='quiet', const=1,
    action='store_const', help="Don't print module names in recursive mode")
recurse.add_argument('-v', '--verbose', dest='verbose', const=1,
    action='append_const', help='Be verbose, print file names on multiple compilation')

# Code annotation
annotate = parser.add_argument_group(title='Code annotation')

annotate.add_argument('-a', '--annotate', dest='annotate', action='store_true',
    help='Produce a colorized HTML version of the source.')
annotate.add_argument('--line-directives', dest='emit_linenums', action='store_true',
    help='Produce #line directives pointing to the .pyx source')

# Code generation options
codegen = parser.add_argument_group(title='Code generation')

#DOCSTRINGS
codegen.add_argument('--embed', dest='embed', const='main', nargs='?',
    help='Generate a main() function that embeds the Python interpreter.')
codegen.add_argument('-+', '--cplus', dest='cplus', const=1, action='store_const',
    help='Output a C++ rather than C file.')
codegen.add_argument('--no-c-in-traceback', dest='c_line_in_traceback',
    action='store_false', help='') #FIXME add help
codegen.add_argument('-2', dest='language_level', const=2, action='store_const',
    help='Compile based on Python-2 syntax and code semantics.')
codegen.add_argument('-3', dest='language_level', const=3, action='store_const',
    help='Compile based on Python-3 syntax and code semantics.')

#Source files
parser.add_argument('sources', help='Source file(s) to be compiled.', nargs='*')

class ArgsError(Exception):
    pass

def parse_command_line(args = sys.argv):
    options = CompilationOptions(default_options)
    parser.parse_args(args, namespace=options)

#    options.verbose = len(options.verbose)
    if options.gdb_debug:
        options.output_dir = os.curdir

    if options.output_file and len(sources) > 1:
        raise ArgsError('Only one source file allowed when using -o')

    if not len(sources) == 0 and not options.show_version:
        pass #FIXME

    if Options.embed and len(sources) > 1:
        raise ArgsError('Only one source file allowed when using -embed')

#    return options, sources

    print vars(options)

if __name__ == '__main__':
    parse_command_line(sys.argv[1:])













usage = """\
  -p, --embed-positions          If specified, the positions in Cython files of each
                                 function definition is embedded in its docstring.
  --cleanup <level>              Release interned objects on python exit, for memory debugging.
                                 Level indicates aggressiveness, default 0 releases nothing.
  -D, --no-docstrings            Strip docstrings from the compiled module.
  --fast-fail                    Abort the compilation on the first error
"""



b = \
"""
  --warning-error, -Werror       Make all warnings into errors
  --warning-extra, -Wextra       Enable extra warnings
  -X, --directive <name>=<value>[,<name=value,...] Overrides a compiler directive
"""

#parser.add_argument("--directive" or option.startswith('-X'):
#                if option.startswith('-X') and option[2:].strip():
#                    x_args = option[2:]
#                else:
#                    x_args = pop_arg()
#                try:
#                    options.compiler_directives = Options.parse_directive_list(
#                        x_args, relaxed_bool=True,
#                        current_settings=options.compiler_directives)
#                except ValueError, e:
#                    sys.stderr.write("Error in compiler directive: %s\n" % e.args[0])
#                    sys.exit(1)
#            elif option.startswith('--debug'):
#                option = option[2:].replace('-', '_')
#                import DebugFlags
#                if option in dir(DebugFlags):
#                    setattr(DebugFlags, option, True)
#                else:
#                    sys.stderr.write("Unknown debug flag: %s\n" % option)
#                    bad_usage()

#            elif option in ('-Werror', '--warning-errors'):
#                Options.warning_errors = True
#            elif option in ('-Wextra', '--warning-extra'):
#                options.compiler_directives.update(Options.extra_warnings)
#            elif option == "--disable-function-redefinition":
#                Options.disable_function_redefinition = True
#            elif option == "--old-style-globals":
#                Options.old_style_globals = True


# The following is broken http://trac.cython.org/cython_trac/ticket/379


#The following experimental options are supported only on MacOSX:
#  -C, --compile    Compile generated .c file to .o file
#  --link           Link .o file to produce extension module (implies -C)
#  Additional .o files to link may be supplied when using -X."""
