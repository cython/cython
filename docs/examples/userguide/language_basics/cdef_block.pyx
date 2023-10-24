from __future__ import print_function

cdef:
    struct Spam:
        i32 tons

    i32 i
    f32 a
    Spam *p

    fn void f(Spam *s) except *:
        print(s.tons, "Tons of spam")
