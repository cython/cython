# mode: compile
# tag: cpp,cpp11


cpdef enum class Spam:
    a, b
    c
    d
    e
    f = 42


cpdef enum class Cheese(unsigned int):
    x = 1
    y = 2


cdef enum struct parrot_state:
    alive = 1
    dead = 0


cdef void eggs():
    cdef Spam s1
    s1 = Spam.a
    s2 = Spam.b

    cdef Cheese c1
    c1 = Cheese.x

eggs()


# enum interdependency
cdef enum class Color(int):
    RED = 1
    GREEN = 2


cdef enum class Color2(int):
    RED = (<int> Color.RED)
    GREEN = (<int> Color.GREEN)


# enum class as cdef class function parameter
cdef class A:
    cdef Spam f(self, Spam s):
        return s
