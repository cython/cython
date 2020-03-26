"""
Non-test that prints debug information about the current build environment.
"""

from __future__ import print_function

import os
import sys
from distutils import sysconfig


cdef extern from *:
    """
    #ifndef PyLong_SHIFT
    #define PyLong_SHIFT 0
    typedef int digit;
    typedef int sdigit;
    #endif
    #ifndef PyLong_BASE
    #define PyLong_BASE 0
    #endif
    #ifndef PyLong_MASK
    #define PyLong_MASK 0
    #endif
    #ifndef SIZEOF_UINTPTR_T
    #define SIZEOF_UINTPTR_T 0
    #endif
    #ifndef SIZEOF_OFF_T
    #define SIZEOF_OFF_T 0
    #endif
    """
    # Python runtime
    cdef long PY_VERSION_HEX

    # Cython config
    cdef int CYTHON_COMPILING_IN_CPYTHON
    cdef int CYTHON_COMPILING_IN_PYPY
    cdef int CYTHON_COMPILING_IN_PYSTON
    cdef int CYTHON_USE_PYLONG_INTERNALS
    cdef int CYTHON_USE_PYLIST_INTERNALS
    cdef int CYTHON_USE_UNICODE_INTERNALS
    cdef int CYTHON_USE_UNICODE_WRITER
    cdef int CYTHON_AVOID_BORROWED_REFS
    cdef int CYTHON_ASSUME_SAFE_MACROS
    cdef int CYTHON_UNPACK_METHODS
    cdef int CYTHON_FAST_THREAD_STATE
    cdef int CYTHON_FAST_PYCALL
    cdef int CYTHON_PEP489_MULTI_PHASE_INIT
    cdef int CYTHON_USE_TP_FINALIZE

    # C and platform specifics
    cdef int SIZEOF_INT
    cdef int SIZEOF_LONG
    cdef int SIZEOF_SIZE_T
    cdef int SIZEOF_LONG_LONG
    cdef int SIZEOF_VOID_P
    cdef int SIZEOF_OFF_T
    cdef int SIZEOF_UINTPTR_T

    # PyLong internals
    cdef long PyLong_BASE
    cdef long PyLong_MASK
    cdef int PyLong_SHIFT
    cdef int digit
    cdef int sdigit


def config_var(name, default=''):
    return sysconfig.get_config_var(name) or default

get_env = os.environ.get


print(f"""Python build environment:
Python  {sys.version_info}
PY_VERSION_HEX  0x{PY_VERSION_HEX:X}

CYTHON_COMPILING_IN_CPYTHON  {CYTHON_COMPILING_IN_CPYTHON}
CYTHON_COMPILING_IN_PYPY  {CYTHON_COMPILING_IN_PYPY}
CYTHON_COMPILING_IN_PYSTON  {CYTHON_COMPILING_IN_PYSTON}

CYTHON_USE_PYLONG_INTERNALS  {CYTHON_USE_PYLONG_INTERNALS}
CYTHON_USE_PYLIST_INTERNALS  {CYTHON_USE_PYLIST_INTERNALS}
CYTHON_USE_UNICODE_INTERNALS  {CYTHON_USE_UNICODE_INTERNALS}
CYTHON_USE_UNICODE_WRITER  {CYTHON_USE_UNICODE_WRITER}
CYTHON_AVOID_BORROWED_REFS  {CYTHON_AVOID_BORROWED_REFS}
CYTHON_ASSUME_SAFE_MACROS  {CYTHON_ASSUME_SAFE_MACROS}
CYTHON_UNPACK_METHODS  {CYTHON_UNPACK_METHODS}
CYTHON_FAST_THREAD_STATE  {CYTHON_FAST_THREAD_STATE}
CYTHON_FAST_PYCALL  {CYTHON_FAST_PYCALL}
CYTHON_PEP489_MULTI_PHASE_INIT  {CYTHON_PEP489_MULTI_PHASE_INIT}
CYTHON_USE_TP_FINALIZE  {CYTHON_USE_TP_FINALIZE}

PyLong_BASE  0x{PyLong_BASE:X}
PyLong_MASK  0x{PyLong_MASK:X}
PyLong_SHIFT  {PyLong_SHIFT}
sizeof(digit)   {sizeof(digit)}
sizeof(sdigit)  {sizeof(sdigit)}
sys.int_info  {getattr(sys, 'int_info', '-')}
sys.getsizeof(1, 2**14, 2**15, 2**29, 2**30, 2**59, 2**60, 2**64)  {tuple(sys.getsizeof(n) for n in (1, 2**14, 2**15, 2**29, 2**30, 2**59, 2**60, 2**64))}

SIZEOF_INT  {SIZEOF_INT}  ({sizeof(int)})
SIZEOF_LONG  {SIZEOF_LONG}  ({sizeof(long)})
SIZEOF_SIZE_T  {SIZEOF_SIZE_T}  ({sizeof(Py_ssize_t)}, {getattr(sys, 'maxsize', getattr(sys, 'maxint', None))})
SIZEOF_LONG_LONG  {SIZEOF_LONG_LONG}  ({sizeof(long long)})
SIZEOF_VOID_P  {SIZEOF_VOID_P}  ({sizeof(void*)})
SIZEOF_UINTPTR_T  {SIZEOF_UINTPTR_T}  ({sizeof(unsigned int *)})
SIZEOF_OFF_T  {SIZEOF_OFF_T}

Distutils:
INCDIR = {sysconfig.get_python_inc()}
LIBS = {config_var('LIBS')}
LIBDIR = {config_var('LIBDIR')}
LIBPL = {config_var('LIBPL')}
Python LIBRARY = {config_var('LIBRARY')}
LINKFORSHARED = {config_var('LINKFORSHARED')}

CC (distutils) = {config_var('CC')}
CC (env) = {get_env('CC', '')}
CFLAGS (distutils) = {config_var('CFLAGS')}
CFLAGS (env) = {get_env('CFLAGS', '')}
LINKCC (distutils) = {config_var('LINKCC')}
LINKCC (env) = {get_env('LINKCC', '')}
""")
