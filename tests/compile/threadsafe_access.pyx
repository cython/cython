# mode: compile

import cython
from cython.parallel import parallel

@cython.test_assert_path_exists("//NameNode[@name = 'x' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'x' and @_needs_threadsafe_access_bool=False]")
def obj_in_parallel():
    with nogil, parallel():
        with gil:
            x = object()

# In this case o is never assigned, so we don't need thread-safe access
@cython.test_assert_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=True]")
def no_assignment_in_parallel1(o):
    with nogil, parallel():
        with gil:
            print(o)


# In this case o is not assigned in the parallel block, so we don't need thread-safe access
@cython.test_assert_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=True]")
def no_assignment_in_parallel2():
    o = "String"
    with nogil, parallel():
        with gil:
            print(o)

# Deletion is an assignment
@cython.test_assert_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=False]")
def parallel_deletion(o):
    with nogil, parallel():
        with gil:
            del o


def locals_same_scope():
    with nogil, parallel():
        with gil:
            a = object()
            b = object()
            with (cython.test_fail_if_path_exists("//SingleAssignmentNode//CoerceToTempNode"),
                  cython.test_assert_path_exists("//SingleAssignmentNode//NameNode")):
                # The rhs of the assignment is in the same scope so does not need its own threadsafe access
                with (cython.test_assert_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=True]"),
                      cython.test_fail_if_path_exists("//NameNode[@name = 'b' and @_needs_threadsafe_access_bool=True]")):
                    a = b

@cython.test_assert_path_exists("//NameNode[@name = 'i' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'i' and @_needs_threadsafe_access_bool=True]")
@cython.threadsafe_variable_access("full")
def c_type_in_parallel():
    # Even though we're on "full" mode, c types are already thread private, so don't need locking
    cdef int i
    with nogil, parallel():
        i = 10

cdef global_obj = object()
cdef global_obj_2 = object()
cdef int global_int = 20
not_cdef = 1.5

@cython.test_assert_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=False]")
@cython.test_assert_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=True]")
def access_globals():
    print(global_obj, global_int, not_cdef)

@cython.test_assert_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=True]")
@cython.threadsafe_variable_access("full")
def access_globals_full():
    print(global_obj, global_int, not_cdef)

@cython.test_assert_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=False]")
@cython.test_assert_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=False]")
@cython.test_assert_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_int' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'not_cdef' and @_needs_threadsafe_access_bool=True]")
@cython.threadsafe_variable_access("off")
def access_globals_off():
    print(global_obj, global_int, not_cdef)

@cython.test_assert_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//NameNode[@name = 'global_obj_2' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_obj' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_obj_2' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//SingleAssignmentNode//CoerceToTempNode")
def globals_same_scope():
    global global_obj
    # shouldn't lock the rhs - since both variables share the same scope
    global_obj = global_obj_2

cdef cfunc():
    pass

cpdef cpfunc():
    pass

@cython.test_fail_if_path_exists("//NameNode[@name = 'cfunc' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'cpfunc' and @_needs_threadsafe_access_bool=True]")
def access_global_cfuncs():
    cfunc()
    cpfunc()

cdef class C:
    cdef py_attr
    cdef double c_attr
    cdef void c_func(self):
        pass
    cpdef void cp_func(self):
        pass
    def py_func(self):
        pass

# C is a function local, so doesn't need threadsafe access
@cython.test_assert_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=True]")
def access_cclass(C c):
    print(c.py_attr, c.c_attr)

@cython.test_assert_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=False]")
@cython.threadsafe_variable_access("full")
def access_cclass_full(C c):
    print(c.py_attr, c.c_attr)

@cython.test_assert_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'c' and @_needs_threadsafe_access_bool=True]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=False]")
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'py_attr' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'c_attr' and @_needs_threadsafe_access_bool=True]")
@cython.threadsafe_variable_access("off")
def access_cclass_off(C c):
    print(c.py_attr, c.c_attr)

# access to C funcs doesn't need locking (because they're immutable).
# access to py_funcs goes through a dictionary and this provides the thread safety rather than Cython.
# They're transformed out anyway, so we can't directly check for the attribute nodes
@cython.test_fail_if_path_exists("AttributeNode[@attribute = 'func' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("AttributeNode[@attribute = 'cp_func' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("AttributeNode[@attribute = 'py_func' and @_needs_threadsafe_access_bool=True]")
def access_cclass_func(C c):
    c.c_func()
    c.cp_func()
    c.py_func()

# Python attributes go through a dictionary lookup so don't need special locking
@cython.test_assert_path_exists("//AttributeNode[@attribute = 'some_attribute' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//AttributeNode[@attribute = 'some_attribute' and @_needs_threadsafe_access_bool=True]")
def access_pyclass(c):
    print(c.some_attribute)


def closure():
    # In principle it should probably be possible to work out that this is safe, but in practice
    # it's hard, so don't assert anything about it
    o = object()

    # once it's in a closure, it does need thread safe access
    @cython.test_assert_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=True]")
    @cython.test_fail_if_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=False]")
    def inner():
        print(o)

    # hard to reason about the value here
    with (cython.test_assert_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=True]"),
          cython.test_fail_if_path_exists("//NameNode[@name = 'o' and @_needs_threadsafe_access_bool=False]")):
        print(o)


# Simple generators are guarded to make sure that they can't be called when they're already running
# and thus don't need checks
@cython.test_assert_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=False]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=True]")
def basic_generator():
    a = object()
    yield a

def func_with_inner_gen(a):
    # This generator has a closure variable, so can't reason about whether other threads can access it
    @cython.test_assert_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=True]")
    @cython.test_fail_if_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=False]")
    def inner_gen():
        yield a

# This generator has a variable that's shared with a closure, so can't reason about whether other threads can access it
@cython.test_assert_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=True]")
@cython.test_fail_if_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=False]")
def gen_with_inner_func(a):
    @cython.test_assert_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=True]")
    @cython.test_fail_if_path_exists("//NameNode[@name = 'a' and @_needs_threadsafe_access_bool=False]")
    def inner():
        nonlocal a
        a = 1
    yield a

cdef class Nested:
    cdef Nested attr

def deep_lookup(Nested n1, Nested n2):
    # Just test that this compiles sensibly, since they get factored out into temps
    n1.attr.attr.attr.attr.attr = n2.attr.attr.attr

cdef double[:] global_mview

@cython.test_assert_path_exists("//NameNode[@name = 'global_mview' and @_needs_threadsafe_access_bool=True")
@cython.test_fail_if_path_exists("//NameNode[@name = 'global_mview' and @_needs_threadsafe_access_bool=False")
def test_global_memview():
    global_mview[0] = global_mview[1]

@cython.test_assert_path_exists("//NameNode[@name = 'mview' and @_needs_threadsafe_access_bool=False")
@cython.test_fail_if_path_exists("//NameNode[@name = 'mview' and @_needs_threadsafe_access_bool=True")
def test_local_memview(double[:] mview):
    return mview[0]

@cython.test_assert_path_exists("//NameNode[@name = 'mview' and @_needs_threadsafe_access_bool=False")
@cython.test_fail_if_path_exists("//NameNode[@name = 'mview' and @_needs_threadsafe_access_bool=True")
def test_parallel_local_memview(double[:] mview):
    # common case that memoryview is never assignment to, so it needs no guards
    with nogil, parallel():
        mview[0] = 1.0
