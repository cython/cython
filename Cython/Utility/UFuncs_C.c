///////////////////////// UFuncsInit.proto /////////////////////////
//@proto_block: utility_code_proto_before_types

#include <numpy/arrayobject.h>
#include <numpy/ufuncobject.h>

/////////////////////// UFuncConsts.proto ////////////////////

static PyUFuncGenericFunction {{ufunc_funcs_name}}[];
static char {{ufunc_types_name}}[];
static void* {{ufunc_data_name}}[] = {NULL};  // always null

/////////////////////// UFuncConsts /////////////////////////


static PyUFuncGenericFunction {{ufunc_funcs_name}}[] = {
    {{for loop, cname in looper(func_cnames)}}
    &{{cname}}{{if not loop.last}},{{endif}}
    {{endfor}}
};

static char {{ufunc_types_name}}[] = {
    {{for loop, tp in looper(type_constants)}}
    {{tp}}{{if not loop.last}},{{endif}}
    {{endfor}}
};
