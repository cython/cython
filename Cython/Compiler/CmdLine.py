#
#   Copyright 2011 Stefano Sanfilippo <satufk on GitHub>
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
            'nargs' : '+', 'metavar' : 'sourcefile.{py,pyx}',
            'help' : 'Source file(s) to be compiled.' }},
    'environment setup': {
        ('-l', '--create-listing') : {
            'dest' : 'use_listing_file', 'action' : 'store_true',
            'help' : 'Write error messages to a listing file'},
        ('-I', '--include-dir') : {
            'dest' : 'include_path', 'action' : 'append',
            'metavar' : '<directory>',
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
            'dest' : 'timestamps', 'action' : 'store_true',
            'help' : 'Only compile newer source files (implied)'},
        ('-f', '--force') : {
            'dest' : 'timestamps', 'action' : 'store_false',
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
            'default' : 0,
            'help' : '''Release interned objects on python exit, for memory debugging.
                        <level> indicates aggressiveness, default 0 releases nothing.'''},
        ('--gdb') : {
            'dest' : 'gdb_debug', 'action' : 'store_true',
            'help' : 'Output debug information for cygdb'}},
    'Python compatibility options' : {
        ('-2') : {
            'dest' : 'language_level', 'const' : 2, 'action' : 'store_const',
            'help' : 'Compile based on Python-2 syntax and code semantics.'},
        ('-3') : {
            'dest' : 'language_level', 'const' : 3, 'action' : 'store_const',
            'help' : 'Compile based on Python-3 syntax and code semantics.'}},
    'recursive compilation': {
        ('-r', '--recursive') : {
            'dest' : 'recursive', 'action' : 'store_true',
            'help' : 'Recursively find and compile dependencies (implies -t)'},
        ('-q', '--quiet') : {
            'dest' : 'quiet', 'action' : 'store_true',
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
            'dest' : 'embed', 'const' : 'main', 'nargs' : '?',
            'metavar' : '<function name>',
            'help' : 'Generate a main() function that embeds the Python interpreter.'},
        ('-+', '--cplus') : {
            'dest' : 'cplus', 'action' : 'store_true',
            'help' : 'Output a C++ rather than C file.' },
        ('-p', '--embed-positions') : {
            'dest' : 'embed_pos_in_docstring', 'action' : 'store_true',
            'help' : '''If specified, the positions in Cython files of each
                        function definition is embedded in its docstring.''' },
        ('--no-c-in-traceback') : {
            'dest' : 'c_line_in_traceback', 'action' : 'store_false',
            'help' : 'Omit C source code line when printing tracebacks.' },
        ('--convert-range') : {
            'dest' : 'convert_range', 'action' : 'store_true',
            'help' : '''Convert `for x in range():` statements in pure C for(),
                      whenever possibile.''' },
        ('-D', '--no-docstrings') : {
            'dest' : 'docstrings', 'action' : 'store_false',
            'help' : 'Strip docstrings from the compiled module.' },
        ('--disable-function-redefinition') : {
            'dest' : 'disable_function_redefinition', 'action' : 'store_true',
            'help' : 'For legacy code only, needed for some circular imports.' },
        ('--old-style-globals') : {
            'dest' : 'old_style_globals', 'action' : 'store_true',
            'help' : '''Makes globals() give the first non-Cython module
                        globals in the call stack. For SAGE compatibility''' }},
   'behavioural options' : {
       ('-X', '--directive') : {
           'dest' : 'compiler_directives', 'action' : 'append',
           'metavar' : '<name>=<value>[,<name>=<value>...]',
           'help' : 'Overrides a #pragma compiler directive'}},
       #('-d', '--debug') : {
            #'dest' : 'debug_flags', 'action' : 'append', 'metavar' : '<flag>',
            #'help' : "Sets Cython's internal debug options"}},
#    'experimental options' : { # MacOS X only
#        ('-C', '--compile') : {
#            'dest' : 'compile', 'action' : 'store_true',
#            'help' : 'Compile generated .c file to .o file' },
#        ('-l', '--link') : {
#            'dest' : 'link', 'action' : 'store_true',
#            'help' : '''Link .o file to produce extension module (implies -C)
#                        Additional .o files to link may be supplied when using -X.''' }},
}

epilog = '''\
Cython (http://cython.org) is a compiler for code written
in the Cython language. Cython is based on Pyrex by Greg Ewing.

WARNING: RECURSIVE COMPILATION IS STILL BROKEN
(see http://trac.cython.org/cython_trac/ticket/379).'''

def makedebuglist():
    import DebugFlags
    flags = {}
    for var in vars(DebugFlags):
        if var.startswith('debug'):
            name = '--' + var.replace('_', '-')
            flags.update({name : dict(dest=var, action='store_true')})
    return menu.update({'compiler debugging options' : flags})

class BasicParser:
    def refine(self, options):
        # Separate source files list from all other options
        sources = options.sources
        del options.sources

        # Basic sanity check
        if options.gdb_debug:
            import os
            options.output_dir = os.curdir
        if not options.include_path: #HACK for optparse compatibility
            options.include_path = []
        if not sources:
            self.error('no source file specified.')
        if options.output_file and len(sources) > 1:
            self.error('only one source file allowed when using -o')
        if getattr(options, 'embed', False) and len(sources) > 1: #HACK
            self.error('only one source file allowed when using --embed. Maybe you placed --embed after sources?')

        # Sets specified debug flags
        #if options.debug_flags:
            #for flag in options.debug_flags:
                #flag = 'debug_' + flag.replace('-', '_')
                #import DebugFlags
                #if flag in dir(DebugFlags):
                    #setattr(DebugFlags, flag, True)
                #else:
                    #parser.error('unknown debug flag: %s' % flag)

        # Parse compiler directives into a dictionary
        if options.compiler_directives:
            dirs = ','.join(options.compiler_directives)
            try:
                options.compiler_directives = Options.parse_directive_list(
                    dirs, relaxed_bool=True,
                    current_settings=Options.directive_defaults)
            except ValueError, e:
                parser.error('compiler directive: %s' % e.args[0])
        else:
            options.compiler_directives = {} #HACK

        # Sets gathered Option values XXX
        for flag in ['embed', 'embed_pos_in_docstring', 'pre_import',
                        'generate_cleanup_code', 'docstrings', 'annotate',
                        'convert_range', 'fast_fail', 'warning_errors',
                        'disable_function_redefinition', 'old_style_globals']:
            try:
                setattr(Options, flag, getattr(options, flag))
            except AttributeError:
                pass

        import DebugFlags
        for flag in vars(DebugFlags):
            try:
                setattr(DebugFlags, flag, getattr(options, flag))
            except AttributeError:
                pass

        return vars(options), sources

try:
    import argparse

    class Parser(BasicParser, argparse.ArgumentParser):
        def __init__(self):
            argparse.ArgumentParser.__init__(self, epilog=epilog,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                fromfile_prefix_chars='@')
            newgroup = lambda t: self.add_argument_group(title=t)
            for grouptitle, flaglist in menu.iteritems():
                group = self if grouptitle == 'default' else newgroup(grouptitle)
                for flag, parameters in flaglist.iteritems():
                    if isinstance(flag, str):
                        group.add_argument(flag, **parameters)
                    else:
                        group.add_argument(*flag, **parameters)

        def parse(self, args):
            results = self.parse_args(args)
            return self.refine(results)

except ImportError:
    import optparse

    class Parser(BasicParser, optparse.OptionParser):
        def __init__(self):
            optparse.OptionParser.__init__(self, epilog=epilog,
                version=menu['default'][('-V', '--version')]['version'],
                usage="%prog [options] sourcefile.{pyx,py} ...")
            newgroup = lambda t: optparse.OptionGroup(self, t)
            for grouptitle, flaglist in menu.iteritems():
                group = self if grouptitle == 'default' else newgroup(grouptitle)
                for flag, parameters in flaglist.iteritems():
                    try:
                        if '--embed' in flag:
                            del parameters['nargs'], parameters['const']
                            parameters['action'] = 'callback'
                            parameters['callback'] = self.__embed_callback
                        if isinstance(flag, str):
                            group.add_option(flag, **parameters)
                        else:
                            group.add_option(*flag, **parameters)
                    except optparse.OptionError:
                        pass

                if group is not self: self.add_option_group(group)

        def parse(self, args):
            results, others = self.parse_args(args)
            results.sources = others
            return self.refine(results)

        # super HACK to support implicit --embed arg 'main' value
        @staticmethod
        def __embed_callback(option, opt_str, value, parser):
            assert value is None
            # If next arg is not last and it is not an option,
            # or a source file had already been specified
            if (not parser.rargs[0].startswith('-') and len(parser.rargs) > 1):
                value = parser.rargs.pop(0)
            else:
                value = 'main'
            setattr(parser.values, option.dest, value)

makedebuglist()
parser = Parser()

def parse_command_line(args):
    #HACK: prevents first source file from being absorbed by --embed
    try:
        pos = args.index('--embed')
    except ValueError:
        pass
    else:
        for x in args[pos+1:]:
            if x.startswith('-'): break
        else:
            args.insert(pos + 1, '--')

    return parser.parse(args)
