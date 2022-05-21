///////////////////////// UFuncsInit.proto /////////////////////////
//@proto_block: utility_code_proto_before_types

#include <numpy/arrayobject.h>
#include <numpy/ufuncobject.h>

// account for change in type of arguments to PyUFuncGenericFunction
#if NPY_API_VERSION >= 0x0000000d  // Numpy 1.19.x
typedef const npy_intp __Pyx_const_npy_intp;
#else
typedef npy_intp __Pyx_const_npy_intp;
#endif

/////////////////////// UFuncConsts.proto ////////////////////

// getter functions because we can't forward-declare arrays
static PyUFuncGenericFunction* {{ufunc_funcs_name}}(void); /* proto */
static char* {{ufunc_types_name}}(void); /* proto */
static void* {{ufunc_data_name}}[] = {NULL};  // always null

/////////////////////// UFuncConsts /////////////////////////

static PyUFuncGenericFunction* {{ufunc_funcs_name}}(void) {
    static PyUFuncGenericFunction arr[] = {
        {{for loop, cname in looper(func_cnames)}}
        &{{cname}}{{if not loop.last}},{{endif}}
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
