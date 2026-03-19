# mode: error

def f(value):
    f"{[value + 1]]}"

_ERRORS = """
4:18: Unmatched ']'
"""
