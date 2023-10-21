# mode: compile

cdef swallow

def spam(w, i32 x = 42, y = "grail", z = swallow):
    pass
