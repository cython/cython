#
#   Cython - Command Line Parsing
#

import sys
import Options

usage = """\
Cython (http://cython.org) is a compiler for code written in the
Cython language.  Cython is based on Pyrex by Greg Ewing.

Usage: cython [options] sourcefile.pyx ...

Options:
  -v, --version                  Display version number of cython compiler
  -l, --create-listing           Write error messages to a listing file
  -I, --include-dir <directory>  Search for include files in named directory
                                 (multiply include directories are allowed).
  -o, --output-file <filename>   Specify name of generated C file
  -p, --embed-positions          If specified, the positions in Cython files of each
                                 function definition is embedded in its docstring.
  -z, --pre-import <module>      If specified, assume undeclared names in this 
                                 module. Emulates the behavior of putting 
                                 "from <module> import *" at the top of the file. 
  --incref-local-binop           Force local an extra incref on local variables before
                                 performing any binary operations.
  -D, --no-docstrings            Remove docstrings.
  -a, --annotate                 Produce an colorized version of the source.
"""  
#The following experimental options are supported only on MacOSX:
#  -C, --compile    Compile generated .c file to .o file
#  -X, --link       Link .o file to produce extension module (implies -C)
#  -+, --cplus      Use C++ compiler for compiling and linking
#  Additional .o files to link may be supplied when using -X."""

def bad_usage():
    print >>sys.stderr, usage
    sys.exit(1)

def parse_command_line(args):
    from Cython.Compiler.Main import \
        CompilationOptions, default_options

    def pop_arg():
        if args:
            return args.pop(0)
        else:
            bad_usage()
    
    def get_param(option):
        tail = option[2:]
        if tail:
            return tail
        else:
            return pop_arg()

    options = CompilationOptions(default_options)
    sources = []
    while args:
        if args[0].startswith("-"):
            option = pop_arg()
            if option in ("-v", "--version"):
                options.show_version = 1
            elif option in ("-l", "--create-listing"):
                options.use_listing_file = 1
            elif option in ("-C", "--compile"):
                options.c_only = 0
            elif option in ("-X", "--link"):
                options.c_only = 0
                options.obj_only = 0
            elif option in ("-+", "--cplus"):
                options.cplus = 1
            elif option.startswith("-I"):
                options.include_path.append(get_param(option))
            elif option == "--include-dir":
                options.include_path.append(pop_arg())
            elif option in ("-o", "--output-file"):
                options.output_file = pop_arg()
            elif option in ("-p", "--embed-positions"):
                Options.embed_pos_in_docstring = 1
            elif option in ("-z", "--pre-import"):
                Options.pre_import = pop_arg()
            elif option == "--incref-local-binop":
                Options.incref_local_binop = 1
            elif option == "--cleanup":
                Options.generate_cleanup_code = int(pop_arg())
            elif option in ("-D", "--no-docstrings"):
                Options.docstrings = False
            elif option in ("-a", "--annotate"):
                Options.annotate = True
            else:
                bad_usage()
        else:
            arg = pop_arg()
            if arg.endswith(".pyx"):
                sources.append(arg)
            elif arg.endswith(".o"):
                options.objects.append(arg)
            else:
                print >>sys.stderr, \
                    "cython: %s: Unknown filename suffix" % arg
    if options.objects and len(sources) > 1:
        print >>sys.stderr, \
            "cython: Only one source file allowed together with .o files"
    if options.use_listing_file and len(sources) > 1:
        print >>sys.stderr, \
            "cython: Only one source file allowed when using -o"
        sys.exit(1)
    if len(sources) == 0:
        bad_usage()
    return options, sources

