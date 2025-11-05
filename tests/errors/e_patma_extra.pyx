# mode: error

def test_invalid_tuplelike(x):
    match x:
        case (*x):  # (*x,) would be correct
            # Note that we give a better error message than cpython 3.11
            # (so the exact text isn't a copy of cpython's)
            return True

_ERRORS = """
5:16: tuple-like pattern of length 1 must finish with ','
"""
