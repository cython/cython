# mode: compile
# tag: cpp, warnings

extern from "templates.h":
    cdef cppclass TemplateTest1[T]:
        TemplateTest1()
        T value
        i32 t
        T getValue()

    cdef cppclass TemplateTest1[T]

