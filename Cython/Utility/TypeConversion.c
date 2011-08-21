/////////////// FromPyStructUtility.proto ///////////////
{{struct_type_decl}};
static {{struct_type_decl}} {{funcname}}(PyObject *);

/////////////// FromPyStructUtility ///////////////
static {{struct_type_decl}} {{funcname}}(PyObject * o) {
    {{struct_type_decl}} result = {{init}};
    PyObject *value = NULL;

    if (!PyMapping_Check(o)) {
        PyErr_Format(PyExc_TypeError, "Expected a mapping, not %s", o->ob_type->tp_name);
        goto bad;
    }

    {{for member in var_entries:}}
        {{py:attr = "result." + member.cname}}

        value = PyMapping_GetItemString(o, (char *) "{{member.name}}");
        if (!value) {
            PyErr_SetString(PyExc_ValueError, "No value specified for struct "
                                              "attribute '{{member.name}}'");
            goto bad;
        }
        {{attr}} = {{member.type.from_py_function}}(value);
        if ({{member.type.error_condition(attr)}})
            goto bad;

        Py_DECREF(value);
    {{endfor}}

    return result;
bad:
    Py_XDECREF(value);
    return result;
}

