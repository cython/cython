#
#   Cython wrapper for the cheesefinder API
#

cdef extern from "cheesefinder.h":
    ctypedef void (*cheesefunc)(char *name, void *user_data)
    void find_cheeses(cheesefunc user_func, void *user_data)

def find(f):
    find_cheeses(callback, <void*>f)

cdef void callback(char *name, void *f):
    (<object>f)(name.decode('utf-8'))

