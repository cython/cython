# mode: error

# very common mistake for new users (handled early by the parser)

def no_tuple_assignment():
    *a = [1]

_ERRORS = u"""
6:4: a starred assignment target must be in a list or tuple - maybe you meant to use an index assignment: var[0] = ...
"""
