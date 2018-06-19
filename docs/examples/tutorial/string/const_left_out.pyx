cdef extern from "someheader.h":
    int process_string(char* s)   # note: looses API information!
