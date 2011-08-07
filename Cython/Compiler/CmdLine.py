#
#   Cython - Command Line Parsing
#

options = {
    'default' : {
        ('-V', '--version') : {
            'dest' : 'show_version', 'const' : 1, 'action' : 'store_const',
            'help' : 'Display version number of cython compiler'}},
    'environment setup': {
        ('-l', '--create-listing') : {
            'dest' : 'use_listing_file', 'const' : 1, 'action' : 'store_const',
            'help' : 'Write error messages to a listing file'},
        ('-I', '--include-dir') : {
            'dest' : 'include_path', 'action' : 'append',
            'help' : '''Search for include files in named directory
                        (multiple include directories are allowed).'''},
        ('-o', '--output-file') : {
            'dest' : 'output_file',
            'help' : 'Specify name of generated C file'},
        ('-w', '--working') : {
            'dest' : 'working_path',
            'help' : '''Sets the working directory for Cython 
                        (the directory modules are searched from)'''}},
    'compilation' : {
        ('-t', '--timestamps') : {
            'dest' : 'timestamps', 'const' : 1, 'action' : 'store_const',
            'help' : 'Only compile newer source files (implied)'},
        ('-f', '--force') : {
            'dest' : 'timestamps', 'const' : 0, 'action' : 'store_const',
            'help' : 'Compile all source files (overrides -t)'}},
    'debugging' : {
        ('--cleanup') : {
            'dest' : 'generate_cleanup_code', 'type' : int,
            'help' : '''Release interned objects on python exit, for memory debugging.
                        Level indicates aggressiveness, default 0 releases nothing.'''},
        ('--gdb') : {
            'dest' : 'gdb_debug', 'action' : 'store_true',
            'help' : 'Output debug information for cygdb'}},
    'recursive compilation': {
        ('-r', '--recursive') : {
            'dest' : 'recursive', 'const' : 1, 'action' : 'store_const',
            'help' : 'Recursively find and compile dependencies (implies -t)'},
        ('-q', '--quiet') : {
            'dest' : 'quiet', 'const' : 1, 'action' : 'store_const',
            'help' : "Don't print module names in recursive mode" },
        ('-v', '--verbose') : {
            'dest' : 'verbose', 'const' : 1, 'action' : 'append_const',
            'help' : 'Be verbose, print file names on multiple compilation' }},
    'code annotation' : {
        ('-a', '--annotate') : {
            'dest' : 'annotate', 'action' : 'store_true',
            'help' : 'Produce a colorized HTML version of the source.' },
        ('--line-directives') : {
            'dest' : 'emit_linenums', 'action' : 'store_true',
            'help' : 'Produce #line directives pointing to the .pyx source' }},
    'code generation' : {
        ('--embed') : {
            'dest' : 'embed', 'const' : 'main', 'nargs' : '?',
            'help' : 'Generate a main() function that embeds the Python interpreter.'},
        ('-+', '--cplus') : {
            'dest' : 'cplus', 'const' : 1, 'action' : 'store_const',
            'help' : 'Output a C++ rather than C file.' },
        ('--no-c-in-traceback') : {
            'dest' : 'c_line_in_traceback', 'action' : 'store_false',
            'help' : '' }, #FIXME add help
        ('-2') : {
            'dest' : 'language_level', 'const' : 2, 'action' : 'store_const',
            'help' : 'Compile based on Python-2 syntax and code semantics.'},
        ('-3') : {
            'dest' : 'language_level', 'const' : 3, 'action' : 'store_const',
            'help' : 'Compile based on Python-3 syntax and code semantics.'}}
}

epilog = '''Cython (http://cython.org) is a compiler for code written in the
    Cython language.  Cython is based on Pyrex by Greg Ewing.
    RECURSIVE COMPILATION IS STILL BROKEN.'''

class ArgsError(Exception):
    pass


import argparse

parser = argparse.ArgumentParser(epilog=epilog)

for grouptitle, flaglist in options.iteritems():
    group = parser.add_argument_group(title=grouptitle)
    for flag, parameters in flaglist.iteritems():
        print flag
        try:
            group.add_argument(flag, **parameters)
        except ValueError:
            group.add_argument(*flag, **parameters)

parser.add_argument('sources', help='Source file(s) to be compiled.', nargs='*')


from Cython.Compiler.Main import CompilationOptions, default_options
import Options

import os
import sys

def parse_command_line(args = sys.argv):
    options = CompilationOptions(default_options)
    parser.parse_args(args, namespace=options)
    sources = options.sources
    del options.sources # FIXME

#    options.verbose = len(options.verbose)
    if options.gdb_debug:
        options.output_dir = os.curdir

    if not sources:
        raise ArgsError('no source file specified.')

    if options.output_file and len(sources) > 1:
        raise ArgsError('only one source file allowed when using -o')

    if not len(options.sources) == 0 and not options.show_version:
        pass #FIXME

    if options.embed and len(sources) > 1:
        raise ArgsError('only one source file allowed when using -embed')

    #FIXME
    Options.embed = options.embed
    print vars(options)

    return options, sources


if __name__ == '__main__':
    parse_command_line(sys.argv[1:])











#-            elif option in ("-p", "--embed-positions"):
#-                Options.embed_pos_in_docstring = 1
#-            elif option in ("-z", "--pre-import"):
#-                Options.pre_import = pop_arg()
#-            elif option == "--cleanup":
#-                Options.generate_cleanup_code = int(pop_arg())
#-            elif option in ("-D", "--no-docstrings"):
#-                Options.docstrings = False
#-            elif option in ("-a", "--annotate"):
#-                Options.annotate = True
#-            elif option == "--convert-range":
#-                Options.convert_range = True
#-            elif option == "--fast-fail":
#-                Options.fast_fail = True
#-            elif option in ('-Werror', '--warning-errors'):
#-                Options.warning_errors = True
#-            elif option == "--disable-function-redefinition":
#-                Options.disable_function_redefinition = True
#-            elif option == "--old-style-globals":
#-                Options.old_style_globals = True

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
