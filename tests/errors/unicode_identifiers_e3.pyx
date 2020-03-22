# -*- coding: utf-8 -*-
# mode: error

def f():
    a = 1
    ́b = 2 # looks like an indentation error but is actually a combining accent as the first letter of column 4
    c = 3

_ERRORS = u"""
6:4: Unrecognized character
"""
