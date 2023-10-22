from c_func cimport get_a_c_string

cdef char* c_string = NULL
cdef isize length = 0

# get pointer and length from a C function
get_a_c_string(&c_string, &length)

ustring = c_string[:length].decode('UTF-8')
