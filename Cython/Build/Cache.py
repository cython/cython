import sys
import os
import hashlib
import shutil
import subprocess
from ..Utils import safe_makedirs, cached_function
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
    gzip_ext = '.gz'
except ImportError:
    gzip_open = open
    gzip_ext = ''


join_path = cached_function(os.path.join)

@cached_function
def file_hash(filename):
    path = os.path.normpath(filename)
    prefix = ('%d:%s' % (len(path), path)).encode("UTF-8")
    m = hashlib.sha1(prefix)
    with open(path, 'rb') as f:
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
    if 'CYTHON_CACHE_DIR' in os.environ:
        return os.environ['CYTHON_CACHE_DIR']

    parent = None
    if os.name == 'posix':
        if sys.platform == 'darwin':
            parent = os.path.expanduser('~/Library/Caches')
        else:
            # this could fallback on ~/.cache
            parent = os.environ.get('XDG_CACHE_HOME')

    if parent and os.path.isdir(parent):
        return os.path.join(parent, 'cython')

    # last fallback: ~/.cython
    return os.path.expanduser(os.path.join('~', '.cython'))


class Cache:

    def __init__(self, cache, cache_size=None):
        if cache is True:
            self.enabled = True
            self.path = os.path.join(get_cython_cache_dir(), 'compiler')
        elif cache:
            self.path = cache
            self.enabled = True
        else:
            self.path = None
            self.enabled = False
        self.cache_size = cache_size if cache_size is not None else 1024 * 1024 * 100
        if self.enabled:
            if not os.path.exists(self.path):
                os.makedirs(self.path)

    def transitive_fingerprint(self, filename, dependencies, compilation_options, language, py_limited_api=False, np_pythran=False):
        r"""
        Return a fingerprint of a cython file that is about to be cythonized.

        Fingerprints are looked up in future compilations. If the fingerprint
        is found, the cythonization can be skipped. The fingerprint must
        incorporate everything that has an influence on the generated code.
        """
        try:
            m = hashlib.sha1(__version__.encode('UTF-8'))
            m.update(file_hash(filename).encode('UTF-8'))
            for x in sorted(dependencies.all_dependencies(filename)):
                if os.path.splitext(x)[1] not in ('.c', '.cpp', '.h'):
                    m.update(file_hash(x).encode('UTF-8'))
            # Include the module attributes that change the compilation result
            # in the fingerprint. We do not iterate over module.__dict__ and
            # include almost everything here as users might extend Extension
            # with arbitrary (random) attributes that would lead to cache
            # misses.
            m.update(
                str((language, py_limited_api,np_pythran)).encode('UTF-8')
            )
            m.update(compilation_options.get_fingerprint().encode('UTF-8'))
            return m.hexdigest()
        except OSError:
            return None

    def fingerprint_file_base(self, cfile, fingerprint):
        return join_path(self.path, "%s-%s" % (os.path.basename(cfile), fingerprint))

    def gz_fingerprint_file(self, cfile, fingerprint):
        return self.fingerprint_file_base(cfile, fingerprint) + gzip_ext


    def zip_fingerprint_file(self, cfile, fingerprint):
        return self.fingerprint_file_base(cfile, fingerprint) + '.zip'

    def lookup_cache(self, c_file, fingerprint):
        # Cython-generated c files are highly compressible.
        # (E.g. a compression ratio of about 10 for Sage).
        if not os.path.exists(self.path):
            safe_makedirs(self.path)
        gz_fingerprint_file = self.gz_fingerprint_file(c_file, fingerprint)
        zip_fingerprint_file = self.zip_fingerprint_file(c_file, fingerprint)
        if os.path.exists(gz_fingerprint_file) or os.path.exists(zip_fingerprint_file):
            if os.path.exists(gz_fingerprint_file):
                os.utime(gz_fingerprint_file, None)
                with gzip_open(gz_fingerprint_file, 'rb') as g:
                    with open(c_file, 'wb') as f:
                        shutil.copyfileobj(g, f)
            else:
                os.utime(zip_fingerprint_file, None)
                dirname = os.path.dirname(c_file)
                with zipfile.ZipFile(zip_fingerprint_file) as z:
                    for artifact in z.namelist():
                        z.extract(artifact, os.path.join(dirname, artifact))
            return True
        return False


    def store_to_cache(self, fingerprint, c_file, compilation_result):
        artifacts = list(filter(None, [
            getattr(compilation_result, attr, None)
            for attr in ('c_file', 'h_file', 'api_file', 'i_file')]))
        if len(artifacts) == 1:
            fingerprint_file = self.gz_fingerprint_file(c_file, fingerprint)
            with open(c_file, 'rb') as f:
                with gzip_open(fingerprint_file + '.tmp', 'wb') as g:
                    shutil.copyfileobj(f, g)
        else:
            fingerprint_file = self.zip_fingerprint_file(c_file, fingerprint)
            with zipfile.ZipFile(
                    fingerprint_file + '.tmp', 'w', zipfile_compression_mode) as zip:
                for artifact in artifacts:
                    zip.write(artifact, os.path.basename(artifact))
        os.rename(fingerprint_file + '.tmp', fingerprint_file)


    def cleanup_cache(self, ratio=.85):
        try:
            p = subprocess.Popen(['du', '-s', '-k', os.path.abspath(self.path)], stdout=subprocess.PIPE)
            stdout, _ = p.communicate()
            res = p.wait()
            if res == 0:
                total_size = 1024 * int(stdout.strip().split()[0])
                if total_size < self.cache_size:
                    return
        except (OSError, ValueError):
            pass
        total_size = 0
        all = []
        for file in os.listdir(self.path):
            path = join_path(self.path, file)
            s = os.stat(path)
            total_size += s.st_size
            all.append((s.st_atime, s.st_size, path))
        if total_size > self.cache_size:
            for time, size, file in reversed(sorted(all)):
                os.unlink(file)
                total_size -= size
                if total_size < self.cache_size * ratio:
                    break
