
from libc.stdio cimport sprintf
from cpython cimport PyType_Check
from cpython cimport PyType_Check as PyType_Check2
from cpython.type cimport PyType_Check as PyType_Check3

# Make sure we can cimport all .pxd files.
cimport cpython.array
cimport cpython.bool
cimport cpython.buffer
cimport cpython.bytearray
cimport cpython.bytes
cimport cpython.cellobject
cimport cpython.ceval
cimport cpython.codecs
cimport cpython.complex
cimport cpython.contextvars
cimport cpython.conversion
cimport cpython.datetime
cimport cpython.dict
cimport cpython.exc
cimport cpython.fileobject
cimport cpython.float
cimport cpython.function
cimport cpython.genobject
cimport cpython.getargs
cimport cpython.instance
cimport cpython.iterator
cimport cpython.iterobject
cimport cpython.list
cimport cpython.long
cimport cpython.longintrepr
cimport cpython.mapping
cimport cpython.marshal
cimport cpython.mem
cimport cpython.memoryview
cimport cpython.method
cimport cpython.module
cimport cpython.number
cimport cpython.object
cimport cpython.pycapsule
cimport cpython.pylifecycle
cimport cpython.pystate
cimport cpython.pythread
cimport cpython.ref
cimport cpython.sequence
cimport cpython.set
cimport cpython.slice
cimport cpython.tuple
cimport cpython.type
cimport cpython.unicode
cimport cpython.version
cimport cpython.weakref


def libc_cimports():
    """
    >>> libc_cimports()
    hello
    """
    cdef char[10] buf
    sprintf(buf, "%s", b'hello')
    print (<object>buf).decode('ASCII')


def cpython_cimports():
    """
    >>> cpython_cimports()
    True
    False
    True
    False
    True
    False
    """
    print PyType_Check(list)
    print PyType_Check([])
    print PyType_Check2(list)
    print PyType_Check2([])
    print PyType_Check3(list)
    print PyType_Check3([])

