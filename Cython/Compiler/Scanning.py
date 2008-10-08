#
#   Pyrex Scanner
#

#import pickle
import cPickle as pickle

import os
import platform
import stat
import sys
from time import time

from Cython import Plex, Utils
from Cython.Plex import Scanner
from Cython.Plex.Errors import UnrecognizedInput
from Errors import CompileError, error
from Lexicon import string_prefixes, raw_prefixes, make_lexicon

from StringEncoding import EncodedString

plex_version = getattr(Plex, '_version', None)
#print "Plex version:", plex_version ###

debug_scanner = 0
trace_scanner = 0
scanner_debug_flags = 0
scanner_dump_file = None
binary_lexicon_pickle = 1
notify_lexicon_unpickling = 0
notify_lexicon_pickling = 1

lexicon = None

#-----------------------------------------------------------------

def hash_source_file(path):
    # Try to calculate a hash code for the given source file.
    # Returns an empty string if the file cannot be accessed.
    #print "Hashing", path ###
    try:
        from hashlib import md5 as new_md5
    except ImportError:
        from md5 import new as new_md5
    try:
        try:
            f = open(path, "rU")
            text = f.read()
        except IOError, e:
            print("Unable to hash scanner source file (%s)" % e)
            return ""
    finally:
        f.close()
    # Normalise spaces/tabs. We don't know what sort of
    # space-tab substitution the file may have been
    # through, so we replace all spans of spaces and
    # tabs by a single space.
    import re
    text = re.sub("[ \t]+", " ", text)
    hash = new_md5(text).hexdigest()
    return hash

def open_pickled_lexicon(expected_hash):
    # Try to open pickled lexicon file and verify that
    # it matches the source file. Returns the opened
    # file if successful, otherwise None. ???
    global lexicon_pickle
    f = None
    result = None
    if os.path.exists(lexicon_pickle):
        try:
            f = open(lexicon_pickle, "rb")
            actual_hash = pickle.load(f)
            if actual_hash == expected_hash:
                result = f
                f = None
            else:
                print("Lexicon hash mismatch:")       ###
                print("   expected " + expected_hash) ###
                print("   got     " + actual_hash)    ###
        except IOError, e:
            print("Warning: Unable to read pickled lexicon " + lexicon_pickle)
            print(e)
    if f:
        f.close()
    return result

def try_to_unpickle_lexicon():
    global lexicon, lexicon_pickle, lexicon_hash
    dir = os.path.dirname(__file__)
    source_file = os.path.join(dir, "Lexicon.py")
    lexicon_hash = hash_source_file(source_file)
    lexicon_pickle = os.path.join(dir, "Lexicon.pickle")
    f = open_pickled_lexicon(expected_hash = lexicon_hash)
    if f:
        if notify_lexicon_unpickling:
            t0 = time()
            print("Unpickling lexicon...")
        lexicon = pickle.load(f)
        f.close()
        if notify_lexicon_unpickling:
            t1 = time()
            print("Done (%.2f seconds)" % (t1 - t0))

def create_new_lexicon():
    global lexicon
    t0 = time()
    print("Creating lexicon...")
    lexicon = make_lexicon()
    t1 = time()
    print("Done (%.2f seconds)" % (t1 - t0))

def pickle_lexicon():
    f = None
    try:
        f = open(lexicon_pickle, "wb")
    except IOError:
        print("Warning: Unable to save pickled lexicon in " + lexicon_pickle)
    if f:
        if notify_lexicon_pickling:
            t0 = time()
            print("Pickling lexicon...")
        pickle.dump(lexicon_hash, f, binary_lexicon_pickle)
        pickle.dump(lexicon, f, binary_lexicon_pickle)
        f.close()
        if notify_lexicon_pickling:
            t1 = time()
            print("Done (%.2f seconds)" % (t1 - t0))

def get_lexicon():
    global lexicon
    if not lexicon and plex_version is None:
        try_to_unpickle_lexicon()
    if not lexicon:
        create_new_lexicon()
        if plex_version is None:
            pickle_lexicon()
    return lexicon
    
#------------------------------------------------------------------

reserved_words = [
    "global", "include", "ctypedef", "cdef", "def", "class",
    "print", "del", "pass", "break", "continue", "return",
    "raise", "import", "exec", "try", "except", "finally",
    "while", "if", "elif", "else", "for", "in", "assert",
    "and", "or", "not", "is", "in", "lambda", "from",
    "cimport", "by", "with", "cpdef", "DEF", "IF", "ELIF", "ELSE"
]

class Method:

    def __init__(self, name):
        self.name = name
        self.__name__ = name # for Plex tracing
    
    def __call__(self, stream, text):
        return getattr(stream, self.name)(text)

#------------------------------------------------------------------

def build_resword_dict():
    d = {}
    for word in reserved_words:
        d[word] = 1
    return d

#------------------------------------------------------------------

class CompileTimeScope(object):

    def __init__(self, outer = None):
        self.entries = {}
        self.outer = outer
    
    def declare(self, name, value):
        self.entries[name] = value
    
    def lookup_here(self, name):
        return self.entries[name]
    
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
    import __builtin__
    names = ('False', 'True',
        'abs', 'bool', 'chr', 'cmp', 'complex', 'dict', 'divmod', 'enumerate',
        'float', 'hash', 'hex', 'int', 'len', 'list', 'long', 'map', 'max', 'min',
        'oct', 'ord', 'pow', 'range', 'reduce', 'repr', 'round', 'slice', 'str',
        'sum', 'tuple', 'xrange', 'zip')
    for name in names:
        benv.declare(name, getattr(__builtin__, name))
    denv = CompileTimeScope(benv)
    return denv

#------------------------------------------------------------------

class SourceDescriptor:
    """
    A SourceDescriptor should be considered immutable.
    """
    _escaped_description = None
    def __str__(self):
        assert False # To catch all places where a descriptor is used directly as a filename
    
    def get_escaped_description(self):
        if self._escaped_description is None:
            self._escaped_description = \
                self.get_description().encode('ASCII', 'replace').decode("ASCII")
        return self._escaped_description

class FileSourceDescriptor(SourceDescriptor):
    """
    Represents a code source. A code source is a more generic abstraction
    for a "filename" (as sometimes the code doesn't come from a file).
    Instances of code sources are passed to Scanner.__init__ as the
    optional name argument and will be passed back when asking for
    the position()-tuple.
    """
    def __init__(self, filename):
        self.filename = filename
    
    def get_lines(self):
        return Utils.open_source_file(self.filename)
    
    def get_description(self):
        return self.filename
    
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
    def __init__(self, name, code):
        self.name = name
        self.codelines = [x + "\n" for x in code.split("\n")]
    
    def get_lines(self):
        return self.codelines
    
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
    resword_dict = build_resword_dict()

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
        #	return
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
        if sy == 'IDENT':
            if systring in self.resword_dict:
                sy = systring
            else:
                systring = EncodedString(systring)
                systring.encoding = self.source_encoding
        self.sy = sy
        self.systring = systring
        if debug_scanner:
            _, line, col = self.position()
            if not self.systring or self.sy == self.systring:
                t = self.sy
            else:
                t = "%s %s" % (self.sy, self.systring)
            print("--- %3d %2d %s" % (line, col, t))
    
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
        if self.sy == 'IDENT' and self.systring == what:
            self.next()
        else:
            self.expected(what, message)
    
    def expected(self, what, message):
        if message:
            self.error(message)
        else:
            self.error("Expected '%s'" % what)
        
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
