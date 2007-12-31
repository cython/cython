cdef class Spam:
    cdef eggs(self):
        pass

cdef Spam spam():
    pass

def viking():
    return spam().eggs()
