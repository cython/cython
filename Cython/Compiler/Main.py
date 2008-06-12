#
#   Cython Top Level
#

import os, sys, re, codecs
if sys.version_info[:2] < (2, 3):
    sys.stderr.write("Sorry, Cython requires Python 2.3 or later\n")
    sys.exit(1)

try:
    set
except NameError:
    # Python 2.3
    from sets import Set as set

from time import time
import Code
import Errors
import Parsing
import Version
from Scanning import PyrexScanner, FileSourceDescriptor
from Errors import PyrexError, CompileError, error
from Symtab import BuiltinScope, ModuleScope
from Cython import Utils

module_name_pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")

# Note: PHASES and TransformSet should be removed soon; but that's for
# another day and another commit.
PHASES = [
    'before_analyse_function', # run in FuncDefNode.generate_function_definitions
    'after_analyse_function'   # run in FuncDefNode.generate_function_definitions
]

class TransformSet(dict):
    def __init__(self):
        for name in PHASES:
            self[name] = []
    def run(self, name, node, **options):
        assert name in self, "Transform phase %s not defined" % name
        for transform in self[name]:
            transform(node, phase=name, **options)

verbose = 0

class Context:
    #  This class encapsulates the context needed for compiling
    #  one or more Cython implementation files along with their
    #  associated and imported declaration files. It includes
    #  the root of the module import namespace and the list
    #  of directories to search for include files.
    #
    #  modules               {string : ModuleScope}
    #  include_directories   [string]
    #  future_directives     [object]
    
    def __init__(self, include_directories):
        #self.modules = {"__builtin__" : BuiltinScope()}
        import Builtin
        self.modules = {"__builtin__" : Builtin.builtin_scope}
        self.include_directories = include_directories
        self.future_directives = set()
        
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
            print("Context.find_module: module_name = %s, relative_to = %s, pos = %s, need_pxd = %s" % (
                    module_name, relative_to, pos, need_pxd))
        scope = None
        pxd_pathname = None
        if not module_name_pattern.match(module_name):
            raise CompileError((path, 0, 0),
                "'%s' is not a valid module name" % module_name)
        if "." not in module_name and relative_to:
            if debug_find_module:
                print("...trying relative import")
            scope = relative_to.lookup_submodule(module_name)
            if not scope:
                qualified_name = relative_to.qualify_name(module_name)
                pxd_pathname = self.find_pxd_file(qualified_name, pos)
                if pxd_pathname:
                    scope = relative_to.find_submodule(module_name)
        if not scope:
            if debug_find_module:
                print("...trying absolute import")
            scope = self
            for name in module_name.split("."):
                scope = scope.find_submodule(name)
        if debug_find_module:
            print("...scope =", scope)
        if not scope.pxd_file_loaded:
            if debug_find_module:
                print("...pxd not loaded")
            scope.pxd_file_loaded = 1
            if not pxd_pathname:
                if debug_find_module:
                    print("...looking for pxd file")
                pxd_pathname = self.find_pxd_file(module_name, pos)
                if debug_find_module:
                    print("......found ", pxd_pathname)
                if not pxd_pathname and need_pxd:
                    error(pos, "'%s.pxd' not found" % module_name)
            if pxd_pathname:
                try:
                    if debug_find_module:
                        print("Context.find_module: Parsing %s" % pxd_pathname)
                    source_desc = FileSourceDescriptor(pxd_pathname)
                    pxd_tree = self.parse(source_desc, scope, pxd = 1,
                                          full_module_name = module_name)
                    pxd_tree.analyse_declarations(scope)
                except CompileError:
                    pass
        return scope
    
    def find_pxd_file(self, qualified_name, pos):
        # Search include path for the .pxd file corresponding to the
        # given fully-qualified module name.
        return self.search_include_directories(qualified_name, ".pxd", pos)

    def find_pyx_file(self, qualified_name, pos):
        # Search include path for the .pyx file corresponding to the
        # given fully-qualified module name, as for find_pxd_file().
        return self.search_include_directories(qualified_name, ".pyx", pos)
    
    def find_include_file(self, filename, pos):
        # Search list of include directories for filename.
        # Reports an error and returns None if not found.
        path = self.search_include_directories(filename, "", pos,
                                               split_package=False)
        if not path:
            error(pos, "'%s' not found" % filename)
        return path
    
    def search_include_directories(self, qualified_name, suffix, pos,
                                   split_package=True):
        # Search the list of include directories for the given
        # file name. If a source file position is given, first
        # searches the directory containing that file. Returns
        # None if not found, but does not report an error.
        dirs = self.include_directories
        if pos:
            file_desc = pos[0]
            if not isinstance(file_desc, FileSourceDescriptor):
                raise RuntimeError("Only file sources for code supported")
            here_dir = os.path.dirname(file_desc.filename)
            dirs = [here_dir] + dirs

        dotted_filename = qualified_name + suffix
        if split_package:
            names = qualified_name.split('.')
            package_names = names[:-1]
            module_name = names[-1]
            module_filename = module_name + suffix
            package_filename = "__init__" + suffix

        for dir in dirs:
            path = os.path.join(dir, dotted_filename)
            if os.path.exists(path):
                return path
            if split_package:
                package_dir = self.check_package_dir(dir, package_names)
                if package_dir is not None:
                    path = os.path.join(package_dir, module_filename)
                    if os.path.exists(path):
                        return path
                    path = os.path.join(dir, package_dir, module_name,
                                        package_filename)
                    if os.path.exists(path):
                        return path
        return None

    def check_package_dir(self, dir, package_names):
        package_dir = os.path.join(dir, *package_names)
        if not os.path.exists(package_dir):
            return None
        for dirname in package_names:
            dir = os.path.join(dir, dirname)
            package_init = os.path.join(dir, "__init__.py")
            if not os.path.exists(package_init) and \
                    not os.path.exists(package_init + "x"): # same with .pyx ?
                return None
        return package_dir

    def c_file_out_of_date(self, source_path):
        c_path = Utils.replace_suffix(source_path, ".c")
        if not os.path.exists(c_path):
            return 1
        c_time = Utils.modification_time(c_path)
        if Utils.file_newer_than(source_path, c_time):
            return 1
        pos = [source_path]
        pxd_path = Utils.replace_suffix(source_path, ".pxd")
        if os.path.exists(pxd_path) and Utils.file_newer_than(pxd_path, c_time):
            return 1
        for kind, name in self.read_dependency_file(source_path):
            if kind == "cimport":
                dep_path = self.find_pxd_file(name, pos)
            elif kind == "include":
                dep_path = self.search_include_directories(name, pos)
            else:
                continue
            if dep_path and Utils.file_newer_than(dep_path, c_time):
                return 1
        return 0
    
    def find_cimported_module_names(self, source_path):
        return [ name for kind, name in self.read_dependency_file(source_path)
                 if kind == "cimport" ]

    def is_package_dir(self, dir_path):
        #  Return true if the given directory is a package directory.
        for filename in ("__init__.py", "__init__.pyx"):
            path = os.path.join(dir_path, filename)
            if os.path.exists(path):
                return 1

    def read_dependency_file(self, source_path):
        dep_path = Utils.replace_suffix(source_path, ".dep")
        if os.path.exists(dep_path):
            f = open(dep_path, "rU")
            chunks = [ line.strip().split(" ", 1)
                       for line in f.readlines()
                       if " " in line.strip() ]
            f.close()
            return chunks
        else:
            return ()

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

    def parse(self, source_desc, scope, pxd, full_module_name):
        if not isinstance(source_desc, FileSourceDescriptor):
            raise RuntimeError("Only file sources for code supported")
        source_filename = Utils.encode_filename(source_desc.filename)
        # Parse the given source file and return a parse tree.
        try:
            f = Utils.open_source_file(source_filename, "rU")
            try:
                s = PyrexScanner(f, source_desc, source_encoding = f.encoding,
                                 scope = scope, context = self)
                tree = Parsing.p_module(s, pxd, full_module_name)
            finally:
                f.close()
        except UnicodeDecodeError, msg:
            error((source_desc, 0, 0), "Decoding error, missing or incorrect coding=<encoding-name> at top of source (%s)" % msg)
        if Errors.num_errors > 0:
            raise CompileError
        return tree

    def extract_module_name(self, path, options):
        # Find fully_qualified module name from the full pathname
        # of a source file.
        dir, filename = os.path.split(path)
        module_name, _ = os.path.splitext(filename)
        if "." in module_name:
            return module_name
        if module_name == "__init__":
            dir, module_name = os.path.split(dir)
        names = [module_name]
        while self.is_package_dir(dir):
            parent, package_name = os.path.split(dir)
            if parent == dir:
                break
            names.append(package_name)
            dir = parent
        names.reverse()
        return ".".join(names)

    def compile(self, source, options = None, full_module_name = None):
        # Compile a Pyrex implementation file in this context
        # and return a CompilationResult.
        if not options:
            options = default_options
        result = CompilationResult()
        cwd = os.getcwd()

        source = os.path.join(cwd, source)
        result.main_source_file = source

        if options.use_listing_file:
            result.listing_file = Utils.replace_suffix(source, ".lis")
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
            result.c_file = Utils.replace_suffix(source, c_suffix)
        c_stat = None
        if result.c_file:
            try:
                c_stat = os.stat(result.c_file)
            except EnvironmentError:
                pass
        full_module_name = full_module_name or self.extract_module_name(source, options)
        source = FileSourceDescriptor(source)
        initial_pos = (source, 1, 0)
        scope = self.find_module(full_module_name, pos = initial_pos, need_pxd = 0)
        errors_occurred = False
        try:
            tree = self.parse(source, scope, pxd = 0,
                              full_module_name = full_module_name)
            tree.process_implementation(scope, options, result)
        except CompileError:
            errors_occurred = True
        Errors.close_listing_file()
        result.num_errors = Errors.num_errors
        if result.num_errors > 0:
            errors_occurred = True
        if errors_occurred and result.c_file:
            try:
                Utils.castrate_file(result.c_file, os.stat(source.filename))
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
#  Main Python entry points
#
#------------------------------------------------------------------------

class CompilationOptions:
    """
    Options to the Cython compiler:
    
    show_version      boolean   Display version number
    use_listing_file  boolean   Generate a .lis file
    errors_to_stderr  boolean   Echo errors to stderr when using .lis
    include_path      [string]  Directories to search for include files
    output_file       string    Name of generated .c file
    generate_pxi      boolean   Generate .pxi file for public declarations
    recursive         boolean   Recursively find and compile dependencies
    timestamps        boolean   Only compile changed source files. If None,
                                defaults to true when recursive is true.
    verbose           boolean   Always print source names being compiled
    quiet             boolean   Don't print source names in recursive mode
    transforms        Transform.TransformSet Transforms to use on the parse tree
    
    Following options are experimental and only used on MacOSX:
    
    c_only            boolean   Stop after generating C file (default)
    obj_only          boolean   Stop after compiling to .o file
    objects           [string]  Extra .o files to link with
    cplus             boolean   Compile as c++ code
    """
    
    def __init__(self, defaults = None, c_compile = 0, c_link = 0, **kw):
        self.include_path = []
        self.objects = []
        if defaults:
            if isinstance(defaults, CompilationOptions):
                defaults = defaults.__dict__
        else:
            defaults = default_options
        self.__dict__.update(defaults)
        self.__dict__.update(kw)
        if c_compile:
            self.c_only = 0
        if c_link:
            self.obj_only = 0


class CompilationResult:
    """
    Results from the Cython compiler:
    
    c_file           string or None   The generated C source file
    h_file           string or None   The generated C header file
    i_file           string or None   The generated .pxi file
    api_file         string or None   The generated C API .h file
    listing_file     string or None   File of error messages
    object_file      string or None   Result of compiling the C file
    extension_file   string or None   Result of linking the object file
    num_errors       integer          Number of compilation errors
    """
    
    def __init__(self):
        self.c_file = None
        self.h_file = None
        self.i_file = None
        self.api_file = None
        self.listing_file = None
        self.object_file = None
        self.extension_file = None
        self.main_source_file = None


class CompilationResultSet(dict):
    """
    Results from compiling multiple Pyrex source files. A mapping
    from source file paths to CompilationResult instances. Also
    has the following attributes:
    
    num_errors   integer   Total number of compilation errors
    """
    
    num_errors = 0

    def add(self, source, result):
        self[source] = result
        self.num_errors += result.num_errors


def compile_single(source, options, full_module_name = None):
    """
    compile_single(source, options, full_module_name)
    
    Compile the given Pyrex implementation file and return a CompilationResult.
    Always compiles a single file; does not perform timestamp checking or
    recursion.
    """
    context = Context(options.include_path)
    return context.compile(source, options, full_module_name)

def compile_multiple(sources, options):
    """
    compile_multiple(sources, options)
    
    Compiles the given sequence of Pyrex implementation files and returns
    a CompilationResultSet. Performs timestamp checking and/or recursion
    if these are specified in the options.
    """
    sources = [os.path.abspath(source) for source in sources]
    processed = set()
    results = CompilationResultSet()
    context = Context(options.include_path)
    recursive = options.recursive
    timestamps = options.timestamps
    if timestamps is None:
        timestamps = recursive
    verbose = options.verbose or ((recursive or timestamps) and not options.quiet)
    for source in sources:
        if source not in processed:
            if not timestamps or context.c_file_out_of_date(source):
                if verbose:
                    sys.stderr.write("Compiling %s\n" % source)
                result = context.compile(source, options)
                # Compiling multiple sources in one context doesn't quite
                # work properly yet.
                context = Context(options.include_path) # to be removed later
                results.add(source, result)
            processed.add(source)
            if recursive:
                for module_name in context.find_cimported_module_names(source):
                    path = context.find_pyx_file(module_name, [source])
                    if path:
                        sources.append(path)
                    else:
                        sys.stderr.write(
                            "Cannot find .pyx file for cimported module '%s'\n" % module_name)
    return results

def compile(source, options = None, c_compile = 0, c_link = 0,
            full_module_name = None, **kwds):
    """
    compile(source [, options], [, <option> = <value>]...)
    
    Compile one or more Pyrex implementation files, with optional timestamp
    checking and recursing on dependecies. The source argument may be a string
    or a sequence of strings If it is a string and no recursion or timestamp
    checking is requested, a CompilationResult is returned, otherwise a
    CompilationResultSet is returned.
    """
    options = CompilationOptions(defaults = options, c_compile = c_compile,
        c_link = c_link, **kwds)
    if isinstance(source, basestring) and not options.timestamps \
            and not options.recursive:
        return compile_single(source, options, full_module_name)
    else:
        return compile_multiple(source, options)

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
        options = CompilationOptions(default_options)
        sources = args
    if options.show_version:
        sys.stderr.write("Cython version %s\n" % Version.version)
    if options.working_path!="":
        os.chdir(options.working_path)
    try:
        result = compile(sources, options)
        if result.num_errors > 0:
            any_failures = 1
    except (EnvironmentError, PyrexError), e:
        sys.stderr.write(str(e) + '\n')
        any_failures = 1
    if any_failures:
        sys.exit(1)



#------------------------------------------------------------------------
#
#  Set the default options depending on the platform
#
#------------------------------------------------------------------------

default_options = dict(
    show_version = 0,
    use_listing_file = 0,
    errors_to_stderr = 1,
    c_only = 1,
    obj_only = 1,
    cplus = 0,
    output_file = None,
    annotate = False,
    generate_pxi = 0,
    transforms = TransformSet(),
    working_path = "",
    recursive = 0,
    timestamps = None,
    verbose = 0,
    quiet = 0)
if sys.platform == "mac":
    from Cython.Mac.MacSystem import c_compile, c_link, CCompilerError
    default_options['use_listing_file'] = 1
elif sys.platform == "darwin":
    from Cython.Mac.DarwinSystem import c_compile, c_link, CCompilerError
else:
    c_compile = None
    c_link = None


