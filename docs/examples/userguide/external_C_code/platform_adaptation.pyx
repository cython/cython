cdef extern from *:
    """
    #if defined(_WIN32) || defined(MS_WINDOWS) || defined(_MSC_VER)
      #include "stdlib.h"
      #define myapp_sleep(m)  _sleep(m)
    #else
      #include <unistd.h>
      #define myapp_sleep(m)  ((void) usleep((m) * 1000))
    #endif
    """
    # using "myapp_" prefix in the C code to prevent C naming conflicts
    void msleep "myapp_sleep"(int milliseconds) nogil

msleep(milliseconds=1)
