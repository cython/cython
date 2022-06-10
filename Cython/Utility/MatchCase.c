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
//@requires: ABCCheck

static int __Pyx_MatchCase_IsMapping(PyObject *o) {
#if PY_VERSION_HEX >= 0x030A0000
    return PyType_GetFlags(Py_TYPE(o)) & Py_TPFLAGS_MAPPING;
#else
    // Py_Dict is the only regularly used mapping type
    // "types.MappingProxyType" also exists but is correctly covered by
    // the isinstance(o, Mapping) check
    if (PyDict_Check(o)) {
        return 1;
    }

    // otherwise check against collections.abc.Mapping
    return __Pyx_MatchCase_ABCCheck(o, "Mapping", "Sequence");
#endif
}

//////////////////////// MappingKeyCheck.proto /////////////////////////

static int __Pyx_MatchCase_CheckDuplicateKeys(PyObject *fixed_keys, PyObject *var_keys); /*proto */

/////////////////////// MappingKeyCheck ////////////////////////////////

static int __Pyx_MatchCase_CheckDuplicateKeys(PyObject *fixed_keys, PyObject *var_keys) {
    // Inputs are tuples, and typically fairly small. It may be more efficient to
    // loop over the tuple than create a set.

    // The CPython implementation (match_keys in ceval.c) does this concurrently with
    // taking the keys out of the dictionary. I'm choosing to do it separately since the
    // majority of the time the keys will be known at compile-time so Cython can skip
    // this step completely.

    PyObject *var_keys_set;
    PyObject *key;
    Py_ssize_t n;
    int contains;

    var_keys_set = PySet_New(NULL);
    if (!var_keys_set) return -1;

    for (n=0; n < PyTuple_GET_SIZE(var_keys); ++n) {
        key = PyTuple_GET_ITEM(var_keys, n);
        contains = PySet_Contains(var_keys_set, key);
        if (contains < 0) {
            goto bad;
        } else if (contains == 1) {
            goto raise_error;
        } else {
            if (PySet_Add(var_keys_set, key)) {
                goto bad;
            }
        }
    }
    for (n=0; n < PyTuple_GET_SIZE(fixed_keys); ++n) {
        key = PyTuple_GET_ITEM(fixed_keys, n);
        contains = PySet_Contains(var_keys_set, key);
        if (contains < 0) {
            goto bad;
        } else if (contains == 1) {
            goto raise_error;
        }
    }
    Py_DECREF(var_keys_set);
    return 0;

    raise_error:
    PyErr_Format(PyExc_ValueError,
                 "mapping pattern checks duplicate key (%R)", key);
    bad:
    Py_DECREF(var_keys_set);
    return -1;
}

/////////////////////////// ExtractExactDict.proto ////////////////

#include <stdarg.h>

// the variadic arguments are a list of PyObject** to subjects to be filled. They may be NULL
// in which case they're ignored.
//
// This is a specialized version for when we have an exact dict (which is likely to be pretty common)

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
static int __Pyx__MatchCase_Mapping_ExtractDictV(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, va_list subjects); /* proto */
#define __Pyx_MatchCase_Mapping_ExtractDict(...) __Pyx__MatchCase_Mapping_ExtractDict(__pyx_refnanny, __VA_ARGS__)
#define __Pyx_MatchCase_Mapping_ExtractDictV(...) __Pyx__MatchCase_Mapping_ExtractDictV(__pyx_refnanny, __VA_ARGS__)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_ExtractDict(PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
static int __Pyx_MatchCase_Mapping_ExtractDictV(PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, va_list subjects); /* proto */
#endif

/////////////////////////// ExtractExactDict ////////////////

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, ...)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_ExtractDict(PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, ...)
#endif
{
    int result;
    va_list subjects;

    va_start(subjects, var_keys);
    result = __Pyx_MatchCase_Mapping_ExtractDictV(dict, fixed_keys, var_keys, subjects);
    va_end(subjects);
    return result;
}

#if CYTHON_REFNANNY
static int __Pyx__MatchCase_Mapping_ExtractDictV(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, va_list subjects)
#else
static int __Pyx_MatchCase_Mapping_ExtractDictV(PyObject *dict, PyObject *fixed_keys, PyObject *var_keys, va_list subjects)
#endif
{
    PyObject *keys[] = {fixed_keys, var_keys};
    Py_ssize_t i, j;

    for (i=0; i<2; ++i) {
        PyObject *tuple = keys[i];
        for (j=0; j<PyTuple_GET_SIZE(tuple); ++j) {
            PyObject *key = PyTuple_GET_ITEM(tuple, j);
            PyObject *value = PyDict_GetItemWithError(dict, key);
            PyObject **subject;
            if (!value) {
                if (PyErr_Occurred()) {
                    return -1; // any set subjects will be cleaned up externally
                } else {
                    return 0; // any set subjects will be cleaned up externally
                }
            }
            subject = va_arg(subjects, PyObject**);
            if (subject) {
                __Pyx_XDECREF_SET(*subject, value);
                __Pyx_INCREF(*subject);  // capture this incref with refnanny!
            }
        }
    }
    return 1;  // success
}

///////////////////////// ExtractNonDict.proto ////////////////////////////////

// the variadic arguments are a list of PyObject** to subjects to be filled. They may be NULL
// in which case they're ignored.
//
// This is a specialized version for the rarer case when the type isn't an exact dict.

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractNonDict(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *mapping, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
static int __Pyx__MatchCase_Mapping_ExtractNonDictV(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *mapping, PyObject *fixed_keys, PyObject *var_keys, va_list subjects); /* proto */
#define __Pyx_MatchCase_Mapping_ExtractNonDict(...) __Pyx__MatchCase_Mapping_ExtractNonDict(__pyx_refnanny, __VA_ARGS__)
#define __Pyx_MatchCase_Mapping_ExtractNonDictV(...) __Pyx__MatchCase_Mapping_ExtractNonDictV(__pyx_refnanny, __VA_ARGS__)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_ExtractNonDict(PyObject *mapping, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
static int __Pyx_MatchCase_Mapping_ExtractNonDictV(PyObject *mapping, PyObject *fixed_keys, PyObject *var_keys, va_list subjects); /* proto */
#endif

///////////////////////// ExtractNonDict //////////////////////////////////////
//@requires: ObjectHandling.c::PyObjectCall2Args


// largely adapter from match_keys in CPython ceval.c

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractNonDict(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_ExtractNonDict(PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...)
#endif
{
    int result;
    va_list subjects;

    va_start(subjects, var_keys);
    result = __Pyx_MatchCase_Mapping_ExtractNonDictV(map, fixed_keys, var_keys, subjects);
    va_end(subjects);
    return result;
}

#if CYTHON_REFNANNY
static int __Pyx__MatchCase_Mapping_ExtractNonDictV(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *map, PyObject *fixed_keys, PyObject *var_keys, va_list subjects)
#else
static int __Pyx_MatchCase_Mapping_ExtractNonDictV(PyObject *map, PyObject *fixed_keys, PyObject *var_keys, va_list subjects)
#endif
{
    PyObject *dummy=NULL, *get=NULL;
    PyObject *keys[] = {fixed_keys, var_keys};
    Py_ssize_t i, j;
    int result = 0;

    dummy = PyObject_CallObject((PyObject *)&PyBaseObject_Type, NULL);
    if (!dummy) {
        return -1;
    }
    get = PyObject_GetAttrString(map, "get");
    if (!get) {
        result = -1;
        goto end;
    }


    for (i=0; i<2; ++i) {
        PyObject *tuple = keys[i];
        for (j=0; j<PyTuple_GET_SIZE(tuple); ++j) {
            PyObject **subject;
            PyObject *value = NULL;
            PyObject *key = PyTuple_GET_ITEM(tuple, j);

            value = __Pyx_PyObject_Call2Args(get, key, dummy);
            if (!value) {
                result = -1;
                goto end;
            } else if (value == dummy) {
                Py_DECREF(value);
                goto end;  // failed
            } else {
                subject = va_arg(subjects, PyObject**);
                if (subject) {
                    __Pyx_XDECREF_SET(*subject, value);
                    __Pyx_GOTREF(*subject);
                } else {
                    Py_DECREF(value);
                }
            }
        }
    }
    result = 1;

    end:
    Py_XDECREF(dummy);
    Py_XDECREF(get);
    return result;
}

///////////////////////// ExtractGeneric.proto ////////////////////////////////

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
#define __Pyx_MatchCase_Mapping_Extract(...) __Pyx__MatchCase_Mapping_Extract(__pyx_refnanny, __VA_ARGS__)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_Extract(PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...); /* proto */
#endif

////////////////////// ExtractGeneric //////////////////////////////////////
//@requires: ExtractExactDict
//@requires: ExtractNonDict

#if CYTHON_REFNANNY
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(__Pyx_RefNannyAPIStruct *__pyx_refnanny, PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...)
#else
static CYTHON_INLINE int __Pyx_MatchCase_Mapping_Extract(PyObject *map, PyObject *fixed_keys, PyObject *var_keys, ...)
#endif
{
    va_list subjects;
    int result;

    va_start(subjects, var_keys);
    if (PyDict_CheckExact(map)) {
        result = __Pyx_MatchCase_Mapping_ExtractDictV(map, fixed_keys, var_keys, subjects);
    } else {
        result = __Pyx_MatchCase_Mapping_ExtractNonDictV(map, fixed_keys, var_keys, subjects);
    }
    va_end(subjects);
    return result;
}

///////////////////////////// DoubleStarCapture.proto //////////////////////

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *map, PyObject *const_temps, PyObject *var_temps); /* proto */

//////////////////////////// DoubleStarCapture //////////////////////////////

// The implementation is largely copied from the original COPY_DICT_WITHOUT_KEYS opcode
// implementation of CPython
// https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Python/ceval.c#L3977
// (now removed in favour of building the same thing from a combination of opcodes)
// The differences are:
//  1. We loop over separate tuples for constant and runtime keys
//  2. We add a shortcut for when there will be no left over keys (because I'm guess it's pretty common)
//
// Tempita variable 'tag' can be "NonDict", "ExactDict" or empty

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *map, PyObject *const_temps, PyObject *var_temps) {
    PyObject *dict_out;
    PyObject *tuples[] = { const_temps, var_temps };
    Py_ssize_t i, j;

    {{if tag != "NonDict"}}
    // shortcut for when there are no left-over keys
    if ({{if tag=="ExactDict"}}PyDict_CheckExact(map){{else}}(1){{endif}}) {
        Py_ssize_t s = PyDict_Size(map);
        if (s == -1) {
            return NULL;
        }
        if (s == (PyTuple_GET_SIZE(const_temps) + PyTuple_GET_SIZE(var_temps))) {
            return PyDict_New();
        }
    }
    {{endif}}

    {{if tag=="ExactDict"}}
    dict_out = PyDict_Copy(map);
    {{else}}
    dict_out = PyDict_New();
    {{endif}}
    if (!dict_out) {
        return NULL;
    }
    {{if tag!="ExactDict"}}
    if (PyDict_Update(dict_out, map)) {
        Py_DECREF(dict_out);
        return NULL;
    }
    {{endif}}

    for (i=0; i<2; ++i) {
        PyObject *keys = tuples[i];
        for (j=0; j<PyTuple_GET_SIZE(keys); ++j) {
            if (PyDict_DelItem(dict_out, PyTuple_GET_ITEM(keys, j))) {
                Py_DECREF(dict_out);
                return NULL;
            }
        }
    }
    return dict_out;
}
