# ticket: 444
# mode: error

def test():
     cdef object[int] not_assigned_to
     not_assigned_to[2] = 3

_ERRORS = """
6:20: local variable 'not_assigned_to' referenced before assignment
"""
