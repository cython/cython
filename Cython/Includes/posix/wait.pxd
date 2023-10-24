# https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_wait.h.html

from posix.types cimport pid_t, id_t
from posix.signal cimport siginfo_t
from posix.resource cimport rusage

extern from "<sys/wait.h>" nogil:
    enum: WNOHANG
    enum: WUNTRACED
    enum: WCONTINUED
    enum: WEXITED
    enum: WSTOPPED
    enum: WNOWAIT

    int WEXITSTATUS(i32 status)
    int WIFCONTINUED(i32 status)
    int WIFEXITED(i32 status)
    int WIFSIGNALED(i32 status)
    int WIFSTOPPED(i32 status)
    int WSTOPSIG(i32 status)
    int WTERMSIG(i32 status)

    ctypedef i32 idtype_t
    enum: P_ALL             # idtype_t values
    enum: P_PID
    enum: P_PGID

    pid_t wait(i32 *stat_loc)
    pid_t waitpid(pid_t pid, i32 *status, i32 options)
    int waitid(idtype_t idtype, id_t id, siginfo_t *infop, i32 options)

# wait3 was in POSIX until 2008 while wait4 was never standardized.
# Even so, these calls are in almost every Unix, always in sys/wait.h.
# Hence, posix.wait is the least surprising place to declare them for Cython.
# libc may require _XXX_SOURCE to be defined at C-compile time to provide them.

    pid_t wait3(i32 *status, i32 options, rusage *rusage)
    pid_t wait4(pid_t pid, i32 *status, i32 options, rusage *rusage)
