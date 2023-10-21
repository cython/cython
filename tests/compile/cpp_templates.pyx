# tag: cpp
# mode: compile
# ticket: t767

cdef extern from "templates.h":
    cdef cppclass TemplateTest1[T]:
        TemplateTest1()
        T value
        i32 t
        T getValue()

    cdef cppclass TemplateTest2[T, U]:
        TemplateTest2()
        T value1
        U value2
        T getValue1()
        U getValue2()

    void template_function[T](TemplateTest1[T] &)

cdef TemplateTest1[int] a
cdef TemplateTest1[int]* b = new TemplateTest1[int]()

cdef int c = a.getValue()
c = b.getValue()

cdef TemplateTest2[i32, i8] d
cdef TemplateTest2[i32, i8]* e = new TemplateTest2[i32, i8]()

c = d.getValue1()
c = e.getValue2()

cdef i8 f = d.getValue2()
f = e.getValue2()

del b, e

ctypedef TemplateTest1[i32] TemplateTest1_int
cdef TemplateTest1_int aa

# Verify that T767 is fixed.
cdef pub i32 func(i32 arg):
    return arg

# Regression test: the function call used to produce
#   template_function<TemplateTest1<int>>(__pyx_v_t);
# which is valid C++11, but not valid C++98 because the ">>" would be
# parsed as a single token.
cdef pub void use_nested_templates():
    cdef TemplateTest1[TemplateTest1[i32]] t
    template_function(t)
