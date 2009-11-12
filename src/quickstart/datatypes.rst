Data types in Cython
====================

Cython is a Python compiler.  This means that it can compile normal
Python code without changes (with a few obvious exceptions of some as-yet
unsupported language features).  However, for performance critical
code, it is often helpful to add static type declarations, as they
will allow Cython to step out of the dynamic nature of the Python code
and generate simpler and faster C code - sometimes faster by orders of
magnitude.

It must be noted, however, that type declarations can make the source
code more verbose and thus less readable.  It is therefore discouraged
to use them without good reason, such as where benchmarks prove
that they really make the code substantially faster in a performance
critical section. Typically a few types in the right spots go a long way.

All C types are available for type declarations: integer and floating
point types, complex numbers, structs, unions and pointer types.
Cython can automatically and correctly convert between the types on
assignment.  This also includes Python's arbitrary size integer types,
where value overflows on conversion to a C type will raise a Python
``OverflowError`` at runtime.  The generated C code will handle the
platform dependent sizes of C types correctly and safely in this case.
