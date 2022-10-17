# mode: error
# tag: and, binop, warnings

def test_and(a, b):
    return a && b


_WARNINGS = """
5:13: Found the C operator '&&', did you mean the Python operator 'and'?
"""

_ERRORS = """
5:13: Syntax error in simple statement list
"""
