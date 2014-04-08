# http://www.opengroup.org/onlinepubs/009695399/basedefs/unistd.h.html

cdef extern from "unistd.h" nogil:

    #:NULL

    enum: R_OK
    enum: W_OK
    enum: X_OK
    enum: F_OK

    # confstr()
    #_CS_PATH
    #_CS_POSIX_*

    enum: SEEK_SET
    enum: SEEK_CUR
    enum: SEEK_END

    enum: F_LOCK
    enum: F_TEST
    enum: F_TLOCK
    enum: F_ULOCK

    # pathconf()
    # _PC_*

    # sysconf()
    # _SC_*

    enum: STDIN_FILENO	#0
    enum: STDOUT_FILENO	#1
    enum: STDERR_FILENO	#2

    #:ctypedef unsigned size_t
    #:ctypedef signed ssize_t
    ctypedef int uid_t
    ctypedef int gid_t
    ctypedef signed off_t
    ctypedef signed pid_t
    ctypedef unsigned useconds_t
    ctypedef signed intptr_t

    int          access(const char *, int)
    unsigned     alarm(unsigned)
    int          chdir(const char *)
    int          chown(const char *, uid_t, gid_t)
    int          close(int)
    size_t       confstr(int, char *, size_t)
    char        *crypt(const char *, const char *)
    char        *ctermid(char *)
    int          dup(int)
    int          dup2(int, int)
    void         encrypt(char[64], int)
    int          execl(const char *, const char *, ...)
    int          execle(const char *, const char *, ...)
    int          execlp(const char *, const char *, ...)
    int          execv(const char *, char *[])
    int          execve(const char *, char *[], char *[])
    int          execvp(const char *, char *[])
    void        _exit(int)
    int          fchown(int, uid_t, gid_t)
    int          fchdir(int)
    int          fdatasync(int)
    pid_t        fork()
    long         fpathconf(int, int)
    int          fsync(int)
    int          ftruncate(int, off_t)
    char        *getcwd(char *, size_t)
    gid_t        getegid()
    uid_t        geteuid()
    gid_t        getgid()
    int          getgroups(int, gid_t [])
    long         gethostid()
    int          gethostname(char *, size_t)
    char        *getlogin()
    int          getlogin_r(char *, size_t)
    int          getopt(int, char * [], const char *)
    pid_t        getpgid(pid_t)
    pid_t        getpgrp()
    pid_t        getpid()
    pid_t        getppid()
    pid_t        getsid(pid_t)
    uid_t        getuid()
    char        *getwd(char *)
    int          isatty(int)
    int          lchown(const char *, uid_t, gid_t)
    int          link(const char *, const char *)
    int          lockf(int, int, off_t)
    off_t        lseek(int, off_t, int)
    int          nice(int)
    long         pathconf(char *, int)
    int          pause()
    int          pipe(int [2])
    ssize_t      pread(int, void *, size_t, off_t)
    ssize_t      pwrite(int, const void *, size_t, off_t)
    ssize_t      read(int, void *, size_t)
    ssize_t      readlink(const char *, char *, size_t)
    int          rmdir(const char *)
    int          setegid(gid_t)
    int          seteuid(uid_t)
    int          setgid(gid_t)
    int          setpgid(pid_t, pid_t)
    pid_t        setpgrp()
    int          setregid(gid_t, gid_t)
    int          setreuid(uid_t, uid_t)
    pid_t        setsid()
    int          setuid(uid_t)
    unsigned     sleep(unsigned)
    void         swab(const void *, void *, ssize_t)
    int          symlink(const char *, const char *)
    void         sync()
    long         sysconf(int)
    pid_t        tcgetpgrp(int)
    int          tcsetpgrp(int, pid_t)
    int          truncate(const char *, off_t)
    char        *ttyname(int)
    int          ttyname_r(int, char *, size_t)
    useconds_t   ualarm(useconds_t, useconds_t)
    int          unlink(const char *)
    int          usleep(useconds_t)
    pid_t        vfork()
    ssize_t      write(int, const void *, size_t)
    char         *optarg
    int          optind
    int          opterr
    int          optopt
