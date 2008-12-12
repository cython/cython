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
    cdef object x, y, obj
    cdef int i, j, k
    global fred
    q()
    with nogil:
        r()
        q()
        i = 42
        obj = None
        17L
        7j
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


_ERRORS = u"""
 1: 5: Function with Python return type cannot be declared nogil
 6: 6: Assignment of Python object not allowed without gil
 4: 5: Function declared nogil has Python locals or temporaries
11: 5: Function with Python return type cannot be declared nogil
15: 5: Calling gil-requiring function without gil
24: 9: Calling gil-requiring function without gil
26:12: Assignment of Python object not allowed without gil
28: 8: Constructing complex number not allowed without gil
29:12: Accessing Python global or builtin not allowed without gil
30: 8: Backquote expression not allowed without gil
31:15: Python import not allowed without gil
31:15: Assignment of Python object not allowed without gil
32:13: Python import not allowed without gil
32:25: Constructing Python list not allowed without gil
33:17: Iterating over Python object not allowed without gil
35:11: Indexing Python object not allowed without gil
36:11: Slicing Python object not allowed without gil
37:11: Constructing Python slice object not allowed without gil
37:11: Indexing Python object not allowed without gil
37:13: Converting to Python object not allowed without gil
37:15: Converting to Python object not allowed without gil
37:17: Converting to Python object not allowed without gil
38:11: Accessing Python attribute not allowed without gil
39: 9: Constructing Python tuple not allowed without gil
40: 8: Constructing Python list not allowed without gil
41: 8: Constructing Python dict not allowed without gil
42:12: Truth-testing Python object not allowed without gil
43:13: Python type test not allowed without gil
#44: 4: Converting to Python object not allowed without gil
45:10: Operation not allowed without gil
46: 8: Operation not allowed without gil
47:10: Assignment of Python object not allowed without gil
47:14: Assignment of Python object not allowed without gil
48: 9: Assignment of Python object not allowed without gil
48:13: Assignment of Python object not allowed without gil
48:16: Creating temporary Python reference not allowed without gil
48:19: Creating temporary Python reference not allowed without gil
49:11: Indexing Python object not allowed without gil
49:11: Assignment of Python object not allowed without gil
50:11: Accessing Python attribute not allowed without gil
50:11: Assignment of Python object not allowed without gil
51: 8: Constructing Python tuple not allowed without gil
51: 8: Python print statement not allowed without gil
52: 8: Deleting Python object not allowed without gil
53: 8: Returning Python object not allowed without gil
54: 8: Raising exception not allowed without gil
55:14: Truth-testing Python object not allowed without gil
57:17: Truth-testing Python object not allowed without gil
59: 8: Converting to Python object not allowed without gil
61: 8: Try-except statement not allowed without gil
65: 8: Try-finally statement not allowed without gil
"""
