Caveats
=======

Since Cython mixes C and Python semantics, some things may be a bit
surprising or unintuitive. Work always goes on to make Cython more natural
for Python users, so this list may change in the future.

 - ``10**-2 == 0``, instead of ``0.01`` like in Python.
 - Given two typed ``int`` variables ``a`` and ``b``, ``a % b`` has the
   same sign as the second argument (following Python semantics) rather than
   having the same sign as the first (as in C).  The C behavior can be
   obtained, at some speed gain, by enabling the cdivision directive
   (versions prior to Cython 0.12 always followed C semantics).
 - Care is needed with unsigned types. ``cdef unsigned n = 10;
   print(range(-n, n))`` will print an empty list, since ``-n`` wraps
   around to a large positive integer prior to being passed to the
   ``range`` function.
 - Python's ``float`` type actually wraps C ``double`` values, and
   the ``int`` type in Python 2.x wraps C ``long`` values.
