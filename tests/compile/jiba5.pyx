# mode: compile

def f():
    cdef int i=0
    global mylist
    del mylist[i]
    return
