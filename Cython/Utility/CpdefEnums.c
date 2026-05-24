//////////////////// EnumToPyProto.proto ////////////////////

PyObject *{{funcname}}({{enum_type}}); /*proto*/


//////////////////// EnumToPyLTO ////////////////////

// Enum to_py function for LTO mode (non-static so it can be called from other modules)
PyObject *{{funcname}}({{enum_type}} __pyx_v_c_val) {
    PyObject *__pyx_v___pyx_enum = 0;
    PyObject *__pyx_r = NULL;
{{if module_name}}
    // Import the Python enum class from the defining module
    __pyx_v___pyx_enum = PyImport_ImportModule("{{module_name}}");
    if (__pyx_v___pyx_enum) {
        PyObject *__pyx_tmp = PyObject_GetAttrString(__pyx_v___pyx_enum, "{{name}}");
        Py_DECREF(__pyx_v___pyx_enum);
        __pyx_v___pyx_enum = __pyx_tmp;
    }
    if (!__pyx_v___pyx_enum) {
        PyErr_Clear();
        // Fall back to returning the underlying integer value
        return PyLong_FromLong((long)__pyx_v_c_val);
    }
{{else}}
    __pyx_v___pyx_enum = {{name}};
    Py_INCREF(__pyx_v___pyx_enum);
{{endif}}
    // Match enum value to Python enum member
{{for item in items}}
    if (__pyx_v_c_val == {{item[1]}}) {
        __pyx_r = PyObject_GetAttrString(__pyx_v___pyx_enum, "{{item[0]}}");
        Py_DECREF(__pyx_v___pyx_enum);
        return __pyx_r;
    }
{{endfor}}
    // Unknown value - return underlying integer
    Py_DECREF(__pyx_v___pyx_enum);
    return PyLong_FromLong((long)__pyx_v_c_val);
}


//////////////////// EnumToPyStatic.proto ////////////////////

static PyObject *{{funcname}}({{enum_type}}); /*proto*/


//////////////////// EnumToPyStatic ////////////////////

// Enum to_py function for non-LTO mode (static, each module gets its own copy)
static PyObject *{{funcname}}({{enum_type}} __pyx_v_c_val) {
    PyObject *__pyx_v___pyx_enum = 0;
    PyObject *__pyx_r = NULL;
{{if module_name}}
    // Import the Python enum class from the defining module
    __pyx_v___pyx_enum = PyImport_ImportModule("{{module_name}}");
    if (__pyx_v___pyx_enum) {
        PyObject *__pyx_tmp = PyObject_GetAttrString(__pyx_v___pyx_enum, "{{name}}");
        Py_DECREF(__pyx_v___pyx_enum);
        __pyx_v___pyx_enum = __pyx_tmp;
    }
    if (!__pyx_v___pyx_enum) {
        PyErr_Clear();
        // Fall back to returning the underlying integer value
        return PyLong_FromLong((long)__pyx_v_c_val);
    }
{{else}}
    __pyx_v___pyx_enum = {{name}};
    Py_INCREF(__pyx_v___pyx_enum);
{{endif}}
    // Match enum value to Python enum member
{{for item in items}}
    if (__pyx_v_c_val == {{item[1]}}) {
        __pyx_r = PyObject_GetAttrString(__pyx_v___pyx_enum, "{{item[0]}}");
        Py_DECREF(__pyx_v___pyx_enum);
        return __pyx_r;
    }
{{endfor}}
    // Unknown value - return underlying integer
    Py_DECREF(__pyx_v___pyx_enum);
    return PyLong_FromLong((long)__pyx_v_c_val);
}
