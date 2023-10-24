# mode: compile
# tag: cpp,cpp11

cpdef enum class Spam:
    a, b
    c
    d
    e
    f = 42

cpdef enum class Cheese(u32):
    x = 1
    y = 2

cdef enum struct parrot_state:
    alive = 1
    dead = 0

fn void eggs():
    let Spam s1
    s1 = Spam.a
    s2 = Spam.b

    let Cheese c1
    c1 = Cheese.x

eggs()

# enum interdependency
cdef enum class Color(i32):
    RED = 1
    GREEN = 2

cdef enum class Color2(i32):
    RED = (<i32>Color.RED)
    GREEN = (<i32>Color.GREEN)

# enum class as cdef class function parameter
cdef class A:
    fn Spam f(self, Spam s):
        return s
