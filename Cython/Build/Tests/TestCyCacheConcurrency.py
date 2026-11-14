from concurrent.futures import ThreadPoolExecutor
import gzip
import multiprocessing
import os
from pathlib import Path
import stat
import tempfile
import threading
import unittest
from unittest import mock
import zipfile

from Cython.Build import Cache as cache_mod
from Cython.Compiler.Main import CompilationResult


STARTUP_TIMEOUT = 60
OPERATION_TIMEOUT = 10


def store_entry(cache_dir, source, header=None):
    result = CompilationResult()
    result.c_file = source
    result.h_file = header
    cache_mod.Cache(cache_dir).store_to_cache(source, 'key', result)


def publish_entries(cache_dir, source, header, start=None):
    os_open = os.open
    threaded = start is None
    if threaded:
        start = threading.Barrier(2)

    def overlapping_temporary(*args, **kwargs):
        fd = os_open(*args, **kwargs)
        try:
            start.wait(STARTUP_TIMEOUT)
            # Neither writer may publish before both have distinct temporary files.
            if len(list(Path(cache_dir).glob('*.tmp'))) != 2:
                raise AssertionError('writers did not create separate temporary files')
            start.wait(STARTUP_TIMEOUT)
        except BaseException:
            os.close(fd)
            raise
        return fd

    with mock.patch.object(cache_mod.os, 'open', overlapping_temporary):
        if threaded:
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(store_entry, cache_dir, source, header) for _ in range(2)]
                for future in futures:
                    future.result(OPERATION_TIMEOUT)
        else:
            store_entry(cache_dir, source, header)


def publish_with_group_permissions(cache_dir, source, header):
    os.umask(0o002)
    store_entry(cache_dir, source, header)


class TestCyCacheConcurrency(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.cache_dir = self.root / 'cache'
        self.source = self.root / 'module.c'
        self.source.write_bytes(b'/* generated source */\n')
        self.header = self.root / 'module.h'
        self.header.write_bytes(b'/* generated header */\n')
        self.cache = cache_mod.Cache(str(self.cache_dir))
        self.context = multiprocessing.get_context('spawn')

    def start_process(self, *args, target=publish_entries):
        process = self.context.Process(target=target, args=args)
        process.start()

        def stop():
            if process.is_alive():
                process.kill()
            process.join(OPERATION_TIMEOUT)
            process.close()

        self.addCleanup(stop)
        return process

    def join_process(self, process):
        process.join(STARTUP_TIMEOUT)
        self.assertFalse(process.is_alive(), 'cache writer did not finish')
        self.assertEqual(process.exitcode, 0)

    def assert_valid_artifact(self, path, zipped):
        if zipped:
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(sorted(archive.namelist()), ['module.c', 'module.h'])
                for artifact in (self.source, self.header):
                    self.assertEqual(archive.read(artifact.name), artifact.read_bytes())
        else:
            with gzip.open(path, 'rb') as artifact:
                self.assertEqual(artifact.read(), self.source.read_bytes())

    def check_publication(self, threaded):
        for zipped in (False, True):
            with self.subTest(zipped=zipped):
                self.cache_dir.rmdir()
                args = (str(self.cache_dir), str(self.source), str(self.header) if zipped else None)
                if threaded:
                    processes = [self.start_process(*args)]
                else:
                    start = self.context.Barrier(2)
                    processes = [self.start_process(*args, start) for _ in range(2)]
                for process in processes:
                    self.join_process(process)
                cached = self.cache.lookup_cache(str(self.source), 'key')
                self.assertIsNotNone(cached)
                self.assert_valid_artifact(cached, zipped)
                self.assertEqual(list(self.cache_dir.iterdir()), [Path(cached)])
                Path(cached).unlink()

    def test_concurrent_processes_publish_complete_artifacts(self):
        self.check_publication(threaded=False)

    def test_concurrent_threads_publish_complete_artifacts(self):
        # A runtime deadlock must not prevent the parent from enforcing a timeout.
        self.check_publication(threaded=True)

    @unittest.skipUnless(os.name == 'posix', 'POSIX file permissions')
    def test_published_entries_preserve_group_permissions(self):
        for zipped in (False, True):
            with self.subTest(zipped=zipped):
                writer = self.start_process(
                    str(self.cache_dir), str(self.source), str(self.header) if zipped else None,
                    target=publish_with_group_permissions)
                self.join_process(writer)
                cached = self.cache.lookup_cache(str(self.source), 'key')
                self.assertEqual(stat.S_IMODE(os.stat(cached).st_mode), 0o664)
                Path(cached).unlink()

    def test_publishes_complete_artifacts_and_preserves_reused_temporary(self):
        rename = os.rename
        reused = []
        for zipped in (False, True):
            with self.subTest(zipped=zipped):
                def publish(temporary, cached):
                    self.assert_valid_artifact(temporary, zipped)
                    rename(temporary, cached)
                    Path(temporary).write_bytes(b'another writer owns this name')
                    reused.append(Path(temporary))

                with mock.patch.object(cache_mod.os, 'rename', publish):
                    store_entry(str(self.cache_dir), str(self.source),
                                str(self.header) if zipped else None)
                self.assertEqual(reused[-1].read_bytes(), b'another writer owns this name')

    def test_temporary_name_collision_preserves_existing_file(self):
        occupied = self.cache_dir / 'occupied.tmp'
        occupied.write_bytes(b'another writer')
        with mock.patch.object(cache_mod.secrets, 'token_hex', side_effect=['occupied', 'available']):
            store_entry(str(self.cache_dir), str(self.source))
        self.assertEqual(occupied.read_bytes(), b'another writer')
        self.assertFalse((self.cache_dir / 'available.tmp').exists())
        cached = self.cache.lookup_cache(str(self.source), 'key')
        self.assert_valid_artifact(cached, zipped=False)

    def test_failed_compression_removes_own_temporary(self):
        for zipped in (False, True):
            with self.subTest(zipped=zipped):
                target, name = (cache_mod.zipfile, 'ZipFile') if zipped else (cache_mod, 'gzip_open')
                with mock.patch.object(target, name, side_effect=OSError('compression failed')):
                    with self.assertRaisesRegex(OSError, 'compression failed'):
                        store_entry(str(self.cache_dir), str(self.source),
                                    str(self.header) if zipped else None)
                self.assertEqual(list(self.cache_dir.iterdir()), [])

    def test_publication_errors_remove_own_temporary(self):
        store_entry(str(self.cache_dir), str(self.source))
        cached = Path(self.cache.lookup_cache(str(self.source), 'key'))
        original = cached.read_bytes()
        for error in (FileExistsError('already published'), PermissionError('rename failed')):
            with self.subTest(error=type(error).__name__):
                with mock.patch.object(cache_mod.os, 'rename', side_effect=error):
                    if isinstance(error, FileExistsError):
                        store_entry(str(self.cache_dir), str(self.source))
                    else:
                        with self.assertRaises(PermissionError):
                            store_entry(str(self.cache_dir), str(self.source))
                self.assertEqual(cached.read_bytes(), original)
                self.assertEqual(list(self.cache_dir.iterdir()), [cached])
