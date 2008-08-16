#
#   Cython -- encoding related tools
#

import re

class UnicodeLiteralBuilder(object):
    """Assemble a unicode string.
    """
    def __init__(self):
        self.chars = []

    def append(self, characters):
        if isinstance(characters, str):
            # this came from a Py2 string literal in the parser code
            characters = characters.decode("ASCII")
        assert isinstance(characters, unicode), str(type(characters))
        self.chars.append(characters)

    def append_charval(self, char_number):
        self.chars.append( unichr(char_number) )

    def getstring(self):
        return EncodedString(u''.join(self.chars))


class BytesLiteralBuilder(object):
    """Assemble a byte string or char value.
    """
    def __init__(self, target_encoding):
        self.chars = []
        self.target_encoding = target_encoding

    def append(self, characters):
        if isinstance(characters, unicode):
            characters = characters.encode(self.target_encoding)
        assert isinstance(characters, str), str(type(characters))
        self.chars.append(characters)

    def append_charval(self, char_number):
        self.chars.append( chr(char_number) )

    def getstring(self):
        # this *must* return a byte string! => fix it in Py3k!!
        s = BytesLiteral(''.join(self.chars))
        s.encoding = self.target_encoding
        return s

    def getchar(self):
        # this *must* return a byte string! => fix it in Py3k!!
        return self.getstring()

class EncodedString(unicode):
    # unicode string subclass to keep track of the original encoding.
    # 'encoding' is None for unicode strings and the source encoding
    # otherwise
    encoding = None

    def byteencode(self):
        assert self.encoding is not None
        return self.encode(self.encoding)

    def utf8encode(self):
        assert self.encoding is None
        return self.encode("UTF-8")

    def is_unicode(self):
        return self.encoding is None
    is_unicode = property(is_unicode)

class BytesLiteral(str):
    # str subclass that is compatible with EncodedString
    encoding = None

    def byteencode(self):
        return str(self)

    def utf8encode(self):
        assert False, "this is not a unicode string: %r" % self

    is_unicode = False

char_from_escape_sequence = {
    r'\a' : u'\a',
    r'\b' : u'\b',
    r'\f' : u'\f',
    r'\n' : u'\n',
    r'\r' : u'\r',
    r'\t' : u'\t',
    r'\v' : u'\v',
    }.get

def _to_escape_sequence(s):
    if s in '\n\r\t':
        return repr(s)[1:-1]
    elif s == '"':
        return r'\"'
    else:
        # within a character sequence, oct passes much better than hex
        return ''.join(['\\%03o' % ord(c) for c in s])

_c_special = ('\0', '\n', '\r', '\t', '??', '"')
_c_special_replacements = zip(_c_special, map(_to_escape_sequence, _c_special))

def _build_specials_test():
    subexps = []
    for special in _c_special:
        regexp = ''.join(['[%s]' % c for c in special])
        subexps.append(regexp)
    return re.compile('|'.join(subexps)).search

_has_specials = _build_specials_test()

def escape_character(c):
    if c in '\n\r\t\\':
        return repr(c)[1:-1]
    elif c == "'":
        return "\\'"
    n = ord(c)
    if n < 32 or n > 127:
        # hex works well for characters
        return "\\x%02X" % n
    else:
        return c

def escape_byte_string(s):
    s = s.replace('\\', '\\\\')
    if _has_specials(s):
        for special, replacement in _c_special_replacements:
            s = s.replace(special, replacement)
    try:
        s.decode("ASCII")
        return s
    except UnicodeDecodeError:
        pass
    l = []
    append = l.append
    for c in s:
        o = ord(c)
        if o >= 128:
            append('\\%3o' % o)
        else:
            append(c)
    return ''.join(l)

def split_docstring(s):
    if len(s) < 2047:
        return s
    return '\\n\"\"'.join(s.split(r'\n'))
