# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def with_no_target(m):
    with m:
        print a
        a = 1

def unbound_manager(m1):
    with m2:
        pass
    m2 = m1

def with_target(m):
    with m as f:
        print(f)

def with_mgr(m):
    try:
        with m() as f:
            pass
    except:
        print f

_ERRORS = """
7:14: local variable 'a' referenced before assignment
11:9: local variable 'm2' referenced before assignment
24:14: local variable 'f' might be referenced before assignment
"""
