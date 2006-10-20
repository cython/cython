#
#   Pyrex Top Level
#

import os, sys
if sys.version_info[:2] < (2, 2):
    print >>sys.stderr, "Sorry, Pyrex requires Python 2.2 or later"
    sys.exit(1)

import os
from time import time
import Version
from Scanning import PyrexScanner
import Errors
from Errors import PyrexError, CompileError, error
import Parsing
from Symtab import BuiltinScope, ModuleScope
import Code
from Pyrex.Utils import replace_suffix

verbose = 0

class Context:
    #  This class encapsulates the context needed for compiling
    #  one or more Pyrex implementation files along with their
    #  associated and imported declaration files. It includes
    #  the root of the module import namespace and the list
    #  of directories to search for include files.
    #
    #  modules               {string : ModuleScope}
    #  include_directories   [string]
    
    def __init__(self, include_directories):
        self.modules = {"__builtin__" : BuiltinScope()}
        self.include_directories = include_directories
        
    def find_module(self, module_name, 
            relative_to = None, pos = None, need_pxd = 1):
        # Finds and returns the module scope corresponding to
        # the given relative or absolute module name. If this
        # is the first time the module has been requested, finds
        # the corresponding .pxd file and process it.
        # If relative_to is not None, it must be a module scope,
        # and the module will first be searched for relative to
        # that module, provided its name is not a dotted name.
        debug_find_module = 0
        if debug_find_module:
            print "Context.find_module: module_name =", module_name, \
                "relative_to =", relative_to, "pos =", pos, "need_pxd =", need_pxd
        scope = None
        pxd_pathname = None
        if "." not in module_name and relative_to:
            if debug_find_module:
                print "...trying relative import"
            scope = relative_to.lookup_submodule(module_name)
            if not scope:
                qualified_name = relative_to.qualify_name(module_name)
                pxd_pathname = self.find_pxd_file(qualified_name, pos)
                if pxd_pathname:
                    scope = relative_to.find_submodule(module_name)
        if not scope:
            if debug_find_module:
                print "...trying absolute import"
            scope = self
            for name in module_name.split("."):
                scope = scope.find_submodule(name)
        if debug_find_module:
            print "...scope =", scope
        if not scope.pxd_file_loaded:
            if debug_find_module:
                print "...pxd not loaded"
            scope.pxd_file_loaded = 1
            if not pxd_pathname:
                if debug_find_module:
                    print "...looking for pxd file"
                pxd_pathname = self.find_pxd_file(module_name, pos)
                if debug_find_module:
                    print "......found ", pxd_pathname
                if not pxd_pathname and need_pxd:
                    error(pos, "'%s.pxd' not found" % module_name)
            if pxd_pathname:
                try:
                    if debug_find_module:
                        print "Context.find_module: Parsing", pxd_pathname
                    pxd_tree = self.parse(pxd_pathname, scope.type_names, pxd = 1)
                    pxd_tree.analyse_declarations(scope)
                except CompileError:
                    pass
        return scope
    
    def find_pxd_file(self, module_name, pos):
        # Search include directories for the .pxd file
        # corresponding to the given (full) module name.
        pxd_filename = "%s.pxd" % module_name
        return self.search_include_directories(pxd_filename, pos)
    
    def find_include_file(self, filename, pos):
        # Search list of include directories for filename.
        # Reports an error and returns None if not found.
        path = self.search_include_directories(filename, pos)
        if not path:
            error(pos, "'%s' not found" % filename)
        return path
    
    def search_include_directories(self, filename, pos):
        # Search the list of include directories for the given
        # file name. If a source file position is given, first
        # searches the directory containing that file. Returns
        # None if not found, but does not report an error.
        dirs = self.include_directories
        if pos:
            here_dir = os.path.dirname(pos[0])
            dirs = [here_dir] + dirs
        for dir in dirs:
            path = os.path.join(dir, filename)
            if os.path.exists(path):
                return path
        return None

    def lookup_submodule(self, name):
        # Look up a top-level module. Returns None if not found.
        return self.modules.get(name, None)

    def find_submodule(self, name):
        # Find a top-level module, creating a new one if needed.
        scope = self.lookup_submodule(name)
        if not scope:
            scope = ModuleScope(name, 
                parent_module = None, context = self)
            self.modules[name] = scope
        return scope

    def parse(self, source_filename, type_names, pxd):
        # Parse the given source file and return a parse tree.
        f = open(source_filename, "rU")
        s = PyrexScanner(f, source_filename, 
            type_names = type_names, context = self)
        try:
            tree = Parsing.p_module(s, pxd)
        finally:
            f.close()
        if Errors.num_errors > 0:
            raise CompileError
        return tree

    def extract_module_name(self, path):
        # Get the module name out of a source file pathname.
        _, tail = os.path.split(path)
        name, _ = os.path.splitext(tail)
        return name

    def compile(self, source, options = None):
        # Compile a Pyrex implementation file in this context
        # and return a CompilationResult.
        if not options:
            options = default_options
        result = CompilationResult()
        cwd = os.getcwd()
        source = os.path.join(cwd, source)
        if options.use_listing_file:
            result.listing_file = replace_suffix(source, ".lis")
            Errors.open_listing_file(result.listing_file,
                echo_to_stderr = options.errors_to_stderr)
        else:
            Errors.open_listing_file(None)
        if options.output_file:
            result.c_file = os.path.join(cwd, options.output_file)
        else:
            if options.cplus:
                c_suffix = ".cpp"
            else:
                c_suffix = ".c"
            result.c_file = replace_suffix(source, c_suffix)
        module_name = self.extract_module_name(source)
        initial_pos = (source, 1, 0)
        scope = self.find_module(module_name, pos = initial_pos, need_pxd = 0)
        errors_occurred = False
        try:
            tree = self.parse(source, scope.type_names, pxd = 0)
            tree.process_implementation(scope, result)
        except CompileError:
            errors_occurred = True
        Errors.close_listing_file()
        result.num_errors = Errors.num_errors
        if result.num_errors > 0:
            errors_occurred = True
        if errors_occurred:
            try:
                os.unlink(result.c_file)
            except EnvironmentError:
                pass
            result.c_file = None
        if result.c_file and not options.c_only and c_compile:
            result.object_file = c_compile(result.c_file,
                verbose_flag = options.show_version,
                cplus = options.cplus)
            if not options.obj_only and c_link:
                result.extension_file = c_link(result.object_file,
                    extra_objects = options.objects,
                    verbose_flag = options.show_version,
                    cplus = options.cplus)
        return result

#------------------------------------------------------------------------
#
#  Main Python entry point
#
#------------------------------------------------------------------------

class CompilationOptions:
    """
    Options to the Pyrex compiler:
    
    show_version      boolean   Display version number
    use_listing_file  boolean   Generate a .lis file
    errors_to_stderr  boolean   Echo errors to stderr when using .lis
    include_path      [string]  Directories to search for include files
    output_file       string    Name of generated .c file
    
    Following options are experimental and only used on MacOSX:
    
    c_only            boolean   Stop after generating C file (default)
    obj_only          boolean   Stop after compiling to .o file
    objects           [string]  Extra .o files to link with
    cplus             boolean   Compile as c++ code
    """
    
    def __init__(self, defaults = None, **kw):
        self.include_path = []
        self.objects = []
        if defaults:
            self.__dict__.update(defaults.__dict__)
        self.__dict__.update(kw)


class CompilationResult:
    """
    Results from the Pyrex compiler:
    
    c_file           string or None   The generated C source file
    h_file           string or None   The generated C header file
    i_file           string or None   The generated .pxi file
    listing_file     string or None   File of error messages
    object_file      string or None   Result of compiling the C file
    extension_file   string or None   Result of linking the object file
    num_errors       integer          Number of compilation errors
    """
    
    def __init__(self):
        self.c_file = None
        self.h_file = None
        self.i_file = None
        self.listing_file = None
        self.object_file = None
        self.extension_file = None


def compile(source, options = None, c_compile = 0, c_link = 0):
    """
    compile(source, options = default_options)
    
    Compile the given Pyrex implementation file and return
    a CompilationResult object describing what was produced.
    """
    if not options:
        options = default_options
    options = CompilationOptions(defaults = options)
    if c_compile:
        options.c_only = 0
    if c_link:
        options.obj_only = 0
    context = Context(options.include_path)
    return context.compile(source, options)

#------------------------------------------------------------------------
#
#  Main command-line entry point
#
#------------------------------------------------------------------------

def main(command_line = 0):
    args = sys.argv[1:]
    any_failures = 0
    if command_line:
        from CmdLine import parse_command_line
        options, sources = parse_command_line(args)
    else:
        options = default_options
        sources = args
    if options.show_version:
        print >>sys.stderr, "Pyrex version %s" % Version.version
    context = Context(options.include_path)
    for source in sources:
        try:
            result = context.compile(source, options)
            if result.num_errors > 0:
                any_failures = 1
        except PyrexError, e:
            print >>sys.stderr, e
            any_failures = 1
    if any_failures:
        sys.exit(1)

#------------------------------------------------------------------------
#
#  Set the default options depending on the platform
#
#------------------------------------------------------------------------

default_options = CompilationOptions(
    show_version = 0,
    use_listing_file = 0,
    errors_to_stderr = 1,
    c_only = 1,
    obj_only = 1,
    cplus = 0,
    output_file = None)
    
if sys.platform == "mac":
    from Pyrex.Mac.MacSystem import c_compile, c_link, CCompilerError
    default_options.use_listing_file = 1
elif sys.platform == "darwin":
    from Pyrex.Mac.DarwinSystem import c_compile, c_link, CCompilerError
else:
    c_compile = None
    c_link = None


