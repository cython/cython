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
        #st = os.stat(path)
        f.seek(0, 0)
        f.truncate()
        f.write(
            "#error Do not use this file, it is the result of a failed Pyrex compilation.\n")
        f.close()
        if st:
            os.utime(path, (st.st_atime, st.st_mtime))

# support for source file encoding detection and unicode decoding

_match_file_encoding = re.compile(u"coding[:=]\s*([-\w.]+)").search

def detect_file_encoding(source_filename):
    # PEPs 263 and 3120
    f = codecs.open(source_filename, "rU", encoding="UTF-8")
    try:
        for line_no, line in enumerate(f):
            encoding = _match_file_encoding(line)
            if encoding:
                return encoding.group(1)
            if line_no == 1:
                break
    finally:
        f.close()
    return "UTF-8"

def open_source_file(source_filename, mode="rU"):
    encoding = detect_file_encoding(source_filename)
    return codecs.open(source_filename, mode=mode, encoding=encoding)
