from dataclasses import dataclass
import sys
import os
import time
import hashlib
import shutil
import subprocess
from ..Utils import cached_function
import zipfile
from .. import __version__

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
# In-progress writes use "<entry>.tmp". Size eviction leaves those names
# alone. A temp left by a dead writer is removed only after this age.
_STALE_CACHE_TEMP_SECONDS = 24 * 60 * 60

join_path = cached_function(os.path.join)


def _unlink_cache_file(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


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
    def __init__(self, path, cache_size=None):
        if path is None:
            self.path = join_path(get_cython_cache_dir(), "compiler")
        else:
            self.path = path
        self.cache_size = cache_size if cache_size is not None else MAX_CACHE_SIZE
        # Make sure the cache directory exists (and allow for concurrent creation).
        os.makedirs(self.path, exist_ok=True)

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

    def lookup_cache(self, c_file, fingerprint):
        # Cython-generated c files are highly compressible.
        # (E.g. a compression ratio of about 10 for Sage).
        os.makedirs(self.path, exist_ok=True)
        gz_fingerprint_file = self.fingerprint_file(c_file, fingerprint, gzip_ext)
        if os.path.exists(gz_fingerprint_file):
            return gz_fingerprint_file
        zip_fingerprint_file = self.fingerprint_file(c_file, fingerprint, zip_ext)
        if os.path.exists(zip_fingerprint_file):
            return zip_fingerprint_file
        return None

    def load_from_cache(self, c_file, cached):
        ext = os.path.splitext(cached)[1]
        if ext == gzip_ext:
            os.utime(cached, None)
            with gzip_open(cached, "rb") as g:
                with open(c_file, "wb") as f:
                    shutil.copyfileobj(g, f)
        elif ext == zip_ext:
            os.utime(cached, None)
            dirname = os.path.dirname(c_file)
            with zipfile.ZipFile(cached) as z:
                for artifact in z.namelist():
                    z.extract(artifact, dirname)
        else:
            raise ValueError(f"Unsupported cache file extension: {ext}")

    def store_to_cache(self, c_file, fingerprint, compilation_result):
        artifacts = compilation_result.get_generated_source_files()
        if len(artifacts) == 1:
            fingerprint_file = self.fingerprint_file(c_file, fingerprint, gzip_ext)
            with open(c_file, "rb") as f:
                with gzip_open(fingerprint_file + ".tmp", "wb") as g:
                    shutil.copyfileobj(f, g)
        else:
            fingerprint_file = self.fingerprint_file(c_file, fingerprint, zip_ext)
            with zipfile.ZipFile(
                fingerprint_file + ".tmp", "w", zipfile_compression_mode
            ) as zip:
                for artifact in artifacts:
                    zip.write(artifact, os.path.basename(artifact))
        os.rename(fingerprint_file + ".tmp", fingerprint_file)

    def cleanup_cache(self, ratio=0.85):
        try:
            completed_process = subprocess.run(
                ["du", "-s", "-k", os.path.abspath(self.path)], stdout=subprocess.PIPE
            )
            stdout = completed_process.stdout
            if completed_process.returncode == 0:
                total_size = 1024 * int(stdout.strip().split()[0])
                if total_size < self.cache_size:
                    return
        except (OSError, ValueError):
            pass
        total_size = 0
        all = []
        now = time.time()
        for file in os.listdir(self.path):
            path = join_path(self.path, file)
            try:
                s = os.stat(path)
            except FileNotFoundError:
                continue
            if file.endswith(".tmp"):
                if now - s.st_mtime >= _STALE_CACHE_TEMP_SECONDS:
                    _unlink_cache_file(path)
                continue
            total_size += s.st_size
            all.append((s.st_atime, s.st_size, path))
        if total_size > self.cache_size:
            for _atime, size, file in reversed(sorted(all)):
                _unlink_cache_file(file)
                total_size -= size
                if total_size < self.cache_size * ratio:
                    break
