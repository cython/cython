#
#   Pyrex Scanner
#

#import pickle
import cPickle as pickle

import os
import stat
import sys
from time import time

from Pyrex import Plex
from Pyrex.Plex import Scanner
from Pyrex.Plex.Errors import UnrecognizedInput
from Errors import CompileError, error
from Lexicon import string_prefixes, make_lexicon

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
    import md5
    try:
        try:
            f = open(path, "rU")
            text = f.read()
        except IOError, e:
            print "Unable to hash scanner source file (%s)" % e
            return ""
    finally:
        f.close()
    # Normalise spaces/tabs. We don't know what sort of
    # space-tab substitution the file may have been
    # through, so we replace all spans of spaces and
    # tabs by a single space.
    import re
    text = re.sub("[ \t]+", " ", text)
    hash = md5.new(text).hexdigest()
    return hash

def open_pickled_lexicon(expected_hash):
    # Try to open pickled lexicon file and verify that
    # it matches the source file. Returns the opened
    # file if successful, otherwise None. ???
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
                print "Lexicon hash mismatch:" ###
                print "   expected", expected_hash ###
                print "   got     ", actual_hash ###
        except IOError, e:
            print "Warning: Unable to read pickled lexicon", lexicon_pickle
            print e
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
            print "Unpickling lexicon..."
        lexicon = pickle.load(f)
        f.close()
        if notify_lexicon_unpickling:
            t1 = time()
            print "Done (%.2f seconds)" % (t1 - t0)

def create_new_lexicon():
    global lexicon
    t0 = time()
    print "Creating lexicon..."
    lexicon = make_lexicon()
    t1 = time()
    print "Done (%.2f seconds)" % (t1 - t0)

def pickle_lexicon():
    f = None
    try:
        f = open(lexicon_pickle, "wb")
    except IOError:
        print "Warning: Unable to save pickled lexicon in", lexicon_pickle
    if f:
        if notify_lexicon_pickling:
            t0 = time()
            print "Pickling lexicon..."
        pickle.dump(lexicon_hash, f, binary_lexicon_pickle)
        pickle.dump(lexicon, f, binary_lexicon_pickle)
        f.close()
        if notify_lexicon_pickling:
            t1 = time()
            print "Done (%.2f seconds)" % (t1 - t0)

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
    "NULL", "cimport"
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

class PyrexScanner(Scanner):
    
    resword_dict = build_resword_dict()

    def __init__(self, file, filename, parent_scanner = None, 
            type_names = None, context = None):
        Scanner.__init__(self, get_lexicon(), file, filename)
        if parent_scanner:
            self.context = parent_scanner.context
            self.type_names = parent_scanner.type_names
        else:
            self.context = context
            self.type_names = type_names
        self.trace = trace_scanner
        self.indentation_stack = [0]
        self.indentation_char = None
        self.bracket_nesting_level = 0
        self.begin('INDENT')
        self.sy = ''
        self.next()
    
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
                if self.indentation_char <> c:
                    self.error("Mixed use of tabs and spaces")
            if text.replace(c, "") <> "":
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
            if new_level <> self.current_level():
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
        if sy == 'IDENT' and systring in self.resword_dict:
            sy = systring
        self.sy = sy
        self.systring = systring
        if debug_scanner:
            _, line, col = self.position()
            if not self.systring or self.sy == self.systring:
                t = self.sy
            else:
                t = "%s %s" % (self.sy, self.systring)
            print "--- %3d %2d %s" % (line, col, t)
    
    def put_back(self, sy, systring):
        self.unread(self.sy, self.systring)
        self.sy = sy
        self.systring = systring
    
    def unread(self, token, value):
        # This method should be added to Plex
        self.queue.insert(0, (token, value))
    
    def add_type_name(self, name):
        self.type_names[name] = 1
    
    def looking_at_type_name(self):
        return self.sy == 'IDENT' and self.systring in self.type_names
    
    def error(self, message, pos = None):
        if pos is None:
            pos = self.position()
        if self.sy == 'INDENT':
            error(pos, "Possible inconsistent indentation")
        raise error(pos, message)
        
    def expect(self, what, message = None):
        if self.sy == what:
            self.next()
        else:
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

    def expect_newline(self, message):
        # Expect either a newline or end of file
        if self.sy <> 'EOF':
            self.expect('NEWLINE', message)
