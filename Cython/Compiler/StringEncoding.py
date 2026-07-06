#
#   Cython -- encoding related tools
#

# cython: infer_types=True

import re
import cython

@cython.final
@cython.cclass
class UnicodeLiteralBuilder:
    """Assemble a unicode string.
    """
    _chars: list

    def __init__(self):
        self._chars = []

    @property
    def chars(self) -> list:
        return self._chars

    @cython.ccall
    def append(self, characters):
        assert isinstance(characters, str), f"Expected str, got {type(characters)}"
        self._chars.append(characters)

    @cython.ccall
    def append_charval(self, char_number):
        self._chars.append( chr(char_number) )

    def append_uescape(self, char_number, escape_string):
        self.append_charval(char_number)

    @cython.ccall
    def getstring(self):
        return EncodedString(''.join(self._chars))

    def getstrings(self):
        return (None, self.getstring())


@cython.final
@cython.cclass
class BytesLiteralBuilder:
    """Assemble a byte string or char value.
    """
    _chars: list
    _target_encoding: str

    def __init__(self, target_encoding):
        self._chars = []
        self._target_encoding = target_encoding

    @property
    def chars(self) -> list:
        return self._chars

    @cython.ccall
    def append(self, characters):
        if isinstance(characters, str):
            characters = characters.encode(self._target_encoding)
        assert isinstance(characters, bytes), str(type(characters))
        self._chars.append(characters)

    @cython.ccall
    def append_charval(self, char_number):
        self._chars.append( chr(char_number).encode('ISO-8859-1') )

    def append_uescape(self, char_number, escape_string):
        self.append(escape_string)

    @cython.ccall
    def getstring(self):
        # this *must* return a byte string!
        return bytes_literal(b''.join(self._chars), self._target_encoding)

    def getchar(self):
        # this *must* return a byte string!
        return self.getstring()

    def getstrings(self):
        return (self.getstring(), None)


@cython.final
@cython.cclass
class StrLiteralBuilder:
    """Assemble both a bytes and a unicode representation of a string.
    """
    _bytes: BytesLiteralBuilder
    _unicode: UnicodeLiteralBuilder

    def __init__(self, target_encoding):
        self._bytes   = BytesLiteralBuilder(target_encoding)
        self._unicode = UnicodeLiteralBuilder()

    @cython.ccall
    def append(self, characters):
        self._bytes.append(characters)
        self._unicode.append(characters)

    @cython.ccall
    def append_charval(self, char_number):
        self._bytes.append_charval(char_number)
        self._unicode.append_charval(char_number)

    def append_uescape(self, char_number, escape_string):
        self._bytes.append(escape_string)
        self._unicode.append_charval(char_number)

    def getstrings(self):
        return (self._bytes.getstring(), self._unicode.getstring())


class EncodedString(str):
    # unicode string subclass to keep track of the original encoding.
    # 'encoding' is None for unicode strings and the source encoding
    # otherwise
    encoding = None

    def __deepcopy__(self, memo):
        return self

    def byteencode(self):
        assert self.encoding is not None
        return self.encode(self.encoding)

    def utf8encode(self):
        assert self.encoding is None, self.encoding
        return self.encode("UTF-8")

    @property
    def is_unicode(self):
        return self.encoding is None

    def as_utf8_string(self):
        return bytes_literal(self.utf8encode(), 'utf8')

    def as_c_string_literal(self):
        # first encodes the string then produces a c string literal
        if self.encoding is None:
            s = self.as_utf8_string()
        else:
            s = bytes_literal(self.byteencode(), self.encoding)
        return s.as_c_string_literal()


def string_contains_lone_surrogates(ustring):
    """
    Check if the unicode string contains lone surrogate code points
    on a CPython platform with wide (UCS-4) or narrow (UTF-16)
    Unicode, i.e. characters that would be spelled as two
    separate code units on a narrow platform, but that do not form a pair.
    """
    for c in map(ord, ustring):
        # Surrogates tend to be rare, so we use separate conditions.
        if 0xD800 <= c and c <= 0xDFFF:
            # on 32bit Unicode platforms, there is never a pair
            return True
    return False


class BytesLiteral(bytes):
    # bytes subclass that is compatible with EncodedString
    encoding = None

    def __deepcopy__(self, memo):
        return self

    def byteencode(self):
        return bytes(self)

    def utf8encode(self):
        assert False, f"this is not a unicode string: {self!r}"

    def __str__(self):
        """Fake-decode the byte string to unicode to support %
        formatting of unicode strings.
        """
        return self.decode('ISO-8859-1')

    is_unicode = False

    def as_c_string_literal(self):
        value = split_string_literal(escape_byte_string(self))
        return f'"{value}"'


@cython.ccall
def bytes_literal(s, encoding):
    assert isinstance(s, bytes)
    s = BytesLiteral(s)
    s.encoding = encoding
    return s


@cython.ccall
def encoded_string(s, encoding):
    assert isinstance(s, (str, bytes))
    s = EncodedString(s)
    if encoding is not None:
        s.encoding = encoding
    return s

def encoded_string_or_bytes_literal(s, encoding):
    if isinstance(s, bytes):
        return bytes_literal(s, encoding)
    else:
        return encoded_string(s, encoding)


char_from_escape_sequence = {
    r'\a' : '\a',
    r'\b' : '\b',
    r'\f' : '\f',
    r'\n' : '\n',
    r'\r' : '\r',
    r'\t' : '\t',
    r'\v' : '\v',
    }.get


@cython.cfunc
def _to_escape_sequence(s: str) -> str:
    if s in '\n\r\t':
        return repr(s)[1:-1]
    elif s == '"':
        return r'\"'
    elif s == '\\':
        return r'\\'
    else:
        # within a character sequence, oct passes much better than hex
        return ''.join([f'\\{ord(c):03o}' for c in s])


@cython.cfunc
def _build_specials_replacer():
    subexps = []
    replacements = {}

    _c_special: tuple = ('\\', '??', '"') + tuple(map(chr, range(32)))

    special: str
    for special in _c_special:
        regexp = ''.join(['[%s]' % c.replace('\\', '\\\\') for c in special])
        subexps.append(regexp)
        replacements[special.encode('ASCII')] = _to_escape_sequence(special).encode('ASCII')

    sub = re.compile(('(%s)' % '|'.join(subexps)).encode('ASCII')).sub
    def replace_specials(m):
        return replacements[m.group(1)]
    def replace(s):
        return sub(replace_specials, s)
    return replace

_replace_specials = cython.declare(object, _build_specials_replacer())


def escape_char(char):
    c: cython.Py_UCS4 = char.decode('ISO-8859-1')
    if c in '\n\r\t\\':
        return repr(c)[1:-1]
    elif c == "'":
        return "\\'"
    n = ord(c)
    if n < 32 or n >= 127:
        # hex works well for characters
        return f"\\x{n:02X}"
    else:
        # strictly £, @ and ` (which fall in this list) are only allowed
        # in C23. But practically they're well-supported earlier.
        return c


@cython.ccall
def escape_byte_string(bytestring) -> str:
    """Escape a byte string so that it can be written into C code.
    Note that this returns a Unicode string instead which, when
    encoded as ASCII, will result in the correct byte sequence
    being written.
    """
    s: bytes = _replace_specials(bytestring)
    try:
        return s.decode("ASCII")  #  trial decoding: plain ASCII => done
    except UnicodeDecodeError:
        pass
    s_new = bytearray()
    append, extend = s_new.append, s_new.extend
    for b in s:
        if b >= 127:
            extend(b'\\%03o' % b)
        else:
            append(b)
    return s_new.decode('ASCII')


@cython.ccall
def split_string_literal(s: str, limit: cython.int = 2000) -> str:
    # MSVC can't handle long string literals.
    if len(s) < limit:
        return s
    else:
        start = 0
        chunks = []
        while start < len(s):
            end = start + limit
            if len(s) > end-4 and '\\' in s[end-4:end]:
                end -= 4 - s[end-4:end].find('\\')  # just before the backslash
                while s[end-1] == '\\':
                    end -= 1
                    if end == start:
                        # must have been a long line of backslashes
                        end = start + limit - (limit % 2) - 4
                        break
            chunks.append(s[start:end])
            start = end
        return '""'.join(chunks)


def encode_pyunicode_string(string):
    """Create Py_UNICODE[] representation of a given unicode string.
    """
    utf16 = None  # Start lazy, we won't need it for BMP strings.
    utf32 = []

    characters = cython.cast(str, string)  # was EncodedString or str
    code_point: cython.Py_UCS4

    for code_point in characters:
        charval = ord(code_point)
        ch = f"{charval:d}"
        if code_point >= 0x10000:  # outside of BMP
            if utf16 is None:
                utf16 = utf32[:]
            high, low = divmod(charval - 0x10000, 1024)
            utf16.append(f"{high + 0xD800:d}")
            utf16.append(f"{low + 0xDC00:d}")
        elif utf16 is not None:
            utf16.append(ch)
        utf32.append(ch)

    return (
        ",".join(utf16) if utf16 is not None else "",
        ",".join(utf32),
    )
