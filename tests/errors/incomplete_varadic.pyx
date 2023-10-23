# mode: error

fn error_time(bool its_fine, .):
    pass

_ERRORS = u"""
3:29: Expected an identifier, found '.'
"""
