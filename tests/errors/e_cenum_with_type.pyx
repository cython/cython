# mode: error

enum Spam(i32):
    A, B

_ERRORS = u"""
3:9: Expected ':', found '('
"""
