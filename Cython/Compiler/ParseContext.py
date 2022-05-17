import io
import os
import re
import sys

from .. import Utils
from . import Errors, Options
from .Errors import CompileError, error, warning
from .Lexicon import (unicode_start_ch_any, unicode_continuation_ch_any,
                      unicode_start_ch_range, unicode_continuation_ch_range)
from .Scanning import FileSourceDescriptor, PyrexScanner
from .StringEncoding import EncodedString
from .Symtab import ModuleScope


standard_include_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Includes'))


def _make_range_re(chrs):
    out = []
    for i in range(0, len(chrs), 2):
        out.append(u"{0}-{1}".format(chrs[i], chrs[i+1]))
    return u"".join(out)

# py2 version looked like r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$"
module_name_pattern = u"[{0}{1}][{0}{2}{1}{3}]*".format(
    unicode_start_ch_any, _make_range_re(unicode_start_ch_range),
    unicode_continuation_ch_any,
    _make_range_re(unicode_continuation_ch_range))
module_name_pattern = re.compile(u"{0}(\\.{0})*$".format(module_name_pattern))


class CompilationSource(object):
    """
    Contains the data necessary to start up a compilation pipeline for
    a single compilation unit.
    """
    def __init__(self, source_desc, full_module_name, cwd):
        self.source_desc = source_desc
        self.full_module_name = full_module_name
        self.cwd = cwd


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

    cython_scope = None
    language_level = None  # warn when not set but default to Py2

    def __init__(self, include_directories, compiler_directives, cpp=False,
                 language_level=None, options=None):
        # cython_scope is a hack, set to False by subclasses, in order to break
        # an infinite loop.
        # Better code organization would fix it.

        from . import Builtin, CythonScope
        self.modules = {"__builtin__" : Builtin.builtin_scope}
        self.cython_scope = CythonScope.create_cython_scope(self)
        self.modules["cython"] = self.cython_scope
        self.include_directories = include_directories
        self.future_directives = set()
        self.compiler_directives = compiler_directives
        self.cpp = cpp
        self.options = options

        self.pxds = {}  # full name -> node tree
        self._interned = {}  # (type(value), value, *key_args) -> interned_value

        if language_level is not None:
            self.set_language_level(language_level)

        self.gdb_debug_outputwriter = None

    @classmethod
    def from_options(cls, options):
        return cls(options.include_path, options.compiler_directives,
                   options.cplus, options.language_level, options=options)

    def set_language_level(self, level):
        from .Future import print_function, unicode_literals, absolute_import, division, generator_stop
        future_directives = set()
        if level == '3str':
            level = 3
        else:
            level = int(level)
            if level >= 3:
                future_directives.add(unicode_literals)
        if level >= 3:
            future_directives.update([print_function, absolute_import, division, generator_stop])
        self.language_level = level
        self.future_directives = future_directives
        if level >= 3:
            self.modules['builtins'] = self.modules['__builtin__']

    def intern_ustring(self, value, encoding=None):
        key = (EncodedString, value, encoding)
        try:
            return self._interned[key]
        except KeyError:
            pass
        value = EncodedString(value)
        if encoding:
            value.encoding = encoding
        self._interned[key] = value
        return value

    # pipeline creation functions can now be found in Pipeline.py

    def process_pxd(self, source_desc, scope, module_name):
        from . import Pipeline, Main
        if isinstance(source_desc, FileSourceDescriptor) and source_desc._file_type == 'pyx':
            source = CompilationSource(source_desc, module_name, os.getcwd())
            result_sink = Main.create_default_resultobj(source, self.options)
            pipeline = Pipeline.create_pyx_as_pxd_pipeline(self, result_sink)
            result = Pipeline.run_pipeline(pipeline, source)
        else:
            pipeline = Pipeline.create_pxd_pipeline(self, scope, module_name)
            result = Pipeline.run_pipeline(pipeline, source_desc)
        return result

    def nonfatal_error(self, exc):
        return Errors.report_error(exc)

    def find_module(self, module_name, relative_to=None, pos=None, need_pxd=1,
                    absolute_fallback=True):
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
        if relative_to:
            if module_name:
                # from .module import ...
                qualified_name = relative_to.qualify_name(module_name)
            else:
                # from . import ...
                qualified_name = relative_to.qualified_name
                scope = relative_to
                relative_to = None
        else:
            qualified_name = module_name

        if not module_name_pattern.match(qualified_name):
            raise CompileError(pos or (module_name, 0, 0),
                               u"'%s' is not a valid module name" % module_name)

        if relative_to:
            if debug_find_module:
                print("...trying relative import")
            scope = relative_to.lookup_submodule(module_name)
            if not scope:
                pxd_pathname = self.find_pxd_file(qualified_name, pos)
                if pxd_pathname:
                    scope = relative_to.find_submodule(module_name)
        if not scope:
            if debug_find_module:
                print("...trying absolute import")
            if absolute_fallback:
                qualified_name = module_name
            scope = self
            for name in qualified_name.split("."):
                scope = scope.find_submodule(name)

        if debug_find_module:
            print("...scope = %s" % scope)
        if not scope.pxd_file_loaded:
            if debug_find_module:
                print("...pxd not loaded")
            if not pxd_pathname:
                if debug_find_module:
                    print("...looking for pxd file")
                # Only look in sys.path if we are explicitly looking
                # for a .pxd file.
                pxd_pathname = self.find_pxd_file(qualified_name, pos, sys_path=need_pxd)
                if debug_find_module:
                    print("......found %s" % pxd_pathname)
                if not pxd_pathname and need_pxd:
                    # Set pxd_file_loaded such that we don't need to
                    # look for the non-existing pxd file next time.
                    scope.pxd_file_loaded = True
                    package_pathname = self.search_include_directories(
                        qualified_name, suffix=".py", source_pos=pos)
                    if package_pathname and package_pathname.endswith(Utils.PACKAGE_FILES):
                        pass
                    else:
                        error(pos, "'%s.pxd' not found" % qualified_name.replace('.', os.sep))
            if pxd_pathname:
                scope.pxd_file_loaded = True
                try:
                    if debug_find_module:
                        print("Context.find_module: Parsing %s" % pxd_pathname)
                    rel_path = module_name.replace('.', os.sep) + os.path.splitext(pxd_pathname)[1]
                    if not pxd_pathname.endswith(rel_path):
                        rel_path = pxd_pathname  # safety measure to prevent printing incorrect paths
                    source_desc = FileSourceDescriptor(pxd_pathname, rel_path)
                    err, result = self.process_pxd(source_desc, scope, qualified_name)
                    if err:
                        raise err
                    (pxd_codenodes, pxd_scope) = result
                    self.pxds[module_name] = (pxd_codenodes, pxd_scope)
                except CompileError:
                    pass
        return scope

    def find_pxd_file(self, qualified_name, pos=None, sys_path=True, source_file_path=None):
        # Search include path (and sys.path if sys_path is True) for
        # the .pxd file corresponding to the given fully-qualified
        # module name.
        # Will find either a dotted filename or a file in a
        # package directory. If a source file position is given,
        # the directory containing the source file is searched first
        # for a dotted filename, and its containing package root
        # directory is searched first for a non-dotted filename.
        pxd = self.search_include_directories(
            qualified_name, suffix=".pxd", source_pos=pos, sys_path=sys_path, source_file_path=source_file_path)
        if pxd is None and Options.cimport_from_pyx:
            return self.find_pyx_file(qualified_name, pos)
        return pxd

    def find_pyx_file(self, qualified_name, pos=None, source_file_path=None):
        # Search include path for the .pyx file corresponding to the
        # given fully-qualified module name, as for find_pxd_file().
        return self.search_include_directories(
            qualified_name, suffix=".pyx", source_pos=pos, source_file_path=source_file_path)

    def find_include_file(self, filename, pos=None, source_file_path=None):
        # Search list of include directories for filename.
        # Reports an error and returns None if not found.
        path = self.search_include_directories(
            filename, source_pos=pos, include=True, source_file_path=source_file_path)
        if not path:
            error(pos, "'%s' not found" % filename)
        return path

    def search_include_directories(self, qualified_name,
                                   suffix=None, source_pos=None, include=False, sys_path=False, source_file_path=None):
        include_dirs = self.include_directories
        if sys_path:
            include_dirs = include_dirs + sys.path
        # include_dirs must be hashable for caching in @cached_function
        include_dirs = tuple(include_dirs + [standard_include_path])
        return search_include_directories(
            include_dirs, qualified_name, suffix or "", source_pos, include, source_file_path)

    def find_root_package_dir(self, file_path):
        return Utils.find_root_package_dir(file_path)

    def check_package_dir(self, dir, package_names):
        return Utils.check_package_dir(dir, tuple(package_names))

    def c_file_out_of_date(self, source_path, output_path):
        if not os.path.exists(output_path):
            return 1
        c_time = Utils.modification_time(output_path)
        if Utils.file_newer_than(source_path, c_time):
            return 1
        pxd_path = Utils.replace_suffix(source_path, ".pxd")
        if os.path.exists(pxd_path) and Utils.file_newer_than(pxd_path, c_time):
            return 1
        for kind, name in self.read_dependency_file(source_path):
            if kind == "cimport":
                dep_path = self.find_pxd_file(name, source_file_path=source_path)
            elif kind == "include":
                dep_path = self.search_include_directories(name, source_file_path=source_path)
            else:
                continue
            if dep_path and Utils.file_newer_than(dep_path, c_time):
                return 1
        return 0

    def find_cimported_module_names(self, source_path):
        return [ name for kind, name in self.read_dependency_file(source_path)
                 if kind == "cimport" ]

    def is_package_dir(self, dir_path):
        return Utils.is_package_dir(dir_path)

    def read_dependency_file(self, source_path):
        dep_path = Utils.replace_suffix(source_path, ".dep")
        if os.path.exists(dep_path):
            with open(dep_path, "rU") as f:
                chunks = [ line.split(" ", 1)
                           for line in (l.strip() for l in f)
                           if " " in line ]
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
        num_errors = Errors.get_errors_count()
        try:
            with Utils.open_source_file(source_filename) as f:
                from . import Parsing
                s = PyrexScanner(f, source_desc, source_encoding = f.encoding,
                                 scope = scope, context = self)
                tree = Parsing.p_module(s, pxd, full_module_name)
                if self.options.formal_grammar:
                    try:
                        from ..Parser import ConcreteSyntaxTree
                    except ImportError:
                        raise RuntimeError(
                            "Formal grammar can only be used with compiled Cython with an available pgen.")
                    ConcreteSyntaxTree.p_module(source_filename)
        except UnicodeDecodeError as e:
            #import traceback
            #traceback.print_exc()
            raise self._report_decode_error(source_desc, e)

        if Errors.get_errors_count() > num_errors:
            raise CompileError()
        return tree

    def _report_decode_error(self, source_desc, exc):
        msg = exc.args[-1]
        position = exc.args[2]
        encoding = exc.args[0]

        line = 1
        column = idx = 0
        with io.open(source_desc.filename, "r", encoding='iso8859-1', newline='') as f:
            for line, data in enumerate(f, 1):
                idx += len(data)
                if idx >= position:
                    column = position - (idx - len(data)) + 1
                    break

        return error((source_desc, line, column),
                     "Decoding error, missing or incorrect coding=<encoding-name> "
                     "at top of source (cannot decode with encoding %r: %s)" % (encoding, msg))

    def extract_module_name(self, path, options):
        # Find fully_qualified module name from the full pathname
        # of a source file.
        dir, filename = os.path.split(path)
        module_name, _ = os.path.splitext(filename)
        if "." in module_name:
            return module_name
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
        Errors.init_thread()
        if options.use_listing_file:
            path = result.listing_file = Utils.replace_suffix(result.main_source_file, ".lis")
        else:
            path = None
        Errors.open_listing_file(path=path, echo_to_stderr=options.errors_to_stderr)

    def teardown_errors(self, err, options, result):
        source_desc = result.compilation_source.source_desc
        if not isinstance(source_desc, FileSourceDescriptor):
            raise RuntimeError("Only file sources for code supported")
        Errors.close_listing_file()
        result.num_errors = Errors.get_errors_count()
        if result.num_errors > 0:
            err = True
        if err and result.c_file:
            try:
                Utils.castrate_file(result.c_file, os.stat(source_desc.filename))
            except EnvironmentError:
                pass
            result.c_file = None


@Utils.cached_function
def search_include_directories(dirs, qualified_name, suffix="", pos=None, include=False, source_file_path=None):
    """
    Search the list of include directories for the given file name.

    If a source file path or position is given, first searches the directory
    containing that file.  Returns None if not found, but does not report an error.

    The 'include' option will disable package dereferencing.
    """
    if pos and not source_file_path:
        file_desc = pos[0]
        if not isinstance(file_desc, FileSourceDescriptor):
            raise RuntimeError("Only file sources for code supported")
        source_file_path = file_desc.filename
    if source_file_path:
        if include:
            dirs = (os.path.dirname(source_file_path),) + dirs
        else:
            dirs = (Utils.find_root_package_dir(source_file_path),) + dirs

    # search for dotted filename e.g. <dir>/foo.bar.pxd
    dotted_filename = qualified_name
    if suffix:
        dotted_filename += suffix

    for dirname in dirs:
        path = os.path.join(dirname, dotted_filename)
        if os.path.exists(path):
            if not include and '.' in qualified_name and '.' in os.path.splitext(dotted_filename)[0]:
                warning(pos, "Dotted filenames ('%s') are deprecated."
                             " Please use the normal Python package directory layout." % dotted_filename, level=1)
            return path

    # search for filename in package structure e.g. <dir>/foo/bar.pxd or <dir>/foo/bar/__init__.pxd
    if not include:

        names = qualified_name.split('.')
        package_names = tuple(names[:-1])
        module_name = names[-1]

        # search for standard packages first - PEP420
        namespace_dirs = []
        for dirname in dirs:
            package_dir, is_namespace = Utils.check_package_dir(dirname, package_names)
            if package_dir is not None:
                if is_namespace:
                    namespace_dirs.append(package_dir)
                    continue
                path = search_module_in_dir(package_dir, module_name, suffix)
                if path:
                    return path

        # search for namespaces second - PEP420
        for package_dir in namespace_dirs:
            path = search_module_in_dir(package_dir, module_name, suffix)
            if path:
                return path

    return None


@Utils.cached_function
def search_module_in_dir(package_dir, module_name, suffix):
    # matches modules of the form: <dir>/foo/bar.pxd
    path = Utils.find_versioned_file(package_dir, module_name, suffix)

    # matches modules of the form: <dir>/foo/bar/__init__.pxd
    if not path and suffix:
        path = Utils.find_versioned_file(os.path.join(package_dir, module_name), "__init__", suffix)

    return path


class StringParseContext(Context):
    # Used in TreeFragment.
    # TODO: Consider moving both Context and StringParseContext elsewhere.

    def __init__(self, name, include_directories=None, compiler_directives=None, cpp=False):
        if include_directories is None:
            include_directories = []
        if compiler_directives is None:
            compiler_directives = {}
        Context.__init__(self, include_directories, compiler_directives, cpp=cpp, language_level='3str')
        self.module_name = name

    def find_module(self, module_name, relative_to=None, pos=None, need_pxd=1, absolute_fallback=True):
        if module_name not in (self.module_name, 'cython'):
            raise AssertionError("Not yet supporting any cimports/includes from string code snippets")
        return ModuleScope(module_name, parent_module=None, context=self)
