from contextlib import contextmanager
from dataclasses import dataclass
import sys
import os
import hashlib
import operator
import shutil
import tempfile
import zipfile

from ..Utils import cached_function
from .. import __version__

if os.name == "posix":
    import fcntl
elif os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes

try:
    import zlib

    zipfile_compression_mode = zipfile.ZIP_DEFLATED
except ImportError:
    zipfile_compression_mode = zipfile.ZIP_STORED

try:
    import gzip

    gzip_open = gzip.open
    gzip_ext = ".gz"
except ImportError:
    gzip_open = open
    gzip_ext = ""

zip_ext = ".zip"

MAX_CACHE_SIZE = 1024 * 1024 * 100
DEFAULT_DELETE_RATIO = 0.85

join_path = cached_function(os.path.join)



class CacheUnavailable(Exception):
    """An optional cache operation could not be completed."""


if os.name == "nt":
    class _OVERLAPPED(ctypes.Structure):
        _fields_ = [
            ("Internal", ctypes.c_size_t),
            ("InternalHigh", ctypes.c_size_t),
            ("Offset", wintypes.DWORD),
            ("OffsetHigh", wintypes.DWORD),
            ("hEvent", wintypes.HANDLE),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _kernel32.LockFileEx.argtypes = (
        wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
        wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(_OVERLAPPED),
    )
    _kernel32.LockFileEx.restype = wintypes.BOOL
    _kernel32.UnlockFileEx.argtypes = (
        wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
        wintypes.DWORD, ctypes.POINTER(_OVERLAPPED),
    )
    _kernel32.UnlockFileEx.restype = wintypes.BOOL
    _LOCKFILE_EXCLUSIVE_LOCK = 0x00000002


@contextmanager
def _file_lock(path, exclusive):
    # Persistent metadata keeps the lock valid when the artifact is replaced.
    try:
        lock_file = open(path, "a+b")
    except OSError as exc:
        raise CacheUnavailable() from exc

    overlapped = None
    try:
        if os.name == "posix":
            fcntl.flock(
                lock_file.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            )
        elif os.name == "nt":
            overlapped = _OVERLAPPED()
            handle = msvcrt.get_osfhandle(lock_file.fileno())
            flags = _LOCKFILE_EXCLUSIVE_LOCK if exclusive else 0
            if not _kernel32.LockFileEx(handle, flags, 0, 1, 0, ctypes.byref(overlapped)):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            raise CacheUnavailable()
    except (OSError, CacheUnavailable) as exc:
        try:
            lock_file.close()
        except OSError:
            pass
        raise CacheUnavailable() from exc

    try:
        yield
    finally:
        try:
            if os.name == "posix":
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            else:
                _kernel32.UnlockFileEx(handle, 0, 1, 0, ctypes.byref(overlapped))
        except OSError:
            pass
        finally:
            try:
                lock_file.close()
            except OSError:
                pass


_cache_read_errors = (OSError, EOFError, zipfile.BadZipFile)
if zipfile_compression_mode == zipfile.ZIP_DEFLATED:
    _cache_read_errors += (zlib.error,)


@contextmanager
def _cache_file(opener, *args):
    try:
        source = opener(*args)
    except _cache_read_errors as exc:
        raise CacheUnavailable() from exc
    try:
        yield source
    finally:
        try:
            source.close()
        except OSError:
            pass


def _copy_from_cache(source, output):
    while True:
        try:
            data = source.read(131072)
        except _cache_read_errors as exc:
            raise CacheUnavailable() from exc
        if not data:
            return
        # Output failures must retain their normal compilation-error semantics.
        output.write(data)


@cached_function
def file_hash(filename):
    path = os.path.normpath(filename)
    prefix = ("%d:%s" % (len(path), path)).encode("UTF-8")
    m = hashlib.sha256(prefix)
    with open(path, "rb") as f:
        data = f.read(65000)
        while data:
            m.update(data)
            data = f.read(65000)
    return m.hexdigest()


@cached_function
def get_cython_cache_dir():
    r"""
    Return the base directory containing Cython's caches.

    Priority:

    1. CYTHON_CACHE_DIR
    2. (OS X): ~/Library/Caches/Cython
       (posix not OS X): XDG_CACHE_HOME/cython if XDG_CACHE_HOME defined
    3. ~/.cython

    """
    if "CYTHON_CACHE_DIR" in os.environ:
        return os.environ["CYTHON_CACHE_DIR"]

    parent = None
    if os.name == "posix":
        if sys.platform == "darwin":
            parent = os.path.expanduser("~/Library/Caches")
        else:
            # this could fallback on ~/.cache
            parent = os.environ.get("XDG_CACHE_HOME")

    if parent and os.path.isdir(parent):
        return join_path(parent, "cython")

    # last fallback: ~/.cython
    return os.path.expanduser(join_path("~", ".cython"))


@dataclass
class FingerprintFlags:
    language: str = "c"
    py_limited_api: bool = False
    np_pythran: bool = False

    def get_fingerprint(self):
        return str((self.language, self.py_limited_api, self.np_pythran))


class Cache:
    _lock_directory = ".locks"
    _lifecycle_lock_name = "lifecycle.lock"

    def __init__(self, path, cache_size=None):
        if path is None:
            self.path = join_path(get_cython_cache_dir(), "compiler")
        else:
            self.path = path
        self.cache_size = cache_size if cache_size is not None else MAX_CACHE_SIZE
        self.enabled = True
        try:
            os.makedirs(self.path, exist_ok=True)
        except OSError:
            self.enabled = False

    def transitive_fingerprint(
        self, filename, dependencies, compilation_options, flags=FingerprintFlags()
    ):
        r"""
        Return a fingerprint of a cython file that is about to be cythonized.

        Fingerprints are looked up in future compilations. If the fingerprint
        is found, the cythonization can be skipped. The fingerprint must
        incorporate everything that has an influence on the generated code.
        """
        try:
            m = hashlib.sha256(__version__.encode("UTF-8"))
            m.update(file_hash(filename).encode("UTF-8"))
            for x in sorted(dependencies):
                if os.path.splitext(x)[1] not in (".c", ".cpp", ".h"):
                    m.update(file_hash(x).encode("UTF-8"))
            # Include the module attributes that change the compilation result
            # in the fingerprint. We do not iterate over module.__dict__ and
            # include almost everything here as users might extend Extension
            # with arbitrary (random) attributes that would lead to cache
            # misses.
            m.update(flags.get_fingerprint().encode("UTF-8"))
            m.update(compilation_options.get_fingerprint().encode("UTF-8"))
            return m.hexdigest()
        except OSError:
            return None

    def fingerprint_file(self, cfile, fingerprint, ext):
        return (
            join_path(self.path, "%s-%s" % (os.path.basename(cfile), fingerprint)) + ext
        )

    def _lock_path(self, name):
        if not self.enabled:
            raise CacheUnavailable()
        directory = join_path(self.path, self._lock_directory)
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            raise CacheUnavailable() from exc
        return join_path(directory, name)

    def _entry_lock_name(self, cache_file):
        # The same entry must use the same lock through relative paths or aliases.
        name = os.path.normcase(os.path.basename(cache_file))
        return hashlib.sha256(os.fsencode(name)).hexdigest() + ".lock"

    @contextmanager
    def _lifecycle_lock(self, exclusive):
        with _file_lock(self._lock_path(self._lifecycle_lock_name), exclusive):
            yield

    @contextmanager
    def _entry_lock(self, cache_file, exclusive):
        with _file_lock(self._lock_path(self._entry_lock_name(cache_file)), exclusive):
            yield

    def lookup_cache(self, c_file, fingerprint):
        """Look up a file in the cache and update its access/modification time.

        Return the compressed file path of the cached file.
        """
        try:
            with self._lifecycle_lock(False):
                for extension in (gzip_ext, zip_ext):
                    cached = self.fingerprint_file(c_file, fingerprint, extension)
                    try:
                        os.utime(cached, None)
                    except FileNotFoundError:
                        continue
                    return cached
        except (CacheUnavailable, OSError):
            pass
        return None

    def load_from_cache(self, c_file, cached):
        with self._lifecycle_lock(False):
            with self._entry_lock(cached, False):
                try:
                    os.utime(cached, None)
                except OSError as exc:
                    raise CacheUnavailable() from exc

                ext = os.path.splitext(cached)[1]
                if ext == gzip_ext:
                    with _cache_file(gzip_open, cached, "rb") as source:
                        with open(c_file, "wb") as output:
                            _copy_from_cache(source, output)
                elif ext == zip_ext:
                    dirname = os.path.dirname(c_file)
                    with _cache_file(zipfile.ZipFile, cached) as archive:
                        if dirname:
                            os.makedirs(dirname, exist_ok=True)
                        for artifact in archive.namelist():
                            # Cython stores only basenames; other paths indicate
                            # an invalid artifact rather than generated output.
                            if artifact != os.path.basename(artifact):
                                raise CacheUnavailable()
                            with _cache_file(archive.open, artifact) as source:
                                with open(join_path(dirname, artifact), "wb") as output:
                                    _copy_from_cache(source, output)
                else:
                    raise ValueError(f"Unsupported cache file extension: {ext}")

    def _temporary_file(self, cache_file):
        return tempfile.mkstemp(
            prefix=os.path.basename(cache_file) + ".",
            suffix=".tmp",
            dir=self.path,
        )

    def store_to_cache(self, c_file, fingerprint, compilation_result):
        artifacts = compilation_result.get_generated_source_files()
        extension = gzip_ext if len(artifacts) == 1 else zip_ext
        cache_file = self.fingerprint_file(c_file, fingerprint, extension)
        try:
            with self._lifecycle_lock(False):
                with self._entry_lock(cache_file, True):
                    if os.path.exists(cache_file):
                        return
                    temporary_file = None
                    try:
                        fd, temporary_file = self._temporary_file(cache_file)
                        os.close(fd)
                        if len(artifacts) == 1:
                            with open(c_file, "rb") as source:
                                with gzip_open(temporary_file, "wb") as output:
                                    shutil.copyfileobj(source, output)
                        else:
                            with zipfile.ZipFile(
                                temporary_file, "w", zipfile_compression_mode
                            ) as archive:
                                for artifact in artifacts:
                                    archive.write(artifact, os.path.basename(artifact))
                        os.replace(temporary_file, cache_file)
                        temporary_file = None
                    finally:
                        if temporary_file is not None:
                            try:
                                os.unlink(temporary_file)
                            except OSError:
                                pass
        except (CacheUnavailable, OSError):
            # Generated output remains valid even when its cache cannot be written.
            pass

    def _list_cache_files(self):
        total_size = 0
        cache_files = []
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.name == self._lock_directory or entry.name.endswith('.tmp'):
                    continue
                try:
                    stat = entry.stat(follow_symlinks=False)
                except OSError:
                    # Cache maintenance is optional even on stale network mounts.
                    continue

                file_size = stat.st_size
                total_size += file_size
                cache_files.append((entry.path, file_size, stat.st_atime))

        return total_size, cache_files

    def _sort_files_by_atime(self, cache_files):
        cache_files.sort(key=operator.itemgetter(2, 1))

    def _delete_cache_files(self, files_to_delete, total_size, max_cache_size):
        for file_path, size, _ in files_to_delete:
            if total_size < max_cache_size:
                return
            try:
                os.unlink(file_path)
                total_size -= size
            except FileNotFoundError:
                # Concurrently deleted. Nothing left to delete for us.
                total_size -= size
            except OSError:
                # Concurrent access on Windows? Keep the file, cannot delete it right now.
                pass

    def _delete_stale_temporary_files(self):
        # Lifecycle is exclusive, so no cooperating writer can own these files.
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.name.endswith(".tmp"):
                    try:
                        os.unlink(entry.path)
                    except OSError:
                        pass

    def _cleanup_orphan_locks(self):
        live_locks = set()
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.name == self._lock_directory:
                    continue
                name = entry.name
                live_locks.add(self._entry_lock_name(name))
                if name.endswith(".tmp"):
                    # Retain locks for temporary files whose removal failed.
                    name = name[:-4]
                    live_locks.add(self._entry_lock_name(name))
                    live_locks.add(self._entry_lock_name(name.rsplit(".", 1)[0]))

        with os.scandir(join_path(self.path, self._lock_directory)) as entries:
            for entry in entries:
                if (entry.name != self._lifecycle_lock_name
                        and entry.name.endswith(".lock")
                        and entry.name not in live_locks):
                    try:
                        os.unlink(entry.path)
                    except OSError:
                        pass

    def cleanup_cache(self, ratio=DEFAULT_DELETE_RATIO):
        """Reduce the total file size in the cache to ratio*cache_size
        by evicting the least recently accessed entries.
        """
        try:
            with self._lifecycle_lock(True):
                self._delete_stale_temporary_files()
                total_size, cache_files = self._list_cache_files()

                if total_size > self.cache_size:
                    self._sort_files_by_atime(cache_files)
                    max_cache_size = int(self.cache_size * ratio)
                    self._delete_cache_files(cache_files, total_size, max_cache_size)

                self._cleanup_orphan_locks()
        except (CacheUnavailable, OSError):
            pass
