cdef extern from "hinsen1.h":

    ctypedef class spam.Spam [object PySpamObject]:
        pass


cdef class SpamAndEggs(Spam):

    cdef cook(self):
        pass
