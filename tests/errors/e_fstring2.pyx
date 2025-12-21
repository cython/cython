# mode: error
# tag: fstring

# These tests are originally from test_fstring but moved here
# because the error comes from later in the pipeline so isn't detected there.

def bad_fstring_assignment(x):
    f'' = 3
    f'{0}' = x
    f'{x}' = x

def bad_starred_expression(a):
    f'{*a}'

_ERRORS = """
8:4: Cannot assign to or delete this
9:7: Cannot assign to or delete this
10:6: Cannot assign to or delete this
13:7: starred expression is not allowed here
"""
