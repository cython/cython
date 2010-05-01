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

Decoding bytes to text
----------------------

The above way of passing and receiving C strings is as simple that
that, as long as we only deal with binary data in the strings.  When
we deal with encoded text, however, it is best practice to decode the C byte
strings to Python Unicode strings on reception, and to encode Python
Unicode strings to C byte strings on the way out.

With a Python byte string object, you would normally just call the
``.decode()`` method to decode it into a Unicode string::

    ustring = byte_string.decode('UTF-8')

Cython allows you to do the same for a C string, as long as it
contains no null bytes::

    cdef char* some_c_string = c_call_returning_a_c_string()
    ustring = some_c_string.decode('UTF-8')

However, this will not work for strings that contain null bytes, and
it is very inefficient for long strings, since Cython has to call
``strlen()`` on the C string first to find out the length by counting
the bytes up to the terminating null byte.  In many cases, the user
code will know the length already, e.g. because a C function returned
it.  In this case, it is much more efficient to tell Cython the exact
number of bytes by slicing the C string::

    cdef char* c_string = NULL
    cdef Py_ssize_t length = 0

    # get pointer and length from a C function
    get_a_c_string(&c_string, &length)

    ustring = c_string[:length].decode('UTF-8')

The same can be used when the string contains null bytes, e.g. when it
uses an encoding like UCS-2, where each character is encoded as two
bytes.

It is common practice to wrap string conversions (and non-trivial type
conversions in general) in dedicated functions, as this needs to be
done in exactly the same way whenever receiving text from C.  This
could look as follows::

    cimport python_unicode
    cimport stdlib

    cdef unicode tounicode(char* s):
        return s.decode('UTF-8', 'strict')

    cdef unicode tounicode_with_length(
            char* s, size_t length):
        return s[:length].decode('UTF-8', 'strict')

    cdef unicode tounicode_with_length_and_free(
            char* s, size_t length):
        try:
            return s[:length].decode('UTF-8', 'strict')
        finally:
            stdlib.free(s)

Most likely, you will prefer shorter function names in your code based
on the kind of string being handled.  Different types of content often
imply different ways of handling them on reception.  To make the code
more readable and to anticipate future changes, it is good practice to
use separate conversion functions for different types of strings.

Encoding text to bytes
----------------------

The reverse way, converting a Python unicode string to a C ``char*``,
is pretty efficient by itself, assuming that what you actually want is
a memory managed byte string::

    py_byte_string = py_unicode_string.encode('UTF-8')
    cdef char* c_string = py_byte_string

As noted before, this takes the pointer to the byte buffer of the
Python byte string.  Trying to do the same without keeping a reference
to the intermediate byte string will fail with a compile error::

    # this will not compile !
    cdef char* c_string = py_unicode_string.encode('UTF-8')

Here, the Cython compiler notices that the code takes a pointer to a
temporary string result that will be garbage collected after the
assignment.  Later access to the invalidated pointer will most likely
result in a crash.  Cython will therefore refuse to compile this code.

Single bytes and characters
---------------------------

The Python C-API uses the normal C ``char`` type to represent a byte
value, but it has a special ``Py_UNICODE`` integer type for a Unicode
code point value, i.e. a single Unicode character.  Since version
0.13, Cython supports the latter natively, which is either defined as
an unsigned 2-byte or 4-byte integer, or as ``wchar_t``, depending on
the platform.  The exact type is a compile time option in the build of
the CPython interpreter.

In Cython, the ``char`` and ``Py_UNICODE`` types behave differently
when coercing to Python objects.  Similar to the behaviour of the
bytes type in Python 3, the ``char`` type coerces to a Python integer
value by default, so that the following prints 65 and not ``A``::

    cdef char char_val = 'A'
    assert char_val == 65   # 'A'
    print( char_val )

If you want a Python bytes string instead, you have to request it
explicitly, and the following will print ``A`` (or ``b'A'`` in Python
3)::

    print( <bytes>char_val )

The coercion will also happen automatically when assigning to a typed
variable, e.g.::

    cdef bytes py_byte_string = char_val

On the other hand, the ``Py_UNICODE`` type is rarely used outside of
the context of a Python unicode string, so its default behaviour is to
coerce to a Python unicode object.  The following will therefore print
the character ``A``::

    cdef Py_UNICODE uchar_val = u'A'
    assert uchar_val == ord(u'A')  # 65
    print( uchar_val )

Again, explicit casting will allow users to override this behaviour.
The following will print 65::

    cdef Py_UNICODE uchar_val = u'A'
    print( <int>uchar_val )

Note that casting to a C ``int`` (or ``unsigned int``) will do just
fine on a platform with 32bit or more, as the maximum code point value
that a Unicode character can have is 1114111 on a 4-byte unicode
CPython platform ("wide unicode") and 65535 on a 2-byte unicode
platform.

Iteration
---------

Cython 0.13 supports efficient iteration over ``char*``, bytes and
unicode strings, as long as the loop variable is appropriately typed.
So the following will generate the expected C code::

    cdef char* c_string = c_call_returning_a_c_string()

    cdef char c
    for c in c_string[:100]:
        if c == 'A': ...

The same applies to unicode objects::

    cdef unicode ustring = ...

    cdef Py_UNICODE uchar
    for uchar in ustring:
        if uchar == u'A': ...

There is also an optimisation for ``in`` tests, so that the following
code will run in plain C code::

    cdef Py_UNICODE uchar_val = get_a_unicode_character()
    if uchar_val in u'abcABCxY':
        ...

