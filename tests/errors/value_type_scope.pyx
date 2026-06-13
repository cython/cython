# mode: error
cimport cython

@cython.value_type
def foo():
    pass

@cython.value_type
class Bar:
    pass


_ERRORS = """
4:0: The value_type compiler directive is not allowed in function scope
9:0: The value_type compiler directive is not allowed in class scope
"""
