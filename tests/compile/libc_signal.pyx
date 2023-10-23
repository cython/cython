# mode: compile

from libc.signal cimport *

fn void sighdl(i32 signum) noexcept nogil:
    pass

cdef sighandler_t h

h = signal(SIGABRT, sighdl)
if h == SIG_ERR: pass
h = signal(SIGABRT, SIG_IGN)
if h == SIG_ERR: pass
h = signal(SIGABRT, SIG_DFL)
if h == SIG_ERR: pass

h = signal(SIGABRT, SIG_IGN)
cdef i32 e = raise_(SIGABRT)
h = signal(SIGABRT, h)
