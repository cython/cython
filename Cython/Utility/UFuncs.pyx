##################### UFuncDefinition ######################

cdef extern from *:
    ctypedef int npy_intp;

# variable names have to come from tempita to avoid duplication
@cname("{{func_cname}}")
cdef void {{func_cname}}(char **{{args}}, const npy_intp *{{dimensions}}, const npy_intp* {{steps}}, void* {{data}}) except *:
    cdef npy_intp {{i}}
    cdef npy_intp {{n}} = {{dimensions}}[0]
    {{for idx, in_name in enumerate(in_names)}}
    cdef char* {{in_name}} = {{args}}[{{idx}}]
    {{endfor}}
    {{for idx, out_name in enumerate(out_names, len(in_names))}}
    cdef char* {{out_name}} = {{args}}[{{idx}}]
    {{endfor}}
    {{for idx, step_name in enumerate(step_names)}}
    cdef npy_intp {{step_name}} = {{steps}}[{{idx}}]
    {{endfor}}
    {{for arg_type, arg_name in zip(arg_types, arg_names)}}
    cdef {{arg_type.declaration_code("", pyrex=True)}} {{arg_name}}
    {{endfor}}

    for {{i}} in range({{n}}):
        {{for arg_name, arg_type, in_name in zip(arg_names, arg_types, in_names)}}
        {{if arg_type.is_pyobject}}
        {{arg_name}} = (<{{arg_type.declaration_code("", pyrex=True)}}>(<void**>{{in_name}})[0])
        {{else}}
        {{arg_name}} = (<{{arg_type.declaration_code("", pyrex=True)}}*>{{in_name}})[0]
        {{endif}}
        {{endfor}}
        {{for out_type, out_name in zip(out_types, out_names) }}
        {{if out_type.is_pyobject}}
        # ensure PyObjects are nulled so we can raise an error if not set
        # (this may be unnecessary but better to be same)
        (<void**>({{out_name}}))[0] = NULL
        {{endif}}
        {{endfor}}

        UFUNC_BODY  # substituted using TreeFragement

        {{for out_type, out_name in zip(out_types, out_names)}}
        {{if out_type.is_pyobject}}
        if (<void**>{{out_name}})[0] == NULL:
            raise ValueError("Python object output was not set")
        {{endif}}
        {{endfor}}
        {{for name, step_name in zip(in_names+out_names, step_names)}}
        {{name}} += {{step_name}}
        {{endfor}}

