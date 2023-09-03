# mode: compile
# tag: test_in_limited_api

cdef swallow

def spam(w, int x = 42, y = "grail", z = swallow):
    pass

