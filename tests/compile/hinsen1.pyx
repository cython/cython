__doc__ = """
    >>> test()
    1
"""

cdef extern from "hinsen1.h":

    ctypedef class spam.Spam [object PySpamObject]:
        pass


cdef class SpamAndEggs(Spam):

    cdef cook(self):
        return 1

def test():
    cdef SpamAndEggs s
    s = SpamAndEggs()
    return s.cook()
