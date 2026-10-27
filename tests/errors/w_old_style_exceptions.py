# mode: compile
# tag: warnings

# cython: language_level=3

def f(callable):
    try:
        callable()
    except TypeError, RuntimeError:
        pass

_WARNINGS = """
9:20: Using a Python-2 style except clause with language_level 3. This will be interpreted as a list of exceptions in a future release.
"""
