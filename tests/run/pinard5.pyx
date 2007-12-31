cdef class Tri:
    pass
    
cdef class Curseur:
    cdef Tri tri
    def detail(self):
        produire_fiches(self.tri)

cdef produire_fiches(Tri tri):
    pass
