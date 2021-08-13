# -*- coding: utf-8 -*-

import os.path
import shutil
import tempfile
import textwrap
import unittest
from copy import deepcopy

from Cython import Utils
from Cython.TestUtils import (
    filled_function_caches, number_of_filled_caches, relative_items,
    relative_lines_from_file, sandbox_for_function_caches, write_file,
    write_newer_file)


class TestTestUtils(unittest.TestCase):
    def setUp(self):
        super(TestTestUtils, self).setUp()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if self.temp_dir and os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        super(TestTestUtils, self).tearDown()

    ################################# Writing ##################################

    def _test_path(self, filename):
        return os.path.join(self.temp_dir, filename)

    def _test_write_file(self, content, expected, **kwargs):
        file_path = self._test_path("abcfile")
        write_file(file_path, content, **kwargs)
        assert os.path.isfile(file_path)

        with open(file_path, 'rb') as f:
            found = f.read()
        assert found == expected, (repr(expected), repr(found))

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
        assert os.path.isfile(file_path_1)
        write_newer_file(file_path_2, file_path_1, "xyz")
        assert os.path.isfile(file_path_2)
        assert os.path.getmtime(file_path_2) > os.path.getmtime(file_path_1)

    def test_write_newer_file_same(self):
        file_path = self._test_path("abcfile.txt")
        write_file(file_path, "abc")
        mtime = os.path.getmtime(file_path)
        write_newer_file(file_path, file_path, "xyz")
        assert os.path.getmtime(file_path) > mtime

    def test_write_newer_file_fresh(self):
        file_path = self._test_path("abcfile.txt")
        assert not os.path.exists(file_path)
        write_newer_file(file_path, file_path, "xyz")
        assert os.path.isfile(file_path)

    ################################# Sandbox ##################################

    def _sandbox_set_up(self):
        Utils._function_caches = self._function_caches

    def sandboxed(self):
        # setup value
        self.assertEqual(Utils._function_caches, self._function_caches)

        Utils._function_caches = [
            "WHAT is the airspeed velocity of an unladen swallow?",
            "What do you mean? African or European swallow?",
            "I, I don't know that!"]

    def _test_sandbox_for_function_caches(self, add_setup_func, asserted):
        self.assertFalse(hasattr(self, "set_up_test_in_sandbox"))
        if add_setup_func:
            self.set_up_test_in_sandbox = self._sandbox_set_up

        caches_before = Utils._function_caches
        caches_contents = Utils._function_caches[:]
        caches_copy = deepcopy(Utils._function_caches)

        sandboxed = sandbox_for_function_caches(asserted)(self.sandboxed)

        self.assertIs(caches_before, Utils._function_caches)
        self.assertEqual(caches_copy, Utils._function_caches)
        for cache1, cache2 in zip(caches_contents, Utils._function_caches):
            # each cache is still linked with its own decorator
            self.assertIs(cache1, cache2)

        if add_setup_func:
            del self.set_up_test_in_sandbox
        self.assertFalse(hasattr(self, "set_up_test_in_sandbox"))

    def _test_sandbox(self, *args, **kwargs):
        self._function_caches = []
        self._test_sandbox_for_function_caches(*args, **kwargs)

        self._function_caches = [1, 2, 3]
        self._test_sandbox_for_function_caches(*args, **kwargs)

        del self._function_caches

    def test_sandbox_with_setup(self):
        self._test_sandbox(add_setup_func=True, asserted=False)

    def test_sandbox_without_setup(self):
        self._test_sandbox(add_setup_func=False, asserted=False)

    def test_asserted_sandbox_with_setup(self):
        self._test_sandbox(add_setup_func=True, asserted=True)

    def test_asserted_sandbox_without_setup(self):
        self._test_sandbox(add_setup_func=False, asserted=True)

    ############################# Function caches ##############################

    def _test_filled_function_caches(self):
        cache_value = {(69,): "ends on the 42nd decimal place of Pi"}

        self.assertFalse(hasattr(self, "set_up_test_in_sandbox"))
        self.assertEqual(list(filled_function_caches()), [])

        Utils._function_caches.append(cache_value)
        self.assertEqual(list(filled_function_caches()), [cache_value])

    def _test_number_of_filled_caches(self):
        cache_value = {("The first",): "42 decimals of Pi have 6 9s"}

        self.assertFalse(hasattr(self, "set_up_test_in_sandbox"))
        self.assertEqual(number_of_filled_caches(), 0)

        Utils._function_caches.append(cache_value)
        self.assertEqual(number_of_filled_caches(), 1)

    # if asserted = True then uses the functionality being tested
    @sandbox_for_function_caches(asserted=False)
    def test_filled_function_caches(self):
        self._test_filled_function_caches()

    @sandbox_for_function_caches(asserted=False)
    def test_number_of_filled_caches(self):
        self._test_number_of_filled_caches()

    @sandbox_for_function_caches(asserted=True)
    def test_asserted_filled_function_caches(self):
        self._test_filled_function_caches()

    @sandbox_for_function_caches(asserted=True)
    def test_asserted_number_of_filled_caches(self):
        self._test_number_of_filled_caches()

    ############################# Relative things ##############################

    def test_relative_items(self):
        self.assertEqual(relative_items(range(10), 5, -1, 1), range(4, 6))

        with self.assertRaises(ValueError):
            relative_items(range(10), 10, 0, 0)

        with self.assertRaisesRegex(
            ValueError, r"^10 was not found, presumably in \n4\n5$"
        ):
            relative_items(range(10), 10, 0, 0, fallback=(5, -1, 1))

    def test_relative_lines_from_file(self):
        path = self._test_path("source of lines")
        write_file(path, "\n".join(map(str, range(10))))

        # same as in test_relative_items
        self.assertEqual(relative_lines_from_file(path, "5\n", -1, 1), "4\n5\n")

        with self.assertRaises(ValueError):
            relative_lines_from_file(path, "10\n", 0, 0)

        with self.assertRaisesRegex(
            ValueError,
            r"^'10\\n' was not found, presumably in \n'4\\n'\n'5\\n'$"
        ):
            relative_lines_from_file(path, "10\n", 0, 0,
                                     fallback=("5\n", -1, 1))
