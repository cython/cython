#
#   Cython -- Things that don't belong
#            anywhere else in particular
#

import os, sys, re, codecs

def replace_suffix(path, newsuf):
    base, _ = os.path.splitext(path)
    return base + newsuf

def open_new_file(path):
    #  Open and truncate existing file to
    #  preserve metadata on the Mac.
    return open(path, "w+")

def castrate_file(path, st):
    #  Remove junk contents from an output file after a
    #  failed compilation, but preserve metadata on Mac.
    #  Also sets access and modification times back to
    #  those specified by st (a stat struct).
    try:
        f = open(path, "r+")
    except EnvironmentError:
        pass
    else:
        f.seek(0, 0)
        f.truncate()
        f.write(
            "#error Do not use this file, it is the result of a failed Cython compilation.\n")
        f.close()
        if st:
            os.utime(path, (st.st_atime, st.st_mtime-1))

def modification_time(path):
    st = os.stat(path)
    return st.st_mtime

def file_newer_than(path, time):
    ftime = modification_time(path)
    return ftime > time

# support for source file encoding detection and unicode decoding

def encode_filename(filename):
    if isinstance(filename, unicode):
        return filename
    try:
        filename_encoding = sys.getfilesystemencoding()
        if filename_encoding is None:
            filename_encoding = sys.getdefaultencoding()
        filename = filename.decode(filename_encoding)
    except UnicodeDecodeError:
        pass
    return filename

_match_file_encoding = re.compile(u"coding[:=]\s*([-\w.]+)").search

def detect_file_encoding(source_filename):
    # PEPs 263 and 3120
    f = codecs.open(source_filename, "rU", encoding="UTF-8")
    try:
        chars = []
        for i in range(2):
            c = f.read(1)
            while c and c != u'\n':
                chars.append(c)
                c = f.read(1)
            encoding = _match_file_encoding(u''.join(chars))
            if encoding:
                return encoding.group(1)
    finally:
        f.close()
    return "UTF-8"

def open_source_file(source_filename, mode="rU"):
    encoding = detect_file_encoding(source_filename)
    return codecs.open(source_filename, mode=mode, encoding=encoding)

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

#    def __eq__(self, other):
#        return unicode.__eq__(self, other) and \
#            getattr(other, 'encoding', '') == self.encoding

def escape_byte_string(s):
    s = s.replace('\0', r'\x00')
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
            append('\\x%X' % o)
        else:
            append(c)
    return ''.join(l)
