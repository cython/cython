# mode: compile

ctypedef enum parrot_state:
    alive = 1
    dead = 2

cdef parrot_state polly

polly = dead

