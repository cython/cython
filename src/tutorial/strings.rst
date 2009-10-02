Unicode and passing strings
===========================

Similar to the string semantics in Python 3, Cython also strictly
separates byte strings and unicode strings.  Above all, this means
that there is no automatic conversion between byte strings and unicode
strings (except for what Python 2 does in string operations).  All
encoding and decoding must pass through an explicit encoding/decoding
step.

It is, however, very easy to pass byte strings between C code and Python.
When receiving a byte string from a C library, you can let Cython
convert it into a Python byte string by simply assigning it to a
Python variable::

    cdef char* c_string = c_call_returning_a_c_string()
    py_string = c_string

This creates a Python byte string object that holds a copy of the
original C string.  It can be safely passed around in Python code, and
will be garbage collected when the last reference to it goes out of
scope.

To convert the byte string back into a C ``char*``, use the opposite
assignment::

    cdef char* other_c_string = py_string

This is a very fast operation after which ``other_c_string`` points to
the byte string buffer of the Python string itself.  It is tied to the
life time of the Python string.  When the Python string is garbage
collected, the pointer becomes invalid.  It is therefore important to
keep a reference to the Python string as long as the ``char*`` is in
use.  Often enough, this only spans the call to a C function that
receives the pointer as parameter.  Special care must be taken,
however, when the C function stores the pointer for later use.  Apart
from keeping a Python reference to the string, no manual memory
management is required.

The above way of passing and receiving C strings is as simple that
that, as long as we only deal with binary data in the strings.  When
we deal with encoded text, however, it is best practice to decode the C byte
strings to Python Unicode strings on reception, and to encode Python
Unicode strings to C byte strings on the way out.

With a Python byte string object, you would normally just call the
``.decode()`` method to decode it into a Unicode string::

    ustring = byte_string.decode('UTF-8')

You can do the same in Cython for a C string, but the generated code
is rather inefficient for small strings.
While Cython could potentially call the Python
C-API function for decoding a C string from UTF-8 to Unicode
(``PyUnicode_DecodeUTF8()``), the problem is that this requires
passing the length of the C string, which Cython cannot know at
compile time nor runtime.  So it would have to call ``strlen()``
first, although the user code will already know the length of the
string in almost all cases.  Also, the encoded byte string might
actually contain null bytes, so this isn't even a safe solution.  It
is therefore currently recommended to call the API functions directly::

    # .pxd file that comes with Cython
    cimport python_unicode

    cdef char* c_string = NULL
    cdef Py_ssize_t length = 0

    # get pointer and length from a C function
    get_a_c_string(&c_string, &length)

    # decode the string to Unicode
    ustring = python_unicode.PyUnicode_DecodeUTF8(
        c_string, length, 'strict')

It is common practice to wrap this in a dedicated function, as this
needs to be done whenever receiving text from C.  This could look as
follows::

    cimport python_unicode
    cimport stdlib
    cdef extern from "string.h":
        size_t strlen(char *s)

    cdef unicode tounicode(char* s):
        return python_unicode.PyUnicode_DecodeUTF8(
            s, strlen(s), 'strict')

    cdef unicode tounicode_with_length(
            char* s, size_t length):
        return python_unicode.PyUnicode_DecodeUTF8(
            s, length, 'strict')

    cdef unicode tounicode_with_length_and_free(
            char* s, size_t length):
        try:
            return python_unicode.PyUnicode_DecodeUTF8(
                s, length, 'strict')
        finally:
            stdlib.free(s)

Most likely, you will prefer shorter function names in your code based
on the kind of string being handled.  Different types of content often
imply different ways of handling them on reception.  To make the code
more readable and to anticipate future changes, it is good practice to
use separate conversion functions for different types of strings.

The reverse way, converting a Python unicode string to a C ``char*``,
is pretty efficient by itself, assuming that what you actually want is
a memory managed byte string::

    py_byte_string = py_unicode_string.encode('UTF-8')
    cdef char* c_string = py_byte_string

As noted above, this takes the pointer to the byte buffer of the
Python byte string.  Trying to do the same without keeping a reference
to the intermediate byte string will fail with a compile error::

    # this will not compile !
    cdef char* c_string = py_unicode_string.encode('UTF-8')

Here, the Cython compiler notices that the code takes a pointer to a
temporary string result that will be garbage collected after the
assignment.  Later access to the invalidated pointer will most likely
result in a crash.  Cython will therefore refuse to compile this code.
