"""
A Cython plugin for coverage.py

Requires the coverage package at least in version 4.0 (which added the plugin API).
"""

from __future__ import absolute_import

import re
import os.path
import sys
from collections import defaultdict
import token
import tokenize

from coverage.plugin import CoveragePlugin, FileTracer, FileReporter  # requires coverage.py 4.0+
from coverage.config import HandyConfigParser, DEFAULT_EXCLUDE
from coverage.misc import join_regex, contract, nice_pair
from coverage import env
from coverage.parser import PythonParser
from coverage.phystokens import generate_tokens

from .Utils import find_root_package_dir, is_package_dir, open_source_file


from . import __version__


def _find_c_source(base_path):
    if os.path.exists(base_path + '.c'):
        c_file = base_path + '.c'
    elif os.path.exists(base_path + '.cpp'):
        c_file = base_path + '.cpp'
    else:
        c_file = None
    return c_file


def _find_dep_file_path(main_file, file_path):
    abs_path = os.path.abspath(file_path)
    if file_path.endswith('.pxi') and not os.path.exists(abs_path):
        # include files are looked up relative to the main source file
        pxi_file_path = os.path.join(os.path.dirname(main_file), file_path)
        if os.path.exists(pxi_file_path):
            abs_path = os.path.abspath(pxi_file_path)
    # search sys.path for external locations if a valid file hasn't been found
    if not os.path.exists(abs_path):
        for sys_path in sys.path:
            test_path = os.path.realpath(os.path.join(sys_path, file_path))
            if os.path.exists(test_path):
                return test_path
    return abs_path


class CythonParser(PythonParser):
    """Parse code to find executable lines, excluded lines, etc. 

    This information is all based on static analysis: no code execution is
    involved.

    """
    @contract(text='unicode|None')
    def __init__(self, text=None, filename=None, exclude=None,
                 c_lines=None, ignore_defs=False, ignore_cdefs=False):
        """
        Source can be provided as `text`, the text itself, or `filename`, from
        which the text will be read.  Excluded lines are those that match
        `exclude`, a regex.

        """
        PythonParser.__init__(self, text=text, filename=filename,
                              exclude=exclude)

        # Set of lines included in the cythonized c/cpp file
        self.c_lines = c_lines

        # Option to ignore python function definition
        self.ignore_defs = ignore_defs

        # Option to ignore cython function definitions
        self.ignore_cdefs = ignore_cdefs

        # The line numbers of python function definitions.
        self.raw_defs = set()

        # The line numbers of cython class and function definitions.
        self.raw_cdefs = set()

    def _raw_parse(self):
        """Parse the source to find the interesting facts about its lines.

        A handful of attributes are updated.

        """
        # Find lines which match an exclusion pattern.
        if self.exclude:
            self.raw_excluded = self.lines_matching(self.exclude)

        # Tokenize, to find excluded suites, to find docstrings, and to find
        # multi-line statements.
        indent = 0
        exclude_indent = 0
        excluding = False
        excluding_decorators = False
        prev_toktype = token.INDENT
        first_line = None
        empty = True
        first_on_line = True
        def_type = None
        def_line = None
        def_closed = False

        tokgen = generate_tokens(self.text)
        for toktype, ttext, (slineno, _), (elineno, _), ltext in tokgen:
            if self.show_tokens:                # pragma: debugging
                print("%10s %5s %-20r %r" % (
                    tokenize.tok_name.get(toktype, toktype),
                    nice_pair((slineno, elineno)), ttext, ltext
                ))
            if toktype == token.INDENT:
                indent += 1
            elif toktype == token.DEDENT:
                indent -= 1
            elif toktype == token.NAME:
                if ttext == 'class':
                    # Class definitions look like branches in the bytecode, so
                    # we need to exclude them.  The simplest way is to note the
                    # lines with the 'class' keyword.
                    self.raw_classdefs.add(slineno)
                elif ttext in ['def', 'cdef']:
                    def_line = slineno
                    def_closed = False
                    def_type = ttext
            elif toktype == token.OP:
                if ttext == ':':
                    should_exclude = (elineno in self.raw_excluded) or excluding_decorators
                    if not excluding and should_exclude:
                        # Start excluding a suite.  We trigger off of the colon
                        # token so that the #pragma comment will be recognized on
                        # the same line as the colon.
                        self.raw_excluded.add(elineno)
                        exclude_indent = indent
                        excluding = True
                        excluding_decorators = False
                    if def_line is not None:
                        def_closed = True
                elif ttext == '@' and first_on_line:
                    # A decorator.
                    if elineno in self.raw_excluded:
                        excluding_decorators = True
                    if excluding_decorators:
                        self.raw_excluded.add(elineno)
            elif toktype == token.STRING and prev_toktype == token.INDENT:
                # Strings that are first on an indented line are docstrings.
                # (a trick from trace.py in the stdlib.) This works for
                # 99.9999% of cases.  For the rest (!) see:
                # http://stackoverflow.com/questions/1769332/x/1769794#1769794
                self.raw_docstrings.update(range(slineno, elineno+1))
            elif toktype == token.NEWLINE:
                if first_line is not None and elineno != first_line:
                    # We're at the end of a line, and we've ended on a
                    # different line than the first line of the statement,
                    # so record a multi-line range.
                    for l in range(first_line, elineno+1):
                        self._multiline[l] = first_line
                first_line = None
                first_on_line = True
                if def_line is not None:
                    if def_closed:
                        if def_type == 'def':
                            self.raw_defs.update(range(def_line, elineno+1))
                        elif def_type == 'cdef':
                            self.raw_cdefs.update(range(def_line, elineno+1))
                    def_line = None
                    def_closed = False
                    def_type = None

            if ttext.strip() and toktype != tokenize.COMMENT:
                # A non-whitespace token.
                empty = False
                if first_line is None:
                    # The token is not whitespace, and is the first in a
                    # statement.
                    self.raw_statements.add(slineno)
                    first_line = slineno
                    # Check whether to end an excluded suite.
                    if excluding and indent <= exclude_indent:
                        excluding = False
                    if excluding:
                        self.raw_excluded.add(elineno)
                    first_on_line = False
                if def_line is not None and def_closed and ttext != ':':
                    # The : was not at the end of the statement
                    def_closed = False

            prev_toktype = toktype

    def parse_source(self):
        """Parse source text to find executable lines, excluded lines, etc.

        Sets the .excluded and .statements attributes, normalized to the first
        line of multi-line statements.

        """
        try:
            self._raw_parse()
        except (tokenize.TokenError, IndentationError) as err:
            if hasattr(err, "lineno"):
                lineno = err.lineno         # IndentationError
            else:
                lineno = err.args[1][0]     # TokenError
            raise NotPython(
                u"Couldn't parse '%s' as Cython source: '%s' at line %d" % (
                    self.filename, err.args[0], lineno
                )
            )
        
        self.excluded = self.first_lines(self.raw_excluded)

        ignore = self.excluded | self.raw_docstrings
        if self.ignore_defs:
            ignore |= self.raw_defs
        if self.ignore_cdefs:
            ignore |= self.raw_cdefs
        if self.c_lines:
            starts = self.c_lines - ignore
        else:
            starts = self.raw_statements - ignore
        self.statements = self.first_lines(starts) - ignore


class Plugin(CoveragePlugin):
    # map from traced file paths to absolute file paths
    _file_path_map = None
    # map from traced file paths to corresponding C files
    _c_files_map = None
    # map from parsed C files to their content
    _parsed_c_files = None

    def __init__(self):
        CoveragePlugin.__init__(self)
        self.exclude_list = DEFAULT_EXCLUDE[:]
        self.ignore_defs = False
        self.ignore_cdefs = False

    def sys_info(self):
        return [('Cython version', __version__)]

    def file_tracer(self, filename):
        """
        Try to find a C source file for a file path found by the tracer.
        """
        if filename.startswith('<') or filename.startswith('memory:'):
            return None
        c_file = py_file = None
        filename = os.path.abspath(filename)
        if self._c_files_map and filename in self._c_files_map:
            c_file = self._c_files_map[filename][0]

        if c_file is None:
            c_file, py_file = self._find_source_files(filename)
            if not c_file:
                return None

            # parse all source file paths and lines from C file
            # to learn about all relevant source files right away (pyx/pxi/pxd)
            # FIXME: this might already be too late if the first executed line
            #        is not from the main .pyx file but a file with a different
            #        name than the .c file (which prevents us from finding the
            #        .c file)
            self._parse_lines(c_file, filename)

        if self._file_path_map is None:
            self._file_path_map = {}
        return CythonModuleTracer(filename, py_file, c_file, self._c_files_map, self._file_path_map)

    def file_reporter(self, filename):
        # TODO: let coverage.py handle .py files itself
        #ext = os.path.splitext(filename)[1].lower()
        #if ext == '.py':
        #    from coverage.python import PythonFileReporter
        #    return PythonFileReporter(filename)

        filename = os.path.abspath(filename)
        if self._c_files_map and filename in self._c_files_map:
            c_file, rel_file_path, code = self._c_files_map[filename]
        else:
            c_file, _ = self._find_source_files(filename)
            if not c_file:
                return None  # unknown file
            rel_file_path, code = self._parse_lines(c_file, filename)
        return CythonModuleReporter(c_file, filename, rel_file_path, code,
                                    self.exclude_list, self.ignore_defs,
                                    self.ignore_cdefs)

    def _find_source_files(self, filename):
        basename, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in ('.py', '.pyx', '.pxd', '.c', '.cpp'):
            pass
        elif ext in ('.so', '.pyd'):
            platform_suffix = re.search(r'[.]cpython-[0-9]+[a-z]*$', basename, re.I)
            if platform_suffix:
                basename = basename[:platform_suffix.start()]
        elif ext == '.pxi':
            # if we get here, it means that the first traced line of a Cython module was
            # not in the main module but in an include file, so try a little harder to
            # find the main source file
            self._find_c_source_files(os.path.dirname(filename), filename)
            if filename in self._c_files_map:
                return self._c_files_map[filename][0], None
        else:
            # none of our business
            return None, None

        c_file = filename if ext in ('.c', '.cpp') else _find_c_source(basename)
        if c_file is None:
            # a module "pkg/mod.so" can have a source file "pkg/pkg.mod.c"
            package_root = find_root_package_dir.uncached(filename)
            package_path = os.path.relpath(basename, package_root).split(os.path.sep)
            if len(package_path) > 1:
                test_basepath = os.path.join(os.path.dirname(filename), '.'.join(package_path))
                c_file = _find_c_source(test_basepath)

        py_source_file = None
        if c_file:
            py_source_file = os.path.splitext(c_file)[0] + '.py'
            if not os.path.exists(py_source_file):
                py_source_file = None

            try:
                with open(c_file, 'rb') as f:
                    if b'/* Generated by Cython ' not in f.read(30):
                        return None, None  # not a Cython file
            except (IOError, OSError):
                c_file = None

        return c_file, py_source_file

    def _find_c_source_files(self, dir_path, source_file):
        """
        Desperately parse all C files in the directory or its package parents
        (not re-descending) to find the (included) source file in one of them.
        """
        if not os.path.isdir(dir_path):
            return
        splitext = os.path.splitext
        for filename in os.listdir(dir_path):
            ext = splitext(filename)[1].lower()
            if ext in ('.c', '.cpp'):
                self._parse_lines(os.path.join(dir_path, filename), source_file)
                if source_file in self._c_files_map:
                    return
        # not found? then try one package up
        if is_package_dir(dir_path):
            self._find_c_source_files(os.path.dirname(dir_path), source_file)

    def _parse_lines(self, c_file, sourcefile):
        """
        Parse a Cython generated C/C++ source file and find the executable lines.
        Each executable line starts with a comment header that states source file
        and line number, as well as the surrounding range of source code lines.
        """
        if self._parsed_c_files is None:
            self._parsed_c_files = {}
        if c_file in self._parsed_c_files:
            code_lines = self._parsed_c_files[c_file]
        else:
            match_source_path_line = re.compile(r' */[*] +"(.*)":([0-9]+)$').match
            match_current_code_line = re.compile(r' *[*] (.*) # <<<<<<+$').match
            match_comment_end = re.compile(r' *[*]/$').match
            not_executable = re.compile(
                r'\s*c(?:type)?def\s+'
                r'(?:(?:public|external)\s+)?'
                r'(?:struct|union|enum|class)'
                r'(\s+[^:]+|)\s*:'
            ).match

            code_lines = defaultdict(dict)
            filenames = set()
            with open(c_file) as lines:
                lines = iter(lines)
                for line in lines:
                    match = match_source_path_line(line)
                    if not match:
                        continue
                    filename, lineno = match.groups()
                    filenames.add(filename)
                    lineno = int(lineno)
                    for comment_line in lines:
                        match = match_current_code_line(comment_line)
                        if match:
                            code_line = match.group(1).rstrip()
                            if not_executable(code_line):
                                break
                            code_lines[filename][lineno] = code_line
                            break
                        elif match_comment_end(comment_line):
                            # unexpected comment format - false positive?
                            break

            self._parsed_c_files[c_file] = code_lines

        if self._c_files_map is None:
            self._c_files_map = {}

        for filename, code in code_lines.items():
            abs_path = _find_dep_file_path(c_file, filename)
            self._c_files_map[abs_path] = (c_file, filename, code)

        if sourcefile not in self._c_files_map:
            return (None,) * 2  # e.g. shared library file
        return self._c_files_map[sourcefile][1:]

    CONFIG_SECTION = "Cython.Coverage"

    CONFIG_FILE_OPTIONS = [
        ('exclude_list', 'exclude_lines', 'regexlist'),
        ('ignore_defs', 'ignore_defs', 'boolean'),
        ('ignore_cdefs', 'ignore_cdefs', 'boolean'),
    ]

    def parse_config_options(self, raw_options):
        """
        Parse config options for the Cython.Coverage plugin.
        """
        section = self.CONFIG_SECTION
        cp = HandyConfigParser("")
        cp.add_section(section)
        for k, v in raw_options.items():
            cp.set(section, k, v)
        for attr, option, type_ in self.CONFIG_FILE_OPTIONS:
            if not cp.has_option(section, option):
                continue
            method = getattr(cp, 'get' + type_)
            setattr(self, attr, method(section, option))


class CythonModuleTracer(FileTracer):
    """
    Find the Python/Cython source file for a Cython module.
    """
    def __init__(self, module_file, py_file, c_file, c_files_map, file_path_map):
        super(CythonModuleTracer, self).__init__()
        self.module_file = module_file
        self.py_file = py_file
        self.c_file = c_file
        self._c_files_map = c_files_map
        self._file_path_map = file_path_map

    def has_dynamic_source_filename(self):
        return True

    def dynamic_source_filename(self, filename, frame):
        """
        Determine source file path.  Called by the function call tracer.
        """
        source_file = frame.f_code.co_filename
        try:
            return self._file_path_map[source_file]
        except KeyError:
            pass
        abs_path = _find_dep_file_path(filename, source_file)

        if self.py_file and source_file[-3:].lower() == '.py':
            # always let coverage.py handle this case itself
            self._file_path_map[source_file] = self.py_file
            return self.py_file

        assert self._c_files_map is not None
        if abs_path not in self._c_files_map:
            self._c_files_map[abs_path] = (self.c_file, source_file, None)
        self._file_path_map[source_file] = abs_path
        return abs_path


class CythonModuleReporter(FileReporter):
    """
    Provide detailed trace information for one source file to coverage.py.
    """
    def __init__(self, c_file, source_file, rel_file_path, code, 
                 exclude_re, ignore_defs, ignore_cdefs):
        super(CythonModuleReporter, self).__init__(source_file)
        self.name = rel_file_path
        self.c_file = c_file
        self._code = code
        self._exclude_re = exclude_re
        self._ignore_defs = ignore_defs
        self._ignore_cdefs = ignore_cdefs
        self._parser = None

    @property
    def exclude_regex(self):
        r"""Join raw regex."""
        return join_regex(self._exclude_re)

    @property
    def parser(self):
        """Lazily create a :class:`PythonParser`."""
        if self._parser is None:
            self._parser = CythonParser(
                filename=self.filename,
                exclude=self.exclude_regex,
                ignore_defs=self._ignore_defs,
                ignore_cdefs=self._ignore_cdefs,
                c_lines=set(self._code),
            )
            self._parser.parse_source()
        return self._parser

    def all_lines(self):
        """
        Return set of line numbers that are possibly executable.
        """
        return set(self._code)

    def lines(self):
        """
        Return set of line numbers that are possibly executable and not
        excluded.
        """
        return self.parser.statements

    def excluded_lines(self):
        """
        Return set of line numbers that have been excluded.
        """
        return self.parser.excluded

    def _iter_source_tokens(self):
        current_line = 1
        for line_no, code_line in sorted(self._code.items()):
            while line_no > current_line:
                yield []
                current_line += 1
            yield [('txt', code_line)]
            current_line += 1

    def source(self):
        """
        Return the source code of the file as a string.
        """
        if os.path.exists(self.filename):
            with open_source_file(self.filename) as f:
                return f.read()
        else:
            return '\n'.join(
                (tokens[0][1] if tokens else '')
                for tokens in self._iter_source_tokens())

    def source_token_lines(self):
        """
        Iterate over the source code tokens.
        """
        if os.path.exists(self.filename):
            with open_source_file(self.filename) as f:
                for line in f:
                    yield [('txt', line.rstrip('\n'))]
        else:
            for line in self._iter_source_tokens():
                yield [('txt', line)]


def coverage_init(reg, options):
    out = Plugin()
    out.parse_config_options(options)
    reg.add_file_tracer(out)
