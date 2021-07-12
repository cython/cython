import unittest

from Cython.Utils import (
    _CACHE_METHOD_NAME, _METHOD_CACHE_PATTERN, build_hex_version,
    cached_function, cached_method, clear_function_caches, clear_method_caches,
    method_and_cache_names)

class TestCythonUtils(unittest.TestCase):
    def test_build_hex_version(self):
        self.assertEqual('0x001D00A1', build_hex_version('0.29a1'))
        self.assertEqual('0x001D03C4', build_hex_version('0.29.3rc4'))
        self.assertEqual('0x001D00F0', build_hex_version('0.29'))
        self.assertEqual('0x040000F0', build_hex_version('4.0'))
