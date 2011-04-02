# mode: error
# -*- coding: utf-8 -*-
# cython: language_level=3

escaped = b'abc\xc3\xbc\xc3\xb6\xc3\xa4'
invalid = b'abcüöä'

_ERRORS = """
6:10: bytes can only contain ASCII literal characters.
"""
