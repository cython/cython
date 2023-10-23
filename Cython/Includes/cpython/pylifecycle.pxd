# Interfaces to configure, query, create & destroy the Python runtime

from libc.stdio cimport FILE
from .pystate cimport PyThreadState

extern from "Python.h":
    ctypedef i32 wchar_t

    void Py_SetProgramName(wchar_t *)
    wchar_t *Py_GetProgramName()

    void Py_SetPythonHome(wchar_t *)
    wchar_t *Py_GetPythonHome()

    # Only used by applications that embed the interpreter and need to
    # override the standard encoding determination mechanism
    int Py_SetStandardStreamEncoding(const char *encoding, const char *errors)

    void Py_Initialize()
    void Py_InitializeEx(i32)
    void _Py_InitializeEx_Private(i32, i32)
    void Py_Finalize()
    i32 Py_FinalizeEx()
    i32 Py_IsInitialized()
    PyThreadState *Py_NewInterpreter()
    void Py_EndInterpreter(PyThreadState *)

    # _Py_PyAtExit is for the atexit module, Py_AtExit is for low-level
    # exit functions.
    void _Py_PyAtExit(void (*func)(object), object)
    i32 Py_AtExit(void (*func)())

    void Py_Exit(int)

    # Restore signals that the interpreter has called SIG_IGN on to SIG_DFL.
    void _Py_RestoreSignals()

    i32 Py_FdIsInteractive(FILE *, const char *)

    # Bootstrap __main__ (defined in Modules/main.c)
    i32 Py_Main(i32 argc, wchar_t **argv)

    # In getpath.c
    wchar_t *Py_GetProgramFullPath()
    wchar_t *Py_GetPrefix()
    wchar_t *Py_GetExecPrefix()
    wchar_t *Py_GetPath()
    void Py_SetPath(const wchar_t *)
    i32 _Py_CheckPython3()

    # In their own files
    const char *Py_GetVersion()
    const char *Py_GetPlatform()
    const char *Py_GetCopyright()
    const char *Py_GetCompiler()
    const char *Py_GetBuildInfo()
    const char *_Py_gitidentifier()
    const char *_Py_gitversion()

    ctypedef void (*PyOS_sighandler_t)(i32)
    PyOS_sighandler_t PyOS_getsig(i32)
    PyOS_sighandler_t PyOS_setsig(i32, PyOS_sighandler_t)

    # Random
    i32 _PyOS_URandom(void *buffer, isize size)
    i32 _PyOS_URandomNonblock(void *buffer, isize size)
