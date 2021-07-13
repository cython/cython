import unittest

from Cython import Utils
from Cython.TestUtils import (
    number_of_filled_caches, sandbox_for_function_caches)
from Cython.Utils import (
    _CACHE_METHOD_NAME, _METHOD_CACHE_PATTERN, build_hex_version,
    cached_function, cached_method, clear_function_caches, clear_method_caches,
    method_and_cache_names)

METHOD_NAME = "cached_next"
CACHE_NAME = _CACHE_METHOD_NAME.format(METHOD_NAME)
NAMES = METHOD_NAME, CACHE_NAME

class Cached:
    @cached_method
    def cached_next(self, x):
        return next(x)


class TestCythonUtils(unittest.TestCase):
    def test_requirements_for_Cached(self):
        test = Cached()

        self.assertTrue(hasattr(test, METHOD_NAME))
        self.assertFalse(hasattr(test, CACHE_NAME))
        self.list_of_names_equal(test, [])

    def test_build_hex_version(self):
        self.assertEqual('0x001D00A1', build_hex_version('0.29a1'))
        self.assertEqual('0x001D03C4', build_hex_version('0.29.3rc4'))
        self.assertEqual('0x001D00F0', build_hex_version('0.29'))
        self.assertEqual('0x040000F0', build_hex_version('4.0'))

    def test_cache_method_name(self):
        method_name = "foo"
        cache_name = _CACHE_METHOD_NAME.format(method_name)
        match = _METHOD_CACHE_PATTERN.match(cache_name)

        self.assertIsNot(match, None)
        self.assertEqual(match.group(1), method_name)

    def test_method_and_cache_names(self):
        test = Cached()
        method_name = "bar"
        cache_name = _CACHE_METHOD_NAME.format(method_name)

        setattr(test, CACHE_NAME, {})
        setattr(test, cache_name, {})

        self.assertFalse(hasattr(test, method_name))

        self.assertEqual(set(method_and_cache_names(test)),
                         {NAMES, (method_name, cache_name)})

    def the_last_cache_is(self, cache):
        self.assertEqual(Utils._function_caches[-1], cache)

    def list_of_names_equal(self, instance, value):
        self.assertEqual(list(method_and_cache_names(instance)), value)

    def number_of_filled_caches_is(self, number):
        self.assertEqual(number_of_filled_caches(), number)

    def test_cached_method(self):
        test = Cached()
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 0}

        # cache args
        self.assertEqual(test.cached_next(value), 0)
        self.list_of_names_equal(test, [NAMES])
        self.assertEqual(getattr(test, CACHE_NAME), cache)

        # use cache
        self.assertEqual(test.cached_next(value), 0)
        self.list_of_names_equal(test, [NAMES])
        self.assertEqual(getattr(test, CACHE_NAME), cache)

    def test_clear_method_caches(self):
        test = Cached()
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 1}

        test.cached_next(value)  # cache args
        test.cached_next(value)  # use cache

        clear_method_caches(test)
        self.list_of_names_equal(test, [])

        self.assertEqual(test.cached_next(value), 1)
        self.list_of_names_equal(test, [NAMES])
        self.assertEqual(getattr(test, CACHE_NAME), cache)

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
