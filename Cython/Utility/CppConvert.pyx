# TODO: Figure out how many of the pass-by-value copies the compiler can eliminate.


#################### string.from_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_string "{{type}}":
        __pyx_cpp_string() except +
        __pyx_cpp_string(char* c_str, size_t size) except +
    cdef const char* __Pyx_PyObject_AsStringAndSize(object, Py_ssize_t*) except NULL

@cname("{{cname}}")
cdef __pyx_cpp_string {{cname}}(object o) except *:
    cdef Py_ssize_t length = 0
    cdef const char* data = __Pyx_PyObject_AsStringAndSize(o, &length)
    return __pyx_cpp_string(data, <size_t> length)


#################### string.to_py ####################

#cimport cython
#from libcpp.string cimport string as __pyx_cpp_string
cdef extern from *:
    const Py_ssize_t PY_SSIZE_T_MAX
    cdef cppclass __pyx_cpp_string "{{type}}":
        char* data()
        size_t size()

{{for py_type in ['PyObject', 'PyUnicode', 'PyBytes', 'PyByteArray']}}
cdef extern from *:
    cdef object __Pyx_{{py_type}}_FromStringAndSize(const char*, size_t)

@cname("{{cname.replace("PyObject", py_type, 1)}}")
cdef inline object {{cname.replace("PyObject", py_type, 1)}}(const __pyx_cpp_string& s):
    if s.size() > <size_t> PY_SSIZE_T_MAX:
        raise MemoryError()
    return __Pyx_{{py_type}}_FromStringAndSize(s.data(), <Py_ssize_t> s.size())
{{endfor}}


#################### vector.from_py ####################
#@requires: ObjectHandling.c::LengthHint

cdef extern from *:
    cdef cppclass __pyx_cpp_vector "std::vector" [T]:
        void push_back(T&) except +
        void reserve(size_t) except +

    cdef Py_ssize_t __Pyx_PyObject_LengthHint(object o, Py_ssize_t defaultval) except -1

@cname("{{cname}}")
cdef __pyx_cpp_vector[X] {{cname}}(object o) except *:

    cdef __pyx_cpp_vector[X] v
    cdef Py_ssize_t s = __Pyx_PyObject_LengthHint(o, 0)

    if s > 0:
        v.reserve(<size_t> s)

    for item in o:
        v.push_back(<X>item)

    return v


#################### vector.to_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_vector "std::vector" [T]:
        size_t size()
        T& operator[](size_t)

cdef extern from "Python.h":
    void Py_INCREF(object)
    object PyList_New(Py_ssize_t size)
    int __Pyx_PyList_SET_ITEM(object pylist, Py_ssize_t i, object o) except -1
    const Py_ssize_t PY_SSIZE_T_MAX

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_vector[X]& v):
    if v.size() > <size_t> PY_SSIZE_T_MAX:
        raise MemoryError()
    v_size_signed = <Py_ssize_t> v.size()

    o = PyList_New(v_size_signed)

    cdef Py_ssize_t i
    cdef object item

    for i in range(v_size_signed):
        item = v[i]
        Py_INCREF(item)
        __Pyx_PyList_SET_ITEM(o, i, item)

    return o

#################### list.from_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_list "std::list" [T]:
        void push_back(T&) except +

@cname("{{cname}}")
cdef __pyx_cpp_list[X] {{cname}}(object o) except *:
    cdef __pyx_cpp_list[X] l
    for item in o:
        l.push_back(<X>item)
    return l


#################### list.to_py ####################

cimport cython

cdef extern from *:
    cdef cppclass __pyx_cpp_list "std::list" [T]:
        cppclass const_iterator:
            T& operator*()
            const_iterator operator++()
            bint operator!=(const_iterator)
        const_iterator begin()
        const_iterator end()
        size_t size()

cdef extern from "Python.h":
    void Py_INCREF(object)
    object PyList_New(Py_ssize_t size)
    void __Pyx_PyList_SET_ITEM(object pylist, Py_ssize_t i, object o)
    cdef Py_ssize_t PY_SSIZE_T_MAX

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_list[X]& v):
    if v.size() > <size_t> PY_SSIZE_T_MAX:
        raise MemoryError()

    o = PyList_New(<Py_ssize_t> v.size())

    cdef object item
    cdef Py_ssize_t i = 0
    cdef __pyx_cpp_list[X].const_iterator iter = v.begin()

    while iter != v.end():
        item = cython.operator.dereference(iter)
        Py_INCREF(item)
        __Pyx_PyList_SET_ITEM(o, i, item)
        cython.operator.preincrement(iter)
        i += 1

    return o


#################### set.from_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_set "std::{{maybe_unordered}}set" [T]:
        void insert(T&) except +

@cname("{{cname}}")
cdef __pyx_cpp_set[X] {{cname}}(object o) except *:
    cdef __pyx_cpp_set[X] s
    for item in o:
        s.insert(<X>item)
    return s


#################### set.to_py ####################

cimport cython

cdef extern from *:
    cdef cppclass __pyx_cpp_set "std::{{maybe_unordered}}set" [T]:
        cppclass const_iterator:
            T& operator*()
            const_iterator operator++()
            bint operator!=(const_iterator)
        const_iterator begin()
        const_iterator end()

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_set[X]& s):
    return {v for v in s}

#################### pair.from_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_pair "std::pair" [T, U]:
        __pyx_cpp_pair() except +
        __pyx_cpp_pair(T&, U&) except +

@cname("{{cname}}")
cdef __pyx_cpp_pair[X,Y] {{cname}}(object o) except *:
    x, y = o
    return __pyx_cpp_pair[X,Y](<X>x, <Y>y)


#################### pair.to_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_pair "std::pair" [T, U]:
        T first
        U second

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_pair[X,Y]& p):
    return p.first, p.second


#################### map.from_py ####################

cdef extern from *:
    cdef cppclass __pyx_cpp_pair "std::pair" [T, U]:
        __pyx_cpp_pair(T&, U&) except +
    cdef cppclass __pyx_cpp_map "std::{{maybe_unordered}}map" [T, U]:
        void insert(__pyx_cpp_pair[T, U]&) except +


@cname("{{cname}}")
cdef __pyx_cpp_map[X,Y] {{cname}}(object o) except *:
    cdef __pyx_cpp_map[X,Y] m
    for key, value in o.items():
        m.insert(__pyx_cpp_pair[X,Y](<X>key, <Y>value))
    return m


#################### map.to_py ####################
# TODO: Work out const so that this can take a const
# reference rather than pass by value.

cimport cython

cdef extern from *:
    cdef cppclass __pyx_cpp_map "std::{{maybe_unordered}}map" [T, U]:
        cppclass value_type:
            T first
            U second
        cppclass const_iterator:
            value_type& operator*()
            const_iterator operator++()
            bint operator!=(const_iterator)
        const_iterator begin()
        const_iterator end()

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_map[X,Y]& s):
    o = {}
    cdef const __pyx_cpp_map[X,Y].value_type *key_value
    cdef __pyx_cpp_map[X,Y].const_iterator iter = s.begin()
    while iter != s.end():
        key_value = &cython.operator.dereference(iter)
        o[key_value.first] = key_value.second
        cython.operator.preincrement(iter)
    return o


#################### complex.from_py ####################

cimport cython

cdef extern from *:
    cdef cppclass __pyx_cpp_std_complex "std::complex" [T]:
        __pyx_cpp_std_complex()
        __pyx_cpp_std_complex(T, T) except +

@cname("{{cname}}")
cdef __pyx_cpp_std_complex[X] {{cname}}(object o) except *:
    cdef cython.doublecomplex z = o
    return __pyx_cpp_std_complex[X](<X>z.real, <X>z.imag)


#################### complex.to_py ####################

cimport cython

cdef extern from *:
    cdef cppclass __pyx_cpp_std_complex "std::complex" [T]:
        X real()
        X imag()

@cname("{{cname}}")
cdef object {{cname}}(const __pyx_cpp_std_complex[X]& z):
    cdef cython.doublecomplex tmp
    tmp.real = <cython.double>z.real()
    tmp.imag = <cython.double>z.imag()
    return tmp
