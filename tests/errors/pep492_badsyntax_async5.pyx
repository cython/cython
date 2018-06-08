# mode: error
# tag: pep492, async

def foo():
    await list()

_ERRORS = """
5:10: Syntax error in simple statement list
"""
