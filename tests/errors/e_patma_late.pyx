# mode: error

# These tests are taken from test_patma. They're skipped there because
# the errors are emitted too late in the compilation process to be
# caught by the test mechanism.

class Class:
    pass

match ...:
    case {"a": _, "a": _}:
        pass
match ...:
    case {0: _, False: _}:
        pass
match ...:
    case {0: _, 0.0: _}:
        pass
match ...:
    case {0: _, -0: _}:
        pass
match ...:
    case {0: _, 0j: _}:
        pass
match ...:
    case Class(a=_, a=_):
        pass


_ERRORS = """
11:18: mapping pattern checks duplicate key (a)
14:16: mapping pattern checks duplicate key (False)
17:16: mapping pattern checks duplicate key (0.0)
20:16: mapping pattern checks duplicate key (0)
23:16: mapping pattern checks duplicate key (0j)
26:9: attribute name repeated in class pattern: 'a'
"""
