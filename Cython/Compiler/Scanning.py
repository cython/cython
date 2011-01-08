# cython: infer_types=True, language_level=3
#
#   Cython Scanner
#

import sys
import os
import platform

import cython
cython.declare(EncodedString=object, string_prefixes=object, raw_prefixes=object, IDENT=unicode,
               print_function=object)

from Cython import Plex, Utils
from Cython.Plex.Scanners import Scanner
from Cython.Plex.Errors import UnrecognizedInput
from Errors import CompileError, error
from Lexicon import string_prefixes, raw_prefixes, make_lexicon, IDENT
from Future import print_function

from StringEncoding import EncodedString

debug_scanner = 0
trace_scanner = 0
scanner_debug_flags = 0
scanner_dump_file = None

lexicon = None

def get_lexicon():
    global lexicon
    if not lexicon:
        lexicon = make_lexicon()
    return lexicon

#------------------------------------------------------------------

py_reserved_words = [
    "global", "def", "class", "print", "del", "pass", "break",
    "continue", "return", "raise", "import", "exec", "try",
    "except", "finally", "while", "if", "elif", "else", "for",
    "in", "assert", "and", "or", "not", "is", "in", "lambda",
    "from", "yield", "with", "nonlocal",
]

pyx_reserved_words = py_reserved_words + [
    "include", "ctypedef", "cdef", "cpdef",
    "cimport", "by", "DEF", "IF", "ELIF", "ELSE"
]

class Method(object):

    def __init__(self, name):
        self.name = name
        self.__name__ = name # for Plex tracing

    def __call__(self, stream, text):
        return getattr(stream, self.name)(text)

#------------------------------------------------------------------

class CompileTimeScope(object):

    def __init__(self, outer = None):
        self.entries = {}
        self.outer = outer

    def declare(self, name, value):
        self.entries[name] = value

    def lookup_here(self, name):
        return self.entries[name]

    def __contains__(self, name):
        return name in self.entries

    def lookup(self, name):
        try:
            return self.lookup_here(name)
        except KeyError:
            outer = self.outer
            if outer:
                return outer.lookup(name)
            else:
                raise

def initial_compile_time_env():
    benv = CompileTimeScope()
    names = ('UNAME_SYSNAME', 'UNAME_NODENAME', 'UNAME_RELEASE',
        'UNAME_VERSION', 'UNAME_MACHINE')
    for name, value in zip(names, platform.uname()):
        benv.declare(name, value)
    try:
        import __builtin__ as builtins
    except ImportError:
        import builtins
    names = ('False', 'True',
        'abs', 'bool', 'chr', 'cmp', 'complex', 'dict', 'divmod', 'enumerate',
        'float', 'hash', 'hex', 'int', 'len', 'list', 'long', 'map', 'max', 'min',
        'oct', 'ord', 'pow', 'range', 'reduce', 'repr', 'round', 'slice', 'str',
        'sum', 'tuple', 'xrange', 'zip')
    for name in names:
        try:
            benv.declare(name, getattr(builtins, name))
        except AttributeError:
            # ignore, likely Py3
            pass
    denv = CompileTimeScope(benv)
    return denv

#------------------------------------------------------------------

class SourceDescriptor(object):
    """
    A SourceDescriptor should be considered immutable.
    """
    _file_type = 'pyx'

    _escaped_description = None
    _cmp_name = ''
    def __str__(self):
        assert False # To catch all places where a descriptor is used directly as a filename

    def set_file_type_from_name(self, filename):
        name, ext = os.path.splitext(filename)
        self._file_type = ext in ('.pyx', '.pxd', '.py') and ext[1:] or 'pyx'

    def is_cython_file(self):
        return self._file_type in ('pyx', 'pxd')

    def is_python_file(self):
        return self._file_type == 'py'

    def get_escaped_description(self):
        if self._escaped_description is None:
            self._escaped_description = \
                self.get_description().encode('ASCII', 'replace').decode("ASCII")
        return self._escaped_description

    def __gt__(self, other):
        # this is only used to provide some sort of order
        try:
            return self._cmp_name > other._cmp_name
        except AttributeError:
            return False

    def __lt__(self, other):
        # this is only used to provide some sort of order
        try:
            return self._cmp_name < other._cmp_name
        except AttributeError:
            return False

    def __le__(self, other):
        # this is only used to provide some sort of order
        try:
            return self._cmp_name <= other._cmp_name
        except AttributeError:
            return False

class FileSourceDescriptor(SourceDescriptor):
    """
    Represents a code source. A code source is a more generic abstraction
    for a "filename" (as sometimes the code doesn't come from a file).
    Instances of code sources are passed to Scanner.__init__ as the
    optional name argument and will be passed back when asking for
    the position()-tuple.
    """
    def __init__(self, filename, path_description=None):
        filename = Utils.decode_filename(filename)
        self.path_description = path_description or filename
        self.filename = filename
        self.set_file_type_from_name(filename)
        self._cmp_name = filename

    def get_lines(self, encoding=None, error_handling=None):
        return Utils.open_source_file(
            self.filename, encoding=encoding,
            error_handling=error_handling,
            # newline normalisation is costly before Py2.6
            require_normalised_newlines=False)

    def get_description(self):
        return self.path_description

    def get_filenametable_entry(self):
        return self.filename

    def __eq__(self, other):
        return isinstance(other, FileSourceDescriptor) and self.filename == other.filename

    def __hash__(self):
        return hash(self.filename)

    def __repr__(self):
        return "<FileSourceDescriptor:%s>" % self.filename

class StringSourceDescriptor(SourceDescriptor):
    """
    Instances of this class can be used instead of a filenames if the
    code originates from a string object.
    """
    filename = None

    def __init__(self, name, code):
        self.name = name
        #self.set_file_type_from_name(name)
        self.codelines = [x + "\n" for x in code.split("\n")]
        self._cmp_name = name

    def get_lines(self, encoding=None, error_handling=None):
        if not encoding:
            return self.codelines
        else:
            return [ line.encode(encoding, error_handling).decode(encoding)
                     for line in self.codelines ]

    def get_description(self):
        return self.name

    def get_filenametable_entry(self):
        return "stringsource"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, StringSourceDescriptor) and self.name == other.name

    def __repr__(self):
        return "<StringSourceDescriptor:%s>" % self.name

#------------------------------------------------------------------

class PyrexScanner(Scanner):
    #  context            Context  Compilation context
    #  included_files     [string] Files included with 'include' statement
    #  compile_time_env   dict     Environment for conditional compilation
    #  compile_time_eval  boolean  In a true conditional compilation context
    #  compile_time_expr  boolean  In a compile-time expression context

    def __init__(self, file, filename, parent_scanner = None,
                 scope = None, context = None, source_encoding=None, parse_comments=True, initial_pos=None):
        Scanner.__init__(self, get_lexicon(), file, filename, initial_pos)
        if parent_scanner:
            self.context = parent_scanner.context
            self.included_files = parent_scanner.included_files
            self.compile_time_env = parent_scanner.compile_time_env
            self.compile_time_eval = parent_scanner.compile_time_eval
            self.compile_time_expr = parent_scanner.compile_time_expr
        else:
            self.context = context
            self.included_files = scope.included_files
            self.compile_time_env = initial_compile_time_env()
            self.compile_time_eval = 1
            self.compile_time_expr = 0
        self.parse_comments = parse_comments
        self.source_encoding = source_encoding
        if filename.is_python_file():
            self.in_python_file = True
            self.keywords = cython.set(py_reserved_words)
        else:
            self.in_python_file = False
            self.keywords = cython.set(pyx_reserved_words)
        self.trace = trace_scanner
        self.indentation_stack = [0]
        self.indentation_char = None
        self.bracket_nesting_level = 0
        self.begin('INDENT')
        self.sy = ''
        self.next()

    def commentline(self, text):
        if self.parse_comments:
            self.produce('commentline', text)

    def current_level(self):
        return self.indentation_stack[-1]

    def open_bracket_action(self, text):
        self.bracket_nesting_level = self.bracket_nesting_level + 1
        return text

    def close_bracket_action(self, text):
        self.bracket_nesting_level = self.bracket_nesting_level - 1
        return text

    def newline_action(self, text):
        if self.bracket_nesting_level == 0:
            self.begin('INDENT')
            self.produce('NEWLINE', '')

    string_states = {
        "'":   'SQ_STRING',
        '"':   'DQ_STRING',
        "'''": 'TSQ_STRING',
        '"""': 'TDQ_STRING'
    }

    def begin_string_action(self, text):
        if text[:1] in string_prefixes:
            text = text[1:]
        if text[:1] in raw_prefixes:
            text = text[1:]
        self.begin(self.string_states[text])
        self.produce('BEGIN_STRING')

    def end_string_action(self, text):
        self.begin('')
        self.produce('END_STRING')

    def unclosed_string_action(self, text):
        self.end_string_action(text)
        self.error("Unclosed string literal")

    def indentation_action(self, text):
        self.begin('')
        # Indentation within brackets should be ignored.
        #if self.bracket_nesting_level > 0:
        #    return
        # Check that tabs and spaces are being used consistently.
        if text:
            c = text[0]
            #print "Scanner.indentation_action: indent with", repr(c) ###
            if self.indentation_char is None:
                self.indentation_char = c
                #print "Scanner.indentation_action: setting indent_char to", repr(c)
            else:
                if self.indentation_char != c:
                    self.error("Mixed use of tabs and spaces")
            if text.replace(c, "") != "":
                self.error("Mixed use of tabs and spaces")
        # Figure out how many indents/dedents to do
        current_level = self.current_level()
        new_level = len(text)
        #print "Changing indent level from", current_level, "to", new_level ###
        if new_level == current_level:
            return
        elif new_level > current_level:
            #print "...pushing level", new_level ###
            self.indentation_stack.append(new_level)
            self.produce('INDENT', '')
        else:
            while new_level < self.current_level():
                #print "...popping level", self.indentation_stack[-1] ###
                self.indentation_stack.pop()
                self.produce('DEDENT', '')
            #print "...current level now", self.current_level() ###
            if new_level != self.current_level():
                self.error("Inconsistent indentation")

    def eof_action(self, text):
        while len(self.indentation_stack) > 1:
            self.produce('DEDENT', '')
            self.indentation_stack.pop()
        self.produce('EOF', '')

    def next(self):
        try:
            sy, systring = self.read()
        except UnrecognizedInput:
            self.error("Unrecognized character")
        if sy == IDENT:
            if systring in self.keywords:
                if systring == u'print' and print_function in self.context.future_directives:
                    self.keywords.discard('print')
                    systring = EncodedString(systring)
                elif systring == u'exec' and self.context.language_level >= 3:
                    self.keywords.discard('exec')
                    systring = EncodedString(systring)
                else:
                    sy = systring
            else:
                systring = EncodedString(systring)
        self.sy = sy
        self.systring = systring
        if False: # debug_scanner:
            _, line, col = self.position()
            if not self.systring or self.sy == self.systring:
                t = self.sy
            else:
                t = "%s %s" % (self.sy, self.systring)
            print("--- %3d %2d %s" % (line, col, t))

    def peek(self):
        saved = self.sy, self.systring
        self.next()
        next = self.sy, self.systring
        self.unread(*next)
        self.sy, self.systring = saved
        return next

    def put_back(self, sy, systring):
        self.unread(self.sy, self.systring)
        self.sy = sy
        self.systring = systring

    def unread(self, token, value):
        # This method should be added to Plex
        self.queue.insert(0, (token, value))

    def error(self, message, pos = None, fatal = True):
        if pos is None:
            pos = self.position()
        if self.sy == 'INDENT':
            err = error(pos, "Possible inconsistent indentation")
        err = error(pos, message)
        if fatal: raise err

    def expect(self, what, message = None):
        if self.sy == what:
            self.next()
        else:
            self.expected(what, message)

    def expect_keyword(self, what, message = None):
        if self.sy == IDENT and self.systring == what:
            self.next()
        else:
            self.expected(what, message)

    def expected(self, what, message = None):
        if message:
            self.error(message)
        else:
            if self.sy == IDENT:
                found = self.systring
            else:
                found = self.sy
            self.error("Expected '%s', found '%s'" % (what, found))

    def expect_indent(self):
        self.expect('INDENT',
            "Expected an increase in indentation level")

    def expect_dedent(self):
        self.expect('DEDENT',
            "Expected a decrease in indentation level")

    def expect_newline(self, message = "Expected a newline"):
        # Expect either a newline or end of file
        if self.sy != 'EOF':
            self.expect('NEWLINE', message)
