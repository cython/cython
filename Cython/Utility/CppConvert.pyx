# TODO: Figure out how many of the pass-by-value copies the compiler can eliminate.


#################### string.from_py ####################

cdef extern from *:
    cdef const char* __Pyx_PyObject_AsStringAndSize(object, Py_ssize_t*) except NULL

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef Py_ssize_t length = 0
    cdef const char* data = __Pyx_PyObject_AsStringAndSize(o, &length)
    return Tp(data, length)


#################### string.to_py ####################

{{for py_type in ['PyObject', 'PyUnicode', 'PyStr', 'PyBytes', 'PyByteArray']}}
cdef extern from *:
    cdef object __Pyx_{{py_type}}_FromStringAndSize(const char*, size_t)

@cname("{{cname.replace("PyObject", py_type, 1)}}")
cdef inline object {{cname.replace("PyObject", py_type, 1)}}(const Tp& s):
    return __Pyx_{{py_type}}_FromStringAndSize(s.data(), s.size())
{{endfor}}


#################### vector.from_py ####################

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef Tp v
    for item in o:
        v.push_back(<Tp.value_type>item)
    return v


#################### vector.to_py ####################

cdef extern from "Python.h":
    void Py_INCREF(object)
    list PyList_New(Py_ssize_t size)
    void PyList_SET_ITEM(object list, Py_ssize_t i, object o)
    cdef Py_ssize_t PY_SSIZE_T_MAX

@cname("{{cname}}")
cdef object {{cname}}(const Tp& v):
    if v.size() > <size_t> PY_SSIZE_T_MAX:
        raise MemoryError()

    o = PyList_New(<Py_ssize_t> v.size())

    cdef Py_ssize_t i
    cdef object item

    for i in range(v.size()):
        item = v[i]
        Py_INCREF(item)
        PyList_SET_ITEM(o, i, item)

    return o

#################### list.from_py ####################

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef Tp l
    for item in o:
        l.push_back(<Tp.value_type>item)
    return l


#################### list.to_py ####################

cimport cython

cdef extern from "Python.h":
    void Py_INCREF(object)
    list PyList_New(Py_ssize_t size)
    void PyList_SET_ITEM(object list, Py_ssize_t i, object o)
    cdef Py_ssize_t PY_SSIZE_T_MAX

@cname("{{cname}}")
cdef object {{cname}}(const Tp& v):
    if v.size() > <size_t> PY_SSIZE_T_MAX:
        raise MemoryError()

    o = PyList_New(<Py_ssize_t> v.size())

    cdef object item
    cdef Py_ssize_t i = 0
    cdef Tp.const_iterator iter = v.const_begin()

    while iter != v.end():
        item = cython.operator.dereference(iter)
        Py_INCREF(item)
        PyList_SET_ITEM(o, i, item)
        cython.operator.preincrement(iter)
        i += 1

    return o


#################### set.from_py ####################

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef Tp s
    for item in o:
        s.insert(<Tp.value_type>item)
    return s


#################### set.to_py ####################

cimport cython

@cname("{{cname}}")
cdef object {{cname}}(const Tp& s):
    # casting away the const is a bit dubious, but helps Cython do the iteration
    return {v for v in <Tp&>s}

#################### pair.from_py ####################

cdef extern from *:
    cdef cppclass pair "std::pair" [T, U]:
        pair() except +
        pair(T&, U&) except +

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    x, y = o
    return Tp(<Tp.first_type>x, <Tp.second_type>y)


#################### pair.to_py ####################

@cname("{{cname}}")
cdef object {{cname}}(const Tp& p):
    return p.first, p.second


#################### map.from_py ####################

cdef extern from *:
    cdef cppclass pair "std::pair" [T, U]:
        pair(T&, U&) except +


@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef dict d = o
    cdef Tp m
    for key, value in d.iteritems():
        m.insert(pair[Tp.key_type, Tp.mapped_type](<Tp.key_type>key, <Tp.mapped_type>value))
    return m


#################### map.to_py ####################

cimport cython

@cname("{{cname}}")
cdef object {{cname}}(const Tp& s):
    o = {}
    cdef const Tp.value_type *key_value
    cdef Tp.const_iterator iter = s.const_begin()
    while iter != s.const_end():
        key_value = &cython.operator.dereference(iter)
        o[key_value.first] = key_value.second
        cython.operator.preincrement(iter)
    return o


#################### complex.from_py ####################

@cname("{{cname}}")
cdef Tp {{cname}}(object o) except *:
    cdef double complex z = o
    return Tp(<Tp.value_type>z.real, <Tp.value_type>z.imag)


#################### complex.to_py ####################

@cname("{{cname}}")
cdef object {{cname}}(const Tp& z):
    cdef double complex tmp
    tmp.real = <double>z.real()
    tmp.imag = <double>z.imag()
    return tmp
