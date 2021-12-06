import unittest

from Cython.Utils import (
    _CACHE_NAME_PATTERN, _build_cache_name, _find_cache_attributes,
    build_hex_version, cached_method, clear_method_caches)

METHOD_NAME = "cached_next"
CACHE_NAME = _build_cache_name(METHOD_NAME)
NAMES = CACHE_NAME, METHOD_NAME

class Cached(object):
    @cached_method
    def cached_next(self, x):
        return next(x)


class TestCythonUtils(unittest.TestCase):
    def test_build_hex_version(self):
        self.assertEqual('0x001D00A1', build_hex_version('0.29a1'))
        self.assertEqual('0x001D03C4', build_hex_version('0.29.3rc4'))
        self.assertEqual('0x001D00F0', build_hex_version('0.29'))
        self.assertEqual('0x040000F0', build_hex_version('4.0'))

    ############################## Cached Methods ##############################

    def test_cache_method_name(self):
        method_name = "foo"
        cache_name = _build_cache_name(method_name)
        match = _CACHE_NAME_PATTERN.match(cache_name)

        self.assertIsNot(match, None)
        self.assertEqual(match.group(1), method_name)

    def test_requirements_for_Cached(self):
        obj = Cached()

        self.assertFalse(hasattr(obj, CACHE_NAME))
        self.assertTrue(hasattr(obj, METHOD_NAME))
        self.set_of_names_equal(obj, set())

    def set_of_names_equal(self, obj, value):
        self.assertEqual(set(_find_cache_attributes(obj)), value)

    def test_find_cache_attributes(self):
        obj = Cached()
        method_name = "bar"
        cache_name = _build_cache_name(method_name)

        setattr(obj, CACHE_NAME, {})
        setattr(obj, cache_name, {})

        self.assertFalse(hasattr(obj, method_name))
        self.set_of_names_equal(obj, {NAMES, (cache_name, method_name)})

    def test_cached_method(self):
        obj = Cached()
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 0}

        # cache args
        self.assertEqual(obj.cached_next(value), 0)
        self.set_of_names_equal(obj, {NAMES})
        self.assertEqual(getattr(obj, CACHE_NAME), cache)

        # use cache
        self.assertEqual(obj.cached_next(value), 0)
        self.set_of_names_equal(obj, {NAMES})
        self.assertEqual(getattr(obj, CACHE_NAME), cache)

    def test_clear_method_caches(self):
        obj = Cached()
        value = iter(range(3))  # iter for Py2
        cache = {(value,): 1}

        obj.cached_next(value)  # cache args

        clear_method_caches(obj)
        self.set_of_names_equal(obj, set())

        self.assertEqual(obj.cached_next(value), 1)
        self.set_of_names_equal(obj, {NAMES})
        self.assertEqual(getattr(obj, CACHE_NAME), cache)

    def test_clear_method_caches_with_missing_method(self):
        obj = Cached()
        method_name = "bar"
        cache_name = _build_cache_name(method_name)
        names = cache_name, method_name

        setattr(obj, cache_name, object())

        self.assertFalse(hasattr(obj, method_name))
        self.set_of_names_equal(obj, {names})

        clear_method_caches(obj)
        self.set_of_names_equal(obj, {names})
