# tag: cpp
# mode: compile

cdef extern from "cpp_nogil.h" nogil:
    cdef cppclass NoGilTest1:
        NoGilTest1()
        void doSomething()

# This is declared in cpp_nogil.h, but here we're testing
# that we can put nogil directly on the cppclass.
cdef extern from *:
    cdef cppclass NoGilTest2 nogil:
        NoGilTest2()
        void doSomething()

with nogil:
    NoGilTest1().doSomething()
    NoGilTest2().doSomething()

# We can override nogil methods as with gil methods.
cdef cppclass WithGilSubclass(NoGilTest1):
  void doSomething() noexcept with gil:
    print "have the gil"
