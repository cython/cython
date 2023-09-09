# mode: compile

cdef swallow

def spam(w, int x = 42, y = "grail", z = swallow):
    pass

