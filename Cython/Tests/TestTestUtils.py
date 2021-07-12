# -*- coding: utf-8 -*-

import os.path
import shutil
import tempfile
import textwrap
import unittest
from copy import deepcopy

from Cython import Utils
from Cython.TestUtils import (
    filled_function_caches, number_of_filled_caches,
    sandbox_for_function_caches, write_file, write_newer_file)


class TestTestUtils(unittest.TestCase):
    def setUp(self):
        super(TestTestUtils, self).setUp()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if self.temp_dir and os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        super(TestTestUtils, self).tearDown()

    def _test_path(self, filename):
        return os.path.join(self.temp_dir, filename)

    def _test_write_file(self, content, expected, **kwargs):
        file_path = self._test_path("abcfile")
        write_file(file_path, content, **kwargs)
        self.assertTrue(os.path.isfile(file_path))

        with open(file_path, 'rb') as f:
            found = f.read()
        self.assertEqual(found, expected, (repr(expected), repr(found)))

    def test_write_file_text(self):
        text = u"abcüöä"
        self._test_write_file(text, text.encode('utf-8'))

    def test_write_file_dedent(self):
        text = u"""
        A horse is a horse,
        of course, of course,
        And no one can talk to a horse
        of course
        """
        self._test_write_file(text, textwrap.dedent(text).encode('utf-8'), dedent=True)

    def test_write_file_bytes(self):
        self._test_write_file(b"ab\0c", b"ab\0c")

    def test_write_newer_file(self):
        file_path_1 = self._test_path("abcfile1.txt")
        file_path_2 = self._test_path("abcfile2.txt")
        write_file(file_path_1, "abc")
        self.assertTrue(os.path.isfile(file_path_1))
        write_newer_file(file_path_2, file_path_1, "xyz")
        self.assertTrue(os.path.isfile(file_path_2))
        self.assertGreater(os.path.getmtime(file_path_2), os.path.getmtime(file_path_1))

    def test_write_newer_file_same(self):
        file_path = self._test_path("abcfile.txt")
        write_file(file_path, "abc")
        mtime = os.path.getmtime(file_path)
        write_newer_file(file_path, file_path, "xyz")
        self.assertGreater(os.path.getmtime(file_path), mtime)

    def test_write_newer_file_fresh(self):
        file_path = self._test_path("abcfile.txt")
        self.assertFalse(os.path.exists(file_path))
        write_newer_file(file_path, file_path, "xyz")
        self.assertTrue(os.path.isfile(file_path))
