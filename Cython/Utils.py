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

# support for source file encoding detection

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

def long_literal(value):
    if isinstance(value, basestring):
        if len(value) < 2:
            value = int(value)
        elif value[0] == 0:
            value = int(value, 8)
        elif value[1] in 'xX':
            value = int(value[2:], 16)
        else:
            value = int(value)
    return not -2**31 <= value < 2**31

# a simple class that simplifies the usage of utility code

class UtilityCode(object):
    def __init__(self, proto=None, impl=None, init=None, cleanup=None):
        self.proto = proto
        self.impl = impl
        self.init = init
        self.cleanup = cleanup

    def write_init_code(self, writer, pos):
        if not self.init:
            return
        if callable(self.init):
            self.init(writer, pos)
        else:
            writer.put(self.init)

    def write_cleanup_code(self, writer, pos):
        if not self.cleanup:
            return
        if callable(self.cleanup):
            self.cleanup(writer, pos)
        else:
            writer.put(self.cleanup)
