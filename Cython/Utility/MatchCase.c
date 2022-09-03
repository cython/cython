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
    return __Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_SEQUENCE);
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

////////////////////// OtherSequenceSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_OtherSequenceSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// OtherSequenceSliceToList //////////////////////////

// This is substantially based off ceval unpack_iterable.
// It's also pretty similar to itertools.islice
// Indices must be postive - there's no wraparound or boundschecking

static PyObject *__Pyx_MatchCase_OtherSequenceSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
    int total = end-start;
    int i;
    PyObject *list;
    ssizeargfunc slot;
    PyTypeObject *type = Py_TYPE(x);
    
    list = PyList_New(total);
    if (!list) {
        return NULL;
    }

#if CYTHON_USE_TYPE_SLOTS || PY_MAJOR_VERSION < 3 || CYTHON_COMPILING_IN_PYPY
    slot = type->tp_as_sequence ? type->tp_as_sequence->sq_item : NULL;
#else
    if ((PY_VERSION_HEX >= 0x030A0000) || __Pyx_PyType_HasFeature(type, Py_TPFLAGS_HEAPTYPE)) {
        // PyType_GetSlot only works on heap types in Python <3.10
        slot = (ssizeargfunc) PyType_GetSlot(type, Py_sq_item);
    }
#endif
    if (!slot) {
        #if !defined(Py_LIMITED_API) && !defined(PySequence_ITEM)
        // PyPy (and maybe others?) implements PySequence_ITEM as a function. In this case
        // it's slightly more efficient than using PySequence_GetItem since it skips negative indices
        slot = PySequence_ITEM;
        #else
        slot = PySequence_GetItem;
        #endif
    }

    for (i=start; i<end; ++i) {
        PyObject *obj = slot(x, i);
        if (!obj) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i-start, obj);
    }
    return list;
}

////////////////////// TupleSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_TupleSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// TupleSliceToList //////////////////////////
//@requires: OtherSequenceSliceToList
//@requires: ObjectHandling.c::TupleAndListFromArray

// Note that this should also work fine on lists (if needed)
// Indices must be postive - there's no wraparound or boundschecking

static PyObject *__Pyx_MatchCase_TupleSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
#if !CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_MatchCase_OtherSequenceSliceToList(x, start, end);
#else
    PyObject **array;

    (void)__Pyx_MatchCase_OtherSequenceSliceToList; // clear unused warning

    array = PySequence_Fast_ITEMS(x);
    return __Pyx_PyList_FromArray(array+start, end-start);
#endif
}

////////////////////////// UnknownTypeSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_UnknownTypeSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

//////////////////////////  UnknownTypeSliceToList.proto //////////////////////
//@requires: TupleSliceToList
//@requires: OtherSequenceSliceToList

static PyObject *__Pyx_MatchCase_UnknownTypeSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
    if (PyList_CheckExact(x)) {
        return PyList_GetSlice(x, start, end);
    }
#if !CYTHON_COMPILING_IN_CPYTHON
    // since __Pyx_MatchCase_TupleToList only does anything special in CPython, skip the check otherwise
    if (PyTuple_CheckExact(x)) {
        return __Pyx_MatchCase_TupleSliceToList(x, start, end);
    }
#else
    (void)__Pyx_MatchCase_TupleSliceToList;
#endif
    return __Pyx_MatchCase_OtherSequenceSliceToList(x, start, end);
}

///////////////////////////// IsMapping.proto //////////////////////

static int __Pyx_MatchCase_IsMapping(PyObject *o, unsigned int *sequence_mapping_temp); /* proto */

//////////////////////////// IsMapping /////////////////////////
//@requires: ABCCheck

static int __Pyx_MatchCase_IsMapping(PyObject *o, unsigned int *sequence_mapping_temp) {
#if PY_VERSION_HEX >= 0x030A0000
    return __Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_MAPPING);
#else
    unsigned int abc_result, dummy=0;
    if (sequence_mapping_temp) {
        // do we already know the answer?
        if (*sequence_mapping_temp & __PYX_DEFINITELY_MAPPING_FLAG) {
            return 1;
        } else if (*sequence_mapping_temp & __PYX_DEFINITELY_NOT_MAPPING_FLAG) {
            return 0;
        }
    } else {
        sequence_mapping_temp = &dummy; // just so we can assign freely without checking
    }

    if (__Pyx_MatchCase_IsExactMapping(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_MAPPING_FLAG | __PYX_DEFINITELY_NOT_SEQUENCE_FLAG);
        return 1;
    }
    if (__Pyx_MatchCase_IsExactSequence(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_SEQUENCE_FLAG | __PYX_DEFINITELY_NOT_MAPPING_FLAG);
        return 0;
    }
    if (__Pyx_MatchCase_IsExactNeitherSequenceNorMapping(o)) {
        *sequence_mapping_temp |= (__PYX_DEFINITELY_NOT_SEQUENCE_FLAG | __PYX_DEFINITELY_NOT_MAPPING_FLAG);
        return 0;
    }

    // otherwise check against collections.abc.Mapping
    abc_result = __Pyx_MatchCase_ABCCheck(
        o, 0,
        *sequence_mapping_temp & __PYX_DEFINITELY_NOT_SEQUENCE_FLAG,
        *sequence_mapping_temp & __PYX_DEFINITELY_NOT_MAPPING_FLAG
    );
    if (abc_result & __PYX_SEQUENCE_MAPPING_ERROR) {
        return -1;
    }
    *sequence_mapping_temp = abc_result;
    return *sequence_mapping_temp & __PYX_DEFINITELY_MAPPING_FLAG;
#endif
}

//////////////////////// MappingKeyCheck.proto /////////////////////////

static int __Pyx_MatchCase_CheckMappingDuplicateKeys(PyObject *keys[], Py_ssize_t nFixedKeys, Py_ssize_t nKeys);

//////////////////////// MappingKeyCheck ///////////////////////////////

static int __Pyx_MatchCase_CheckMappingDuplicateKeys(PyObject *keys[], Py_ssize_t nFixedKeys, Py_ssize_t nKeys) {
    // Inputs are arrays, and typically fairly small. It may be more efficient to
    // loop over the array than create a set.

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

    for (n=nFixedKeys; n < nKeys; ++n) {
        key = keys[n];
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
    for (n=0; n < nFixedKeys; ++n) {
        key = keys[n];
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
    #if PY_MAJOR_VERSION > 2
    PyErr_Format(PyExc_ValueError,
                 "mapping pattern checks duplicate key (%R)", key);
    #else
    // DW really can't be bothered working around features that don't exist in
    // Python 2, so just provide less information!
    PyErr_SetString(PyExc_ValueError,
                    "mapping pattern checks duplicate key");
    #endif
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
#define __Pyx_MatchCase_Mapping_ExtractDict(...) __Pyx__MatchCase_Mapping_ExtractDict(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_Mapping_ExtractDict(...) __Pyx__MatchCase_Mapping_ExtractDict(NULL, __VA_ARGS__)
#endif
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(void *__pyx_refnanny, PyObject *dict, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]); /* proto */

/////////////////////////// ExtractExactDict ////////////////

static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(void *__pyx_refnanny, PyObject *dict, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]) {
    Py_ssize_t i;

    for (i=0; i<nKeys; ++i) {
        PyObject *key = keys[i];
        PyObject **subject = subjects[i];
        if (!subject) {
            int contains = PyDict_Contains(dict, key);
            if (contains <= 0) {
                return -1; // any subjects that were already set will be cleaned up externally
            }
        } else {
            PyObject *value = __Pyx_PyDict_GetItemStrWithError(dict, key);
            if (!value) {
                return (PyErr_Occurred()) ? -1 : 0;  // any subjects that were already set will be cleaned up externally
            }
            __Pyx_XDECREF_SET(*subject, value);
            __Pyx_INCREF(*subject);  // capture this incref with refnanny!
        }
    }
    return 1;  // success
}

///////////////////////// ExtractNonDict.proto ////////////////////////////////

// the variadic arguments are a list of PyObject** to subjects to be filled. They may be NULL
// in which case they're ignored.
//
// This is a specialized version for the rarer case when the type isn't an exact dict.

#include <stdarg.h>

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_Mapping_ExtractNonDict(...) __Pyx__MatchCase_Mapping_ExtractNonDict(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_Mapping_ExtractNonDict(...) __Pyx__MatchCase_Mapping_ExtractNonDict(NULL, __VA_ARGS__)
#endif
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractNonDict(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]); /* proto */

///////////////////////// ExtractNonDict //////////////////////////////////////
//@requires: ObjectHandling.c::PyObjectCall2Args

// largely adapted from match_keys in CPython ceval.c

static int __Pyx__MatchCase_Mapping_ExtractNonDict(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]) {
    PyObject *dummy=NULL, *get=NULL;
    Py_ssize_t i;
    int result = 0;

    dummy = PyObject_CallObject((PyObject *)&PyBaseObject_Type, NULL);
    if (!dummy) {
        return -1;
    }
    get = PyObject_GetAttrString(mapping, "get");
    if (!get) {
        result = -1;
        goto end;
    }

    for (i=0; i<nKeys; ++i) {
        PyObject **subject;
        PyObject *value = NULL;
        PyObject *key = keys[i];

        // TODO - there's an optimization here (although it deviates from the strict definition of pattern matching). 
        // If we don't need the values then we can call PyObject_Contains instead of "get". If we don't need *any*
        // of the values then we can skip initialization "get" and "dummy"
        value = __Pyx_PyObject_Call2Args(get, key, dummy);
        if (!value) {
            result = -1;
            goto end;
        } else if (value == dummy) {
            Py_DECREF(value);
            goto end;  // failed
        } else {
            subject = subjects[i];
            if (subject) {
                __Pyx_XDECREF_SET(*subject, value);
                __Pyx_GOTREF(*subject);
            } else {
                Py_DECREF(value);
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

#include <stdarg.h>

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_Mapping_Extract(...) __Pyx__MatchCase_Mapping_Extract(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_Mapping_Extract(...) __Pyx__MatchCase_Mapping_Extract(NULL, __VA_ARGS__)
#endif
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]); /* proto */

////////////////////// ExtractGeneric //////////////////////////////////////
//@requires: ExtractExactDict
//@requires: ExtractNonDict

static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]) {
    if (PyDict_CheckExact(mapping)) {
        return __Pyx_MatchCase_Mapping_ExtractDict(mapping, keys, nKeys, subjects);
    } else {
        return __Pyx_MatchCase_Mapping_ExtractNonDict(mapping, keys, nKeys, subjects);
    }
}

///////////////////////////// DoubleStarCapture.proto //////////////////////

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys); /* proto */

//////////////////////////// DoubleStarCapture //////////////////////////////

// The implementation is largely copied from the original COPY_DICT_WITHOUT_KEYS opcode
// implementation of CPython
// https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Python/ceval.c#L3977
// (now removed in favour of building the same thing from a combination of opcodes)
// The differences are:
//  1. We use an array of keys rather than a tuple of keys
//  2. We add a shortcut for when there will be no left over keys (because I guess it's pretty common)
//
// Tempita variable 'tag' can be "NonDict", "ExactDict" or empty

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys) {
    PyObject *dict_out;
    Py_ssize_t i;

    {{if tag != "NonDict"}}
    // shortcut for when there are no left-over keys
    if ({{if tag=="ExactDict"}}(1){{else}}PyDict_CheckExact(mapping){{endif}}) {
        Py_ssize_t s = PyDict_Size(mapping);
        if (s == -1) {
            return NULL;
        }
        if (s == nKeys) {
            return PyDict_New();
        }
    }
    {{endif}}

    {{if tag=="ExactDict"}}
    dict_out = PyDict_Copy(mapping);
    {{else}}
    dict_out = PyDict_New();
    {{endif}}
    if (!dict_out) {
        return NULL;
    }
    {{if tag!="ExactDict"}}
    if (PyDict_Update(dict_out, mapping)) {
        Py_DECREF(dict_out);
        return NULL;
    }
    {{endif}}

    for (i=0; i<nKeys; ++i) {
        if (PyDict_DelItem(dict_out, keys[i])) {
            Py_DECREF(dict_out);
            return NULL;
        }
    }
    return dict_out;
}

////////////////////////////// ClassPositionalPatterns.proto ////////////////////////

#include <stdarg.h>

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_ClassPositional(...) __Pyx__MatchCase_ClassPositional(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_ClassPositional(...) __Pyx__MatchCase_ClassPositional(NULL, __VA_ARGS__)
#endif
static int __Pyx__MatchCase_ClassPositional(void *__pyx_refnanny, PyObject *subject, PyTypeObject *type, PyObject *keysnames_tuple, int match_self, int num_args, ...); /* proto */

/////////////////////////////// ClassPositionalPatterns //////////////////////////////

static int __Pyx_MatchCase_ClassCheckDuplicateAttrs(const char *tp_name, PyObject *fixed_names_tuple, PyObject *match_args,  Py_ssize_t num_args) {
    // a lot of the basic logic of this is shared with __Pyx_MatchCase_CheckMappingDuplicateKeys
    // but they take different input types so it isn't easy to actually share the code.

    // Inputs are tuples, and typically fairly small. It may be more efficient to
    // loop over the tuple than create a set.
 
    PyObject *attrs_set;
    PyObject *attr = NULL;
    Py_ssize_t n;
    int contains;

    attrs_set = PySet_New(NULL);
    if (!attrs_set) return -1;

    num_args = PyTuple_GET_SIZE(match_args) < num_args ? PyTuple_GET_SIZE(match_args) : num_args;
    for (n=0; n < num_args; ++n) {
        attr = PyTuple_GET_ITEM(match_args, n);
        contains = PySet_Contains(attrs_set, attr);
        if (contains < 0) {
            goto bad;
        } else if (contains == 1) {
            goto raise_error;
        } else {
            if (PySet_Add(attrs_set, attr)) {
                goto bad;
            }
        }
    }
    for (n=0; n < PyTuple_GET_SIZE(fixed_names_tuple); ++n) {
        attr = PyTuple_GET_ITEM(fixed_names_tuple, n);
        contains = PySet_Contains(attrs_set, attr);
        if (contains < 0) {
            goto bad;
        } else if (contains == 1) {
            goto raise_error;
        }
    }
    Py_DECREF(attrs_set);
    return 0;

    raise_error:
    #if PY_MAJOR_VERSION > 2
    PyErr_Format(PyExc_TypeError, "%s() got multiple sub-patterns for attribute %R",
                    tp_name, attr);
    #else
    // DW has no interest in working around the lack of %R in Python 2.7
    PyErr_Format(PyExc_TypeError, "%s() got multiple sub-patterns for attribute",
                    tp_name);
    #endif
    bad:
    Py_DECREF(attrs_set);
    return -1;
}

// Adapted from ceval.c "match_class" in CPython
//
// The argument match_self can equal 1 for "known to be true"
//                                   0 for "known to be false"
//                                  -1 for "unknown", runtime test
// nargs is >= 0 otherwise this function will be skipped
static int __Pyx__MatchCase_ClassPositional(void *__pyx_refnanny, PyObject *subject, PyTypeObject *type, PyObject *keysnames_tuple, int match_self, int num_args, ...)
{
    PyObject *match_args, *dup_key;
    Py_ssize_t allowed, i;
    int result;
    va_list subjects;

    match_args = PyObject_GetAttrString((PyObject*)type, "__match_args__");
    if (!match_args) {
        if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Clear();

            if (match_self == -1) {
                #if defined(_Py_TPFLAGS_MATCH_SELF)
                match_self = PyType_HasFeature(type,
                                            _Py_TPFLAGS_MATCH_SELF);
                #else
                // probably an earlier version of Python. Go off the known list in the specification
                match_self = ((PyType_GetFlags(type) &
                                // long should capture bool too
                                (Py_TPFLAGS_LONG_SUBCLASS | Py_TPFLAGS_LIST_SUBCLASS | Py_TPFLAGS_TUPLE_SUBCLASS |
                                 Py_TPFLAGS_BYTES_SUBCLASS | Py_TPFLAGS_UNICODE_SUBCLASS | Py_TPFLAGS_DICT_SUBCLASS
                                 #if PY_MAJOR_VERSION < 3
                                 | Py_TPFLAGS_IN_SUBCLASS
                                 #endif
                                )) ||
                              PyType_IsSubtype(type, &PyByteArray_Type) ||
                              PyType_IsSubtype(type, &PyFloat_Type) ||
                              PyType_IsSubtype(type, &PyFrozenSet_Type) ||
                              );
                #endif
            }
        } else {
            return -1;
        }
    } else {
        match_self = 0;
        if (!PyTuple_CheckExact(match_args)) {
            PyErr_Format(PyExc_TypeError, "%s.__match_args__ must be a tuple (got %s)",
                type->tp_name,
                Py_TYPE(match_args)->tp_name
            );
            Py_DECREF(match_args);
            return -1;
        }
    }

    allowed = match_self ?
        1 : (match_args ? PyTuple_GET_SIZE(match_args) : 0);
    if (allowed < num_args) {
        const char *plural = (allowed == 1) ? "" : "s";
        PyErr_Format(PyExc_TypeError,
                     "%s() accepts %d positional sub-pattern%s (%d given)",
                     type->tp_name,
                     allowed, plural, num_args);
        Py_XDECREF(match_args);
        return -1;
    }
    va_start(subjects, num_args);
    if (match_self) {
        PyObject **self_subject = va_arg(subjects, PyObject**);
        if (self_subject) {
            // Easy. Copy the subject itself, and move on to kwargs.
            __Pyx_XDECREF_SET(*self_subject, subject);
            __Pyx_INCREF(*self_subject);
        }
        result = 1;
        goto end_match_self;
    }
    // next stage is to check for duplicate attributes.
    if (__Pyx_MatchCase_ClassCheckDuplicateAttrs(type->tp_name, keysnames_tuple, match_args, num_args)) {
        result = -1;
        goto end;
    }

    for (i = 0; i < num_args; i++) {
        PyObject *attr;
        PyObject **subject_i;
        PyObject *name = PyTuple_GET_ITEM(match_args, i);
        if (!PyUnicode_CheckExact(name)) {
            PyErr_Format(PyExc_TypeError,
                         "__match_args__ elements must be strings "
                         "(got %s)", Py_TYPE(name)->tp_name);
            result = -1;
            goto end;
        }

        attr = PyObject_GetAttr(subject, name);
        if (attr == NULL && PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Clear();
            result = 0;
            goto end;
        }
        subject_i = va_arg(subjects, PyObject**);
        if (subject_i) {
            __Pyx_XDECREF_SET(*subject_i, attr);
            __Pyx_GOTREF(attr);
        } else {
            Py_DECREF(attr);
        }
    }
    result = 1;

    end:
    Py_DECREF(match_args);
    end_match_self:  // because match_args isn't set
    va_end(subjects);
    return result;
}

//////////////////////// MatchClassIsType.proto /////////////////////////////

static PyTypeObject* __Pyx_MatchCase_IsType(PyObject* type); /* proto */

//////////////////////// MatchClassIsType /////////////////////////////

static PyTypeObject* __Pyx_MatchCase_IsType(PyObject* type) {
    #if PY_MAJOR_VERSION < 3
    if (PyClass_Check(type)) {
        // I don't really think it's worth the effort getting this to work!
        PyErr_Format(PyExc_TypeError, "called match pattern must be a new-style class.");
        return NULL;
    }
    #endif
    if (!PyType_Check(type)) {
        PyErr_Format(PyExc_TypeError, "called match pattern must be a type");
        return NULL;
    }
    Py_INCREF(type);
    return (PyTypeObject*)type;
}
