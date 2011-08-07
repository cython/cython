#
#   Copyright 2011 Stefano Sanfilippo
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

'''Cython - Command Line Parsing'''

from Cython import __version__ as version
import Options

menu = {
    'default' : {
        ('-V', '--version') : {
            'dest' : 'show_version', 'action' : 'version',
            'version' : 'Cython version %s' % version,
            'help' : 'Display version number of cython compiler'},
        ('sources') : {
            'nargs' : '*',
            'help' : 'Source file(s) to be compiled.' }},
    'environment setup': {
        ('-l', '--create-listing') : {
            'dest' : 'use_listing_file', 'const' : 1, 'action' : 'store_const',
            'help' : 'Write error messages to a listing file'},
        ('-I', '--include-dir') : {
            'dest' : 'include_path', 'action' : 'append', 'metavar' : '<directory>',
            'help' : '''Search for include files in named <directory>
                        (multiple include directories are allowed).'''},
        ('-o', '--output-file') : {
            'dest' : 'output_file', 'metavar' : '<output file>',
            'help' : 'Specify name of generated C file'},
        ('-w', '--working') : {
            'dest' : 'working_path', 'metavar' : '<directory>',
            'help' : '''Sets the working directory for Cython 
                        (the directory modules are searched from)'''}},
    'compilation' : {
        ('-t', '--timestamps') : {
            'dest' : 'timestamps', 'const' : 1, 'action' : 'store_const',
            'help' : 'Only compile newer source files (implied)'},
        ('-f', '--force') : {
            'dest' : 'timestamps', 'const' : 0, 'action' : 'store_const',
            'help' : 'Compile all source files (overrides -t)'},
        ('-z', '--pre-import') : {
            'dest' : 'pre_import', 'metavar' : '<module>',
            'help' : 'Import <module> before compilation.' },
        ('--fast-fail') : {
            'dest' : 'fast_fail', 'action' : 'store_true',
            'help' : 'Abort the compilation on the first error.' },
        ('-Werror', '--warning-errors'): {
            'dest' : 'warning_errors', 'action' : 'store_true',
            'help' : 'Make all warnings into errors.' },
        ('-Wextra', '--warning-extra'): {
            'dest' : 'compiler_directives', 'const' : Options.extra_warnings,
            'action' : 'append_const',
            'help' : 'Enable extra warnings' }},
    'debugging' : {
        ('--cleanup') : {
            'dest' : 'generate_cleanup_code', 'type' : int, 'metavar' : '<level>',
            'help' : '''Release interned objects on python exit, for memory debugging.
                        <level> indicates aggressiveness, default 0 releases nothing.'''},
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
            'dest' : 'verbose', 'action' : 'count',
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
            'dest' : 'embed', 'const' : 'main', 'nargs' : '?', 'metavar' : '<module>',
            'help' : 'Generate a main() function that embeds the Python interpreter.'},
        ('-+', '--cplus') : {
            'dest' : 'cplus', 'const' : 1, 'action' : 'store_const',
            'help' : 'Output a C++ rather than C file.' },
        ('-p', '--embed-positions') : {
            'dest' : 'embed_pos_in_docstring', 'const' : 1, 'action' : 'store_const',
            'help' : '''If specified, the positions in Cython files of each
                        function definition is embedded in its docstring.''' },
        ('--no-c-in-traceback') : {
            'dest' : 'c_line_in_traceback', 'action' : 'store_false',
            'help' : '' }, #FIXME
        ('--convert-range') : {
            'dest' : 'convert_range', 'action' : 'store_true',
            'help' : '''Convert `for x in range():` statements in pure C for(),
                      whenever possibile.''' },
        ('-D', '--no-docstrings') : {
            'dest' : 'docstrings', 'action' : 'store_false',
            'help' : 'Strip docstrings from the compiled module.' },
        ('--disable-function-redefinition') : {
            'dest' : 'disable_function_redefinition', 'action' : 'store_true',
            'help' : '' }, #FIXME
        ('--old-style-globals') : {
            'dest' : 'old_style_globals', 'action' : 'store_true',
            'help' : '' }}, #FIXME
    'Python compatibility options' : {
        ('-2') : {
            'dest' : 'language_level', 'const' : 2, 'action' : 'store_const',
            'help' : 'Compile based on Python-2 syntax and code semantics.'},
        ('-3') : {
            'dest' : 'language_level', 'const' : 3, 'action' : 'store_const',
            'help' : 'Compile based on Python-3 syntax and code semantics.'}},
#    'experimental options (MacOS X only)' : {
#        ('-C', '--compile') : {
#            'dest' : 'compile', 'action' : 'store_true',
#            'help' : 'Compile generated .c file to .o file' },
#        ('--link') : {
#            'dest' : 'link', 'action' : 'store_true',
#            'help' : '''Link .o file to produce extension module (implies -C)
#                        Additional .o files to link may be supplied when using -X.''' }}
}

epilog = '''\
Cython (http://cython.org) is a compiler for code written
in the Cython language. Cython is based on Pyrex by Greg Ewing.

WARNING: RECURSIVE COMPILATION IS STILL BROKEN
(see http://trac.cython.org/cython_trac/ticket/379).'''


from Cython.Compiler.Main import CompilationOptions, default_options
import argparse
import os

class BasicParser:
    def error(self, message):
        pass

    def refine(self, options):
        sources = options.sources
        del options.sources

        if options.gdb_debug:
            options.output_dir = os.curdir
        if not sources:
            self.error('no source file specified.')
        if options.output_file and len(sources) > 1:
            self.error('only one source file allowed when using -o')
        if not len(sources) == 0 and not options.show_version:
            self.error('malformed command line.')
        if options.embed and len(sources) > 1:
            self.error('only one source file allowed when using --embed')

        return options, sources


class Parser(BasicParser, argparse.ArgumentParser):
    def __init__(self):
        format = argparse.RawDescriptionHelpFormatter
        argparse.ArgumentParser.__init__(self, epilog=epilog, formatter_class=format)
        newgroup = lambda t: self.add_argument_group(title=t)
        for grouptitle, flaglist in menu.iteritems():
            group = self if grouptitle == 'default' else newgroup(grouptitle)
            for flag, parameters in flaglist.iteritems():
                try:
                    group.add_argument(flag, **parameters)
                except ValueError:
                    group.add_argument(*flag, **parameters)

    def parse(self, args):
        options = CompilationOptions(default_options)
        parser.parse_args(args, namespace=options)
        return self.refine(options)


parser = Parser()


def XXX_compatibility_assign_variables(options):
    for option in ['embed', 'embed_pos_in_docstring', 'pre_import',
                    'generate_cleanup_code', 'docstrings', 'annotate',
                    'convert_range', 'fast_fail', 'warning_errors',
                    'disable_function_redefinition', 'old_style_globals',
                    'warning_errors', 'disable_function_redefinition',
                    'old_style_globals']:
        setattr(Options, option, getattr(options, option, None))
        try:
            del options.__dict__[option]
        except KeyError:
            pass

def parse_command_line(args):
    options, sources = parser.parse(args)
    XXX_compatibility_assign_variables(options)
    return options, sources

import sys

if __name__ == '__main__':
    parse_command_line(sys.argv[1:])

# TODO
#"""
#  -X, --directive <name>=<value>[,<name=value,...] Overrides a compiler directive
#"""
#    class split(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string=None):
#           pass
#
#           if option == "--directive" or option.startswith('-X'):
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
