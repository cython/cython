# tag: cpp
# mode: compile

cdef extern from "templates.h":
    cdef cppclass TemplateTest1[T]:
        TemplateTest1()
        T value
        int t
        T getValue()

    cdef cppclass TemplateTest2[T, U]:
        TemplateTest2()
        T value1
        U value2
        T getValue1()
        U getValue2()

cdef TemplateTest1[int] a
cdef TemplateTest1[int]* b = new TemplateTest1[int]()

cdef int c = a.getValue()
c = b.getValue()

cdef TemplateTest2[int, char] d
cdef TemplateTest2[int, char]* e = new TemplateTest2[int, char]()

c = d.getValue1()
c = e.getValue2()

cdef char f = d.getValue2()
f = e.getValue2()

del b, e

ctypedef TemplateTest1[int] TemplateTest1_int
cdef TemplateTest1_int aa

