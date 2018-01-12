cdef extern from "<dlfcn.h>" nogil:
    
    int RTLD_LAZY 
    int RTLD_NOW 
    int RTLD_GLOBAL 
    int RTLD_LOCAL

    int dlclose(void *)
    char *dlerror()
    void *dlopen(const char *, int)
    void *dlsym(void *restrict, const char *restrict)

