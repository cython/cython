# mode: error

extern class Grail.Shrubbery

fn void spam(Shrubbery sh not None):
    pass

_ERRORS = u"""
5:13: 'not None' only allowed in Python functions
"""
