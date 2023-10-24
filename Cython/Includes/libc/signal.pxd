# 7.14 Signal handling <signal.h>

ctypedef void (*sighandler_t)(i32 SIGNUM) noexcept nogil

extern from "<signal.h>" nogil:

    ctypedef i32 sig_atomic_t

    sighandler_t SIG_DFL
    sighandler_t SIG_IGN
    sighandler_t SIG_ERR

    sighandler_t signal        (i32 signum, sighandler_t action)
    int          raise_"raise" (i32 signum)

    # Signals
    enum:
        # Program Error
        SIGFPE
        SIGILL
        SIGSEGV
        SIGBUS
        SIGABRT
        SIGIOT
        SIGTRAP
        SIGEMT
        SIGSYS
        SIGSTKFLT
        # Termination
        SIGTERM
        SIGINT
        SIGQUIT
        SIGKILL
        SIGHUP
        # Alarm
        SIGALRM
        SIGVTALRM
        SIGPROF
        # Asynchronous I/O
        SIGIO
        SIGURG
        SIGPOLL
        # Job Control
        SIGCHLD
        SIGCLD
        SIGCONT
        SIGSTOP
        SIGTSTP
        SIGTTIN
        SIGTTOU
        # Operation Error
        SIGPIPE
        SIGLOST
        SIGXCPU
        SIGXFSZ
        SIGPWR
        # Miscellaneous
        SIGUSR1
        SIGUSR2
        SIGWINCH
        SIGINFO
        # Real-time signals
        SIGRTMIN
        SIGRTMAX
