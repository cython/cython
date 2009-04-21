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
  -V, --version                  Display version number of cython compiler
  -l, --create-listing           Write error messages to a listing file
  -I, --include-dir <directory>  Search for include files in named directory
                                 (multiply include directories are allowed).
  -o, --output-file <filename>   Specify name of generated C file
  -r, --recursive                Recursively find and compile dependencies
  -t, --timestamps               Only compile newer source files (implied with -r)
  -f, --force                    Compile all source files (overrides implied -t)
  -q, --quiet                    Don't print module names in recursive mode
  -v, --verbose                  Be verbose, print file names on multiple compilation
  -p, --embed-positions          If specified, the positions in Cython files of each
                                 function definition is embedded in its docstring.
  -z, --pre-import <module>      If specified, assume undeclared names in this 
                                 module. Emulates the behavior of putting 
                                 "from <module> import *" at the top of the file. 
  --incref-local-binop           Force local an extra incref on local variables before
                                 performing any binary operations.
  --cleanup <level>              Release interned objects on python exit, for memory debugging. 
                                 Level indicates aggressiveness, default 0 releases nothing. 
  -w, --working <directory>      Sets the working directory for Cython (the directory modules 
                                 are searched from)

  -D, --no-docstrings            Remove docstrings.
  -a, --annotate                 Produce a colorized HTML version of the source.
  --line-directives              Produce #line directives pointing to the .pyx source
  --cplus                        Output a c++ rather than c file.
  --embed                        Embed the Python interpreter in a main() method.
  --directive <name>=<value>[,<name=value,...] Overrides a compiler directive
"""

#The following experimental options are supported only on MacOSX:
#  -C, --compile    Compile generated .c file to .o file
#  -X, --link       Link .o file to produce extension module (implies -C)
#  -+, --cplus      Use C++ compiler for compiling and linking
#  Additional .o files to link may be supplied when using -X."""

def bad_usage():
    sys.stderr.write(usage)
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
        print args
        if args[0].startswith("-"):
            option = pop_arg()
            if option in ("-V", "--version"):
                options.show_version = 1
            elif option in ("-l", "--create-listing"):
                options.use_listing_file = 1
            elif option in ("-C", "--compile"):
                options.c_only = 0
            elif option in ("-X", "--link"):
                if option == "-X":
                    print >>sys.stderr, "Deprecation warning: The -X command line switch will be changed to a"
                    print >>sys.stderr, "shorthand for --directive in Cython 0.12. Please use --link instead."
                    print >>sys.stderr
                options.c_only = 0
                options.obj_only = 0
            elif option in ("-+", "--cplus"):
                options.cplus = 1
            elif option == "--embed":
                Options.embed = True
            elif option.startswith("-I"):
                options.include_path.append(get_param(option))
            elif option == "--include-dir":
                options.include_path.append(pop_arg())
            elif option in ("-w", "--working"):
                options.working_path = pop_arg()
            elif option in ("-o", "--output-file"):
                options.output_file = pop_arg()
            elif option in ("-r", "--recursive"):
                options.recursive = 1
            elif option in ("-t", "--timestamps"):
                options.timestamps = 1
            elif option in ("-f", "--force"):
                options.timestamps = 0
            elif option in ("-v", "--verbose"):
                options.verbose += 1
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
            elif option == "--convert-range":
                Options.convert_range = True
            elif option == "--line-directives":
                options.emit_linenums = True
            elif option in ("-X", "--directive"):
                try:
                    options.pragma_overrides = Options.parse_option_list(pop_arg())
                except ValueError, e:
                    sys.stderr.write("Error in compiler directive: %s\n" % e.message)
                    sys.exit(1)
            else:
                bad_usage()
        else:
            arg = pop_arg()
            if arg.endswith(".pyx"):
                sources.append(arg)
            elif arg.endswith(".py"):
                # maybe do some other stuff, but this should work for now
                sources.append(arg)
            elif arg.endswith(".o"):
                options.objects.append(arg)
            else:
                sys.stderr.write(
                    "cython: %s: Unknown filename suffix\n" % arg)
    if options.objects and len(sources) > 1:
        sys.stderr.write(
            "cython: Only one source file allowed together with .o files\n")
    if options.use_listing_file and len(sources) > 1:
        sys.stderr.write(
            "cython: Only one source file allowed when using -o\n")
        sys.exit(1)
    if len(sources) == 0 and not options.show_version:
        bad_usage()
    return options, sources

