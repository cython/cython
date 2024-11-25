# mode: error

cimport cython

def f():
    o = object()
    with cython.critical_section():  # no arguments
        pass
    with cython.critical_section(o, o, o):  # Too many arguments (also the same argument, but we don't check for that)
        pass
    with cython.critical_section(please_ensure_thread_safety=True):  # While this keyword argument would be nice, it doesn't exist
        pass
    with cython.critical_section(1):  # C argument type
        pass
    with cython.critical_section(<void*>o):  # silly, but again, a C argument
        pass
    with nogil:
        with cython.critical_section(o):  # critical sections require the GIL
            pass

_ERRORS = """
7:9: critical_section directive accepts one or two positional arguments
9:9: critical_section directive accepts one or two positional arguments
11:9: critical_section directive accepts one or two positional arguments
13:33: Arguments to cython.critical_section must be Python objects.
15:33: Arguments to cython.critical_section must be Python objects.
18:13: Critical sections require the GIL
# slightly extraneous, but no real harm
18:37: Creating temporary Python reference not allowed without gil
"""
