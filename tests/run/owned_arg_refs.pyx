
cdef class Owner:
    cdef object x

cdef call_me_with_owner(Owner owner, x):
    owner.x = "def" # overwrite external reference
    return x        # crashes if x is not owned by function or caller

def test_ext_type_attr():
    """
    >>> test_ext_type_attr()
    'abc5'
    """
    owner = Owner()
    owner.x = ''.join("abc%d" % 5) # non-interned object
    return call_me_with_owner(owner, owner.x)


cdef void call_me_without_gil(Owner owner, x) with gil:
    owner.x = "def" # overwrite external reference
    print x         # crashes if x is not owned by function or caller

def test_ext_type_attr_nogil():
    """
    >>> test_ext_type_attr_nogil()
    abc5
    """
    owner = Owner()
    owner.x = ''.join("abc%d" % 5) # non-interned object
    with nogil:
        call_me_without_gil(owner, owner.x)


# the following isn't dangerous as long as index access uses temps

cdef call_me_with_list(list l, x):
    l[:] = [(1,2), (3,4)] # overwrite external reference
    return x              # crashes if x is not owned by function or caller

def test_index():
    """
    >>> test_index()
    [3, 4]
    """
    l = [[1,2],[3,4]]
    return call_me_with_list(l, l[1])
