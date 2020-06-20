# -*- coding: utf-8 -*-

import unittest

import Cython.Compiler.StringEncoding as StringEncoding


class StringEncodingTest(unittest.TestCase):
    """
    Test the StringEncoding module.
    """
    def test_string_contains_lone_surrogates(self):
        self.assertFalse(StringEncoding.string_contains_lone_surrogates(u"abc"))
        self.assertFalse(StringEncoding.string_contains_lone_surrogates(u"\uABCD"))
        self.assertFalse(StringEncoding.string_contains_lone_surrogates(u"\N{SNOWMAN}"))

        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uDFFF\uD800"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800x\uDFFF"))
