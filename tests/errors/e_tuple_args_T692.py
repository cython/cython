# ticket: 692
# mode: error

def func((a, b)):
    return a + b

_ERRORS = u"""
4:9: Missing argument name
5:13: undeclared name not builtin: a
5:16: undeclared name not builtin: b
"""

