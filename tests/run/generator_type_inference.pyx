# mode: run
# tag: typeinference, generators

cimport cython

def test_type_inference():
    """
    >>> [ item for item in test_type_inference() ]
    [(2.0, 'double'), (2.0, 'double'), (2.0, 'double')]
    """
    x = 1.0
    for i in range(3):
        yield x * 2.0, cython.typeof(x)
