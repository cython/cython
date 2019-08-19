# distutils: extra_compile_args=-Werror
# mode: compile

ctypedef bint mybool

cdef mybool c
cdef mybool x
c = True
x = True
x = not x if c else x
