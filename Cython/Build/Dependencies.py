from glob import glob
import re, os, sys


from distutils.extension import Extension

from Cython import Utils
from Cython.Compiler.Main import Context, CompilationOptions, default_options

def cached_function(f):
    cache_name = '__%s_cache' % f.__name__
    def wrapper(*args):
        cache = getattr(f, cache_name, None)
        if cache is None:
            cache = {}
            setattr(f, cache_name, cache)
        if args in cache:
            return cache[args]
        res = cache[args] = f(*args)
        return res
    return wrapper

def cached_method(f):
    cache_name = '__%s_cache' % f.__name__
    def wrapper(self, *args):
        cache = getattr(self, cache_name, None)
        if cache is None:
            cache = {}
            setattr(self, cache_name, cache)
        if args in cache:
            return cache[args]
        res = cache[args] = f(self, *args)
        return res
    return wrapper
    
def extended_iglob(pattern):
    if '**/' in pattern:
        seen = set()
        first, rest = pattern.split('**/', 1)
        if first == '':
            first = '.'
        for root in glob(first + "/"):
            for path in extended_iglob(os.path.join(root, rest)):
                if path not in seen:
                    seen.add(path)
                    yield path
            for path in extended_iglob(os.path.join(root, '*', '**', rest)):
                if path not in seen:
                    seen.add(path)
                    yield path
    else:
        for path in glob(pattern):
            yield path

def parse_list(s):
    """
    >>> parse_list("a b c")
    ['a', 'b', 'c']
    >>> parse_list("[a, b, c]")
    ['a', 'b', 'c']
    >>> parse_list('a " " b')
    ['a', ' ', 'b']
    >>> parse_list('[a, ",a", "a,", ",", ]')
    ['a', ',a', 'a,', ',']
    """
    if s[0] == '[' and s[-1] == ']':
        s = s[1:-1]
        delimiter = ','
    else:
        delimiter = ' '
    s, literals = strip_string_literals(s)
    def unquote(literal):
        literal = literal.strip()
        if literal[0] in "'\"":
            return literals[literal[1:-1]]
        else:
            return literal
    return [unquote(item) for item in s.split(delimiter) if item.strip()]

transitive_str = object()
transitive_list = object()

distutils_settings = {
    'name':                 str,
    'sources':              list,
    'define_macros':        list,
    'undef_macros':         list,
    'libraries':            transitive_list,
    'library_dirs':         transitive_list,
    'runtime_library_dirs': transitive_list,
    'include_dirs':         transitive_list,
    'extra_objects':        list,
    'extra_compile_args':   transitive_list,
    'extra_link_args':      transitive_list,
    'export_symbols':       list,
    'depends':              transitive_list,
    'language':             transitive_str,
}

def line_iter(source):
    start = 0
    while True:
        end = source.find('\n', start)
        if end == -1:
            yield source[start:]
            return
        yield source[start:end]
        start = end+1

class DistutilsInfo(object):

    def __init__(self, source=None, exn=None):
        self.values = {}
        if source is not None:
            for line in line_iter(source):
                line = line.strip()
                if line != '' and line[0] != '#':
                    break
                line = line[1:].strip()
                if line[:10] == 'distutils:':
                    line = line[10:]
                    ix = line.index('=')
                    key = str(line[:ix].strip())
                    value = line[ix+1:].strip()
                    type = distutils_settings[key]
                    if type in (list, transitive_list):
                        value = parse_list(value)
                        if key == 'define_macros':
                            value = [tuple(macro.split('=')) for macro in value]
                    self.values[key] = value
        elif exn is not None:
            for key in distutils_settings:
                if key in ('name', 'sources'):
                    continue
                value = getattr(exn, key, None)
                if value:
                    self.values[key] = value

    def merge(self, other):
        if other is None:
            return self
        for key, value in other.values.items():
            type = distutils_settings[key]
            if type is transitive_str and key not in self.values:
                self.values[key] = value
            elif type is transitive_list:
                if key in self.values:
                    all = self.values[key]
                    for v in value:
                        if v not in all:
                            all.append(v)
                else:
                    self.values[key] = value
        return self

    def subs(self, aliases):
        if aliases is None:
            return self
        resolved = DistutilsInfo()
        for key, value in self.values.items():
            type = distutils_settings[key]
            if type in [list, transitive_list]:
                new_value_list = []
                for v in value:
                    if v in aliases:
                        v = aliases[v]
                    if isinstance(v, list):
                        new_value_list += v
                    else:
                        new_value_list.append(v)
                value = new_value_list
            else:
                if value in aliases:
                    value = aliases[value]
            resolved.values[key] = value
        return resolved


def strip_string_literals(code, prefix='__Pyx_L'):
    """
    Normalizes every string literal to be of the form '__Pyx_Lxxx',
    returning the normalized code and a mapping of labels to
    string literals.
    """
    new_code = []
    literals = {}
    counter = 0
    start = q = 0
    in_quote = False
    raw = False
    while True:
        hash_mark = code.find('#', q)
        single_q = code.find("'", q)
        double_q = code.find('"', q)
        q = min(single_q, double_q)
        if q == -1: q = max(single_q, double_q)

        # We're done.
        if q == -1 and hash_mark == -1:
            new_code.append(code[start:])
            break

        # Try to close the quote.
        elif in_quote:
            if code[q-1] == '\\' and not raw:
                k = 2
                while q >= k and code[q-k] == '\\':
                    k += 1
                if k % 2 == 0:
                    q += 1
                    continue
            if code[q:q+len(in_quote)] == in_quote:
                counter += 1
                label = "%s%s_" % (prefix, counter)
                literals[label] = code[start+len(in_quote):q]
                new_code.append("%s%s%s" % (in_quote, label, in_quote))
                q += len(in_quote)
                in_quote = False
                start = q
            else:
                q += 1

        # Process comment.
        elif -1 != hash_mark and (hash_mark < q or q == -1):
            end = code.find('\n', hash_mark)
            if end == -1:
                end = None
            new_code.append(code[start:hash_mark+1])
            counter += 1
            label = "%s%s_" % (prefix, counter)
            literals[label] = code[hash_mark+1:end]
            new_code.append(label)
            if end is None:
                break
            q = end
            start = q

        # Open the quote.
        else:
            raw = False
            if len(code) >= q+3 and (code[q+1] == code[q] == code[q+2]):
                in_quote = code[q]*3
            else:
                in_quote = code[q]
            end = marker = q
            while marker > 0 and code[marker-1] in 'rRbBuU':
                if code[marker-1] in 'rR':
                    raw = True
                marker -= 1
            new_code.append(code[start:end])
            start = q
            q += len(in_quote)

    return "".join(new_code), literals


def parse_dependencies(source_filename):
    # Actual parsing is way to slow, so we use regular expressions.
    # The only catch is that we must strip comments and string
    # literals ahead of time.
    fh = Utils.open_source_file(source_filename, "rU")
    try:
        source = fh.read()
    finally:
        fh.close()
    distutils_info = DistutilsInfo(source)
    source, literals = strip_string_literals(source)
    source = source.replace('\\\n', ' ')
    if '\t' in source:
        source = source.replace('\t', ' ')
    # TODO: pure mode
    dependancy = re.compile(r"(cimport +([0-9a-zA-Z_.]+)\b)|(from +([0-9a-zA-Z_.]+) +cimport)|(include +'([^']+)')|(cdef +extern +from +'([^']+)')")
    cimports = []
    includes = []
    externs  = []
    for m in dependancy.finditer(source):
        groups = m.groups()
        if groups[0]:
            cimports.append(groups[1])
        elif groups[2]:
            cimports.append(groups[3])
        elif groups[4]:
            includes.append(literals[groups[5]])
        else:
            externs.append(literals[groups[7]])
    return cimports, includes, externs, distutils_info


class DependencyTree(object):

    def __init__(self, context):
        self.context = context
        self._transitive_cache = {}

    @cached_method
    def parse_dependencies(self, source_filename):
        return parse_dependencies(source_filename)
    
    @cached_method
    def cimports_and_externs(self, filename):
        cimports, includes, externs = self.parse_dependencies(filename)[:3]
        cimports = set(cimports)
        externs = set(externs)
        for include in includes:
            include_path = os.path.join(os.path.dirname(filename), include)
            if not os.path.exists(include_path):
                include_path = self.context.find_include_file(include, None)
            if include_path:
                a, b = self.cimports_and_externs(include_path)
                cimports.update(a)
                externs.update(b)
            else:
                print("Unable to locate '%s' referenced from '%s'" % (filename, include))
        return tuple(cimports), tuple(externs)

    def cimports(self, filename):
        return self.cimports_and_externs(filename)[0]

    @cached_method
    def package(self, filename):
        dir = os.path.dirname(os.path.abspath(filename))
        if dir != filename and os.path.exists(os.path.join(dir, '__init__.py')):
            return self.package(dir) + (os.path.basename(dir),)
        else:
            return ()

    @cached_method
    def fully_qualifeid_name(self, filename):
        module = os.path.splitext(os.path.basename(filename))[0]
        return '.'.join(self.package(filename) + (module,))

    def find_pxd(self, module, filename=None):
        if module[0] == '.':
            raise NotImplementedError("New relative imports.")
        if filename is not None:
            relative = '.'.join(self.package(filename) + tuple(module.split('.')))
            pxd = self.context.find_pxd_file(relative, None)
            if pxd:
                return pxd
        return self.context.find_pxd_file(module, None)
    find_pxd = cached_method(find_pxd)

    @cached_method
    def cimported_files(self, filename):
        if filename[-4:] == '.pyx' and os.path.exists(filename[:-4] + '.pxd'):
            self_pxd = [filename[:-4] + '.pxd']
        else:
            self_pxd = []
        a = self.cimports(filename)
        b = filter(None, [self.find_pxd(m, filename) for m in self.cimports(filename)])
        if len(a) - int('cython' in a) != len(b):
            print("missing cimport", filename)
            print("\n\t".join(a))
            print("\n\t".join(b))
        return tuple(self_pxd + filter(None, [self.find_pxd(m, filename) for m in self.cimports(filename)]))

    def immediate_dependencies(self, filename):
        all = list(self.cimported_files(filename))
        for extern in sum(self.cimports_and_externs(filename), ()):
            all.append(os.path.normpath(os.path.join(os.path.dirname(filename), extern)))
        return tuple(all)

    @cached_method
    def timestamp(self, filename):
        return os.path.getmtime(filename)

    def extract_timestamp(self, filename):
        # TODO: .h files from extern blocks
        return self.timestamp(filename), filename

    def newest_dependency(self, filename):
        return self.transitive_merge(filename, self.extract_timestamp, max)

    def distutils_info0(self, filename):
        return self.parse_dependencies(filename)[3]

    def distutils_info(self, filename, aliases=None, base=None):
        return (self.transitive_merge(filename, self.distutils_info0, DistutilsInfo.merge)
            .subs(aliases)
            .merge(base))

    def transitive_merge(self, node, extract, merge):
        try:
            seen = self._transitive_cache[extract, merge]
        except KeyError:
            seen = self._transitive_cache[extract, merge] = {}
        return self.transitive_merge_helper(
            node, extract, merge, seen, {}, self.cimported_files)[0]

    def transitive_merge_helper(self, node, extract, merge, seen, stack, outgoing):
        if node in seen:
            return seen[node], None
        deps = extract(node)
        if node in stack:
            return deps, node
        try:
            stack[node] = len(stack)
            loop = None
            for next in outgoing(node):
                sub_deps, sub_loop = self.transitive_merge_helper(next, extract, merge, seen, stack, outgoing)
                if sub_loop is not None:
                    if loop is not None and stack[loop] < stack[sub_loop]:
                        pass
                    else:
                        loop = sub_loop
                deps = merge(deps, sub_deps)
            if loop == node:
                loop = None
            if loop is None:
                seen[node] = deps
            return deps, loop
        finally:
            del stack[node]

_dep_tree = None
def create_dependency_tree(ctx=None):
    global _dep_tree
    if _dep_tree is None:
        if ctx is None:
            ctx = Context(["."], CompilationOptions(default_options))
        _dep_tree = DependencyTree(ctx)
    return _dep_tree

# This may be useful for advanced users?
def create_extension_list(patterns, exclude=[], ctx=None, aliases=None):
    seen = set()
    deps = create_dependency_tree(ctx)
    to_exclude = set()
    if not isinstance(exclude, list):
        exclude = [exclude]
    for pattern in exclude:
        to_exclude.update(extended_iglob(pattern))
    if not isinstance(patterns, list):
        patterns = [patterns]
    module_list = []
    for pattern in patterns:
        if isinstance(pattern, str):
            filepattern = pattern
            template = None
            name = '*'
            base = None
            exn_type = Extension
        elif isinstance(pattern, Extension):
            filepattern = pattern.sources[0]
            if os.path.splitext(filepattern)[1] not in ('.py', '.pyx'):
                # ignore non-cython modules
                module_list.append(pattern)
                continue
            template = pattern
            name = template.name
            base = DistutilsInfo(exn=template)
            exn_type = template.__class__
        else:
            raise TypeError(pattern)
        for file in extended_iglob(filepattern):
            if file in to_exclude:
                continue
            pkg = deps.package(file)
            if '*' in name:
                module_name = deps.fully_qualifeid_name(file)
            else:
                module_name = name
            if module_name not in seen:
                kwds = deps.distutils_info(file, aliases, base).values
                if base is not None:
                    for key, value in base.values.items():
                        if key not in kwds:
                            kwds[key] = value
                sources = [file]
                if template is not None:
                    sources += template.sources[1:]
                module_list.append(exn_type(
                        name=module_name,
                        sources=sources,
                        **kwds))
                m = module_list[-1]
                seen.add(name)
    return module_list

# This is the user-exposed entry point.
def cythonize(module_list, exclude=[], nthreads=0, aliases=None, quiet=False, force=False, **options):
    if 'include_path' not in options:
        options['include_path'] = ['.']
    c_options = CompilationOptions(**options)
    cpp_options = CompilationOptions(**options); cpp_options.cplus = True
    ctx = c_options.create_context()
    module_list = create_extension_list(
        module_list,
        exclude=exclude,
        ctx=ctx,
        aliases=aliases)
    deps = create_dependency_tree(ctx)
    to_compile = []
    for m in module_list:
        new_sources = []
        for source in m.sources:
            base, ext = os.path.splitext(source)
            if ext in ('.pyx', '.py'):
                if m.language == 'c++':
                    c_file = base + '.cpp'
                    options = cpp_options
                else:
                    c_file = base + '.c'
                    options = c_options
                if os.path.exists(c_file):
                    c_timestamp = os.path.getmtime(c_file)
                else:
                    c_timestamp = -1
                # Priority goes first to modified files, second to direct
                # dependents, and finally to indirect dependents.
                if c_timestamp < deps.timestamp(source):
                    dep_timestamp, dep = deps.timestamp(source), source
                    priority = 0
                else:
                    dep_timestamp, dep = deps.newest_dependency(source)
                    priority = 2 - (dep in deps.immediate_dependencies(source))
                if force or c_timestamp < dep_timestamp:
                    if not quiet:
                        if source == dep:
                            print("Compiling %s because it changed." % source)
                        else:
                            print("Compiling %s because it depends on %s." % (source, dep))
                    to_compile.append((priority, source, c_file, options))
                new_sources.append(c_file)
            else:
                new_sources.append(source)
        m.sources = new_sources
    to_compile.sort()
    if nthreads:
        # Requires multiprocessing (or Python >= 2.6)
        try:
            import multiprocessing
            pool = multiprocessing.Pool(nthreads)
            pool.map(cythonize_one_helper, to_compile)
        except ImportError:
            print("multiprocessing required for parallel cythonization")
            nthreads = 0
    if not nthreads:
        for priority, pyx_file, c_file, options in to_compile:
            cythonize_one(pyx_file, c_file, quiet, options)
    return module_list

# TODO: Share context? Issue: pyx processing leaks into pxd module
def cythonize_one(pyx_file, c_file, quiet, options=None):
    from Cython.Compiler.Main import compile, default_options
    from Cython.Compiler.Errors import CompileError, PyrexError

    if not quiet:
        print "Cythonizing %s" % pyx_file
    if options is None:
        options = CompilationOptions(default_options)
    options.output_file = c_file

    any_failures = 0
    try:
        result = compile([pyx_file], options)
        if result.num_errors > 0:
            any_failures = 1
    except (EnvironmentError, PyrexError), e:
        sys.stderr.write(str(e) + '\n')
        any_failures = 1
    if any_failures:
        raise CompileError(None, pyx_file)

def cythonize_one_helper(m):
    return cythonize_one(*m[1:])
