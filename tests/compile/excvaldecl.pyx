# mode: compile

cdef i32 spam() except 42:
    pass

cdef f32 eggs() except 3.14:
    pass

cdef char *grail() except NULL:
    pass

cdef i32 tomato() except *:
    pass

cdef i32 brian() except? 0:
    pass

cdef i32 silly() except -1:
    pass

spam()
eggs()
grail()
tomato()
brian()
silly()
