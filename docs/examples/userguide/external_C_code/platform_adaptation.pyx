cdef extern from *:
    """
    #if defined(_WIN32) || defined(MS_WINDOWS) || defined(_MSC_VER)
      #define WIN32_LEAN_AND_MEAN
      #include <windows.h>
      #define myapp_sleep(m)  Sleep(m)
    #else
      #include <unistd.h>
      #define myapp_sleep(m)  ((void) usleep((m) * 1000))
    #endif
    """
    # using "myapp_" prefix in the C code to prevent C naming conflicts
    void msleep "myapp_sleep"(int milliseconds) nogil

msleep(milliseconds=1)
