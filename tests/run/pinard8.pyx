cdef class Fiche:

    def __setitem__(self, element, valeur):
        if valeur is None:
            return
