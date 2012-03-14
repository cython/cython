#
#   Cython -- Things that don't belong
#            anywhere else in particular
#

import os, sys, re, codecs

modification_time = os.path.getmtime

def replace_suffix(path, newsuf):
    base, _ = os.path.splitext(path)
    return base + newsuf

def open_new_file(path):
    if os.path.exists(path):
        # Make sure to create a new file here so we can
        # safely hard link the output files.
        os.unlink(path)

    # we use the ISO-8859-1 encoding here because we only write pure
    # ASCII strings or (e.g. for file names) byte encoded strings as
    # Unicode, so we need a direct mapping from the first 256 Unicode
    # characters to a byte sequence, which ISO-8859-1 provides
    return codecs.open(path, "w", encoding="ISO-8859-1")

def castrate_file(path, st):
    #  Remove junk contents from an output file after a
    #  failed compilation.
    #  Also sets access and modification times back to
    #  those specified by st (a stat struct).
    try:
        f = open_new_file(path)
    except EnvironmentError:
        pass
    else:
        f.write(
            "#error Do not use this file, it is the result of a failed Cython compilation.\n")
        f.close()
        if st:
            os.utime(path, (st.st_atime, st.st_mtime-1))

def file_newer_than(path, time):
    ftime = modification_time(path)
    return ftime > time

def path_exists(path):
    # try on the filesystem first
    if os.path.exists(path):
        return True
    # figure out if a PEP 302 loader is around
    try:
        loader = __loader__
        # XXX the code below assumes as 'zipimport.zipimporter' instance
        # XXX should be easy to generalize, but too lazy right now to write it
        if path.startswith(loader.archive):
            nrmpath = os.path.normpath(path)
            arcname = nrmpath[len(loader.archive)+1:]
            try:
                loader.get_data(arcname)
                return True
            except IOError:
                return False
    except NameError:
        pass
    return False

# file name encodings

def decode_filename(filename):
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

# support for source file encoding detection

_match_file_encoding = re.compile(u"coding[:=]\s*([-\w.]+)").search

def detect_file_encoding(source_filename):
    # PEPs 263 and 3120
    f = open_source_file(source_filename, encoding="UTF-8", error_handling='ignore')
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

normalise_newlines = re.compile(u'\r\n?|\n').sub

class NormalisedNewlineStream(object):
  """The codecs module doesn't provide universal newline support.
  This class is used as a stream wrapper that provides this
  functionality.  The new 'io' in Py2.6+/3.x supports this out of the
  box.
  """
  def __init__(self, stream):
    # let's assume .read() doesn't change
    self._read = stream.read
    self.close = stream.close
    self.encoding = getattr(stream, 'encoding', 'UTF-8')

  def read(self, count=-1):
    data = self._read(count)
    if u'\r' not in data:
      return data
    if data.endswith(u'\r'):
      # may be missing a '\n'
      data += self._read(1)
    return normalise_newlines(u'\n', data)

  def readlines(self):
    content = []
    data = self.read(0x1000)
    while data:
        content.append(data)
        data = self.read(0x1000)

    return u''.join(content).splitlines(True)

io = None
if sys.version_info >= (2,6):
    try:
        import io
    except ImportError:
        pass

def open_source_file(source_filename, mode="r",
                     encoding=None, error_handling=None,
                     require_normalised_newlines=True):
    if encoding is None:
        encoding = detect_file_encoding(source_filename)
    #
    try:
        loader = __loader__
        if source_filename.startswith(loader.archive):
            return open_source_from_loader(
                loader, source_filename,
                encoding, error_handling,
                require_normalised_newlines)
    except (NameError, AttributeError):
        pass
    #
    if io is not None:
        return io.open(source_filename, mode=mode,
                       encoding=encoding, errors=error_handling)
    else:
        # codecs module doesn't have universal newline support
        stream = codecs.open(source_filename, mode=mode,
                             encoding=encoding, errors=error_handling)
        if require_normalised_newlines:
            stream = NormalisedNewlineStream(stream)
        return stream

def open_source_from_loader(loader,
                            source_filename,
                            encoding=None, error_handling=None,
                            require_normalised_newlines=True):
    nrmpath = os.path.normpath(source_filename)
    arcname = nrmpath[len(loader.archive)+1:]
    data = loader.get_data(arcname)
    if io is not None:
        return io.TextIOWrapper(io.BytesIO(data),
                                encoding=encoding,
                                errors=error_handling)
    else:
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO
        reader = codecs.getreader(encoding)
        stream = reader(StringIO.StringIO(data))
        if require_normalised_newlines:
            stream = NormalisedNewlineStream(stream)
        return stream

def str_to_number(value):
    # note: this expects a string as input that was accepted by the
    # parser already
    if len(value) < 2:
        value = int(value, 0)
    elif value[0] == '0':
        if value[1] in 'xX':
            # hex notation ('0x1AF')
            value = int(value[2:], 16)
        elif value[1] in 'oO':
            # Py3 octal notation ('0o136')
            value = int(value[2:], 8)
        elif value[1] in 'bB':
            # Py3 binary notation ('0b101')
            value = int(value[2:], 2)
        else:
            # Py2 octal notation ('0136')
            value = int(value, 8)
    else:
        value = int(value, 0)
    return value

def long_literal(value):
    if isinstance(value, basestring):
        value = str_to_number(value)
    return not -2**31 <= value < 2**31

# all() and any() are new in 2.5
try:
    # Make sure to bind them on the module, as they will be accessed as
    # attributes
    all = all
    any = any
except NameError:
    def all(items):
        for item in items:
            if not item:
                return False
        return True

    def any(items):
        for item in items:
            if item:
                return True
        return False
