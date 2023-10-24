cdef i32 g = 7

def test(x, i32 y):
    """
    >>> test(1, 2)
    4 1 2 2 0 7 8
    """
    if True:
        before = 0
    let i32 a = 4, b = x, c = y
    let i32 *p = &y
    let object o = int(8)
    print a, b, c, p[0], before, g, o

# Also test that pruning cdefs doesn't hurt
def empty():
    let i32 i
