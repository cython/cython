# mode: run
# tag: syntax

"""
Uses TreeFragment to test invalid syntax.
"""

from __future__ import absolute_import

from ...TestUtils import CythonTest
from ..Errors import CompileError

# Copied from CPython's test_grammar.py
VALID_UNDERSCORE_LITERALS = [
    '0_0_0',
    '4_2',
    '1_0000_0000',
    '0b1001_0100',
    '0xffff_ffff',
    '0o5_7_7',
    '1_00_00.5',
    '1e1_0',
    '.1_4',
]

# Copied from CPython's test_grammar.py
INVALID_UNDERSCORE_LITERALS = [
    # Trailing underscores:
    '0_',
    '42_',
    '1.4j_',
    '0b1_',
    '0xf_',
    '0o5_',
    # Underscores in the base selector:
    '0_b0',
    '0_xf',
    '0_o5',
    # Underscore right after the base selector:
    '0b_0',
    '0x_f',
    '0o_5',
    # Old-style octal, still disallowed:
    #'0_7',
    #'09_99',
    # Special case with exponent:
    '0 if 1_Else 1',
    # Underscore right before a dot:
    '1_.4',
    '1_.4j',
    # Underscore right after a dot:
    '1._4',
    '1._4j',
    '._5',
    # Underscore right after a sign:
    '1.0e+_1',
    # Multiple consecutive underscores:
    '4_______2',
    '0.1__4',
    '0b1001__0100',
    '0xffff__ffff',
    '0o5__77',
    '1e1__0',
    # Underscore right before j:
    '1.4_j',
    '1.4e5_j',
    # Underscore right before e:
    '1_e1',
    '1.4_e1',
    # Underscore right after e:
    '1e_1',
    '1.4e_1',
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
