# TODO: Figure out how many of the pass-by-value copies the compiler can eliminate.


#################### string.from_py ####################

cdef extern from *:
    cdef cppclass string "std::string":
        string(char* c_str, size_t size)

@cname("{{cname}}")
cdef string {{cname}}(object o) except *:
    return string(<char*>o, len(o))


#################### string.to_py ####################

#cimport cython
#from libcpp.string cimport string
cdef extern from *:
    cdef cppclass string "const std::string":
        char* c_str()
        size_t size()

@cname("{{cname}}")
cdef object {{cname}}(string& s):
    return s.c_str()[:s.size()]


#################### vector.from_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef X X_from_py "{{T0_from_py}}" (object) except *

cdef extern from *:
    cdef cppclass vector "std::vector" [T]:
        void push_back(T&)

@cname("{{cname}}")
cdef vector[X] {{cname}}(object o) except *:
    cdef vector[X] v
    for item in o:
        v.push_back(X_from_py(item))
    return v


#################### vector.to_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef object X_to_py "{{T0_to_py}}" (X)

cdef extern from *:
    cdef cppclass vector "const std::vector" [T]:
        size_t size()
        T& operator[](size_t)

@cname("{{cname}}")
cdef object {{cname}}(vector[X]& v):
    return [X_to_py(v[i]) for i in range(v.size())]


#################### list.from_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef X X_from_py "{{T0_from_py}}" (object) except *

cdef extern from *:
    cdef cppclass cpp_list "std::list" [T]:
        void push_back(T&)

@cname("{{cname}}")
cdef cpp_list[{{T0}}] {{cname}}(object o) except *:
    cdef cpp_list[{{T0}}] l
    for item in o:
        l.push_back(X_from_py(item))
    return l


#################### list.to_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef object X_to_py "{{T0_to_py}}" (X)

cdef extern from *:
    cdef cppclass cpp_list "std::list" [T]:
        cppclass const_iterator:
            T& operator*()
            const_iterator operator++()
            bint operator!=(const_iterator)
        const_iterator begin()
        const_iterator end()
    cdef cppclass const_cpp_list "const std::list" [T] (cpp_list)

@cname("{{cname}}")
cdef object {{cname}}(const_cpp_list[X]& v):
    o = []
    cdef cpp_list[X].const_iterator iter = s.begin()
    while iter != s.end():
        o.append(X_to_py(cython.operator.dereference(iter)))
        cython.operator.preincrement(iter)
    return o


#################### set.from_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef X X_from_py "{{T0_from_py}}" (object) except *

cdef extern from *:
    cdef cppclass set "std::set" [T]:
        void insert(T&)

@cname("{{cname}}")
cdef set[X] {{cname}}(object o) except *:
    cdef set[X] s
    for item in o:
        s.insert(X_from_py(item))
    return s


#################### set.to_py ####################

cimport cython

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    cdef object X_to_py "{{T0_to_py}}" (X)

cdef extern from *:
    cdef cppclass cpp_set "std::set" [T]:
        cppclass const_iterator:
            T& operator*()
            const_iterator operator++()
            bint operator!=(const_iterator)
        const_iterator begin()
        const_iterator end()
    cdef cppclass const_cpp_set "const std::set" [T](cpp_set):
        pass

@cname("{{cname}}")
cdef object {{cname}}(const_cpp_set[X]& s):
    o = set()
    cdef cpp_set[X].const_iterator iter = s.begin()
    while iter != s.end():
        o.add(X_to_py(cython.operator.dereference(iter)))
        cython.operator.preincrement(iter)
    return o

#################### pair.from_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    ctypedef struct Y "{{T1}}":
        pass
    cdef X X_from_py "{{T0_from_py}}" (object) except *
    cdef Y Y_from_py "{{T1_from_py}}" (object) except *

cdef extern from *:
    cdef cppclass pair "std::pair" [T, U]:
        pair(T&, U&)

@cname("{{cname}}")
cdef pair[X,Y] {{cname}}(object o) except *:
    x, y = o
    return pair[X,Y](X_from_py(x), Y_from_py(y))


#################### pair.to_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    ctypedef struct Y "{{T1}}":
        pass
    cdef object X_to_py "{{T0_to_py}}" (X)
    cdef object Y_to_py "{{T1_to_py}}" (Y)

cdef extern from *:
    cdef cppclass pair "const std::pair" [T, U]:
        T first
        U second

@cname("{{cname}}")
cdef object {{cname}}(pair[X,Y]& p):
    return X_to_py(p.first), Y_to_py(p.second)


#################### map.from_py ####################

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    ctypedef struct Y "{{T1}}":
        pass
    cdef X X_from_py "{{T0_from_py}}" (object) except *
    cdef Y Y_from_py "{{T1_from_py}}" (object) except *

cdef extern from *:
    cdef cppclass pair "std::pair" [T, U]:
        pair(T&, U&)
    cdef cppclass map "std::map" [T, U]:
        void insert(pair[T, U]&)

    cdef cppclass pair "std::pair" [T, U]:
        pass
    cdef cppclass vector "std::vector" [T]:
        pass


@cname("{{cname}}")
cdef map[X,Y] {{cname}}(object o) except *:
    cdef dict d = o
    cdef map[X,Y] m
    for key, value in d.iteritems():
        m.insert(pair[X,Y](X_from_py(key), Y_from_py(value)))
    return m


#################### map.to_py ####################
# TODO: Work out const so that this can take a const
# reference rather than pass by value.

cimport cython

cdef extern from *:
    ctypedef struct X "{{T0}}":
        pass
    ctypedef struct Y "{{T1}}":
        pass
    cdef object X_to_py "{{T0_to_py}}" (X)
    cdef object Y_to_py "{{T1_to_py}}" (Y)

cdef extern from *:
    cdef cppclass map "std::map" [T, U]:
        cppclass value_type:
            T first
            U second
        cppclass iterator:
            value_type& operator*()
            iterator operator++()
            bint operator!=(iterator)
        iterator begin()
        iterator end()

@cname("{{cname}}")
cdef object {{cname}}(map[X,Y] s):
    o = {}
    cdef map[X,Y].value_type *key_value
    cdef map[X,Y].iterator iter = s.begin()
    while iter != s.end():
        key_value = &cython.operator.dereference(iter)
        o[X_to_py(key_value.first)] = Y_to_py(key_value.second)
        cython.operator.preincrement(iter)
    return o
