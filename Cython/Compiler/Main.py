#
#   Cython Top Level
#

import os, sys, re
if sys.version_info[:2] < (2, 3):
    sys.stderr.write("Sorry, Cython requires Python 2.3 or later\n")
    sys.exit(1)

try:
    set
except NameError:
    # Python 2.3
    from sets import Set as set

import itertools
from time import time

import Code
import Errors
# Do not import Parsing here, import it when needed, because Parsing imports
# Nodes, which globally needs debug command line options initialized to set a
# conditional metaclass. These options are processed by CmdLine called from
# main() in this file.
# import Parsing
import Version
from Scanning import PyrexScanner, FileSourceDescriptor
from Errors import PyrexError, CompileError, InternalError, AbortError, error, warning
from Symtab import BuiltinScope, ModuleScope
from Cython import Utils
from Cython.Utils import open_new_file, replace_suffix
import CythonScope
import DebugFlags

module_name_pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")

verbose = 0

def dumptree(t):
    # For quick debugging in pipelines
    print t.dump()
    return t

def abort_on_errors(node):
    # Stop the pipeline if there are any errors.
    if Errors.num_errors != 0:
        raise AbortError, "pipeline break"
    return node

class CompilationData(object):
    #  Bundles the information that is passed from transform to transform.
    #  (For now, this is only)

    #  While Context contains every pxd ever loaded, path information etc.,
    #  this only contains the data related to a single compilation pass
    #
    #  pyx                   ModuleNode              Main code tree of this compilation.
    #  pxds                  {string : ModuleNode}   Trees for the pxds used in the pyx.
    #  codewriter            CCodeWriter             Where to output final code.
    #  options               CompilationOptions
    #  result                CompilationResult
    pass

class Context(object):
    #  This class encapsulates the context needed for compiling
    #  one or more Cython implementation files along with their
    #  associated and imported declaration files. It includes
    #  the root of the module import namespace and the list
    #  of directories to search for include files.
    #
    #  modules               {string : ModuleScope}
    #  include_directories   [string]
    #  future_directives     [object]
    #  language_level        int     currently 2 or 3 for Python 2/3

    def __init__(self, include_directories, compiler_directives, cpp=False, language_level=2):
        import Builtin, CythonScope
        self.modules = {"__builtin__" : Builtin.builtin_scope}
        self.modules["cython"] = CythonScope.create_cython_scope(self)
        self.include_directories = include_directories
        self.future_directives = set()
        self.compiler_directives = compiler_directives
        self.cpp = cpp

        self.pxds = {} # full name -> node tree

        standard_include_path = os.path.abspath(os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.path.pardir, 'Includes')))
        self.include_directories = include_directories + [standard_include_path]

        self.set_language_level(language_level)

        self.gdb_debug_outputwriter = None

    def set_language_level(self, level):
        self.language_level = level
        if level >= 3:
            from Future import print_function, unicode_literals
            self.future_directives.add(print_function)
            self.future_directives.add(unicode_literals)
            self.modules['builtins'] = self.modules['__builtin__']

    def create_pipeline(self, pxd, py=False):
        from Visitor import PrintTree
        from ParseTreeTransforms import WithTransform, NormalizeTree, PostParse, PxdPostParse
        from ParseTreeTransforms import AnalyseDeclarationsTransform, AnalyseExpressionsTransform
        from ParseTreeTransforms import CreateClosureClasses, MarkClosureVisitor, DecoratorTransform
        from ParseTreeTransforms import InterpretCompilerDirectives, TransformBuiltinMethods
        from ParseTreeTransforms import ExpandInplaceOperators
        from TypeInference import MarkAssignments, MarkOverflowingArithmetic
        from ParseTreeTransforms import AlignFunctionDefinitions, GilCheck
        from AnalysedTreeTransforms import AutoTestDictTransform
        from AutoDocTransforms import EmbedSignature
        from Optimize import FlattenInListTransform, SwitchTransform, IterationTransform
        from Optimize import EarlyReplaceBuiltinCalls, OptimizeBuiltinCalls
        from Optimize import ConstantFolding, FinalOptimizePhase
        from Optimize import DropRefcountingTransform
        from Buffer import IntroduceBufferAuxiliaryVars
        from ModuleNode import check_c_declarations, check_c_declarations_pxd

        if pxd:
            _check_c_declarations = check_c_declarations_pxd
            _specific_post_parse = PxdPostParse(self)
        else:
            _check_c_declarations = check_c_declarations
            _specific_post_parse = None

        if py and not pxd:
            _align_function_definitions = AlignFunctionDefinitions(self)
        else:
            _align_function_definitions = None

        return [
            NormalizeTree(self),
            PostParse(self),
            _specific_post_parse,
            InterpretCompilerDirectives(self, self.compiler_directives),
            _align_function_definitions,
            MarkClosureVisitor(self),
            ConstantFolding(),
            FlattenInListTransform(),
            WithTransform(self),
            DecoratorTransform(self),
            AnalyseDeclarationsTransform(self),
            AutoTestDictTransform(self),
            EmbedSignature(self),
            EarlyReplaceBuiltinCalls(self),  ## Necessary?
            MarkAssignments(self),
            MarkOverflowingArithmetic(self),
            TransformBuiltinMethods(self),  ## Necessary?
            IntroduceBufferAuxiliaryVars(self),
            _check_c_declarations,
            AnalyseExpressionsTransform(self),
            CreateClosureClasses(self),  ## After all lookups and type inference
            ExpandInplaceOperators(self),
            OptimizeBuiltinCalls(self),  ## Necessary?
            IterationTransform(),
            SwitchTransform(),
            DropRefcountingTransform(),
            FinalOptimizePhase(self),
            GilCheck(),
            ]

    def create_pyx_pipeline(self, options, result, py=False):
        def generate_pyx_code(module_node):
            module_node.process_implementation(options, result)
            result.compilation_source = module_node.compilation_source
            return result

        def inject_pxd_code(module_node):
            from textwrap import dedent
            stats = module_node.body.stats
            for name, (statlistnode, scope) in self.pxds.iteritems():
                # Copy over function nodes to the module
                # (this seems strange -- I believe the right concept is to split
                # ModuleNode into a ModuleNode and a CodeGenerator, and tell that
                # CodeGenerator to generate code both from the pyx and pxd ModuleNodes.
                 stats.append(statlistnode)
                 # Until utility code is moved to code generation phase everywhere,
                 # we need to copy it over to the main scope
                 module_node.scope.utility_code_list.extend(scope.utility_code_list)
            return module_node

        test_support = []
        if options.evaluate_tree_assertions:
            from Cython.TestUtils import TreeAssertVisitor
            test_support.append(TreeAssertVisitor())

        if options.gdb_debug:
            from Cython.Debugger import DebugWriter
            from ParseTreeTransforms import DebugTransform
            self.gdb_debug_outputwriter = DebugWriter.CythonDebugWriter(
                options.output_dir)
            debug_transform = [DebugTransform(self, options, result)]
        else:
            debug_transform = []

        return list(itertools.chain(
            [create_parse(self)],
            self.create_pipeline(pxd=False, py=py),
            test_support,
            [inject_pxd_code, abort_on_errors],
            debug_transform,
            [generate_pyx_code]))

    def create_pxd_pipeline(self, scope, module_name):
        def parse_pxd(source_desc):
            tree = self.parse(source_desc, scope, pxd=True,
                              full_module_name=module_name)
            tree.scope = scope
            tree.is_pxd = True
            return tree

        from CodeGeneration import ExtractPxdCode

        # The pxd pipeline ends up with a CCodeWriter containing the
        # code of the pxd, as well as a pxd scope.
        return [parse_pxd] + self.create_pipeline(pxd=True) + [
            ExtractPxdCode(self),
            ]

    def create_py_pipeline(self, options, result):
        return self.create_pyx_pipeline(options, result, py=True)


    def process_pxd(self, source_desc, scope, module_name):
        pipeline = self.create_pxd_pipeline(scope, module_name)
        result = self.run_pipeline(pipeline, source_desc)
        return result

    def nonfatal_error(self, exc):
        return Errors.report_error(exc)

    def run_pipeline(self, pipeline, source):
        error = None
        data = source
        try:
            try:
                for phase in pipeline:
                    if phase is not None:
                        if DebugFlags.debug_verbose_pipeline:
                            t = time()
                            print "Entering pipeline phase %r" % phase
                        data = phase(data)
                        if DebugFlags.debug_verbose_pipeline:
                            print "    %.3f seconds" % (time() - t)
            except CompileError, err:
                # err is set
                Errors.report_error(err)
                error = err
        except InternalError, err:
            # Only raise if there was not an earlier error
            if Errors.num_errors == 0:
                raise
            error = err
        except AbortError, err:
            error = err
        return (error, data)

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
            if pos is None:
                pos = (module_name, 0, 0)
            raise CompileError(pos,
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
                    package_pathname = self.search_include_directories(module_name, ".py", pos)
                    if package_pathname and package_pathname.endswith('__init__.py'):
                        pass
                    else:
                        error(pos, "'%s.pxd' not found" % module_name)
            if pxd_pathname:
                try:
                    if debug_find_module:
                        print("Context.find_module: Parsing %s" % pxd_pathname)
                    rel_path = module_name.replace('.', os.sep) + os.path.splitext(pxd_pathname)[1]
                    if not pxd_pathname.endswith(rel_path):
                        rel_path = pxd_pathname # safety measure to prevent printing incorrect paths
                    source_desc = FileSourceDescriptor(pxd_pathname, rel_path)
                    err, result = self.process_pxd(source_desc, scope, module_name)
                    if err:
                        raise err
                    (pxd_codenodes, pxd_scope) = result
                    self.pxds[module_name] = (pxd_codenodes, pxd_scope)
                except CompileError:
                    pass
        return scope

    def find_pxd_file(self, qualified_name, pos):
        # Search include path for the .pxd file corresponding to the
        # given fully-qualified module name.
        # Will find either a dotted filename or a file in a
        # package directory. If a source file position is given,
        # the directory containing the source file is searched first
        # for a dotted filename, and its containing package root
        # directory is searched first for a non-dotted filename.
        pxd = self.search_include_directories(qualified_name, ".pxd", pos)
        if pxd is None: # XXX Keep this until Includes/Deprecated is removed
            if (qualified_name.startswith('python') or
                qualified_name in ('stdlib', 'stdio', 'stl')):
                standard_include_path = os.path.abspath(os.path.normpath(
                        os.path.join(os.path.dirname(__file__), os.path.pardir, 'Includes')))
                deprecated_include_path = os.path.join(standard_include_path, 'Deprecated')
                self.include_directories.append(deprecated_include_path)
                try:
                    pxd = self.search_include_directories(qualified_name, ".pxd", pos)
                finally:
                    self.include_directories.pop()
                if pxd:
                    name = qualified_name
                    if name.startswith('python'):
                        warning(pos, "'%s' is deprecated, use 'cpython'" % name, 1)
                    elif name in ('stdlib', 'stdio'):
                        warning(pos, "'%s' is deprecated, use 'libc.%s'" % (name, name), 1)
                    elif name in ('stl'):
                        warning(pos, "'%s' is deprecated, use 'libcpp.*.*'" % name, 1)
        return pxd

    def find_pyx_file(self, qualified_name, pos):
        # Search include path for the .pyx file corresponding to the
        # given fully-qualified module name, as for find_pxd_file().
        return self.search_include_directories(qualified_name, ".pyx", pos)

    def find_include_file(self, filename, pos):
        # Search list of include directories for filename.
        # Reports an error and returns None if not found.
        path = self.search_include_directories(filename, "", pos,
                                               include=True)
        if not path:
            error(pos, "'%s' not found" % filename)
        return path

    def search_include_directories(self, qualified_name, suffix, pos,
                                   include=False):
        # Search the list of include directories for the given
        # file name. If a source file position is given, first
        # searches the directory containing that file. Returns
        # None if not found, but does not report an error.
        # The 'include' option will disable package dereferencing.
        dirs = self.include_directories
        if pos:
            file_desc = pos[0]
            if not isinstance(file_desc, FileSourceDescriptor):
                raise RuntimeError("Only file sources for code supported")
            if include:
                dirs = [os.path.dirname(file_desc.filename)] + dirs
            else:
                dirs = [self.find_root_package_dir(file_desc.filename)] + dirs

        dotted_filename = qualified_name
        if suffix:
            dotted_filename += suffix
        if not include:
            names = qualified_name.split('.')
            package_names = names[:-1]
            module_name = names[-1]
            module_filename = module_name + suffix
            package_filename = "__init__" + suffix

        for dir in dirs:
            path = os.path.join(dir, dotted_filename)
            if Utils.path_exists(path):
                return path
            if not include:
                package_dir = self.check_package_dir(dir, package_names)
                if package_dir is not None:
                    path = os.path.join(package_dir, module_filename)
                    if Utils.path_exists(path):
                        return path
                    path = os.path.join(dir, package_dir, module_name,
                                        package_filename)
                    if Utils.path_exists(path):
                        return path
        return None

    def find_root_package_dir(self, file_path):
        dir = os.path.dirname(file_path)
        while self.is_package_dir(dir):
            parent = os.path.dirname(dir)
            if parent == dir:
                break
            dir = parent
        return dir

    def check_package_dir(self, dir, package_names):
        for dirname in package_names:
            dir = os.path.join(dir, dirname)
            if not self.is_package_dir(dir):
                return None
        return dir

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
        for filename in ("__init__.py",
                         "__init__.pyx",
                         "__init__.pxd"):
            path = os.path.join(dir_path, filename)
            if Utils.path_exists(path):
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
        source_filename = source_desc.filename
        scope.cpp = self.cpp
        # Parse the given source file and return a parse tree.
        try:
            f = Utils.open_source_file(source_filename, "rU")
            try:
                import Parsing
                s = PyrexScanner(f, source_desc, source_encoding = f.encoding,
                                 scope = scope, context = self)
                tree = Parsing.p_module(s, pxd, full_module_name)
            finally:
                f.close()
        except UnicodeDecodeError, msg:
            #import traceback
            #traceback.print_exc()
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

    def setup_errors(self, options, result):
        Errors.reset() # clear any remaining error state
        if options.use_listing_file:
            result.listing_file = Utils.replace_suffix(source, ".lis")
            path = result.listing_file
        else:
            path = None
        Errors.open_listing_file(path=path,
                                 echo_to_stderr=options.errors_to_stderr)

    def teardown_errors(self, err, options, result):
        source_desc = result.compilation_source.source_desc
        if not isinstance(source_desc, FileSourceDescriptor):
            raise RuntimeError("Only file sources for code supported")
        Errors.close_listing_file()
        result.num_errors = Errors.num_errors
        if result.num_errors > 0:
            err = True
        if err and result.c_file:
            try:
                Utils.castrate_file(result.c_file, os.stat(source_desc.filename))
            except EnvironmentError:
                pass
            result.c_file = None

def create_parse(context):
    def parse(compsrc):
        source_desc = compsrc.source_desc
        full_module_name = compsrc.full_module_name
        initial_pos = (source_desc, 1, 0)
        scope = context.find_module(full_module_name, pos = initial_pos, need_pxd = 0)
        tree = context.parse(source_desc, scope, pxd = 0, full_module_name = full_module_name)
        tree.compilation_source = compsrc
        tree.scope = scope
        tree.is_pxd = False
        return tree
    return parse

def create_default_resultobj(compilation_source, options):
    result = CompilationResult()
    result.main_source_file = compilation_source.source_desc.filename
    result.compilation_source = compilation_source
    source_desc = compilation_source.source_desc
    if options.output_file:
        result.c_file = os.path.join(compilation_source.cwd, options.output_file)
    else:
        if options.cplus:
            c_suffix = ".cpp"
        else:
            c_suffix = ".c"
        result.c_file = Utils.replace_suffix(source_desc.filename, c_suffix)
    return result

def run_pipeline(source, options, full_module_name = None):
    # Set up context
    context = options.create_context()

    # Set up source object
    cwd = os.getcwd()
    abs_path = os.path.abspath(source)
    source_ext = os.path.splitext(source)[1]
    full_module_name = full_module_name or context.extract_module_name(source, options)
    if options.relative_path_in_code_position_comments:
        rel_path = full_module_name.replace('.', os.sep) + source_ext
        if not abs_path.endswith(rel_path):
            rel_path = source # safety measure to prevent printing incorrect paths
    else:
        rel_path = abs_path
    source_desc = FileSourceDescriptor(abs_path, rel_path)
    source = CompilationSource(source_desc, full_module_name, cwd)

    # Set up result object
    result = create_default_resultobj(source, options)

    # Get pipeline
    if source_ext.lower() == '.py':
        pipeline = context.create_py_pipeline(options, result)
    else:
        pipeline = context.create_pyx_pipeline(options, result)

    context.setup_errors(options, result)
    err, enddata = context.run_pipeline(pipeline, source)
    context.teardown_errors(err, options, result)
    return result


#------------------------------------------------------------------------
#
#  Main Python entry points
#
#------------------------------------------------------------------------

class CompilationSource(object):
    """
    Contains the data necesarry to start up a compilation pipeline for
    a single compilation unit.
    """
    def __init__(self, source_desc, full_module_name, cwd):
        self.source_desc = source_desc
        self.full_module_name = full_module_name
        self.cwd = cwd

class CompilationOptions(object):
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
    compiler_directives  dict      Overrides for pragma options (see Options.py)
    evaluate_tree_assertions boolean  Test support: evaluate parse tree assertions
    language_level    integer   The Python language level: 2 or 3

    cplus             boolean   Compile as c++ code
    """

    def __init__(self, defaults = None, **kw):
        self.include_path = []
        if defaults:
            if isinstance(defaults, CompilationOptions):
                defaults = defaults.__dict__
        else:
            defaults = default_options
        self.__dict__.update(defaults)
        self.__dict__.update(kw)

    def create_context(self):
        return Context(self.include_path, self.compiler_directives,
                      self.cplus, self.language_level)


class CompilationResult(object):
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
    compilation_source CompilationSource
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
    return run_pipeline(source, options, full_module_name)


def compile_multiple(sources, options):
    """
    compile_multiple(sources, options)

    Compiles the given sequence of Pyrex implementation files and returns
    a CompilationResultSet. Performs timestamp checking and/or recursion
    if these are specified in the options.
    """
    context = options.create_context()
    sources = [os.path.abspath(source) for source in sources]
    processed = set()
    results = CompilationResultSet()
    recursive = options.recursive
    timestamps = options.timestamps
    if timestamps is None:
        timestamps = recursive
    verbose = options.verbose or ((recursive or timestamps) and not options.quiet)
    for source in sources:
        if source not in processed:
            # Compiling multiple sources in one context doesn't quite
            # work properly yet.
            if not timestamps or context.c_file_out_of_date(source):
                if verbose:
                    sys.stderr.write("Compiling %s\n" % source)

                result = run_pipeline(source, options)
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

def compile(source, options = None, full_module_name = None, **kwds):
    """
    compile(source [, options], [, <option> = <value>]...)

    Compile one or more Pyrex implementation files, with optional timestamp
    checking and recursing on dependecies. The source argument may be a string
    or a sequence of strings If it is a string and no recursion or timestamp
    checking is requested, a CompilationResult is returned, otherwise a
    CompilationResultSet is returned.
    """
    options = CompilationOptions(defaults = options, **kwds)
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
def setuptools_main():
    return main(command_line = 1)

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
    cplus = 0,
    output_file = None,
    annotate = False,
    generate_pxi = 0,
    working_path = "",
    recursive = 0,
    timestamps = None,
    verbose = 0,
    quiet = 0,
    compiler_directives = {},
    evaluate_tree_assertions = False,
    emit_linenums = False,
    relative_path_in_code_position_comments = True,
    c_line_in_traceback = True,
    language_level = 2,
    gdb_debug = False,
)
