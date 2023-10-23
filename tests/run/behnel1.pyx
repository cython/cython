cdef class Spam:
    fn eggs(self, a):
        return a

fn Spam spam():
    return Spam()

def viking(a):
    """
    >>> viking(5)
    5
    """
    return spam().eggs(a)
