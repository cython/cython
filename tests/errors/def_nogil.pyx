# mode: error

def test() nogil:
    pass

_ERRORS = """
3:0: Python function cannot be declared nogil
"""
