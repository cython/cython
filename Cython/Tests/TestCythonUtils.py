import unittest

from Cython import Utils
from Cython.TestUtils import number_of_filled_caches, sandbox_for_function_caches
from Cython.Utils import build_hex_version, cached_function, clear_function_caches


class TestCythonUtils(unittest.TestCase):
    def test_build_hex_version(self):
        self.assertEqual('0x001D00A1', build_hex_version('0.29a1'))
        self.assertEqual('0x001D03C4', build_hex_version('0.29.3rc4'))
        self.assertEqual('0x001D00F0', build_hex_version('0.29'))
        self.assertEqual('0x040000F0', build_hex_version('4.0'))

    def the_last_cache_is(self, cache):
        self.assertEqual(Utils._function_caches[-1], cache)

    def number_of_filled_caches_is(self, number):
        self.assertEqual(number_of_filled_caches(), number)

    def set_up_test_in_sandbox(self):
        @cached_function
        def cached_next(x):
            return next(x)

        self.cached_next = cached_next

    @sandbox_for_function_caches(asserted=True)
    def test_cached_function(self):
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 0}

        # cache args
        self.assertEqual(self.cached_next(value), 0)
        self.number_of_filled_caches_is(1)
        self.the_last_cache_is(cache)

        # use cache
        self.assertEqual(self.cached_next(value), 0)
        self.number_of_filled_caches_is(1)
        self.the_last_cache_is(cache)

    @sandbox_for_function_caches(asserted=True)
    def test_clear_function_caches(self):
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 1}

        self.cached_next(value)  # cache args
        self.cached_next(value)  # use cache

        clear_function_caches()
        self.number_of_filled_caches_is(0)

        self.assertEqual(self.cached_next(value), 1)
        self.number_of_filled_caches_is(1)
        self.the_last_cache_is(cache)
