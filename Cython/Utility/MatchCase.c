///////////////////////////// ABCCheck //////////////////////////////
//@requires: Builtins.c::PyFrozenDict

#if PY_VERSION_HEX < 0x030A0000 || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY
static CYTHON_INLINE int __Pyx_MatchCase_IsExactSequence(PyObject *o) {
    // Is one of the small list of builtin types known to be a sequence.
    if (PyList_CheckExact(o) || PyTuple_CheckExact(o) ||
            Py_IS_TYPE(o, &PyRange_Type) || Py_IS_TYPE(o, &PyMemoryView_Type)) {
        // Use exact type match for these checks. In in the event of inheritance we need to make sure
        // that it isn't a mapping too
        return 1;
    }
    return 0;
}

static CYTHON_INLINE int __Pyx_MatchCase_IsExactMapping(PyObject *o) {
    // dict and frozendict are the only regularly used mapping type.
    // "types.MappingProxyType" also exists but is correctly covered by
    // the isinstance(o, Mapping) check.
    return __Pyx_PyAnyDict_CheckExact(o);
}

static int __Pyx_MatchCase_IsExactNeitherSequenceNorMapping(PyObject *o) {
    if (PyByteArray_Check(o) || PyBytes_Check(o) || PyUnicode_Check(o)) {
        // These types are deliberately excluded from the sequence test
        // even though they look like sequences for most other purposes.
        // Leaving them as inexact checks since they do pass
        // "isinstance(o, collections.abc.Sequence)" so it's very hard to
        // reason about their subclasses.
        return 1;
    }
    // No-exhaustive list of other common builtin types as an optimization.
    if (o == Py_None || PyLong_CheckExact(o) || PyFloat_CheckExact(o) ||
        Py_TYPE(o) == &PyBool_Type || Py_TYPE(o) == &PySlice_Type ||
        PyAnySet_CheckExact(o) || PyComplex_CheckExact(o)) {
        return 1;
    }

    return 0;
}

// sequence_mapping_temp: For Python 3.10 testing sequences and mappings are
// really quick and this is ignored. For lower versions of Python they're
// slow, especially in the "fail" case.
// Therefore, we store an int temp to avoid duplicating tests.
// The bits of it in order are:
//  0. definitely a sequence
//  1. definitely a mapping
//     - note that both of the above can be true when
//        the type is registered with both abc types (not via inheritance)
//       and in this case we return true for both IsSequence or IsMapping
//       (which seems like the best handling of an ambiguous situation)
//  2. definitely not a sequence
//  3. definitely not a mapping

#define __PYX_DEFINITELY_SEQUENCE_FLAG 1U
#define __PYX_DEFINITELY_MAPPING_FLAG (1U<<1)
#define __PYX_DEFINITELY_NOT_SEQUENCE_FLAG (1U<<2)
#define __PYX_DEFINITELY_NOT_MAPPING_FLAG (1U<<3)
#define __PYX_SEQUENCE_MAPPING_ERROR (1U<<4)  // only used by the ABCCheck function

static int __Pyx_MatchCase_InitAbcType(PyObject *abc_module, PyObject **abc_type, PyObject *name) {
    if (*abc_type) return 0;
    *abc_type = PyObject_GetAttr(abc_module, name);
    return *abc_type ? 0 : -1;
}

// The result is defined using the specification for sequence_mapping_temp
// (detailed in "is_sequence").
static unsigned int __Pyx_MatchCase_ABCCheck(PyObject *o, int sequence_first, int definitely_not_sequence, int definitely_not_mapping) {
    // In Python 3.10+, objects can have their sequence bit set or their mapping bit set
    // but not both. Practically, this translates to "which type is registered first".
    // In Python < 3.10 we can only determine this if they're direct bases (by looking
    // at the MRO order). If they're registered manually then we can't tell.

    PyObject *abc_module=NULL, *sequence_type=NULL, *mapping_type=NULL;
    PyObject *mro;
    int sequence_result=0, mapping_result=0;
    unsigned int result = 0;

    if (sequence_first && definitely_not_sequence) {
        return __PYX_DEFINITELY_NOT_SEQUENCE_FLAG;
    }
    if (!sequence_first && definitely_not_mapping) {
        return __PYX_DEFINITELY_NOT_MAPPING_FLAG;
    }

    abc_module = PyImport_ImportModule("collections.abc");
    if (!abc_module) {
        return __PYX_SEQUENCE_MAPPING_ERROR;
    }
    if (sequence_first) {
        if (unlikely(__Pyx_MatchCase_InitAbcType(abc_module, &sequence_type, PYIDENT("Sequence")) == -1)) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        }
        sequence_result = PyObject_IsInstance(o, sequence_type);
        if (sequence_result <= 0) {
            result = sequence_result < 0 ? __PYX_SEQUENCE_MAPPING_ERROR : __PYX_DEFINITELY_NOT_SEQUENCE_FLAG;
            goto end;
        }
        // else sequence_result==1 but wait to see what mapping is
    }
    if (!definitely_not_mapping) {
        if (unlikely(__Pyx_MatchCase_InitAbcType(abc_module, &mapping_type, PYIDENT("Mapping")) == -1)) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        }
        mapping_result = PyObject_IsInstance(o, mapping_type);
        if (unlikely(mapping_result < 0)) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        } else if (mapping_result == 0 && !sequence_first) {
            result = __PYX_DEFINITELY_NOT_MAPPING_FLAG;
            goto end;
        } // else mapping_result == 1
    }
    if (!sequence_first && !definitely_not_sequence) {
        if (unlikely(__Pyx_MatchCase_InitAbcType(abc_module, &sequence_type, PYIDENT("Sequence")) == -1)) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        }
        sequence_result = PyObject_IsInstance(o, sequence_type);
        if (unlikely(sequence_result < 0)) {
            result = __PYX_SEQUENCE_MAPPING_ERROR;
            goto end;
        }
    }
    result |= (sequence_result ? __PYX_DEFINITELY_SEQUENCE_FLAG : __PYX_DEFINITELY_NOT_SEQUENCE_FLAG);
    result |= (mapping_result ? __PYX_DEFINITELY_MAPPING_FLAG : __PYX_DEFINITELY_NOT_MAPPING_FLAG);
    if (result != (__PYX_DEFINITELY_SEQUENCE_FLAG | __PYX_DEFINITELY_MAPPING_FLAG)) {
        goto end;
    }

    // It's an instance of both types. Look up the MRO order.
    // In event of failure treat it as "could be either"
    mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
    Py_ssize_t i, mro_size;
    if (!mro) {
        PyErr_Clear();
        goto end;
    }
    if (!PyTuple_Check(mro)) {
        Py_DECREF(mro);
        goto end;
    }
    mro_size = __Pyx_PyTuple_GET_SIZE(mro);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(mro_size == -1)) {
        goto loop_error;
    }
#endif
    for (i=1; i < mro_size; ++i) {
        int is_subclass_sequence, is_subclass_mapping;
        PyObject *mro_item = __Pyx_PyTuple_GET_ITEM(mro, i);
#if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!mro_item)) goto loop_error;
#endif
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
    // registered first so accept the object as either as a compromise.
    loop_error_recovery:
    Py_DECREF(mro);

    end:
    Py_XDECREF(abc_module);
    Py_XDECREF(sequence_type);
    Py_XDECREF(mapping_type);
    return result;

    loop_error:
    PyErr_Clear();
    goto loop_error_recovery;
}
#endif

///////////////////////////// IsSequence.proto //////////////////////

static int __Pyx_MatchCase_IsSequence(PyObject *o, unsigned int *sequence_mapping_temp); /* proto */

//////////////////////////// IsSequence /////////////////////////
//@requires: ABCCheck

static int __Pyx_MatchCase_IsSequence(PyObject *o, unsigned int *sequence_mapping_temp) {
#if PY_VERSION_HEX >= 0x030A0000 && !(CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY)
    return __Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_SEQUENCE);
#else
#if CYTHON_COMPILING_IN_LIMITED_API
    // In the Limited API we have runtime access to Py_TPFLAGS_SEQUENCE
    // by looking it up on module init so it's still worth attempting
    // the fast path.
    if (__Pyx_Runtime_TPFLAGS_SEQUENCE) {
        return __Pyx_PyType_HasFeature(Py_TYPE(o), __Pyx_Runtime_TPFLAGS_SEQUENCE);
    }
#elif defined(Py_TPFLAGS_SEQUENCE)
    // Elsewhere *we* define Py_TPFLAGS_SEQUENCE but that doesn't necessarily
    // mean other types use it, so only success is meaningful.
    if (__Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_SEQUENCE)) {
        return 1;
    }
#endif
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
        // Probably quicker to just assign it and not check from here.
        sequence_mapping_temp = &dummy;
    }

    // Start by checking a known list of types.
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
    // Do the test by checking the module name, and then importing/testing the class.
    // It also doesn't give perfect results for classes that inherit from both array.array
    // and a mapping.
#if !CYTHON_COMPILING_IN_LIMITED_API || __PYX_LIMITED_VERSION_HEX < 0x030A0000
#if CYTHON_COMPILING_IN_LIMITED_API
    if (__Pyx_get_runtime_version() < 0x030A0000)
#endif
    {
        o_module_name = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__module__");
        if (!o_module_name) {
            return -1;
        }
        if (PyUnicode_Check(o_module_name) && PyUnicode_CompareWithASCIIString(o_module_name, "array") == 0)
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
    }
#else
    CYTHON_UNUSED_VAR(o_module_name);
#endif
    *sequence_mapping_temp |= __PYX_DEFINITELY_NOT_SEQUENCE_FLAG;
    return 0;
#endif
}

////////////////////// OtherSequenceSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_OtherSequenceSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// OtherSequenceSliceToList //////////////////////////

// This is substantially based off ceval unpack_iterable.
// It's also pretty similar to itertools.islice.
// Indices must be positive - there's no wraparound or boundschecking.

static PyObject *__Pyx_MatchCase_OtherSequenceSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
    int total = end-start;
    int i;
    PyObject *list;
    ssizeargfunc slot;

    list = PyList_New(total);
    if (!list) {
        return NULL;
    }

    slot = __Pyx_PyObject_TryGetSubSlot(x, tp_as_sequence, sq_item, ssizeargfunc);
    if (!slot) {
        #if !CYTHON_COMPILING_IN_LIMITED_API && !defined(PySequence_ITEM)
        // PyPy (and maybe others?) implements PySequence_ITEM as a function. In this case.
        // it's slightly more efficient than using PySequence_GetItem since it skips negative indices.
        slot = PySequence_ITEM;
        #else
        slot = PySequence_GetItem;
        #endif
    }

    for (i=start; i<end; ++i) {
        PyObject *obj = slot(x, i);
        if (unlikely(!obj) || unlikely(__Pyx_PyList_SET_ITEM(list, i-start, obj) == -1)) {
            Py_DECREF(list);
            return NULL;
        }
    }
    return list;
}

////////////////////// TupleSliceToList.proto //////////////////////

static PyObject *__Pyx_MatchCase_TupleSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end); /* proto */

////////////////////// TupleSliceToList //////////////////////////
//@requires: OtherSequenceSliceToList
//@requires: ObjectHandling.c::ListFromArray

// Indices must be positive - there's no wraparound or boundschecking.

static PyObject *__Pyx_MatchCase_TupleSliceToList(PyObject *x, Py_ssize_t start, Py_ssize_t end) {
#if !CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_MatchCase_OtherSequenceSliceToList(x, start, end);
#else
    PyObject **array;

    (void)__Pyx_MatchCase_OtherSequenceSliceToList; // clear unused warning

    array = &PyTuple_GET_ITEM(x, 0);
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
#if PY_VERSION_HEX >= 0x030A0000 && !(CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY)
    return __Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_MAPPING);
#else
#if CYTHON_COMPILING_IN_LIMITED_API
    // In the Limited API we have runtime access to Py_TPFLAGS_MAPPING
    // by looking it up on module init so it's still worth attempting
    // the fast path.
    if (__Pyx_Runtime_TPFLAGS_MAPPING) {
        return __Pyx_PyType_HasFeature(Py_TYPE(o), __Pyx_Runtime_TPFLAGS_MAPPING);
    }
#elif defined(Py_TPFLAGS_MAPPING)
    // Elsewhere *we* define Py_TPFLAGS_SEQUENCE but that doesn't necessarily
    // mean other types use it, so only success is meaningful.
    if (__Pyx_PyType_HasFeature(Py_TYPE(o), Py_TPFLAGS_MAPPING)) {
        return 1;
    }
#endif
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
    PyErr_Format(PyExc_ValueError,
                 "mapping pattern checks duplicate key (%R)", key);
    bad:
    Py_DECREF(var_keys_set);
    return -1;
}

/////////////////////////// ExtractExactDict.proto ////////////////

// The subjects array is a list of PyObject** to subjects to be filled. They may be NULL
// in which case they're ignored.
//
// This is a specialized version for when we have an exact (frozen)dict (which is likely to be pretty common)

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_Mapping_ExtractDict(...) __Pyx__MatchCase_Mapping_ExtractDict(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_Mapping_ExtractDict(...) __Pyx__MatchCase_Mapping_ExtractDict(NULL, __VA_ARGS__)
#endif
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(void *__pyx_refnanny, PyObject *dict, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]); /* proto */

/////////////////////////// ExtractExactDict ////////////////

static CYTHON_INLINE int __Pyx__MatchCase_Mapping_ExtractDict(void *__pyx_refnanny, PyObject *dict, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]) {
    Py_ssize_t i;
    Py_ssize_t size;
    size = PyDict_Size(dict);
    if (size < nKeys) {
        return size == -1 ? -1: 0;
    }

    for (i=0; i<nKeys; ++i) {
        PyObject *key = keys[i];
        PyObject **subject = subjects[i];
        if (!subject) {
            int contains = PyDict_Contains(dict, key);
            if (contains <= 0) {
                return contains; // any subjects that were already set will be cleaned up externally
            }
        } else {
            PyObject *value;
            int getref_result = __Pyx_PyDict_GetItemRef(dict, key, &value);
            if (getref_result != 1) {
                return getref_result;  // any subjects that were already set will be cleaned up externally
            }
            __Pyx_GOTREF(value);
            __Pyx_XDECREF_SET(*subject, value);
        }
    }
    return 1;  // success
}

///////////////////////// ExtractNonDict.proto ////////////////////////////////

// The subjects array is a list of PyObject** to subjects to be filled. They may be NULL
// in which case they're ignored.
//
// This is a specialized version for the rarer case when the type isn't an exact dict.

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
    Py_ssize_t i, size;
    int result = 0;
#if CYTHON_UNPACK_METHODS && CYTHON_VECTORCALL
    PyObject *get_method = NULL, *get_self = NULL;
#endif

    // Length check is undocumented but does take place in CPython and is probably worthwhile.
    size = PyObject_Length(mapping);
    if (size < nKeys) {
        return size == -1 ? -1: 0;
    }

    dummy = PyObject_CallObject((PyObject *)&PyBaseObject_Type, NULL);
    if (!dummy) {
        return -1;
    }
    get = PyObject_GetAttr(mapping, PYIDENT("get"));
    if (!get) {
        result = -1;
        goto end;
    }
#if CYTHON_UNPACK_METHODS && CYTHON_VECTORCALL
    if (likely(PyMethod_Check(get))) {
        // both of these are borrowed
        get_method = PyMethod_GET_FUNCTION(get);
        get_self = PyMethod_GET_SELF(get);
    }
#endif

    for (i=0; i<nKeys; ++i) {
        PyObject **subject;
        PyObject *value = NULL;
        PyObject *key = keys[i];

        // TODO - there's an optimization here (although it deviates from the strict definition of pattern matching).
        // If we don't need the values then we can call PyObject_Contains instead of "get". If we don't need *any*
        // of the values then we can skip initialization "get" and "dummy"
#if CYTHON_UNPACK_METHODS && CYTHON_VECTORCALL
        if (likely(get_method)) {
            PyObject *args[] = { get_self, key, dummy };
            value = PyObject_Vectorcall(get_method, args, 3, NULL);
        }
        else
#endif
        {
            value = __Pyx_PyObject_Call2Args(get, key, dummy);
        }
        if (!value) {
            result = -1;
            goto end;
        } else if (value == dummy) {
            Py_DECREF(value);
            goto end;  // failed to match.
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

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_Mapping_Extract(...) __Pyx__MatchCase_Mapping_Extract(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_Mapping_Extract(...) __Pyx__MatchCase_Mapping_Extract(NULL, __VA_ARGS__)
#endif
static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]); /* proto */

////////////////////// ExtractGeneric //////////////////////////////////////
//@requires: ExtractExactDict
//@requires: ExtractNonDict
//@requires: Builtins.c::PyFrozenDict

static CYTHON_INLINE int __Pyx__MatchCase_Mapping_Extract(void *__pyx_refnanny, PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys, PyObject **subjects[]) {
    if (__Pyx_PyAnyDict_CheckExact(mapping)) {
        return __Pyx_MatchCase_Mapping_ExtractDict(mapping, keys, nKeys, subjects);
    } else {
        return __Pyx_MatchCase_Mapping_ExtractNonDict(mapping, keys, nKeys, subjects);
    }
}

///////////////////////////// DoubleStarCapture.proto //////////////////////

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys); /* proto */

//////////////////////////// DoubleStarCapture //////////////////////////////
//@requires: Builtins.c::PyFrozenDict

// The implementation is largely copied from the original COPY_DICT_WITHOUT_KEYS opcode
// implementation of CPython
// https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Python/ceval.c#L3977
// (now removed in favour of building the same thing from a combination of opcodes)
// The differences are:
//  1. We use an array of keys rather than a tuple of keys
//  2. We add a shortcut for when there will be no left over keys (because I guess it's pretty common)
//
// Tempita variable 'tag' can be "NonDict", "ExactDict", "ExactFrozenDict" or empty

static PyObject* __Pyx_MatchCase_DoubleStarCapture{{tag}}(PyObject *mapping, PyObject *keys[], Py_ssize_t nKeys) {
    PyObject *dict_out;
    Py_ssize_t i, size;

    // shortcut for when there are no left-over keys
    {{if tag=="ExactDict" or tag=="ExactFrozenDict"}}
    if ((1))
    {{else}}
    if (__Pyx_PyAnyDict_CheckExact(mapping))
    {{endif}}
    {
        size = PyDict_Size(mapping);
    } else {
        size = PyObject_Length(mapping);
    }
    if (unlikely(size == -1)) return NULL;
    if (size == nKeys) {
        return PyDict_New();
    }

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

#if CYTHON_REFNANNY
#define __Pyx_MatchCase_ClassPositional(...) __Pyx__MatchCase_ClassPositional(__pyx_refnanny, __VA_ARGS__)
#else
#define __Pyx_MatchCase_ClassPositional(...) __Pyx__MatchCase_ClassPositional(NULL, __VA_ARGS__)
#endif
static int __Pyx__MatchCase_ClassPositional(void *__pyx_refnanny, PyObject *subject, PyTypeObject *type, PyObject *fixed_names[], Py_ssize_t n_fixed, int match_self, PyObject **subjects[], Py_ssize_t n_subjects); /* proto */

/////////////////////////// ClassPositionalPatterns //////////////////////////////
//@requires: ObjectHandling.c::FormatTypeName
//@requires: Builtins.c::PyFrozenDict

static int __Pyx_MatchCase_ClassCheckDuplicateAttrs(PyTypeObject *type, PyObject *fixed_names[], Py_ssize_t n_fixed, PyObject *match_args,  Py_ssize_t num_args) {
    // a lot of the basic logic of this is shared with __Pyx_MatchCase_CheckMappingDuplicateKeys
    // but they take different input types so it isn't easy to actually share the code.

    // Inputs are tuples, and typically fairly small. It may be more efficient to
    // loop over the tuple than create a set.
 
    PyObject *attrs_set;
    PyObject *attr = NULL;
    Py_ssize_t n, match_args_size;
    int contains;

    attrs_set = PySet_New(NULL);
    if (unlikely(!attrs_set)) return -1;

    match_args_size = __Pyx_PyTuple_GET_SIZE(match_args);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(match_args_size < 0)) return -1;
#endif
    num_args = match_args_size < num_args ? match_args_size : num_args;
    for (n=0; n < num_args; ++n) {
        attr = __Pyx_PyTuple_GET_ITEM(match_args, n);
#if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!attr)) goto bad;
#endif
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
    for (n=0; n < n_fixed; ++n) {
        attr = fixed_names[n];
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
    {
        __Pyx_TypeName tp_name = __Pyx_PyType_GetFullyQualifiedName(type);
        PyErr_Format(PyExc_TypeError, __Pyx_FMT_TYPENAME "() got multiple sub-patterns for attribute %R",
                        tp_name, attr);
        __Pyx_DECREF_TypeName(tp_name);
    }
    bad:
    Py_DECREF(attrs_set);
    return -1;
}

// Adapted from ceval.c "match_class" in CPython
//
// The argument match_self can equal 1 for "known to be true"
//                                   0 for "known to be false"
//                                  -1 for "unknown", runtime test
// n_subjects is >= 0 otherwise this function will be skipped
static int __Pyx__MatchCase_ClassPositional(void *__pyx_refnanny, PyObject *subject, PyTypeObject *type, PyObject *fixed_names[], Py_ssize_t n_fixed, int match_self, PyObject **subjects[], Py_ssize_t n_subjects)
{
    PyObject *match_args = NULL;
    Py_ssize_t allowed, i;
    int result;

    if (match_self != 1) {
#if __PYX_LIMITED_VERSION_HEX >= 0x030d0000
        if (PyObject_GetOptionalAttr((PyObject*)type, PYIDENT("__match_args__"), &match_args) == -1) {
            return -1;
        }
#else
        match_args = PyObject_GetAttr((PyObject*)type, PYIDENT("__match_args__"));
        if (!match_args) {
            if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
                PyErr_Clear();
            } else {
                return -1;
            }
        }
#endif
    }
    if (match_args) {
        match_self = 0;
        if (!PyTuple_CheckExact(match_args)) {
            __Pyx_TypeName type_typename = __Pyx_PyType_GetFullyQualifiedName(type);
            __Pyx_TypeName match_args_type_name = __Pyx_PyType_GetFullyQualifiedName(Py_TYPE(match_args));
            PyErr_Format(PyExc_TypeError, __Pyx_FMT_TYPENAME ".__match_args__ must be a tuple (got " __Pyx_FMT_TYPENAME ")",
                type_typename,
                match_args_type_name
            );
            Py_DECREF(match_args);
            __Pyx_DECREF_TypeName(type_typename);
            __Pyx_DECREF_TypeName(match_args_type_name);
            return -1;
        }
    } else if (!match_args && match_self == -1) {
        // Mysteriously, this private flag seems to have ended up defined in the Limited API
        #if defined(_Py_TPFLAGS_MATCH_SELF) && !(CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030A0000)
        match_self = PyType_HasFeature(type,
                                    _Py_TPFLAGS_MATCH_SELF);
        #else
        // probably an earlier version of Python. Go off the known list in the specification
        match_self = ((PyType_GetFlags(type) &
                        // long should capture bool too
                        (Py_TPFLAGS_LONG_SUBCLASS | Py_TPFLAGS_LIST_SUBCLASS | Py_TPFLAGS_TUPLE_SUBCLASS |
                            Py_TPFLAGS_BYTES_SUBCLASS | Py_TPFLAGS_UNICODE_SUBCLASS | Py_TPFLAGS_DICT_SUBCLASS
                        )) ||
                        PyType_IsSubtype(type, &PyByteArray_Type) ||
                        PyType_IsSubtype(type, &PyFloat_Type) ||
                        PyType_IsSubtype(type, &PyFrozenSet_Type) ||
                        PyType_IsSubtype(type, __Pyx_PyFrozenDict_TypePtr)
                        );
        #endif
    }

    if (match_self) {
        allowed = 1;
    } else if (match_args) {
        allowed = __Pyx_PyTuple_GET_SIZE(match_args);
#if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(allowed < 0)) goto end;
#endif
    } else {
        allowed = 0;
    }
    if (allowed < n_subjects) {
        const char *plural = (allowed == 1) ? "" : "s";
        __Pyx_TypeName type_name = __Pyx_PyType_GetFullyQualifiedName(type);
        PyErr_Format(PyExc_TypeError,
                     __Pyx_FMT_TYPENAME "() accepts %d positional sub-pattern%s (%d given)",
                     type_name,
                     allowed, plural, n_subjects);
        __Pyx_DECREF_TypeName(type_name);
        Py_XDECREF(match_args);
        return -1;
    }
    if (match_self) {
        PyObject **self_subject = subjects[0];
        if (self_subject) {
            // Easy. Copy the subject itself, and move on to kwargs.
            __Pyx_XDECREF_SET(*self_subject, subject);
            __Pyx_INCREF(*self_subject);
        }
        result = 1;
        goto end_match_self;
    }
    // next stage is to check for duplicate attributes.
    if (__Pyx_MatchCase_ClassCheckDuplicateAttrs(type, fixed_names, n_fixed, match_args, n_subjects)) {
        result = -1;
        goto end;
    }

    for (i = 0; i < n_subjects; i++) {
        PyObject *attr;
        PyObject **subject_i;
        PyObject *name = __Pyx_PyTuple_GET_ITEM(match_args, i);
#if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!name)) {
            result = -1;
            goto end;
        } 
#endif
        if (!PyUnicode_CheckExact(name)) {
            __Pyx_TypeName name_type_name = __Pyx_PyType_GetFullyQualifiedName(Py_TYPE(name));    
            PyErr_Format(PyExc_TypeError,
                         "__match_args__ elements must be strings "
                         "(got " __Pyx_FMT_TYPENAME ")", name_type_name);
            __Pyx_DECREF_TypeName(name_type_name);
            result = -1;
            goto end;
        }

        attr = PyObject_GetAttr(subject, name);
        if (attr == NULL && PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Clear();
            result = 0;
            goto end;
        }
        subject_i = subjects[i];
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
    return result;
}

//////////////////////// MatchClassIsType.proto /////////////////////////////

static PyTypeObject* __Pyx_MatchCase_IsType(PyObject* type); /* proto */

//////////////////////// MatchClassIsType /////////////////////////////

static PyTypeObject* __Pyx_MatchCase_IsType(PyObject* type) {
    if (!PyType_Check(type)) {
        PyErr_Format(PyExc_TypeError, "called match pattern must be a type");
        return NULL;
    }
    Py_INCREF(type);
    return (PyTypeObject*)type;
}
