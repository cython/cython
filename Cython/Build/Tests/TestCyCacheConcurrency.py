from concurrent.futures import ThreadPoolExecutor
import gzip
import multiprocessing
import os
from pathlib import Path
import threading
from unittest import mock

from Cython.Build import Cache as cache_mod
from Cython.Build.Tests.TestCyCache import CacheTestCase, store_entry


STARTUP_TIMEOUT = 60
OPERATION_TIMEOUT = 10


def publish_entry(cache_dir, source, start):
    start.wait(STARTUP_TIMEOUT)
    store_entry(cache_dir, source)


def publish_threads(cache_dir, source):
    start = threading.Barrier(2)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(publish_entry, cache_dir, source, start) for _ in range(2)]
        for future in futures:
            future.result(OPERATION_TIMEOUT)


def paused_cache_io(cache_dir, source, output, mode, ready, release):
    real_open = cache_mod.gzip_open

    def paused_open(path, file_mode):
        handle = real_open(path, file_mode)
        ready.set()
        if not release.wait(STARTUP_TIMEOUT * 2):
            handle.close()
            raise TimeoutError('cache operation was not released')
        return handle

    cache = cache_mod.Cache(cache_dir)
    with mock.patch.object(cache_mod, 'gzip_open', paused_open):
        if mode == 'write':
            store_entry(cache_dir, source)
        else:
            cached = cache.fingerprint_file(source, 'key', cache_mod.gzip_ext)
            cache.load_from_cache(output, cached)


def cleanup_entry(cache_dir):
    cache_mod.Cache(cache_dir).cleanup_cache()


def abandon_temporary_file(cache_dir, source):
    cache = cache_mod.Cache(cache_dir)
    cached = cache.fingerprint_file(source, 'key', cache_mod.gzip_ext)
    with cache._lifecycle_lock(False), cache._entry_lock(cached, True):
        fd, _ = cache._temporary_file()
        os.write(fd, b'abandoned temporary artifact')
        os.close(fd)
        # Termination must release OS locks without running Python cleanup.
        os._exit(0)


class TestCyCacheConcurrency(CacheTestCase):
    def setUp(self):
        super().setUp()
        self.context = multiprocessing.get_context('spawn')

    def start_process(self, target, *args):
        process = self.context.Process(target=target, args=args)
        process.start()

        def stop():
            if process.is_alive():
                process.kill()
            process.join(OPERATION_TIMEOUT)
            process.close()

        self.addCleanup(stop)
        return process

    def join_process(self, process, timeout=STARTUP_TIMEOUT):
        process.join(timeout)
        self.assertFalse(process.is_alive(), f'{process.name} did not finish within {timeout}s')
        self.assertEqual(process.exitcode, 0)

    def test_concurrent_processes_publish_one_valid_entry(self):
        self.cache_dir.rmdir()
        start = self.context.Barrier(3)
        processes = [self.start_process(
            publish_entry, str(self.cache_dir), str(self.source), start,
        ) for _ in range(2)]
        start.wait(STARTUP_TIMEOUT)
        for process in processes:
            self.join_process(process, OPERATION_TIMEOUT)
        self.assert_valid_entry()

    def test_concurrent_threads_publish_one_valid_entry(self):
        # A blocked interpreter must not prevent the parent from enforcing a timeout.
        worker = self.start_process(publish_threads, str(self.cache_dir), str(self.source))
        self.join_process(worker)
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
        worker = self.start_process(
            paused_cache_io, str(self.cache_dir), str(self.source), str(output),
            mode, ready, release,
        )
        self.addCleanup(release.set)
        self.assertTrue(ready.wait(STARTUP_TIMEOUT), 'cache operation did not become ready')
        cleaner = self.start_process(cleanup_entry, str(self.cache_dir))
        try:
            self.join_process(cleaner)
        finally:
            release.set()
        self.join_process(worker, OPERATION_TIMEOUT)
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
