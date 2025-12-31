# mode: error

def f(value):
    f"{(value +)) 1} yy"

_ERRORS = """
4:16: Unmatched ')'
"""