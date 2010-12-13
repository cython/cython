cdef int tomato() except -1:
    print "Entering tomato"
    raise Exception("Eject! Eject! Eject!")
    print "Leaving tomato"

cdef void sandwich():
    print "Entering sandwich"
    tomato()
    print "Leaving sandwich"

def snack():
    print "Entering snack"
    tomato()
    print "Leaving snack"

def lunch():
    print "Entering lunch"
    sandwich()
    print "Leaving lunch"
