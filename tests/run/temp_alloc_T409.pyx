__doc__ = """
    >>> foo()
    ([0, 0], [0, 0])
"""

# Extracted from sage/plot/plot3d/index_face_set.pyx:502
# Turns out to be a bug in implementation of PEP 3132 (Extended Iterable Unpacking)

def foo():
    a = b = [0,0]
    return a, b
