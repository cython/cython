cdef extern from "<dlfcn.h>" nogil:
    
    enum: RTLD_LAZY 
    enum: RTLD_NOW 
    enum：RTLD_GLOBAL 
    enum: RTLD_LOCAL

    int dlclose(void *)
    char *dlerror(void)
    void *dlopen(const char *, int)
    void *dlsym(void *restrict, const char *restrict)

