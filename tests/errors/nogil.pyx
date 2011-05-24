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
3:5: Function with Python return type cannot be declared nogil
6:5: Function declared nogil has Python locals or temporaries
8:6: Assignment of Python object not allowed without gil
11:5: Discarding owned Python object not allowed without gil
13:5: Function with Python return type cannot be declared nogil
17:5: Calling gil-requiring function not allowed without gil
26:9: Calling gil-requiring function not allowed without gil
28:12: Assignment of Python object not allowed without gil
30:8: Discarding owned Python object not allowed without gil
30:16: Constructing complex number not allowed without gil
32:8: Backquote expression not allowed without gil
32:8: Discarding owned Python object not allowed without gil
32:9: Operation not allowed without gil
33:15: Assignment of Python object not allowed without gil
33:15: Operation not allowed without gil
33:15: Python import not allowed without gil
34:8: Operation not allowed without gil
34:13: Python import not allowed without gil
34:25: Constructing Python list not allowed without gil
34:25: Operation not allowed without gil
35:17: Iterating over Python object not allowed without gil
37:11: Discarding owned Python object not allowed without gil
37:11: Indexing Python object not allowed without gil
38:11: Discarding owned Python object not allowed without gil
38:11: Slicing Python object not allowed without gil
39:11: Constructing Python slice object not allowed without gil
39:11: Discarding owned Python object not allowed without gil
39:11: Indexing Python object not allowed without gil
39:13: Converting to Python object not allowed without gil
39:15: Converting to Python object not allowed without gil
39:17: Converting to Python object not allowed without gil
40:11: Accessing Python attribute not allowed without gil
40:11: Discarding owned Python object not allowed without gil
41:9: Constructing Python tuple not allowed without gil
41:9: Discarding owned Python object not allowed without gil
42:8: Constructing Python list not allowed without gil
42:8: Discarding owned Python object not allowed without gil
43:8: Constructing Python dict not allowed without gil
43:8: Discarding owned Python object not allowed without gil
44:12: Discarding owned Python object not allowed without gil
44:12: Truth-testing Python object not allowed without gil
45:13: Python type test not allowed without gil
47:10: Discarding owned Python object not allowed without gil
47:10: Operation not allowed without gil
48:8: Discarding owned Python object not allowed without gil
48:8: Operation not allowed without gil
49:10: Assignment of Python object not allowed without gil
49:14: Assignment of Python object not allowed without gil
50:9: Assignment of Python object not allowed without gil
50:13: Assignment of Python object not allowed without gil
50:16: Creating temporary Python reference not allowed without gil
50:19: Creating temporary Python reference not allowed without gil
51:11: Assignment of Python object not allowed without gil
51:11: Indexing Python object not allowed without gil
52:11: Accessing Python attribute not allowed without gil
52:11: Assignment of Python object not allowed without gil
53:8: Constructing Python tuple not allowed without gil
53:8: Python print statement not allowed without gil
54:8: Deleting Python object not allowed without gil
55:8: Returning Python object not allowed without gil
56:8: Raising exception not allowed without gil
57:14: Truth-testing Python object not allowed without gil
59:17: Truth-testing Python object not allowed without gil
61:8: For-loop using object bounds or target not allowed without gil
63:8: Try-except statement not allowed without gil
67:8: Cannot use try/finally in nogil sections unless it contains a 'with gil' statement.
84:8: For-loop using object bounds or target not allowed without gil
"""
