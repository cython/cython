///////////////////////// UFuncsInit.proto /////////////////////////
//@proto_block: utility_code_proto_before_types

#include <numpy/arrayobject.h>
#include <numpy/ufuncobject.h>

// account for change in type of arguments to PyUFuncGenericFunction in Numpy 1.19.x
// Unfortunately we can only test against Numpy version 1.20.x since it wasn't marked
// as an API break. Therefore, I'm "solving" the issue by casting function pointer types
// on lower Numpy versions.
#if NPY_API_VERSION >= 0x0000000e // Numpy 1.20.x
#define __PYX_PYUFUNCGENERICFUNCTION_CAST(x) x
#else
#define __PYX_PYUFUNCGENERICFUNCTION_CAST(x) (PyUFuncGenericFunction)x
#endif

/////////////////////// UFuncTypeHandling.proto //////////////

#define __PYX_GET_NPY_COMPLEX_TYPE(tp) \
    sizeof(tp) == sizeof(npy_cfloat) ? NPY_CFLOAT : \
    sizeof(tp) == sizeof(npy_cdouble) ? NPY_CDOUBLE : \
    sizeof(tp) == sizeof(npy_clongdouble) ? NPY_CLONGDOUBLE : NPY_NOTYPE

#define __PYX_GET_NPY_FLOAT_TYPE(tp) \
    sizeof(tp) == sizeof(npy_float) ? NPY_FLOAT : \
    sizeof(tp) == sizeof(npy_double) ? NPY_DOUBLE : \
    sizeof(tp) == sizeof(npy_longdouble) ? NPY_LONGDOUBLE : NPY_NOTYPE

#define __PYX_GET_NPY_UINT_TYPE(tp) \
    sizeof(tp) == 1 ? NPY_UINT8 : \
    sizeof(tp) == 2 ? NPY_UINT16 : \
    sizeof(tp) == 4 ? NPY_UINT32 : \
    sizeof(tp) == 8 ? NPY_UINT64 : NPY_NOTYPE

#define __PYX_GET_NPY_SINT_TYPE(tp) \
    sizeof(tp) == 1 ? NPY_INT8 : \
    sizeof(tp) == 2 ? NPY_INT16 : \
    sizeof(tp) == 4 ? NPY_INT32 : \
    sizeof(tp) == 8 ? NPY_INT64 : NPY_NOTYPE

#define __PYX_GET_NPY_INT_TYPE(tp) ( \
    (((tp)-1) > (tp)0) ? \
        (__PYX_GET_NPY_UINT_TYPE(tp)) : \
        (__PYX_GET_NPY_SINT_TYPE(tp)) )

static int __Pyx_validate_ufunc_types(char *types, Py_ssize_t count, Py_ssize_t input_count);

/////////////////////// UFuncTypeHandling ///////////////

// DW - it's a bit of a shame that this has to be a runtime check since the C compiler does
// know it. We could make this a compile-time error in C++, but not easily in C.
static int __Pyx_validate_ufunc_types(char *types, Py_ssize_t count, Py_ssize_t input_count) {
    Py_ssize_t i;
    for (i=0; i<count; ++i) {
        if (types[i] == NPY_NOTYPE) {
            PyErr_Format(
                PyExc_TypeError,
                "Invalid type for %s argument %d to ufunc. "
                "This is from an external typedef that Cython could not resolve.",
                (i < input_count ? "input" : "output"),
                (i < input_count ? i : i - input_count)
            );
            return -1;
        }
    }
    return 0;
}

/////////////////////// UFuncConsts.proto ////////////////////

// getter functions because we can't forward-declare arrays
static PyUFuncGenericFunction* {{ufunc_funcs_name}}(void); /* proto */
static char* {{ufunc_types_name}}(void); /* proto */
static void* {{ufunc_data_name}}[] = {NULL};  /* always null */

/////////////////////// UFuncConsts /////////////////////////

static PyUFuncGenericFunction* {{ufunc_funcs_name}}(void) {
    static PyUFuncGenericFunction arr[] = {
        {{for loop, cname in looper(func_cnames)}}
        __PYX_PYUFUNCGENERICFUNCTION_CAST(&{{cname}}){{if not loop.last}},{{endif}}
        {{endfor}}
    };
    return arr;
}

static char* {{ufunc_types_name}}(void) {
    static char arr[] = {
        {{for loop, tp in looper(type_constants)}}
        {{tp}}{{if not loop.last}},{{endif}}
        {{endfor}}
    };
    return arr;
}
