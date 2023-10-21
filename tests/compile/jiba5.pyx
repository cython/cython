# mode: compile

def f():
    cdef i32 i=0
    global mylist
    del mylist[i]
    return
