def function_without_typing(a, b):
    # c is a Python integer here, matching the behavior when annotations are ignored.
    c = a + b
    return c * a




cdef class NotAnnotatedClass:
    cdef object d

    def __init__(self, dictionary):
        self.d = dictionary

    # Method where C types are explicitly declared.
    cpdef annotated_method(self, str key, int a, int b):
        cdef str prefixed_key = 'prefix_' + key
        self.d[prefixed_key] = a + b


cpdef list annotated_function(int a, int b):
    cdef int s = a + b
    
    # In the original, 'c' was ignored, making it a Python list.
    cdef list c = []
    
    c.append(a)
    c.append(b)
    c.append(s)
    return c