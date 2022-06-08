///////////////////////////// ABCCheck //////////////////////////////

#if PY_VERSION_HEX < 0x030A0000
static int __Pyx_MatchCase_IsExactSequence(PyObject *o) {
    // is one of the small list of builtin types known to be a sequence
    if (PyList_CheckExact(o) || PyTuple_CheckExact(o)) {
        // Use exact type match for these checks. I in the event of inheritence we need to make sure
        // that it isn't a mapping too
        return 1;
    }
    if (PyRange_Check(o) || PyMemoryView_Check(o)) {
        // Exact check isn't possible so do exact check in another way
        PyObject *mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
        if (mro) {
            Py_ssize_t len = PyObject_Length(mro);
            Py_DECREF(mro);
            if (len < 0) {
                PyErr_Clear(); // doesn't really matter, just proceed with other checks
            } else if (len == 2) {
                return 1; // the type and "object" and no other bases
            }
        } else {
            PyErr_Clear(); // doesn't really matter, just proceed with other checks
        }
    }
    return 0;
}

static CYTHON_INLINE int __Pyx_MatchCase_IsExactMapping(PyObject *o) {
    // Py_Dict is the only regularly used mapping type
    // "types.MappingProxyType" also exists but is correctly covered by
    // the isinstance(o, Mapping) check
    return PyDict_CheckExact(o);
}

static int __Pyx_MatchCase_IsExactNeitherSequenceNorMapping(PyObject *o) {
    if (PyUnicode_Check(o) || PyBytes_Check(o) || PyByteArray_Check(o)) {
        return 1;  // these types are deliberately excluded from the sequence test
            // even though they look like sequences for most other purposes.
            // They're therefore "inexact" checks
    }
    if (o == Py_None || PyLong_CheckExact(o) || PyFloat_CheckExact(o)) {
        return 1;
    }
    #if PY_MAJOR_VERSION < 3
    if (PyInt_CheckExact(o)) {
        return 1;
    }
    #endif

    return 0;
}

// sequence_mapping_temp: For Python 3.10 testing sequences and mappings are
// really quick and this is ignored. For lower versions of Python they're
// slow, especially in the "fail" case.
// Therefore, we store an int temp to avoid duplicating tests.
// The bits of it in order are:
//  0. definitely a sequence
//  1. definitely a mapping
//     - note that both of the above and be true when
//        the type is registered with both abc types (not via inheritance)
//       and in this case we return true for both IsSequence or IsMapping
//       (which seems like the best handling of an ambiguous situation)
//  2. definitely not a sequence
//  3. definitely not a mapping

#if PY_VERSION_HEX < 0x030A0000
#define __PYX_DEFINITELY_SEQUENCE_FLAG 1U
#define __PYX_DEFINITELY_MAPPING_FLAG (1U<<1)
#define __PYX_DEFINITELY_NOT_SEQUENCE_FLAG (1U<<2)
#define __PYX_DEFINITELY_NOT_MAPPING_FLAG (1U<<3)
#define __PYX_SEQUENCE_MAPPING_ERROR (1U<<4)  // only used by the ABCCheck function
#endif

// the result is defined using the specification for sequence_mapping_temp
// (detailed in "is_sequence")
static unsigned int __Pyx_MatchCase_ABCCheck(PyObject *o, int sequence_first, int definitely_not_sequence, int definitely_not_mapping) {
    // in Python 3.10 objects can have their sequence bit set or their mapping bit set
    // but not both. Practically this translates to "which type is registered first".
    // In Python < 3.10 we can only determine this if they're direct bases (by looking
    // at the MRO order). If they're registered manually then we can't tell

    PyObject *abc_module=NULL, *sequence_type=NULL, *mapping_type=NULL;
    PyObject *mro;
    int sequence_result=0, mapping_result=0;
    unsigned int result = 0;

    abc_module = PyImport_ImportModule(
#if PY_VERSION_HEX > 0x03030000
        "collections.abc"
#else
        "collections"
#endif
                 );
    if (!abc_module) {
        return __PYX_SEQUENCE_MAPPING_ERROR;
    }
    if (sequence_first) {
        if (definitely_not_sequence) {
            result = __PYX_DEFINITELY_SEQUENCE_FLAG;
            goto end;
        }
        sequence_type = PyObject_GetAttr(abc_module, PYIDENT("Sequence"));
        if (!sequence_type) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        }
        sequence_result = PyObject_IsInstance(o, sequence_type);
        if (sequence_result < 0) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        } else if (sequence_result == 0) {
            result |= __PYX_DEFINITELY_NOT_SEQUENCE_FLAG;
            goto end;
        }
        // else wait to see what mapping is        
    }
    if (!definitely_not_mapping) {
        mapping_type = PyObject_GetAttr(abc_module, PYIDENT("Mapping"));
        if (!mapping_type) {
            goto end;
        }
        mapping_result = PyObject_IsInstance(o, mapping_type);
    }
    if (mapping_result < 0) {
        result = __PYX_SEQUENCE_MAPPING_ERROR;
        goto end;
    } else if (mapping_result == 0) {
        result |= __PYX_DEFINITELY_NOT_MAPPING_FLAG;
        if (sequence_first) {
            assert(sequence_result);
            result |= __PYX_DEFINITELY_SEQUENCE_FLAG;
        }
        goto end;
    } else /* mapping_result == 1 */ {
        if (sequence_first && !sequence_result) {
            result |= __PYX_DEFINITELY_MAPPING_FLAG;
            goto end;
        }
    }
    if (!sequence_first) {
        // here we know mapping_result is true because we'd have returned otherwise
        assert(mapping_result);
        if (!definitely_not_sequence) {
            sequence_type = PyObject_GetAttr(abc_module, PYIDENT("Sequence"));
            if (!sequence_type) {
                result = __PYX_SEQUENCE_MAPPING_ERROR;
                goto end;
            }
            sequence_result = PyObject_IsInstance(o, sequence_type);
        }
        if (sequence_result < 0) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        } else if (sequence_result == 0) {
            result |= (__PYX_DEFINITELY_NOT_SEQUENCE_FLAG | __PYX_DEFINITELY_MAPPING_FLAG);
            goto end;
        } /* else sequence_result == 1, continue to check both */
    }

    // It's an instance of both types. Look up the MRO order.
    // In event of failure treat it as "could be either"
    result = __PYX_DEFINITELY_SEQUENCE_FLAG | __PYX_DEFINITELY_MAPPING_FLAG;
    mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
    Py_ssize_t i;
    if (!mro) {
        PyErr_Clear();
        goto end;
    } 
    if (!PyTuple_Check(mro)) {
        Py_DECREF(mro);
        goto end;
    }
    for (i=1; i < PyTuple_GET_SIZE(mro); ++i) {
        int is_subclass_sequence, is_subclass_mapping;
        PyObject *mro_item = PyTuple_GET_ITEM(mro, i);
        is_subclass_sequence = PyObject_IsSubclass(mro_item, sequence_type);
        if (is_subclass_sequence < 0) goto loop_error;
        is_subclass_mapping = PyObject_IsSubclass(mro_item, mapping_type);
        if (is_subclass_mapping < 0) goto loop_error;
        if (is_subclass_sequence && !is_subclass_mapping) {
            result = (__PYX_DEFINITELY_SEQUENCE_FLAG | __PYX_DEFINITELY_NOT_MAPPING_FLAG);
            break;
        } else if (is_subclass_mapping && !is_subclass_sequence) {
            result = (__PYX_DEFINITELY_NOT_SEQUENCE_FLAG | __PYX_DEFINITELY_MAPPING_FLAG);
            break;
        }
    }
    // If we get to the end of the loop without breaking then neither type is in
    // the MRO, so they've both been registered manually. We don't know which was
    // registered first so accept the object as either as a compromise
    if (0) {
        loop_error:
        PyErr_Clear();
    }
    Py_DECREF(mro);

    end:
    Py_XDECREF(abc_module);
    Py_XDECREF(sequence_type);
    Py_XDECREF(mapping_type);
    return result;
}
#endif

///////////////////////////// IsSequence.proto //////////////////////

static int __Pyx_MatchCase_IsSequence(PyObject *o, unsigned int *sequence_mapping_temp); /* proto */

//////////////////////////// IsSequence /////////////////////////
//@requires: ABCCheck

static int __Pyx_MatchCase_IsSequence(PyObject *o, unsigned int *sequence_mapping_temp) {
#if PY_VERSION_HEX >= 0x030A0000
    return PyType_GetFlags(Py_TYPE(o)) & Py_TPFLAGS_SEQUENCE;
#else
    // Py_TPFLAGS_SEQUENCE doesn't exit.
    PyObject *o_module_name;
    unsigned int abc_result, dummy=0;

    if (sequence_mapping_temp) {
        // maybe we already know the answer
        if (*sequence_mapping_temp & __PYX_DEFINITELY_SEQUENCE_FLAG) {
            return 1;
        }
        if (*sequence_mapping_temp & __PYX_DEFINITELY_NOT_SEQUENCE_FLAG) {
            return 0;
        }
    } else {
        // Probably quicker to just assign it and not check from here
        sequence_mapping_temp = &dummy;
    }

    // Start by check a known list of types
    if (__Pyx_MatchCase_IsExactSequence(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_SEQUENCE_FLAG | __PYX_DEFINITELY_NOT_MAPPING_FLAG);
        return 1;
    }
    if (__Pyx_MatchCase_IsExactMapping(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_MAPPING_FLAG | __PYX_DEFINITELY_NOT_SEQUENCE_FLAG);
        return 0;
    }
    if (__Pyx_MatchCase_IsExactNeitherSequenceNorMapping(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_NOT_SEQUENCE_FLAG | __PYX_DEFINITELY_NOT_MAPPING_FLAG);
        return 0;
    }

    abc_result = __Pyx_MatchCase_ABCCheck(
        o, 1,
        *sequence_mapping_temp & __PYX_DEFINITELY_NOT_SEQUENCE_FLAG,
        *sequence_mapping_temp & __PYX_DEFINITELY_NOT_MAPPING_FLAG
    );
    if (abc_result & __PYX_SEQUENCE_MAPPING_ERROR) {
        return -1;
    }
    *sequence_mapping_temp = abc_result;
    if (*sequence_mapping_temp & __PYX_DEFINITELY_SEQUENCE_FLAG) {
        return 1;
    }

    // array.array is a more complicated check (and unfortunately isn't covered by
    // collections.abc.Sequence on Python <3.10).
    // Do the test by checking the module name, and then importing/testing the class
    // It also doesn't give perfect results for classes that inherit from both array.array
    // and a mapping
    o_module_name = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__module__");
    if (!o_module_name) {
        return -1;
    }
#if PY_MAJOR_VERSION >= 3
    if (PyUnicode_Check(o_module_name) && PyUnicode_CompareWithASCIIString(o_module_name, "array") == 0)
#else
    if (PyBytes_Check(o_module_name) && PyBytes_AS_STRING(o_module_name)[0] == 'a' &&
        PyBytes_AS_STRING(o_module_name)[1] == 'r' && PyBytes_AS_STRING(o_module_name)[2] == 'r' &&
        PyBytes_AS_STRING(o_module_name)[3] == 'a' && PyBytes_AS_STRING(o_module_name)[4] == 'y' &&
        PyBytes_AS_STRING(o_module_name)[5] == '\0')
#endif
    {
        int is_array;
        PyObject *array_module, *array_object;
        Py_DECREF(o_module_name);
        array_module = PyImport_ImportModule("array");
        if (!array_module) {
            PyErr_Clear();
            return 0;  // treat these tests as "soft" and don't cause an exception
        }
        array_object = PyObject_GetAttrString(array_module, "array");
        Py_DECREF(array_module);
        if (!array_object) {
            PyErr_Clear();
            return 0;
        }
        is_array = PyObject_IsInstance(o, array_object);
        Py_DECREF(array_object);
        if (is_array) {
            *sequence_mapping_temp |= __PYX_DEFINITELY_SEQUENCE_FLAG;
            return 1;
        }
        PyErr_Clear();
    } else {
        Py_DECREF(o_module_name);
    }
    *sequence_mapping_temp |= __PYX_DEFINITELY_NOT_SEQUENCE_FLAG;
    return 0;
#endif
}

////////////////////// IterableSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_IterableToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// IterableSliceToList //////////////////////////

// This is substantially based off ceval unpack_iterable.
// It's also pretty similar to itertools.islice
// Indices must be postive - there's no wraparound or boundschecking

static PyObject *__Pyx_MatchCase_IterableToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
    int total;
    int i;
    PyObject *list, *it;

    total = end-start;
    
    list = PyList_New(total);
    if (!list) {
        return NULL;
    }
    it = PyObject_GetIter(x);
    if (!it) {
        goto bad;
    }
    // first use up "start" elements
    for (i=0; i<start; ++i) {
        PyObject *obj = PyIter_Next(it);
        if (!obj) {
            if (!PyErr_Occurred()) {
                PyErr_SetString(PyExc_ValueError, "Iteration failed when unpacking pattern matching star argument");
            }
            goto bad;
        }
        Py_DECREF(obj);
    }
    // now copy the remaining elements into the list
    for (i=0; i<total; ++i) {
        PyObject *obj = PyIter_Next(it);
        if (!obj) {
            if (!PyErr_Occurred()) {
                PyErr_SetString(PyExc_ValueError, "Iteration failed when unpacking pattern matching star argument");
            }
            goto bad;
        }
        PyList_SET_ITEM(list, i, obj);
    }

    if (0) {
        bad:
        Py_CLEAR(list);
    }
    Py_XDECREF(it);
    return list;
}

////////////////////// TupleSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_TupleToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// TupleSliceToList //////////////////////////
//@requires: IterableSliceToList
//@requires: ObjectHandling.c::TupleAndListFromArray

// Note that this should also work fine on lists (if needed)
// Indices must be postive - there's no wraparound or boundschecking

static PyObject *__Pyx_MatchCase_TupleToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
#if !CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_MatchCase_IterableToList(x, start, end);
#else
    PyObject **array;

    (void)__Pyx_MatchCase_IterableToList; // clear unused warning

    array = PySequence_Fast_ITEMS(x);
    return __Pyx_PyList_FromArray(array+start, end-start);
#endif
}

///////////////////////////// IsMapping.proto //////////////////////

static int __Pyx_MatchCase_IsMapping(PyObject *o); /* proto */

//////////////////////////// IsMapping /////////////////////////

static int __Pyx_MatchCase_IsMapping(PyObject *o) {
#if PY_VERSION_HEX >= 0x030A0000
    return PyType_GetFlags(Py_TYPE(o)) & Py_TPFLAGS_MAPPING;
#else
    PyObject *abc_module, *Mapping;
    int result;
    // Py_Dict is the only regularly used mapping type
    // "types.MappingProxyType" also exists but is correctly covered by
    // the isinstance(o, Mapping) check
    if (PyDict_Check(o)) {
        return 1;

    // otherwise check against collections.abc.Mapping
    abc_module = PyImport_ImportModule(
#if PY_VERSION_HEX > 0x03030000
        "collections.abc"
#else
        "collections"
#endif
                 );
    if (!abc_module) {
        return -1;
    }
    Mapping = PyObject_GetAttrString(abc_module, "Mapping");
    Py_DECREF(abc_module);
    if (!Mapping) {
        return -1;
    }
    result = PyObject_IsInstance(o, Mapping);
    Py_DECREF(Mapping);
    return result;
#endif
}
