# Test that variable visible outside of the local scope (e.g. closure, cglobals)
# is set before original value is decrefed.
cdef object g

def test_cglobals_reassignment():
    """
    >>> test_cglobals_reassignment()
    1234
    """
    global g
    class Special:
        def __del__(self):
            print g
    g = (Special(),)
    g = 1234

def test_closure_reassignment():
    """
    >>> test_closure_reassignment()
    4321
    """
    class Special:
        def __del__(self):
            print c
    c = (Special(),)
    c = 4321
