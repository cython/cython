# tag: cpp
# mode: compile

cdef extern from "templates.h":
    cdef cppclass TemplateTest1[T]:
        TemplateTest1()
        T value
        int t
        T getValue()

    cdef cppclass TemplateTest1[T]

