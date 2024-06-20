# mode: error
# tag: or, binop, warnings

def test_or(a, b):
    return a || b


_WARNINGS = """
5:13: Found the C operator '||', did you mean the Python operator 'or'?
"""

_ERRORS = """
5:13: Syntax error in simple statement list
"""
