# mode: error

fn void spam():
    None = 42

_ERRORS = u"""
4:4: Cannot assign to or delete this
"""
