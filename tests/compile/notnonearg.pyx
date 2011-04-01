# mode: compile

cdef extern class external.Spam [object Spam]: pass
cdef extern class external.Eggs [object Eggs]: pass

def ham(Spam s, Eggs e not None):
    pass
