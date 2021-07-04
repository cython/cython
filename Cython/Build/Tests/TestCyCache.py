import difflib
import glob
import gzip
import os
import tempfile

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import CythonTest, write_file, fresh_cythonize


class TestCyCache(CythonTest):

    def setUp(self):
        CythonTest.setUp(self)
        self.temp_dir = tempfile.mkdtemp(
            prefix='cycache-test',
            dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None)
        self.src_dir = tempfile.mkdtemp(prefix='src', dir=self.temp_dir)
        self.cache_dir = tempfile.mkdtemp(prefix='cache', dir=self.temp_dir)

    def cache_files(self, file_glob):
        return glob.glob(os.path.join(self.cache_dir, file_glob))

    def fresh_cythonize(self, *args, **kwargs):
        kwargs.update(cache=self.cache_dir)
        fresh_cythonize(*args, **kwargs)

    def test_cycache_switch(self):
        content1 = 'value = 1\n'
        content2 = 'value = 2\n'
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'

        write_file(a_pyx, content1)
        self.fresh_cythonize(a_pyx)
        self.fresh_cythonize(a_pyx)
        self.assertEqual(1, len(self.cache_files('a.c*')))
        with open(a_c) as f:
            a_contents1 = f.read()
        os.unlink(a_c)

        write_file(a_pyx, content2)
        self.fresh_cythonize(a_pyx)
        with open(a_c) as f:
            a_contents2 = f.read()
        os.unlink(a_c)

        self.assertNotEqual(a_contents1, a_contents2, 'C file not changed!')
        self.assertEqual(2, len(self.cache_files('a.c*')))

        write_file(a_pyx, content1)
        self.fresh_cythonize(a_pyx)
        self.assertEqual(2, len(self.cache_files('a.c*')))
        with open(a_c) as f:
            a_contents = f.read()
        self.assertEqual(
            a_contents, a_contents1,
            msg='\n'.join(list(difflib.unified_diff(
                a_contents.split('\n'), a_contents1.split('\n')))[:10]))

    def test_cycache_uses_cache(self):
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'
        write_file(a_pyx, 'pass')
        self.fresh_cythonize(a_pyx)
        a_cache = os.path.join(self.cache_dir, os.listdir(self.cache_dir)[0])
        gzip.GzipFile(a_cache, 'wb').write('fake stuff'.encode('ascii'))
        os.unlink(a_c)
        self.fresh_cythonize(a_pyx)
        with open(a_c) as f:
            a_contents = f.read()
        self.assertEqual(a_contents, 'fake stuff',
                         'Unexpected contents: %s...' % a_contents[:100])

    def test_multi_file_output(self):
        a_pyx = os.path.join(self.src_dir, 'a.pyx')
        a_c = a_pyx[:-4] + '.c'
        a_h = a_pyx[:-4] + '.h'
        a_api_h = a_pyx[:-4] + '_api.h'
        write_file(a_pyx, 'cdef public api int foo(int x): return x\n')
        self.fresh_cythonize(a_pyx)
        expected = [a_c, a_h, a_api_h]
        for output in expected:
            self.assertTrue(os.path.exists(output), output)
            os.unlink(output)
        self.fresh_cythonize(a_pyx)
        for output in expected:
            self.assertTrue(os.path.exists(output), output)

    def test_options_invalidation(self):
        hash_pyx = os.path.join(self.src_dir, 'options.pyx')
        hash_c = hash_pyx[:-len('.pyx')] + '.c'

        write_file(hash_pyx, 'pass')
        self.fresh_cythonize(hash_pyx, cplus=False)
        self.assertEqual(1, len(self.cache_files('options.c*')))

        os.unlink(hash_c)
        self.fresh_cythonize(hash_pyx, cplus=True)
        self.assertEqual(2, len(self.cache_files('options.c*')))

        os.unlink(hash_c)
        self.fresh_cythonize(hash_pyx, cplus=False, show_version=False)
        self.assertEqual(2, len(self.cache_files('options.c*')))

        os.unlink(hash_c)
        self.fresh_cythonize(hash_pyx, cplus=False, show_version=True)
        self.assertEqual(2, len(self.cache_files('options.c*')))
