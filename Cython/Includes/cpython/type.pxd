
cdef extern from "Python.h":
    # The C structure of the objects used to describe built-in types.

    ############################################################################
    # 7.1.1 Type Objects
    ############################################################################

    ctypedef class __builtin__.type [object PyTypeObject]:
        pass

    # PyObject* PyType_Type
    # This is the type object for type objects; it is the same object
    # as type and types.TypeType in the Python layer.

    bint PyType_Check(object o)
    # Return true if the object o is a type object, including
    # instances of types derived from the standard type object. Return
    # false in all other cases.

    bint PyType_CheckExact(object o)
    # Return true if the object o is a type object, but not a subtype
    # of the standard type object. Return false in all other
    # cases.

    void PyType_Modified(type type)
    # Invalidate the internal lookup cache for the type and all of its
    # subtypes. This function must be called after any manual modification
    # of the attributes or base classes of the type.

    bint PyType_HasFeature(object o, int feature)
    # Return true if the type object o sets the feature feature. Type
    # features are denoted by single bit flags.

    bint PyType_IS_GC(object o)
    # Return true if the type object includes support for the cycle
    # detector; this tests the type flag Py_TPFLAGS_HAVE_GC.

    bint PyType_IsSubtype(type a, type b)
    # Return true if a is a subtype of b.

    object PyType_GenericAlloc(object type, Py_ssize_t nitems)
    # Return value: New reference.

    object PyType_GenericNew(type type, object args, object kwds)
    # Return value: New reference.

    bint PyType_Ready(type type) except -1
    # Finalize a type object. This should be called on all type
    # objects to finish their initialization. This function is
    # responsible for adding inherited slots from a type's base
    # class. Return 0 on success, or return -1 and sets an exception
    # on error.

    enum:
        # Constants for PyType_GetSlot() slot IDs.
        Py_bf_getbuffer = 1
        Py_bf_releasebuffer = 2
        Py_mp_ass_subscript = 3
        Py_mp_length = 4
        Py_mp_subscript = 5
        Py_nb_absolute = 6
        Py_nb_add = 7
        Py_nb_and = 8
        Py_nb_bool = 9
        Py_nb_divmod = 10
        Py_nb_float = 11
        Py_nb_floor_divide = 12
        Py_nb_index = 13
        Py_nb_inplace_add = 14
        Py_nb_inplace_and = 15
        Py_nb_inplace_floor_divide = 16
        Py_nb_inplace_lshift = 17
        Py_nb_inplace_multiply = 18
        Py_nb_inplace_or = 19
        Py_nb_inplace_power = 20
        Py_nb_inplace_remainder = 21
        Py_nb_inplace_rshift = 22
        Py_nb_inplace_subtract = 23
        Py_nb_inplace_true_divide = 24
        Py_nb_inplace_xor = 25
        Py_nb_int = 26
        Py_nb_invert = 27
        Py_nb_lshift = 28
        Py_nb_multiply = 29
        Py_nb_negative = 30
        Py_nb_or = 31
        Py_nb_positive = 32
        Py_nb_power = 33
        Py_nb_remainder = 34
        Py_nb_rshift = 35
        Py_nb_subtract = 36
        Py_nb_true_divide = 37
        Py_nb_xor = 38
        Py_sq_ass_item = 39
        Py_sq_concat = 40
        Py_sq_contains = 41
        Py_sq_inplace_concat = 42
        Py_sq_inplace_repeat = 43
        Py_sq_item = 44
        Py_sq_length = 45
        Py_sq_repeat = 46
        Py_tp_alloc = 47
        Py_tp_base = 48
        Py_tp_bases = 49
        Py_tp_call = 50
        Py_tp_clear = 51
        Py_tp_dealloc = 52
        Py_tp_del = 53
        Py_tp_descr_get = 54
        Py_tp_descr_set = 55
        Py_tp_doc = 56
        Py_tp_getattr = 57
        Py_tp_getattro = 58
        Py_tp_hash = 59
        Py_tp_init = 60
        Py_tp_is_gc = 61
        Py_tp_iter = 62
        Py_tp_iternext = 63
        Py_tp_methods = 64
        Py_tp_new = 65
        Py_tp_repr = 66
        Py_tp_richcompare = 67
        Py_tp_setattr = 68
        Py_tp_setattro = 69
        Py_tp_str = 70
        Py_tp_traverse = 71
        Py_tp_members = 72
        Py_tp_getset = 73
        Py_tp_free = 74
        Py_nb_matrix_multiply = 75
        Py_nb_inplace_matrix_multiply = 76
        Py_am_await = 77
        Py_am_aiter = 78
        Py_am_anext = 79
        Py_tp_finalize = 80
        Py_am_send = 81           # New in 3.10
        Py_tp_vectorcall = 82     # New in 3.14
        Py_tp_token = 83          # New in 3.14

    void* PyType_GetSlot(type t, int slot) except? NULL
    # Return the function pointer stored in the given slot.
    # If the result is NULL, this indicates that either the slot is NULL,
    # or that the function was called with invalid parameters and raised an exception.
    # In Python 3.9, this function only supports heap types and raises otherwise.
    # Callers will typically cast the result pointer into the appropriate function type.
