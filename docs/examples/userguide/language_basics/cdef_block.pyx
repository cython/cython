from __future__ import print_function

cdef:
    struct Spam:
        int tons

    int i
    float a
    Spam *p

    void f(Spam *s) except *:
        print(s.tons, "Tons of spam")
