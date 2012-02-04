# cython: remove_unreachable=False
# mode: error

cdef object f(object x) nogil:
    pass

cdef void g(int x) nogil:
    cdef object z
    z = None

cdef void h(int x) nogil:
    p()

cdef object p() nogil:
    pass

cdef void r() nogil:
    q()

cdef object m():
    cdef object x, y = 0, obj
    cdef int i, j, k
    global fred
    q()
    with nogil:
        r()
        q()
        i = 42
        obj = None
        17L
        <object>7j
        help
        `"Hello"`
        import fred
        from fred import obj
        for x in obj:
            pass
        obj[i]
        obj[i:j]
        obj[i:j:k]
        obj.fred
        (x, y)
        [x, y]
        {x: y}
        obj and x
        t(obj)
#        f(42) # Cython handles this internally
        x + obj
        -obj
        x = y = obj
        x, y = y, x
        obj[i] = x
        obj.fred = x
        print obj
        del fred
        return obj
        raise obj
        if obj:
            pass
        while obj:
            pass
        for x <= obj <= y:
            pass
        try:
            pass
        except:
            pass
        try:
            pass
        finally:
            pass

cdef void q():
    pass

cdef class C:
    pass

cdef void t(C c) nogil:
    pass

def ticket_338():
    cdef object obj
    with nogil:
        for obj from 0 <= obj < 4:
            pass

def bare_pyvar_name(object x):
    with nogil:
        x

# For m(), the important thing is that there are errors on all lines in the range 23-69
# except these: 29, 34, 44, 56, 58, 60, 62-64

_ERRORS = u"""
4:5: Function with Python return type cannot be declared nogil
7:5: Function declared nogil has Python locals or temporaries
9:6: Assignment of Python object not allowed without gil
12:5: Discarding owned Python object not allowed without gil
14:5: Function with Python return type cannot be declared nogil
18:5: Calling gil-requiring function not allowed without gil
27:9: Calling gil-requiring function not allowed without gil
29:12: Assignment of Python object not allowed without gil
31:16: Constructing complex number not allowed without gil
33:8: Backquote expression not allowed without gil
33:8: Discarding owned Python object not allowed without gil
33:9: Operation not allowed without gil
34:15: Assignment of Python object not allowed without gil
34:15: Operation not allowed without gil
34:15: Python import not allowed without gil
35:8: Operation not allowed without gil
35:13: Python import not allowed without gil
35:25: Constructing Python list not allowed without gil
35:25: Operation not allowed without gil
36:17: Iterating over Python object not allowed without gil
38:11: Discarding owned Python object not allowed without gil
38:11: Indexing Python object not allowed without gil
39:11: Discarding owned Python object not allowed without gil
39:11: Slicing Python object not allowed without gil
40:11: Constructing Python slice object not allowed without gil
40:11: Discarding owned Python object not allowed without gil
40:11: Indexing Python object not allowed without gil
40:13: Converting to Python object not allowed without gil
40:15: Converting to Python object not allowed without gil
40:17: Converting to Python object not allowed without gil
41:11: Accessing Python attribute not allowed without gil
41:11: Discarding owned Python object not allowed without gil
42:9: Constructing Python tuple not allowed without gil
42:9: Discarding owned Python object not allowed without gil
43:8: Constructing Python list not allowed without gil
43:8: Discarding owned Python object not allowed without gil
44:8: Constructing Python dict not allowed without gil
44:8: Discarding owned Python object not allowed without gil
45:12: Discarding owned Python object not allowed without gil
45:12: Truth-testing Python object not allowed without gil
46:13: Python type test not allowed without gil
48:10: Discarding owned Python object not allowed without gil
48:10: Operation not allowed without gil
49:8: Discarding owned Python object not allowed without gil
49:8: Operation not allowed without gil
50:10: Assignment of Python object not allowed without gil
50:14: Assignment of Python object not allowed without gil
51:9: Assignment of Python object not allowed without gil
51:13: Assignment of Python object not allowed without gil
51:16: Creating temporary Python reference not allowed without gil
51:19: Creating temporary Python reference not allowed without gil
52:11: Assignment of Python object not allowed without gil
52:11: Indexing Python object not allowed without gil
53:11: Accessing Python attribute not allowed without gil
53:11: Assignment of Python object not allowed without gil
54:8: Constructing Python tuple not allowed without gil
54:8: Python print statement not allowed without gil
55:8: Deleting Python object not allowed without gil
56:8: Returning Python object not allowed without gil
57:8: Raising exception not allowed without gil
58:14: Truth-testing Python object not allowed without gil
60:17: Truth-testing Python object not allowed without gil
62:8: For-loop using object bounds or target not allowed without gil
62:14: Coercion from Python not allowed without the GIL
62:25: Coercion from Python not allowed without the GIL
64:8: Try-except statement not allowed without gil
85:8: For-loop using object bounds or target not allowed without gil
"""
