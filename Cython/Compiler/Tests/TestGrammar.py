# mode: run
# tag: syntax

"""
Uses TreeFragment to test invalid syntax.
"""

from __future__ import absolute_import

from ...TestUtils import CythonTest
from ..Errors import CompileError


VALID_UNDERSCORE_LITERALS = [
    # Copied from CPython's test_grammar.py
    '0_0_0',
    '4_2',
    '4_______2',
    '1_0000_0000',
    '0b_1001_0100',
    '0x_ffff_ffff',
    '0o_5_7_7',
    '1__.4',
    '42_j',
    '1.4_j',
    '1.4e5_j',
    '1_00_00_.5',
    '1_e10',
    '1_E10',
    '1_e1_0',
    '.1_4',
    '0_',
    '42_',
    '0b1_',
    '0xf_',
    '0o5_',
]

INVALID_UNDERSCORE_LITERALS = [
    # Copied from CPython's test_grammar.py
    # Trailing underscores:
    # Underscores in the base selector:
    '0_b0',
    '0_xf',
    '0_o5',
    # Old-style octal, still disallowed:
    #'0_7',
    #'09_99',
    # Underscore after non-digit:
    '1.4j_',
    '1.4e_1',
    '.1_4e_1',
    '1.0e+_1',
    '1._4',
    '1._4j',
    '1._4e5_j',
    '._5',
]


class TestGrammar(CythonTest):

    def test_invalid_number_literals(self):
        for literal in INVALID_UNDERSCORE_LITERALS:
            for expression in ['%s', '1 + %s', '%s + 1', '2 * %s', '%s * 2']:
                code = 'x = ' + expression % literal
                try:
                    self.fragment(u'''\
                    # cython: language_level=3
                    ''' + code)
                except CompileError as exc:
                    assert code in [s.strip() for s in str(exc).splitlines()], str(exc)
                else:
                    assert False, "Invalid Cython code '%s' failed to raise an exception" % code

    def test_valid_number_literals(self):
        for literal in VALID_UNDERSCORE_LITERALS:
            for expression in ['%s', '1 + %s', '%s + 1', '2 * %s', '%s * 2']:
                code = 'x = ' + expression % literal
                assert self.fragment(u'''\
                    # cython: language_level=3
                    ''' + code) is not None


if __name__ == "__main__":
    import unittest
    unittest.main()
