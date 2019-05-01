# mode: error
# tag: posonly

def f(/, a = 1):
    pass

_ERRORS = u"""
4:6: Got zero positional-only arguments despite presence of positional-only specifier '/'
"""
