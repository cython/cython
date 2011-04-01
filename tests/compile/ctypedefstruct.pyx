# mode: compile

ctypedef struct order:
    int spam
    int eggs

cdef order order1

order1.spam = 7
order1.eggs = 2

ctypedef struct linked:
    int a
    linked *next
