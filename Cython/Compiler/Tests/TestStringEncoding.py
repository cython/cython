# -*- coding: utf-8 -*-

import sys
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

        # This behaves differently in Py2 when freshly parsed and read from a .pyc file,
        # but it seems to be a parser bug in Py2, which doesn't hurt us in Cython.
        if sys.version_info[0] != 2:
            self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uDFFF\uD800"[::-1]))

        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uDFFF\uD800"))
        self.assertTrue(StringEncoding.string_contains_lone_surrogates(u"\uD800x\uDFFF"))

    def test_string_contains_surrogates(self):
        self.assertFalse(StringEncoding.string_contains_surrogates(u"abc"))
        self.assertFalse(StringEncoding.string_contains_surrogates(u"\uABCD"))
        self.assertFalse(StringEncoding.string_contains_surrogates(u"\N{SNOWMAN}"))

        self.assertTrue(StringEncoding.string_contains_surrogates(u"\uD800"))
        self.assertTrue(StringEncoding.string_contains_surrogates(u"\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_surrogates(u"\uD800\uDFFF"))
        self.assertTrue(StringEncoding.string_contains_surrogates(u"\uDFFF\uD800"))
        self.assertTrue(StringEncoding.string_contains_surrogates(u"\uD800x\uDFFF"))
