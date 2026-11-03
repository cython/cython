from contextlib import contextmanager
import errno
import gzip
import multiprocessing
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import unittest
from unittest import mock
import zipfile

from Cython.Build import Cache as cache_mod
from Cython.Compiler import Main


class GeneratedSources:
    def __init__(self, *files):
        self.files = files

    def get_generated_source_files(self):
        return self.files


def store_entry(cache_dir, source, start, results):
    try:
        if not start.wait(10):
            raise TimeoutError('writers did not start')
        cache_mod.Cache(cache_dir).store_to_cache(
            source, 'key', GeneratedSources(source))
        results.put(None)
    except Exception as exc:
        results.put(repr(exc))


def paused_cache_io(cache_dir, source, output, mode, ready, release, results):
    real_open = cache_mod.gzip_open

    def paused_open(path, file_mode):
        handle = real_open(path, file_mode)
        ready.set()
        if not release.wait(30):
            handle.close()
            raise TimeoutError('cache operation was not released')
        return handle

    try:
        cache = cache_mod.Cache(cache_dir)
        with mock.patch.object(cache_mod, 'gzip_open', paused_open):
            if mode == 'write':
                cache.store_to_cache(source, 'key', GeneratedSources(source))
            else:
                cached = cache.fingerprint_file(source, 'key', cache_mod.gzip_ext)
                cache.load_from_cache(output, cached)
        results.put(None)
    except Exception as exc:
        results.put(repr(exc))


def cleanup_entry(cache_dir, attempted, completed):
    real_lock = cache_mod._file_lock

    @contextmanager
    def tracked_lock(path, exclusive, blocking=True):
        if exclusive and os.path.basename(path) == cache_mod.Cache._lifecycle_lock_name:
            attempted.set()
        with real_lock(path, exclusive, blocking) as lock_file:
            yield lock_file

    with mock.patch.object(cache_mod, '_file_lock', tracked_lock):
        cache_mod.Cache(cache_dir).cleanup_cache()
    completed.set()


def abandon_temporary_file(cache_dir, source):
    cache = cache_mod.Cache(cache_dir)
    cached = cache.fingerprint_file(source, 'key', cache_mod.gzip_ext)
    with cache._lifecycle_lock(False):
        with cache._entry_lock(cached, True):
            fd, _ = cache._temporary_file()
            os.write(fd, b'abandoned temporary artifact')
            os.close(fd)
            # Termination must release OS locks without running Python cleanup.
            os._exit(0)


class TestCyCacheConcurrency(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache_dir = self.root / 'cache'
        self.cache = cache_mod.Cache(str(self.cache_dir), cache_size=5000)
        self.source = self.root / 'module.c'
        self.source.write_bytes(b'/* generated source */\n')
        self.context = multiprocessing.get_context('spawn')

    def store(self, *artifacts):
        artifacts = artifacts or (str(self.source),)
        self.cache.store_to_cache(str(self.source), 'key', GeneratedSources(*artifacts))
        return self.cache.lookup_cache(str(self.source), 'key')

    def start_process(self, target, *args):
        process = self.context.Process(target=target, args=args)
        process.start()

        def stop():
            if process.is_alive():
                process.terminate()
            process.join(10)

        self.addCleanup(stop)
        return process

    def join_process(self, process):
        process.join(10)
        self.assertFalse(process.is_alive(), 'cache process did not finish')
        self.assertEqual(process.exitcode, 0)

    def test_concurrent_processes_publish_one_valid_entry(self):
        start = self.context.Event()
        results = self.context.Queue()
        processes = [self.start_process(
            store_entry, str(self.cache_dir), str(self.source), start, results,
        ) for _ in range(2)]
        start.set()
        for process in processes:
            self.join_process(process)
        self.assertEqual([results.get(timeout=5) for _ in processes], [None, None])
        self.assert_valid_entry()

    def test_concurrent_threads_publish_one_valid_entry(self):
        start = threading.Event()
        results = queue.Queue()
        threads = [threading.Thread(
            target=store_entry,
            args=(str(self.cache_dir), str(self.source), start, results),
        ) for _ in range(2)]
        for thread in threads:
            thread.start()
        start.set()
        for thread in threads:
            thread.join(10)
            self.assertFalse(thread.is_alive())
        self.assertEqual([results.get(timeout=5) for _ in threads], [None, None])
        self.assert_valid_entry()

    def assert_valid_entry(self):
        entries = list(self.cache_dir.glob('module.c-*.gz'))
        self.assertEqual(len(entries), 1)
        with gzip.open(entries[0], 'rb') as source:
            self.assertEqual(source.read(), self.source.read_bytes())
        self.assertEqual(list(self.cache_dir.glob('*.tmp')), [])
        self.assertEqual(list(Path(self.cache._temporary_path).glob('*.tmp')), [])

    def check_cleanup_skips(self, mode):
        if mode == 'read':
            self.store()
        output = self.root / 'output.c'
        ready = self.context.Event()
        release = self.context.Event()
        results = self.context.Queue()
        worker = self.start_process(
            paused_cache_io, str(self.cache_dir), str(self.source), str(output),
            mode, ready, release, results,
        )
        self.addCleanup(release.set)
        self.assertTrue(ready.wait(10))
        attempted = self.context.Event()
        completed = self.context.Event()
        cleaner = self.start_process(
            cleanup_entry, str(self.cache_dir), attempted, completed,
        )
        self.assertTrue(attempted.wait(10))
        self.assertTrue(completed.wait(5), 'cleanup waited for an active cache operation')
        release.set()
        self.join_process(worker)
        self.join_process(cleaner)
        self.assertIsNone(results.get(timeout=5))
        self.assertTrue(completed.is_set())
        self.cache.cleanup_cache()
        if mode == 'read':
            self.assertEqual(output.read_bytes(), self.source.read_bytes())
        else:
            self.assert_valid_entry()

    def test_cleanup_skips_active_writer(self):
        self.check_cleanup_skips('write')

    def test_cleanup_skips_active_reader(self):
        self.check_cleanup_skips('read')

    def test_cleanup_reclaims_crashed_writer_temporary_file_and_lock(self):
        writer = self.start_process(
            abandon_temporary_file, str(self.cache_dir), str(self.source),
        )
        self.join_process(writer)
        temporary_path = Path(self.cache._temporary_path)
        self.assertEqual(len(list(temporary_path.glob('*.tmp'))), 1)
        lock_dir = self.cache_dir / self.cache._lock_directory
        self.assertEqual(len(list(lock_dir.glob('*.lock'))), 2)
        self.cache.cleanup_cache()
        self.assertEqual(list(temporary_path.glob('*.tmp')), [])
        self.assertEqual([p.name for p in lock_dir.glob('*.lock')], [self.cache._lifecycle_lock_name])

    def test_cleanup_coalesces_recent_work_across_instances(self):
        with mock.patch.object(cache_mod.os, 'scandir', wraps=os.scandir) as scandir:
            self.cache.cleanup_cache()
            initial_scans = scandir.call_count
            other = cache_mod.Cache(str(self.cache_dir))
            other.cleanup_cache()
            self.assertEqual(scandir.call_count, initial_scans)

            marker = self.cache._lock_path(self.cache._lifecycle_lock_name)
            os.utime(marker, (1, 1))
            other.cleanup_cache()
            self.assertGreater(scandir.call_count, initial_scans)
            self.assertEqual(os.stat(marker).st_size, 1)

    def test_cleanup_scans_artifact_directory_once(self):
        self.store()
        with mock.patch.object(cache_mod.os, 'scandir', wraps=os.scandir) as scandir:
            self.cache.cleanup_cache()
        root_scans = sum(os.fspath(call.args[0]) == str(self.cache_dir)
                         for call in scandir.call_args_list)
        self.assertEqual(root_scans, 1)

    def test_cleanup_ignores_live_lock_metadata(self):
        cached = self.store()
        lock_file = Path(self.cache._lock_path(self.cache._entry_lock_name(cached)))
        lock_file.write_bytes(b'x' * 20000)
        self.cache.cleanup_cache()
        self.assertTrue(Path(cached).exists())
        self.assertTrue(lock_file.exists())

    def test_cleanup_does_not_use_du(self):
        with mock.patch.object(subprocess, 'run', side_effect=AssertionError('unexpected du')):
            self.cache.cleanup_cache()

    def test_lock_open_failure_bypasses_cache(self):
        original_open = open

        def unavailable_lock(filename, *args, **kwargs):
            if os.fspath(filename).endswith('.lock'):
                raise PermissionError('lock is inaccessible')
            return original_open(filename, *args, **kwargs)

        with mock.patch('builtins.open', unavailable_lock):
            self.assertIsNone(self.cache.lookup_cache(str(self.source), 'key'))
            self.cache.store_to_cache(str(self.source), 'key', GeneratedSources(str(self.source)))
            self.cache.cleanup_cache()

    @unittest.skipUnless(os.name == 'posix', 'POSIX lock backend')
    def test_lock_acquisition_failure_closes_file(self):
        handle = tempfile.TemporaryFile()
        with mock.patch('builtins.open', return_value=handle):
            with mock.patch.object(cache_mod.fcntl, 'flock', side_effect=OSError('no locking')):
                with self.assertRaises(cache_mod.CacheUnavailable):
                    with cache_mod._file_lock('unavailable.lock', True):
                        self.fail('lock acquisition unexpectedly succeeded')
        self.assertTrue(handle.closed)

    def test_entry_lock_name_is_independent_of_cache_path_alias(self):
        cached = self.cache.fingerprint_file(str(self.source), 'key', cache_mod.gzip_ext)
        self.assertEqual(
            self.cache._entry_lock_name(cached),
            self.cache._entry_lock_name(os.path.basename(cached)),
        )

    def test_failed_temporary_removal_allows_republishing_entry(self):
        cached = self.cache.fingerprint_file(str(self.source), 'key', cache_mod.gzip_ext)
        with self.cache._lifecycle_lock(False), self.cache._entry_lock(cached, True):
            fd, temporary = self.cache._temporary_file()
            os.close(fd)
        real_unlink = os.unlink

        def sharing_violation(path):
            if os.fspath(path) == temporary:
                raise PermissionError('temporary artifact is in use')
            return real_unlink(path)

        lock_file = Path(self.cache._lock_path(self.cache._entry_lock_name(cached)))
        with mock.patch.object(cache_mod.os, 'unlink', sharing_violation):
            self.cache.cleanup_cache()
        self.assertTrue(Path(temporary).exists())
        self.assertFalse(lock_file.exists())
        self.assertIsNotNone(self.store())

    def prepare_compile_hit(self, zip_artifact=False):
        self.pyx = self.root / 'example.pyx'
        self.pyx.write_text('cdef public int value = 42\n' if zip_artifact else 'value = 42\n')
        result = Main.compile(str(self.pyx), cache=str(self.cache_dir))
        self.assertEqual(result.num_errors, 0)
        Path(result.c_file).unlink()
        return result.c_file

    def test_cache_creation_failure_bypasses_cache(self):
        original_makedirs = os.makedirs

        def unavailable_directory(path, *args, **kwargs):
            if os.fspath(path) == str(self.cache_dir):
                raise PermissionError('cache is inaccessible')
            return original_makedirs(path, *args, **kwargs)

        with mock.patch.object(cache_mod.os, 'makedirs', unavailable_directory):
            cache = cache_mod.Cache(str(self.cache_dir))
            self.assertIsNone(cache.lookup_cache(str(self.source), 'key'))

    def test_lookup_stale_handle_bypasses_cache(self):
        self.store()
        with mock.patch.object(cache_mod.os, 'utime', side_effect=OSError(errno.ESTALE, 'stale')):
            self.assertIsNone(self.cache.lookup_cache(str(self.source), 'key'))

    def test_cache_read_failure_recompiles(self):
        output = self.prepare_compile_hit()
        real_open = cache_mod.gzip_open

        def unavailable_read(path, mode):
            if mode == 'rb':
                raise PermissionError('cache read sharing violation')
            return real_open(path, mode)

        with mock.patch.object(cache_mod, 'gzip_open', unavailable_read):
            result = Main.compile(str(self.pyx), cache=str(self.cache_dir))
        self.assertEqual(result.num_errors, 0)
        self.assertTrue(Path(output).is_file())

    def test_zip_cache_read_failure_recompiles(self):
        output = self.prepare_compile_hit(zip_artifact=True)
        with mock.patch.object(zipfile.ZipFile, 'open', side_effect=OSError(errno.ESTALE, 'stale')):
            result = Main.compile(str(self.pyx), cache=str(self.cache_dir))
        self.assertEqual(result.num_errors, 0)
        self.assertTrue(Path(output).is_file())

    def test_cache_write_failure_does_not_fail_compile(self):
        pyx = self.root / 'example.pyx'
        pyx.write_text('value = 42\n')
        with mock.patch.object(cache_mod, 'gzip_open', side_effect=PermissionError('read-only cache')):
            result = Main.compile(str(pyx), cache=str(self.cache_dir))
        self.assertEqual(result.num_errors, 0)
        self.assertTrue(Path(result.c_file).is_file())
        self.assertEqual(list(self.cache_dir.glob('*.tmp')), [])
        self.assertEqual(list(Path(self.cache._temporary_path).glob('*.tmp')), [])

    def test_compile_preserves_output_errors_during_cache_load(self):
        output = self.prepare_compile_hit()
        original_open = open

        for error in (FileNotFoundError('output directory vanished'),
                      PermissionError('output is not writable')):
            with self.subTest(error=repr(error)):
                def unavailable_output(filename, mode='r', *args, **kwargs):
                    if os.fspath(filename) == output and mode == 'wb':
                        raise error
                    return original_open(filename, mode, *args, **kwargs)

                with mock.patch('builtins.open', unavailable_output):
                    with self.assertRaises(type(error)):
                        Main.compile(str(self.pyx), cache=str(self.cache_dir))

    def test_cleanup_scan_errors_are_best_effort(self):
        for error in (FileNotFoundError('missing'), PermissionError('sharing violation'),
                      OSError(errno.ESTALE, 'stale')):
            with self.subTest(error=repr(error)):
                with mock.patch.object(cache_mod.os, 'scandir', side_effect=error):
                    self.cache.cleanup_cache()

    def test_cleanup_stat_errors_are_best_effort(self):
        entry = mock.Mock(name='stale.gz')
        entry.name = 'stale.gz'
        entry.stat.side_effect = OSError(errno.ESTALE, 'stale')
        with mock.patch.object(cache_mod.os, 'scandir') as scandir:
            scandir.return_value.__enter__.return_value = [entry]
            self.assertEqual(self.cache._list_cache_files(), (0, []))
