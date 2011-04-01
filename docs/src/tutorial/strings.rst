.. highlight:: cython

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
    cdef bytes py_string = c_string

This creates a Python byte string object that holds a copy of the
original C string.  It can be safely passed around in Python code, and
will be garbage collected when the last reference to it goes out of
scope.  It is important to remember that null bytes in the string act
as terminator character, as generally known from C.  The above will
therefore only work correctly for C strings that do not contain null
bytes.

Note that the creation of the Python bytes string can fail with an
exception, e.g. due to insufficient memory.  If you need to ``free()``
the string after the conversion, you should wrap the assignment in a
try-finally construct::

    cimport stdlib
    cdef bytes py_string
    cdef char* c_string = c_call_returning_a_c_string()
    try:
        py_string = c_string
    finally:
        stdlib.free(c_string)

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

The initially presented way of passing and receiving C strings is
sufficient if your code only deals with binary data in the strings.
When we deal with encoded text, however, it is best practice to decode
the C byte strings to Python Unicode strings on reception, and to
encode Python Unicode strings to C byte strings on the way out.

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
uses an encoding like UCS-4, where each character is encoded in four
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
to the Python byte string will fail with a compile error::

    # this will not compile !
    cdef char* c_string = py_unicode_string.encode('UTF-8')

Here, the Cython compiler notices that the code takes a pointer to a
temporary string result that will be garbage collected after the
assignment.  Later access to the invalidated pointer will read invalid
memory and likely result in a segfault.  Cython will therefore refuse
to compile this code.

Source code encoding
--------------------

When string literals appear in the code, the source code encoding is
important.  It determines the byte sequence that Cython will store in
the C code for bytes literals, and the Unicode code points that Cython
builds for unicode literals when parsing the byte encoded source file.
Following `PEP 263`_, Cython supports the explicit declaration of
source file encodings.  For example, putting the following comment at
the top of an ``ISO-8859-15`` (Latin-9) encoded source file (into the
first or second line) is required to enable ``ISO-8859-15`` decoding
in the parser::

    # -*- coding: ISO-8859-15 -*-

When no explicit encoding declaration is provided, the source code is
parsed as UTF-8 encoded text, as specified by `PEP 3120`_.  `UTF-8`_
is a very common encoding that can represent the entire Unicode set of
characters and is compatible with plain ASCII encoded text that it
encodes efficiently.  This makes it a very good choice for source code
files which usually consist mostly of ASCII characters.

.. _`PEP 263`: http://www.python.org/dev/peps/pep-0263/
.. _`PEP 3120`: http://www.python.org/dev/peps/pep-3120/
.. _`UTF-8`: http://en.wikipedia.org/wiki/UTF-8

As an example, putting the following line into a UTF-8 encoded source
file will print ``5``, as UTF-8 encodes the letter ``'ö'`` in the two
byte sequence ``'\xc3\xb6'``::

    print( len(b'abcö') )

whereas the following ``ISO-8859-15`` encoded source file will print
``4``, as the encoding uses only 1 byte for this letter::

    # -*- coding: ISO-8859-15 -*-
    print( len(b'abcö') )

Note that the unicode literal ``u'abcö'`` is a correctly decoded four
character Unicode string in both cases, whereas the unprefixed Python
``str`` literal ``'abcö'`` will become a byte string in Python 2 (thus
having length 4 or 5 in the examples above), and a 4 character Unicode
string in Python 3.  If you are not familiar with encodings, this may
not appear obvious at first read.  See `CEP 108`_ for details.

As a rule of thumb, it is best to avoid unprefixed non-ASCII ``str``
literals and to use unicode string literals for all text.  Cython also
supports the ``__future__`` import ``unicode_literals`` that instructs
the parser to read all unprefixed ``str`` literals in a source file as
unicode string literals, just like Python 3.

.. _`CEP 108`: http://wiki.cython.org/enhancements/stringliterals

Single bytes and characters
---------------------------

The Python C-API uses the normal C ``char`` type to represent a byte
value, but it has two special integer types for a Unicode code point
value, i.e. a single Unicode character: ``Py_UNICODE`` and
``Py_UCS4``.  Since version 0.13, Cython supports the first natively,
support for ``Py_UCS4`` is new in Cython 0.15.  ``Py_UNICODE`` is
either defined as an unsigned 2-byte or 4-byte integer, or as
``wchar_t``, depending on the platform.  The exact type is a compile
time option in the build of the CPython interpreter and extension
modules inherit this definition at C compile time.  The advantage of
``Py_UCS4`` is that it is guaranteed to be large enough for any
Unicode code point value, regardless of the platform.  It is defined
as a 32bit unsigned int or long.

In Cython, the ``char`` type behaves differently from the
``Py_UNICODE`` and ``Py_UCS4`` types when coercing to Python objects.
Similar to the behaviour of the bytes type in Python 3, the ``char``
type coerces to a Python integer value by default, so that the
following prints 65 and not ``A``::

    # -*- coding: ASCII -*-

    cdef char char_val = 'A'
    assert char_val == 65   # ASCII encoded byte value of 'A'
    print( char_val )

If you want a Python bytes string instead, you have to request it
explicitly, and the following will print ``A`` (or ``b'A'`` in Python
3)::

    print( <bytes>char_val )

The explicit coercion works for any C integer type.  Values outside of
the range of a ``char`` or ``unsigned char`` will raise an
``OverflowError`` at runtime.  Coercion will also happen automatically
when assigning to a typed variable, e.g.::

    cdef bytes py_byte_string
    py_byte_string = char_val

On the other hand, the ``Py_UNICODE`` and ``Py_UCS4`` types are rarely
used outside of the context of a Python unicode string, so their
default behaviour is to coerce to a Python unicode object.  The
following will therefore print the character ``A``, as would the same
code with the ``Py_UNICODE`` type::

    cdef Py_UCS4 uchar_val = u'A'
    assert uchar_val == 65 # character point value of u'A'
    print( uchar_val )

Again, explicit casting will allow users to override this behaviour.
The following will print 65::

    cdef Py_UCS4 uchar_val = u'A'
    print( <long>uchar_val )

Note that casting to a C ``long`` (or ``unsigned long``) will work
just fine, as the maximum code point value that a Unicode character
can have is 1114111 (``0x10FFFF``).  On platforms with 32bit or more,
``int`` is just as good.


Narrow Unicode builds
----------------------

In narrow Unicode builds of CPython, i.e. builds where
``sys.maxunicode`` is 65535 (such as all Windows builds, as opposed to
1114111 in wide builds), it is still possible to use Unicode character
code points that do not fit into the 16 bit wide ``Py_UNICODE`` type.
For example, such a CPython build will accept the unicode literal
``u'\U00012345'``.  However, the underlying system level encoding
leaks into Python space in this case, so that the length of this
literal becomes 2 instead of 1.  This also shows when iterating over
it or when indexing into it.  The visible substrings are ``u'\uD808'``
and ``u'\uDF45'`` in this example.  They form a so-called surrogate
pair that represents the above character.

For more information on this topic, it is worth reading the `Wikipedia
article about the UTF-16 encoding`_.

.. _`Wikipedia article about the UTF-16 encoding`: http://en.wikipedia.org/wiki/UTF-16/UCS-2

The same properties apply to Cython code that gets compiled for a
narrow CPython runtime environment.  In most cases, e.g. when
searching for a substring, this difference can be ignored as both the
text and the substring will contain the surrogates.  So most Unicode
processing code will work correctly also on narrow builds.  Encoding,
decoding and printing will work as expected, so that the above literal
turns into exactly the same byte sequence on both narrow and wide
Unicode platforms.

However, programmers should be aware that a single ``Py_UNICODE``
value (or single 'character' unicode string in CPython) may not be
enough to represent a complete Unicode character on narrow platforms.
For example, if an independent search for ``u'\uD808'`` and
``u'\uDF45'`` in a unicode string succeeds, this does not necessarily
mean that the character ``u'\U00012345`` is part of that string.  It
may well be that two different characters are in the string that just
happen to share a code unit with the surrogate pair of the character
in question.  Looking for substrings works correctly because the two
code units in the surrogate pair use distinct value ranges, so the
pair is always identifiable in a sequence of code points.

As of version 0.15, Cython has extended support for surrogate pairs so
that you can safely use an ``in`` test to search character values from
the full ``Py_UCS4`` range even on narrow platforms::

    cdef Py_UCS4 uchar = 0x12345
    print( uchar in some_unicode_string )

Similarly, it can coerce a one character string with a high Unicode
code point value to a Py_UCS4 value on both narrow and wide Unicode
platforms::

    cdef Py_UCS4 uchar = u'\U00012345'
    assert uchar == 0x12345


Iteration
---------

Cython 0.13 supports efficient iteration over ``char*``, bytes and
unicode strings, as long as the loop variable is appropriately typed.
So the following will generate the expected C code::

    cdef char* c_string = ...

    cdef char c
    for c in c_string[:100]:
        if c == 'A': ...

The same applies to bytes objects::

    cdef bytes bytes_string = ...

    cdef char c
    for c in bytes_string:
        if c == 'A': ...

For unicode objects, Cython will automatically infer the type of the
loop variable as ``Py_UCS4``::

    cdef unicode ustring = ...

    # NOTE: no typing required for 'uchar' !
    for uchar in ustring:
        if uchar == u'A': ...

The automatic type inference usually leads to much more efficient code
here.  However, note that some unicode operations still require the
value to be a Python object, so Cython may end up generating redundant
conversion code for the loop variable value inside of the loop.  If
this leads to a performance degradation for a specific piece of code,
you can either type the loop variable as a Python object explicitly,
or assign its value to a Python typed variable somewhere inside of the
loop to enforce one-time coercion before running Python operations on
it.

There are also optimisations for ``in`` tests, so that the following
code will run in plain C code, (actually using a switch statement)::

    cdef Py_UCS4 uchar_val = get_a_unicode_character()
    if uchar_val in u'abcABCxY':
        ...

Combined with the looping optimisation above, this can result in very
efficient character switching code, e.g. in unicode parsers.
