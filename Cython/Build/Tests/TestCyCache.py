import difflib
import errno
import glob
import gzip
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock
import zipfile

import Cython.Build.Dependencies
import Cython.Compiler.Main
import Cython.Utils
from Cython.TestUtils import CythonTest
from Cython.Build import Cache as cache_mod
from Cython.Build.Cache import Cache


class TestCyCache(CythonTest):

    def setUp(self):
        CythonTest.setUp(self)
        self.temp_dir = tempfile.TemporaryDirectory(
            prefix='cycache-test',
            dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
        )
        self.src_dir = tempfile.mkdtemp(prefix='src', dir=self.temp_dir.name)
        self.cache_dir = tempfile.mkdtemp(prefix='cache', dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def cache_files(self, file_glob):
        return glob.glob(os.path.join(self.cache_dir, file_glob))

    def fresh_cythonize(self, *args, **kwargs):
        Cython.Utils.clear_function_caches()
        Cython.Build.Dependencies._dep_tree = None  # discard method caches
        Cython.Build.Dependencies.cythonize(*args, **kwargs)

    def fresh_compile(self, *args, **kwargs):
        Cython.Utils.clear_function_caches()
        Cython.Compiler.Main.compile(*args, **kwargs)


    def _test_cycache_switch(self, compilation_method):
        content1 = 'value = 1\n'
        content2 = 'value = 2\n'
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'

        with open(a_pyx, 'w') as f:
            f.write(content1)

        compilation_method(a_pyx, cache=self.cache_dir)
        compilation_method(a_pyx, cache=self.cache_dir)

        self.assertEqual(1, len(self.cache_files('a.c*')))
        with open(a_c) as f:
            a_contents1 = f.read()
        os.unlink(a_c)

        with open(a_pyx, 'w') as f:
            f.write(content2)

        compilation_method(a_pyx, cache=self.cache_dir)

        with open(a_c) as f:
            a_contents2 = f.read()
        os.unlink(a_c)

        self.assertNotEqual(a_contents1, a_contents2, 'C file not changed!')
        self.assertEqual(2, len(self.cache_files('a.c*')))

        with open(a_pyx, 'w') as f:
            f.write(content1)

        compilation_method(a_pyx, cache=self.cache_dir)

        self.assertEqual(2, len(self.cache_files('a.c*')))
        with open(a_c) as f:
            a_contents = f.read()
        self.assertEqual(
            a_contents, a_contents1,
            msg='\n'.join(list(difflib.unified_diff(
                a_contents.split('\n'), a_contents1.split('\n')))[:10]))

    def test_cycache_switch_cythonize(self):
        self._test_cycache_switch(self.fresh_cythonize)

    def test_cycache_switch_compile(self):
        self._test_cycache_switch(self.fresh_compile)

    def _test_cycache_fingerprint(self, compilation_method, **kwargs):
        content = 'value = 1\n'
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'

        with open(a_pyx, 'w') as f:
            f.write(content)

        compilation_method(a_pyx, cache=self.cache_dir)
        with open(a_c) as f:
            a_contents1 = f.read()
        os.unlink(a_c)

        compilation_method(a_pyx, cache=self.cache_dir, **kwargs)

        with open(a_c) as f:
            a_contents2 = f.read()
        os.unlink(a_c)

        self.assertNotEqual(a_contents1, a_contents2, 'C file not changed!')

    def test_cycache_fingerprint_cythonize(self):
        self._test_cycache_fingerprint(self.fresh_cythonize, compiler_directives={'linetrace': True})

    def test_cycache_fingerprint_compile(self):
        self._test_cycache_fingerprint(self.fresh_compile, compiler_directives={'linetrace': True})

    def _test_cycache_uses_cache(self, compilation_method):
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'
        with open(a_pyx, 'w') as f:
            f.write('pass')

        compilation_method(a_pyx, cache=self.cache_dir)

        a_cache = self.cache_files('a.c*.gz')[0]
        with gzip.GzipFile(a_cache, 'wb') as gzipfile:
            gzipfile.write(b'fake stuff')
        os.unlink(a_c)

        compilation_method(a_pyx, cache=self.cache_dir)

        with open(a_c) as f:
            a_contents = f.read()
        self.assertEqual(a_contents, 'fake stuff',
                         'Unexpected contents: %s...' % a_contents[:100])


    def test_cycache_uses_cache_cythonize(self):
        self._test_cycache_uses_cache(self.fresh_cythonize)

    def test_cycache_uses_cache_compile(self):
        self._test_cycache_uses_cache(self.fresh_compile)

    def _test_cycache_annotation(self, compilation_method):
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'
        a_html = a_pyx[:-4] + '.html'
        with open(a_pyx, 'w') as f:
            f.write('pass')

        compilation_method(a_pyx, cache=self.cache_dir, annotate='default')
        self.assertTrue(os.path.exists(a_html), a_html)
        os.unlink(a_html)
        os.unlink(a_c)
        compilation_method(a_pyx, cache=self.cache_dir, annotate='default')
        self.assertTrue(os.path.exists(a_html), a_html)

    def test_cycache_annotation_cythonize(self):
        self._test_cycache_annotation(self.fresh_cythonize)

    def test_cycache_annotation_compile(self):
        self._test_cycache_annotation(self.fresh_compile)

    def _test_multi_file_output(self, compilation_method):
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'
        a_h = a_pyx[:-4] + '.h'
        a_api_h = a_pyx[:-4] + '_api.h'
        with open(a_pyx, 'w') as f:
            f.write('cdef public api int foo(int x): return x\n')

        compilation_method(a_pyx, cache=self.cache_dir)

        expected = [a_c, a_h, a_api_h]
        for output in expected:
            self.assertTrue(os.path.exists(output), output)
            os.unlink(output)

        compilation_method(a_pyx, cache=self.cache_dir)

        for output in expected:
            self.assertTrue(os.path.exists(output), output)
            self.assertTrue(os.path.isfile(output), output)

    def test_multi_file_output_cythonize(self):
        self._test_multi_file_output(self.fresh_cythonize)

    def test_multi_file_output_compile(self):
        self._test_multi_file_output(self.fresh_compile)

    def _test_options_invalidation(self, compilation_method):
        hash_pyx = os.path.join(self.src_dir, 'options.pyx')
        hash_c = hash_pyx[:-len('.pyx')] + '.c'
        hash_cpp = hash_pyx[:-len('.pyx')] + '.cpp'

        with open(hash_pyx, 'w') as f:
            f.write('pass')
        compilation_method(hash_pyx, cache=self.cache_dir, cplus=False)
        self.assertEqual(1, len(self.cache_files('options.c*')))

        os.unlink(hash_c)

        compilation_method(hash_pyx, cache=self.cache_dir, cplus=True)

        self.assertEqual(2, len(self.cache_files('options.c*')))

        try:
            os.unlink(hash_c)
        except FileNotFoundError:
            # fresh_cythonize() produces .c file, fresh_compile produces .cpp file
            os.unlink(hash_cpp)

        compilation_method(hash_pyx, cache=self.cache_dir, cplus=False, show_version=False)

        self.assertEqual(2, len(self.cache_files('options.c*')))

        os.unlink(hash_c)

        compilation_method(hash_pyx, cache=self.cache_dir, cplus=False, show_version=True)

        self.assertEqual(2, len(self.cache_files('options.c*')))

    def test_options_invalidation_cythonize(self):
        self._test_options_invalidation(self.fresh_cythonize)

    def test_options_invalidation_compile(self):
        self._test_options_invalidation(self.fresh_compile)


class TestCyCacheCleanup(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir = self.temp_dir.name

        # Set a small cache size to trigger cleanup easily
        self.cache_size = 10_000  # 10 KB
        self.cache = Cache(self.cache_dir, self.cache_size)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_cache_file(self, filename, size_bytes, access_time=None):
        """
        Create a cache file with specified size and access time.

        Args:
            filename: Name of the file to create
            size_bytes: Size of the file in bytes
            access_time: Unix timestamp for file access time (uses current time if None)
        """
        file_path = os.path.join(self.cache_dir, filename)

        # Create file with specified size
        with open(file_path, 'wb') as f:
            f.write(b'x' * size_bytes)

        # Set access time if provided
        if access_time is not None:
            os.utime(file_path, (access_time, access_time))
        else:
            self.assertTrue(os.path.exists(file_path), f"{file_path} should exist after creation")

        return file_path

    def test_cleanup_deletes_oldest_files_first(self):
        """
        Validate that cleanup_cache() deletes files with older access times
        before more recently accessed files.
        """
        # Get current time and create files with staggered access times
        base_time = time.time()

        # Create files with progressively newer access times
        file1 = self._create_cache_file('file1.cache', 3000, base_time - 1000)
        file2 = self._create_cache_file('file2.cache', 3000, base_time - 500)
        file3 = self._create_cache_file('file3.cache', 3000, base_time - 100)
        file4 = self._create_cache_file('file4.cache', 3000, base_time)

        # Run cleanup
        self.cache.cleanup_cache()

        # Oldest file should be deleted first
        self.assertFalse(os.path.exists(file1), "Oldest file should be deleted first")

        # Files should still exist or be deleted based on access time order
        # and remaining size relative to cache_size * ratio
        remaining_files = [file2, file3, file4]
        existing_count = sum(1 for f in remaining_files if os.path.exists(f))
        self.assertGreaterEqual(existing_count, 1, "Some files should persist")

        # Verify that the ratio threshold has been met
        _, remaining_cache_files = self.cache._list_cache_files()
        remaining_size = sum(size for _, size, _ in remaining_cache_files)
        self.assertLess(
            remaining_size,
            self.cache_size * 0.85,
            "Remaining cache size should be below 85% of cache_size limit"
        )

    def test_cleanup_skips_temp_files(self):
        """Verify that .tmp files are not deleted during cleanup."""
        base_time = time.time()

        # Create regular and temp files
        regular_file = self._create_cache_file('old_file.cache', 12000, base_time - 1000)
        temp_file = self._create_cache_file('temp_file.tmp', 12000, base_time - 2000)

        # Run cleanup
        self.cache.cleanup_cache()

        # Temp file should still exist even though it's older
        self.assertTrue(
            os.path.exists(temp_file),
            "Temporary .tmp files should not be deleted"
        )
        self.assertFalse(
            os.path.exists(regular_file),
            "No files were deleted by cleanup"
        )

    def test_cleanup_stops_at_ratio_threshold(self):
        """
        Verify that cleanup_cache() stops deleting once total size
        falls below cache_size * ratio.
        """
        base_time = time.time()

        # Create files with clear access time ordering
        self._create_cache_file('file1.cache', 2000, base_time - 1000)
        self._create_cache_file('file2.cache', 2000, base_time - 800)
        self._create_cache_file('file3.cache', 2000, base_time - 600)
        self._create_cache_file('file4.cache', 2000, base_time - 400)
        self._create_cache_file('file5.cache', 2000, base_time - 200)
        self._create_cache_file('file6.cache', 2000, base_time)

        # Run cleanup with custom ratio.
        ratio = 0.70
        self.cache.cleanup_cache(ratio=ratio)

        # Remaining size should be less than cache_size * ratio.
        _, remaining_files = self.cache._list_cache_files()
        remaining_size = sum(size for _, size, _ in remaining_files)

        max_cache_size = int(self.cache_size * ratio)
        self.assertLess(
            remaining_size,
            max_cache_size,
            f"Remaining size {remaining_size} should be less than "
            f"cache_size * ratio ({max_cache_size})"
        )

    def test_cleanup_no_action_when_under_limit(self):
        """
        Verify that cleanup_cache() does not delete files when
        total cache size is already under the limit.
        """
        base_time = time.time()

        # Create small files that don't exceed cache_size.
        file1 = self._create_cache_file('file1.cache', 1000, base_time - 1000)
        file2 = self._create_cache_file('file2.cache', 1000, base_time)

        # Run cleanup.
        self.cache.cleanup_cache()

        # Both files should still exist.
        self.assertTrue(os.path.exists(file1), "Files should not be deleted when under limit")
        self.assertTrue(os.path.exists(file2), "Files should not be deleted when under limit")

    def test_cleanup_no_action_when_at_limit(self):
        """
        Verify that cleanup_cache() does not delete files when
        total cache size is only at the limit.
        """
        base_time = time.time()

        file1 = self._create_cache_file('file1.cache', 3000, base_time - 1000)
        file2 = self._create_cache_file('file2.cache', 3000, base_time)
        file3 = self._create_cache_file('file2.cache', 4000, base_time)

        # Run cleanup.
        self.cache.cleanup_cache()

        # All files should still exist.
        self.assertTrue(os.path.exists(file1), "Files should not be deleted when not over limit")
        self.assertTrue(os.path.exists(file2), "Files should not be deleted when not over limit")
        self.assertTrue(os.path.exists(file3), "Files should not be deleted when not over limit")

    def test_cleanup_preserves_recent_files(self):
        """
        Verify that cleanup_cache() preserves the most recently accessed files.
        """
        base_time = time.time()

        # Create files: one very old, several recent ones
        old_file = self._create_cache_file('old.cache', 4000, base_time - 10000)
        recent_file1 = self._create_cache_file('recent1.cache', 4000, base_time - 10)
        recent_file2 = self._create_cache_file('recent2.cache', 4000, base_time)

        # Run cleanup.
        self.cache.cleanup_cache()

        # Old file should be deleted.
        self.assertFalse(os.path.exists(old_file), "Old file should be deleted")

        # At least one recent file should still exist.
        files_exist = os.path.exists(recent_file1) or os.path.exists(recent_file2)
        self.assertTrue(
            files_exist,
            "At least one recently accessed file should be preserved"
        )

    def test_cleanup_handles_concurrent_file_deletion(self):
        """
        Verify that cleanup_cache() handles concurrent file deletion gracefully.

        This test simulates a race condition where a file is deleted by another
        process between _list_cache_files() and _delete_cache_files().
        """
        base_time = time.time()
        ratio = 85  # %
        max_cache_size = int(self.cache_size * ratio / 100)

        # Create cache files with staggered access times to exceed cache_size.
        file1 = self._create_cache_file('file1.cache', 3000, base_time - 1000)
        file2 = self._create_cache_file('file2.cache', 3000, base_time - 500)
        file3 = self._create_cache_file('file3.cache', 3000, base_time - 100)
        file4 = self._create_cache_file('file4.cache', 3000, base_time)

        # Verify all files exist.
        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        self.assertTrue(os.path.exists(file3))
        self.assertTrue(os.path.exists(file4))

        # Get the sorted list of files that cleanup_cache() would process.
        _, cache_files = self.cache._list_cache_files()
        self.cache._sort_files_by_atime(cache_files)

        # The oldest file should be first.
        oldest_path, _, _ = cache_files[0]
        self.assertEqual(oldest_path, file1, "file1 should be the oldest")

        total_size, _ = self.cache._list_cache_files()

        # Simulate concurrent deletion: delete the oldest file before _delete_cache_files processes it.
        os.unlink(oldest_path)
        self.assertFalse(os.path.exists(oldest_path))

        # Call _delete_cache_files directly with the pre-computed list.
        # This isolates the deletion logic and allows us to test the race condition.
        try:
            self.cache._delete_cache_files(cache_files, total_size, max_cache_size)
        except FileNotFoundError:
            self.fail(
                "_delete_cache_files() should handle FileNotFoundError from concurrent "
                "deletion gracefully without propagating the exception"
            )

        # Verify that cleanup continued and deleted additional files.
        remaining_total_size, remaining_files = self.cache._list_cache_files()
        self.assertLessEqual(
            remaining_total_size,
            max_cache_size,
            f"Cache should be cleaned up to below {ratio}% despite concurrent deletions"
        )

        # Verify that files were actually deleted.
        deleted_count = 4 - len(remaining_files)
        self.assertGreater(
            deleted_count,
            0,
            "Cleanup should have deleted files to reach the target ratio"
        )


def store_entry(cache_dir, source):
    result = Cython.Compiler.Main.CompilationResult()
    result.c_file = source
    cache = Cache(cache_dir)
    cache.store_to_cache(source, 'key', result)
    return cache.lookup_cache(source, 'key')


class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache_dir = self.root / 'cache'
        self.cache = Cache(str(self.cache_dir), cache_size=5000)
        self.source = self.root / 'module.c'
        self.source.write_bytes(b'/* generated source */\n')

    def store(self):
        return store_entry(str(self.cache_dir), str(self.source))


class TestCyCacheOperations(CacheTestCase):
    def test_cleanup_coalesces_recent_work_across_instances(self):
        with mock.patch.object(cache_mod.os, 'scandir', wraps=os.scandir) as scandir:
            self.cache.cleanup_cache()
            initial_scans = scandir.call_count
            marker = self.cache._lock_path(self.cache._lifecycle_lock_name)
            completed_at = os.stat(marker).st_mtime
            interval = self.cache._cleanup_interval
            with mock.patch.object(cache_mod.time, 'time', return_value=completed_at + interval / 2):
                other = cache_mod.Cache(str(self.cache_dir))
                other.cleanup_cache()
                self.assertEqual(scandir.call_count, initial_scans)
            with mock.patch.object(cache_mod.time, 'time', return_value=completed_at + interval * 2):
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

    def test_lock_open_failure_bypasses_cache(self):
        cached = self.store()
        original_open = open

        def unavailable_lock(filename, *args, **kwargs):
            if os.fspath(filename).endswith('.lock'):
                raise PermissionError('lock is inaccessible')
            return original_open(filename, *args, **kwargs)

        with mock.patch('builtins.open', unavailable_lock):
            self.assertEqual(self.cache.lookup_cache(str(self.source), 'key'), cached)
            with self.assertRaises(cache_mod.CacheUnavailable):
                self.cache.load_from_cache(str(self.root / 'output.c'), cached)
            store_entry(str(self.cache_dir), str(self.source))
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
        result = Cython.Compiler.Main.compile(str(self.pyx), cache=str(self.cache_dir))
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

    def test_cache_write_failure_does_not_fail_compile(self):
        pyx = self.root / 'example.pyx'
        pyx.write_text('value = 42\n')
        with mock.patch.object(cache_mod, 'gzip_open', side_effect=PermissionError('read-only cache')):
            result = Cython.Compiler.Main.compile(str(pyx), cache=str(self.cache_dir))
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
                        Cython.Compiler.Main.compile(str(self.pyx), cache=str(self.cache_dir))

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

    def test_cache_read_failure_recompiles(self):
        for zip_artifact in (False, True):
            with self.subTest(zip_artifact=zip_artifact):
                output = self.prepare_compile_hit(zip_artifact=zip_artifact)
                target, name = (zipfile.ZipFile, 'open') if zip_artifact else (cache_mod, 'gzip_open')
                with mock.patch.object(target, name, side_effect=PermissionError('cache is inaccessible')):
                    result = Cython.Compiler.Main.compile(str(self.pyx), cache=str(self.cache_dir))
                self.assertEqual(result.num_errors, 0)
                self.assertTrue(Path(output).is_file())

    def test_streaming_errors_preserve_cache_output_boundary(self):
        for error in (PermissionError('sharing violation'), OSError(errno.ESTALE, 'stale'),
                      EOFError('truncated cache'), zipfile.BadZipFile('corrupt cache')):
            with self.subTest(read_error=repr(error)):
                source = mock.Mock()
                source.read.side_effect = [b'partial output', error]
                output = mock.Mock()
                with self.assertRaises(cache_mod.CacheUnavailable):
                    cache_mod._copy_from_cache(source, output)
                output.write.assert_called_once_with(b'partial output')

        for error in (FileNotFoundError('output vanished'), PermissionError('output is read-only')):
            with self.subTest(write_error=repr(error)):
                source = mock.Mock()
                source.read.return_value = b'generated output'
                output = mock.Mock()
                output.write.side_effect = error
                with self.assertRaises(type(error)):
                    cache_mod._copy_from_cache(source, output)
