from . import Naming


class APIBackend:
    hpy_guard = "CYTHON_COMPILING_IN_HPY"
    name = "NIL"
    pyobject_ctype = "NULL"
    pyobject_global_ctype = "NULL"
    pytype_global_ctype = "NULL"

    @staticmethod
    def put_init_code(code):
        pass

    @classmethod
    def get_pyobject_var_decl(cls, var_name):
        """
        Create a local C variable declaration for a Python object.
        """
        return "%s %s" % (cls.pyobject_ctype, var_name)


class CApiBackend(APIBackend):
    name = "cpython"
    pyobject_ctype = "PyObject *"
    pyobject_ctype_base_part = "PyObject"
    pyobject_ctype_entity_part = "*"
    pyobject_init_value = "NULL"
    pyobject_global_ctype = pyobject_ctype
    pyobject_global_ctype_base_part = pyobject_ctype_base_part
    pyobject_global_ctype_entity_part = pyobject_ctype_entity_part
    pytype_global_ctype = "PyTypeObject *"
    pyobject_global_init_value = "NULL"
    pyssizet_ctype = "Py_ssize_t"

    # constants
    pynone = "Py_None"

    # module
    pymoduledef_ctype = "PyModuleDef"
    module_create = "PyModule_Create"

    # tuple building
    tuple_builder_ctype = pyobject_ctype
    tuple_builder_new = "PyTuple_New"
    tuple_builder_set_item = "__PYX_TUPLE_BUILDER_SET_ITEM"
    tuple_builder_build = ""
    tuple_pack = "PyTuple_Pack"
    tuple_get_size = "PyTuple_GET_SIZE"

    # list building
    list_builder_ctype = pyobject_ctype
    list_builder_new = "PyList_New"
    list_builder_set_item = "__PYX_LIST_BUILDER_SET_ITEM"
    list_builder_build = ""

    # bytes
    bytes_from_string_and_size = "PyBytes_FromStringAndSize"

    # unicode
    unicode_from_string = "PyUnicode_FromString"

    # dict
    dict_set_item = "PyDict_SetItem"

    # type conversion functions
    pyfloat_fromdouble = 'PyFloat_FromDouble'
    pylong_fromstring = 'PyLong_FromString'
    pyint_fromstring = 'PyInt_FromString'
    pylong_fromlong = "PyLong_FromLong"
    pyint_fromlong = "PyInt_FromLong"

    py_functions = {
        "|":        "PyNumber_Or",
        "^":        "PyNumber_Xor",
        "&":        "PyNumber_And",
        "<<":       "PyNumber_Lshift",
        ">>":       "PyNumber_Rshift",
        "+":        "PyNumber_Add",
        "-":        "PyNumber_Subtract",
        "*":        "PyNumber_Multiply",
        "@":        "__Pyx_PyNumber_MatrixMultiply",
        "/":        "__Pyx_PyNumber_Divide",
        "//":       "PyNumber_FloorDivide",
        "%":        "PyNumber_Remainder",
        "**":       "PyNumber_Power",
    }

    @staticmethod
    def put_init_code(code):
        code.putln("#define __PYX_TUPLE_BUILDER_SET_ITEM(b, k, v) if (b) { PyTuple_SET_ITEM(b, k, v); }")
        code.putln("#define __PYX_LIST_BUILDER_SET_ITEM(b, k, v) if (b) { PyList_SET_ITEM(b, k, v); }")

    @staticmethod
    def get_binary_operation_function(operator, inplace):
        function_name = CApiBackend.py_functions[operator]
        if inplace:
            function_name = function_name.replace('PyNumber_', 'PyNumber_InPlace')
        return function_name

    @staticmethod
    def get_arg_list(*args):
        return ", ".join(args) if args else "void"

    @staticmethod
    def get_args(*args):
        return ", ".join("%s" % arg for arg in args)

    @staticmethod
    def get_call(func, *args):
        return "%s(%s)" % (func, CApiBackend.get_args(*args))

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "Py_CLEAR(%s)" % var_cname

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return cexpr

    @staticmethod
    def get_write_global(module_cname, globalvar_cname, cexpr):
        return "%s = %s" % (globalvar_cname, cexpr)

    @staticmethod
    def get_close_loaded_global(cexpr):
        # since we do not incref when loading the global, nothing to do here
        return ""

    @staticmethod
    def get_visit_global(var_cname):
        return "Py_VISIT(%s);" % var_cname

    @staticmethod
    def get_newref(var_cname, nanny):
        if nanny:
            return "__Pyx_NEWREF(%s)" % var_cname
        return "__Pyx_NEWREF_NO_REFNANNY(%s)" % var_cname

    @staticmethod
    def get_closeref(var_cname, nanny, null_check=False):
        X = "X" if null_check else ""
        if nanny:
            return "__Pyx_%sDECREF(%s)" % (X, var_cname)
        return "Py_%sDECREF(%s)" % (X, var_cname)

    @staticmethod
    def get_clear(var_cname, nanny, null_check):
        if nanny:
            X = "X" if null_check else ""
            return "__Pyx_%sCLEAR(%s)" % (X, var_cname)
        return "Py_CLEAR(%s)" % (var_cname)

    @staticmethod
    def get_err_occurred():
        return "PyErr_Occurred()"

    @staticmethod
    def get_none():
        return CApiBackend.pynone

    @staticmethod
    def get_method_definition(entry, wrapper_code_writer=None):
        method_flags = entry.signature.method_flags()
        if not method_flags:
            return None
        return 'static PyMethodDef %s = %s;' % (
            entry.pymethdef_cname,
            CApiBackend.get_method_definition_entry(entry, wrapper_code_writer))

    @staticmethod
    def get_method_definition_entry(entry, wrapper_code_writer=None):
        entry_name = entry.name.as_c_string_literal()
        method_flags = entry.signature.method_flags()
        if not method_flags:
            return None
        if entry.is_special:
            from . import TypeSlots
            method_flags += [TypeSlots.method_coexist]
        method_flags = entry.signature.method_flags()
        if not method_flags:
            return
        func_ptr = wrapper_code_writer.put_pymethoddef_wrapper(entry) if wrapper_code_writer else entry.func_cname
        # Add required casts, but try not to shadow real warnings.
        cast = entry.signature.method_function_type()
        if cast != 'PyCFunction':
            func_ptr = '(void*)(%s)%s' % (cast, func_ptr)
        return '{%s, (PyCFunction)%s, %s, %s}' % (
                entry_name,
                func_ptr,
                "|".join(method_flags),
                entry.doc_cname if entry.doc else '0')

    @staticmethod
    def get_arg_list_keywords():
        return "PyObject *%s, PyObject *%s" % (
            Naming.args_cname, Naming.kwds_cname)

    @staticmethod
    def get_arg_list_fastcall():
        return "PyObject *const *%s, Py_ssize_t %s, PyObject *%s" % (
            Naming.args_cname, Naming.nargs_cname, Naming.kwds_cname)

    # Expression generation methods

    @staticmethod
    def get_is_null_cond(expr):
        """
        Generates a is-null condition (e.g. "!something").
        """
        return "!(%s)" % expr

    @staticmethod
    def get_is_not_null_cond(expr):
        """
        Generates a not-null condition (like "something != NULL").
        """
        return "%s" % expr

    @staticmethod
    def get_global_is_null_cond(expr):
        return CApiBackend.get_is_null_cond(expr)

    @staticmethod
    def get_global_is_not_null_cond(expr):
        return CApiBackend.get_is_not_null_cond(expr)

    # Backend selection methods

    @staticmethod
    def get_both(cpy_code, hpy_code):
        return cpy_code

    @staticmethod
    def get_hpy(hpy_code):
        return ""

    @staticmethod
    def get_cpy(cpy_code):
        return cpy_code

    @staticmethod
    def put_cpy(code, cpy_code):
        return code.putln(cpy_code)

    @staticmethod
    def put_hpy(code, cpy_code):
        pass

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(cpy_code)


class HPyBackend(APIBackend):
    name = "hpy"
    pyobject_ctype = "HPy"
    pyobject_ctype_base_part = "HPy"
    pyobject_ctype_entity_part = ""
    pyobject_init_value = "HPy_NULL"
    pyobject_global_ctype = "HPyField"
    pyobject_global_ctype_base_part = "HPyField"
    pyobject_global_ctype_entity_part = ""
    pytype_global_ctype = "HPyField"
    pyobject_global_init_value = "HPyField_NULL"
    pyssizet_ctype = "HPy_ssize_t"

    # constants
    pynone = "%s->h_None" % Naming.hpy_context_cname

    # module
    pymoduledef_ctype = "HPyModuleDef"
    module_create = "HPyModule_Create"

    # tuple building
    tuple_builder_ctype = "HPyTupleBuilder"
    tuple_builder_new = "HPyTupleBuilder_New"
    tuple_builder_set_item = "HPyTupleBuilder_Set"
    tuple_builder_build = "HPyTupleBuilder_Build"
    tuple_pack = "HPyTuple_Pack"
    tuple_get_size = "HPy_Length"

    # list building
    list_builder_ctype = "HPyListBuilder"
    list_builder_new = "HPyListBuilder_New"
    list_builder_set_item = "HPyListBuilder_Set"
    list_builder_build = "HPyListBuilder_Build"

    # bytes
    bytes_from_string_and_size = "HPyBytes_FromStringAndSize"

    # unicode
    unicode_from_string = "HPyUnicode_FromString"

    # dict
    dict_set_item = "HPy_SetItem"

    # type conversion functions
    pyfloat_fromdouble = 'HPyFloat_FromDouble'
    pylong_fromstring = 'HPyLong_FromString'
    pyint_fromstring = pylong_fromstring
    pylong_fromlong = "HPyLong_FromLong"
    pyint_fromlong = pylong_fromlong

    hpy_functions = {
        "|":        "HPy_Or",
        "^":        "HPy_Xor",
        "&":        "HPy_And",
        "<<":       "HPy_Lshift",
        ">>":       "HPy_Rshift",
        "+":        "HPy_Add",
        "-":        "HPy_Subtract",
        "*":        "HPy_Multiply",
        "@":        "HPy_MatrixMultiply",
        "/":        "HPy_Divide",
        "//":       "HPy_FloorDivide",
        "%":        "HPy_Remainder",
        "**":       "HPy_Power",
    }

    @staticmethod
    def get_binary_operation_function(operator, inplace):
        function_name = HPyBackend.hpy_functions[operator]
        if inplace:
            function_name = function_name.replace('HPy_', 'HPy_InPlace')
        return function_name

    @staticmethod
    def get_arg_list(*args):
        return ", ".join(("HPyContext *" + Naming.hpy_context_cname,) + args)

    @staticmethod
    def get_args(*args):
        return ", ".join([Naming.hpy_context_cname, ] + ["%s" % arg for arg in args])

    @staticmethod
    def get_call(func, *args):
        return "%s(%s)" % (func, HPyBackend.get_args(*args))

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "HPyField_Store(%s, %s->h_None, &(%s), HPy_NULL);" % (
            Naming.hpy_context_cname, Naming.hpy_context_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "HPyField_Load(%s, %s->h_None, %s)" % (
            Naming.hpy_context_cname, Naming.hpy_context_cname, cexpr)

    @staticmethod
    def get_write_global(module_cname, globalvar_cname, cexpr):
        return "HPyField_Store(%s, %s->h_None, &(%s), %s)" % (
            Naming.hpy_context_cname, Naming.hpy_context_cname, globalvar_cname, cexpr)

    @staticmethod
    def get_close_loaded_global(cexpr):
        return "HPy_Close(%s, %s);" % (
            Naming.hpy_context_cname, cexpr)

    @staticmethod
    def get_visit_global(var_cname):
        return "HPy_VISIT(&(%s));" % var_cname

    @staticmethod
    def get_newref(var_cname, nanny):
        return "HPy_Dup(%s, %s)" % (Naming.hpy_context_cname, var_cname)

    @staticmethod
    def get_closeref(var_cname, nanny, null_check):
        return "HPy_Close(%s, %s)" % (Naming.hpy_context_cname, var_cname)

    @staticmethod
    def get_clear(var_cname, nanny, null_check):
        return "HPy_CLEAR(%s)" % var_cname

    @staticmethod
    def get_err_occurred():
        return "HPyErr_Occurred(%s)" % Naming.hpy_context_cname

    @staticmethod
    def get_pyobject_var_decl(var_name):
        return "HPy " + var_name

    @staticmethod
    def get_none():
        return "HPy_Dup(%s, %s->h_None)" % (Naming.hpy_context_cname, Naming.hpy_context_cname)

    @staticmethod
    def get_method_definition(entry, wrapper_code_writer):
        method_flags = entry.signature.hpy_method_flags()
        if not method_flags:
            return None
        entry_name = entry.name.as_c_string_literal()
        return "HPyDef_METH(%s, %s, %s, %s, .doc=%s);" % (
            entry.pymethdef_cname, entry_name, entry.func_cname, method_flags, entry.doc_cname)

    @staticmethod
    def get_method_definition_entry(entry, wrapper_code_writer):
        return '&' + entry.pymethdef_cname

    @staticmethod
    def get_arg_list_keywords():
        return "HPy *%s, HPy_ssize_t %s, HPy %s" % (
            Naming.args_cname, Naming.nargs_cname, Naming.kwds_cname)

    @staticmethod
    def get_arg_list_fastcall():
        return "#error \"fastcall not yet implemented in HPy\""

    # Expression generation methods

    @staticmethod
    def get_is_null_cond(expr):
        """
        Generates a null-check condition (e.g. "HPy_IsNull(something)").
        """
        return "HPy_IsNull(%s)" % expr

    @staticmethod
    def get_is_not_null_cond(expr):
        """
        Generates a not-null condition (like "!HPy_IsNull(something)").
        """
        return "!HPy_IsNull(%s)" % expr

    @staticmethod
    def get_global_is_null_cond(expr):
        """
        Generates a null-check condition (e.g. "HPyField_IsNull(something)").
        """
        return "HPyField_IsNull(%s)" % expr

    @staticmethod
    def get_global_is_not_null_cond(expr):
        """
        Generates a not-null condition (like "!HPyField_IsNull(something)").
        """
        return "!HPyField_IsNull(%s)" % expr


    # Backend selection methods

    @staticmethod
    def get_both(cpy_code, hpy_code):
        return hpy_code

    @staticmethod
    def get_hpy(hpy_code):
        return hpy_code

    @staticmethod
    def get_cpy(cpy_code):
        return ""

    @staticmethod
    def put_cpy(code, hpy_code):
        pass

    @staticmethod
    def put_hpy(code, hpy_code):
        return code.putln(hpy_code)

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(hpy_code)


class CombinedBackend(APIBackend):
    name = "combined"
    pyobject_ctype = "__PYX_OBJECT_CTYPE"
    pyobject_ctype_base_part = "__PYX_OBJECT_CTYPE"
    pyobject_ctype_entity_part = ""
    # __PYX_NULL is defined in ModuleSetupCode::ApiBackendInitCode
    pyobject_init_value = "__PYX_NULL"
    # __PYX_GLOBAL_OBJECT_CTYPE is defined in ModuleSetupCode::ApiBackendInitCode
    pyobject_global_ctype = "__PYX_GLOBAL_OBJECT_CTYPE"
    pyobject_global_ctype_base_part = "__PYX_GLOBAL_OBJECT_CTYPE_BP"
    pyobject_global_ctype_entity_part = ""
    pytype_global_ctype = "__PYX_GLOBAL_TYPE_CTYPE"
    pyobject_global_init_value = "__PYX_GLOBAL_NULL"
    pyssizet_ctype = "__PYX_SSIZE_T"

    # constants
    pynone = "__PYX_NONE"

    # module
    pymoduledef_ctype = "__PYX_MODULEDEF_CTYPE"
    module_create = "__PYX_MODULE_CREATE"

    # tuple building
    tuple_builder_ctype = "__PYX_TUPLE_BUILDER_CTYPE"
    tuple_builder_new = "__PYX_TUPLE_BUILDER_NEW"
    tuple_builder_set_item = "__PYX_TUPLE_BUILDER_SET_ITEM"
    tuple_builder_build = "__PYX_TUPLE_BUILDER_BUILD"
    tuple_pack = "__PYX_TUPLE_PACK"
    tuple_get_size = "__PYX_TUPLE_GET_SIZE"

    # list building
    list_builder_ctype = "__PYX_LIST_BUILDER_CTYPE"
    list_builder_new = "__PYX_LIST_BUILDER_NEW"
    list_builder_set_item = "__PYX_LIST_BUILDER_SET_ITEM"
    list_builder_build = "__PYX_LIST_BUILDER_BUILD"

    # bytes
    bytes_from_string_and_size = "__Pyx_PyBytes_FromStringAndSize"

    # unicode
    unicode_from_string = "__Pyx_API_PyUnicode_FromString"

    # dict
    dict_set_item = "__PYX_DICT_SETITEM"

    # type conversion functions
    pyfloat_fromdouble = "__PYX_FLOAT_FROM_DOUBLE"
    pylong_fromstring = "__PYX_LONG_FROM_STRING"
    pyint_fromstring = "__PYX_INT_FROM_STRING"
    pylong_fromlong = "__PYX_LONG_FROM_LONG"
    pyint_fromlong = "__PYX_INT_FROM_LONG"

    hpy_functions = {
        "|":        "__PYX_Or",
        "^":        "__PYX_Xor",
        "&":        "__PYX_And",
        "<<":       "__PYX_Lshift",
        ">>":       "__PYX_Rshift",
        "+":        "__PYX_Add",
        "-":        "__PYX_Subtract",
        "*":        "__PYX_Multiply",
        "@":        "__PYX_MatrixMultiply",
        "/":        "__PYX_Divide",
        "//":       "__PYX_FloorDivide",
        "%":        "__PYX_Remainder",
        "**":       "__PYX_Power",
    }

    @staticmethod
    def put_init_code(code):
        hpy_guard = CApiBackend.hpy_guard
        code.putln("#if !" + hpy_guard)
        code.putln("#define __PYX_API_CALL0(fun) fun()")
        code.putln("#define __PYX_API_CALL(fun, ...) fun(__VA_ARGS__)")
        code.putln("#define __PYX_OBJECT_CTYPE_BP PyObject")
        code.putln("#define __PYX_OBJECT_CTYPE_EP *")
        code.putln("#define __PYX_GLOBAL_OBJECT_CTYPE_BP PyObject *")
        code.putln("#define __PYX_GLOBAL_TYPE_CTYPE PyTypeObject *")
        code.putln("#define __Pyx_CLEAR_GLOBAL(m, v) Py_CLEAR((v))")
        code.putln("#define __PYX_READ_GLOBAL(m, v) (v)")
        code.putln("#define __PYX_WRITE_GLOBAL(m, l, v) (l) = (v)")
        code.putln("#define __PYX_CLOSE_LOADED_GLOBAL(v) %s" % CApiBackend.get_close_loaded_global("v"))
        code.putln("#define __PYX_VISIT(x) Py_VISIT((x))")
        code.putln("#define __PYX_CLEAR __Pyx_CLEAR")
        code.putln("#define __PYX_XCLEAR __Pyx_XCLEAR")
        code.putln("#define __PYX_CLEAR_NO_REFNANNY Py_CLEAR")
        code.putln("#define __PYX_GLOBAL_NULL NULL")
        code.putln("#define __PYX_MODULE_CREATE %s" % CApiBackend.module_create)
        code.putln("#define __PYX_MODULEDEF_CTYPE %s" % CApiBackend.pymoduledef_ctype)
        code.putln("#define __PYX_SSIZE_T %s" % CApiBackend.pyssizet_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_CTYPE %s" % CApiBackend.tuple_builder_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_NEW %s" % CApiBackend.tuple_builder_new)
        code.putln("#define __PYX_TUPLE_BUILDER_BUILD %s" % CApiBackend.tuple_builder_build)
        code.putln("#define __PYX_TUPLE_PACK %s" % CApiBackend.tuple_pack)
        code.putln("#define __PYX_TUPLE_GET_SIZE %s" % CApiBackend.tuple_get_size)
        code.putln("#define __PYX_LIST_BUILDER_CTYPE %s" % CApiBackend.list_builder_ctype)
        code.putln("#define __PYX_LIST_BUILDER_NEW %s" % CApiBackend.list_builder_new)
        code.putln("#define __PYX_LIST_BUILDER_BUILD %s" % CApiBackend.list_builder_build)
        code.putln("#define __Pyx_PyBytes_FromStringAndSize %s" % CApiBackend.bytes_from_string_and_size)
        code.putln("#define __Pyx_API_PyUnicode_FromString %s" % CApiBackend.unicode_from_string)
        code.putln("#define __PYX_DICT_SETITEM %s" % CApiBackend.dict_set_item)
        code.putln("#define __PYX_ERR_OCCURRED() PyErr_Occurred()")
        code.putln("#define __PYX_FLOAT_FROM_DOUBLE %s" % CApiBackend.pyfloat_fromdouble)
        code.putln("#define __PYX_LONG_FROM_STRING %s" % CApiBackend.pylong_fromstring)
        code.putln("#define __PYX_INT_FROM_STRING %s" % CApiBackend.pyint_fromstring)
        code.putln("#define __PYX_LONG_FROM_LONG %s" % CApiBackend.pylong_fromlong)
        code.putln("#define __PYX_INT_FROM_LONG %s" % CApiBackend.pyint_fromlong)
        code.putln("#define __PYX_NONE %s" % CApiBackend.pynone)
        code.putln("#define __PYX_NONE_NEW %s" % CApiBackend.get_none())
        for k in CombinedBackend.hpy_functions:
            code.putln("#define %s %s" % (CombinedBackend.hpy_functions[k], CApiBackend.py_functions[k]))
        CApiBackend.put_init_code(code)

        code.putln("#else /* %s */" % hpy_guard)

        code.putln("#define __PYX_API_CALL0(fun) fun(%s)" % Naming.hpy_context_cname)
        code.putln("#define __PYX_API_CALL(fun, ...) fun(%s, __VA_ARGS__)" % Naming.hpy_context_cname)
        code.putln("#define __PYX_OBJECT_CTYPE_BP HPy")
        code.putln("#define __PYX_OBJECT_CTYPE_EP ")
        code.putln("#define __PYX_GLOBAL_OBJECT_CTYPE_BP HPyField")
        code.putln("#define __PYX_GLOBAL_TYPE_CTYPE HPyField")
        code.putln("#define __Pyx_CLEAR_GLOBAL(m, v) HPyField_Store(%s, %s->h_None, &(v), HPy_NULL)" %
                   (Naming.hpy_context_cname, Naming.hpy_context_cname))
        code.putln("#define __PYX_READ_GLOBAL(m, v) HPyField_Load(%s, %s->h_None, (v))" %
                   (Naming.hpy_context_cname, Naming.hpy_context_cname))
        code.putln("#define __PYX_WRITE_GLOBAL(m, l, v) HPyField_Store(%s, %s->h_None, &(l), (v))" %
                   (Naming.hpy_context_cname, Naming.hpy_context_cname))
        code.putln("#define __PYX_CLOSE_LOADED_GLOBAL(v) %s" % HPyBackend.get_close_loaded_global("v"))
        code.putln("#define __PYX_VISIT(x) HPy_VISIT(&(x))")
        code.putln("#define __PYX_CLEAR HPy_CLEAR")
        code.putln("#define __PYX_CLEAR_NO_REFNANNY HPy_CLEAR")
        code.putln("#define __PYX_GLOBAL_NULL HPyField_NULL")
        code.putln("#define __PYX_MODULE_CREATE %s" % HPyBackend.module_create)
        code.putln("#define __PYX_MODULEDEF_CTYPE %s" % HPyBackend.pymoduledef_ctype)
        code.putln("#define __PYX_SSIZE_T %s" % HPyBackend.pyssizet_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_CTYPE %s" % HPyBackend.tuple_builder_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_NEW %s" % HPyBackend.tuple_builder_new)
        code.putln("#define __PYX_TUPLE_BUILDER_SET_ITEM %s" % HPyBackend.tuple_builder_set_item)
        code.putln("#define __PYX_TUPLE_BUILDER_BUILD %s" % HPyBackend.tuple_builder_build)
        code.putln("#define __PYX_TUPLE_PACK %s" % HPyBackend.tuple_pack)
        code.putln("#define __PYX_TUPLE_GET_SIZE %s" % HPyBackend.tuple_get_size)
        code.putln("#define __PYX_LIST_BUILDER_CTYPE %s" % HPyBackend.list_builder_ctype)
        code.putln("#define __PYX_LIST_BUILDER_NEW %s" % HPyBackend.list_builder_new)
        code.putln("#define __PYX_LIST_BUILDER_SET_ITEM %s" % HPyBackend.list_builder_set_item)
        code.putln("#define __PYX_LIST_BUILDER_BUILD %s" % HPyBackend.list_builder_build)
        code.putln("#define __Pyx_PyBytes_FromStringAndSize %s" % HPyBackend.bytes_from_string_and_size)
        code.putln("#define __Pyx_API_PyUnicode_FromString %s" % HPyBackend.unicode_from_string)
        code.putln("#define __PYX_DICT_SETITEM %s" % HPyBackend.dict_set_item)
        code.putln("#define __PYX_ERR_OCCURRED() HPyErr_Occurred(%s)" % Naming.hpy_context_cname)
        code.putln("#define __PYX_FLOAT_FROM_DOUBLE %s" % HPyBackend.pyfloat_fromdouble)
        code.putln("#define __PYX_LONG_FROM_STRING %s" % HPyBackend.pylong_fromstring)
        code.putln("#define __PYX_INT_FROM_STRING %s" % HPyBackend.pyint_fromstring)
        code.putln("#define __PYX_LONG_FROM_LONG %s" % HPyBackend.pylong_fromlong)
        code.putln("#define __PYX_INT_FROM_LONG %s" % HPyBackend.pyint_fromlong)
        code.putln("#define __PYX_NONE %s" % HPyBackend.pynone)
        code.putln("#define __PYX_NONE_NEW %s" % HPyBackend.get_none())
        for k in CombinedBackend.hpy_functions:
            code.putln("#define %s %s" % (CombinedBackend.hpy_functions[k], HPyBackend.hpy_functions[k]))
        code.putln("#endif /* %s */" % hpy_guard)

    @staticmethod
    def get_binary_operation_function(operator, inplace):
        function_name = CombinedBackend.hpy_functions[operator]
        if inplace:
            function_name = function_name.replace('__PYX_', '__PYX_InPlace')
        return function_name

    @staticmethod
    def get_arg_list(*args):
        if args:
            return "__PYX_CONTEXT_DECL " + ", ".join(args)
        return "__PYX_CONTEXT_DECL0"

    @staticmethod
    def get_args(*args):
        return ", ".join(["%s" % arg for arg in args])

    @staticmethod
    def get_call(func, *args):
        if args:
            return "__PYX_API_CALL(%s, %s)" % (func, CombinedBackend.get_args(*args))
        return "__PYX_API_CALL0(%s)" % (func)

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "__Pyx_CLEAR_GLOBAL(%s, %s);" % (module_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "__PYX_READ_GLOBAL(%s, %s)" % (module_cname, cexpr)

    @staticmethod
    def get_write_global(module_cname, globalvar_cname, cexpr):
        return "__PYX_WRITE_GLOBAL(%s, %s, %s)" % (module_cname, globalvar_cname, cexpr)

    @staticmethod
    def get_close_loaded_global(cexpr):
        return "__PYX_CLOSE_LOADED_GLOBAL(%s);" % cexpr

    @staticmethod
    def get_visit_global(var_cname):
        return "__PYX_VISIT(%s);" % var_cname

    @staticmethod
    def get_newref(var_cname, nanny=True):
        if nanny:
            # '__Pyx_NEWREF' is define in ModuleSetupCode::ApiBackendInitCode
            return "__Pyx_NEWREF(%s)" % var_cname
        # '__Pyx_NEWREF_NO_REFNANNY' is define in ModuleSetupCode::ApiBackendInitCode
        return "__Pyx_NEWREF_NO_REFNANNY(%s)" % var_cname

    @staticmethod
    def get_closeref(var_cname, nanny, null_check):
        X = "X" if null_check else ""
        if nanny:
            return "__Pyx_%sDECREF(%s)" % (X, var_cname)
        # '__Pyx_DECREF_NO_REFNANNY' is define in ModuleSetupCode::ApiBackendInitCode
        return "__Pyx_%sDECREF_NO_REFNANNY(%s)" % (X, var_cname)\

    @staticmethod
    def get_clear(var_cname, nanny, null_check):
        if nanny:
            X = "X" if null_check else ""
            return "__PYX_%sCLEAR(%s)" % (X, var_cname)
        return "__PYX_CLEAR_NO_REFNANNY(%s)" % var_cname

    @staticmethod
    def get_err_occurred():
        return "__PYX_ERR_OCCURRED()"

    @staticmethod
    def get_none():
        return "__PYX_NONE_NEW"

    @staticmethod
    def get_method_definition(entry, wrapper_code_writer=None):
        return CombinedBackend.get_both(
            CApiBackend.get_method_definition(entry, wrapper_code_writer),
            HPyBackend.get_method_definition(entry, wrapper_code_writer))

    @staticmethod
    def get_method_definition_entry(entry, wrapper_code_writer=None):
        raise NotImplementedError


    @staticmethod
    def get_arg_list_keywords():
        return "\n%s\n" % CombinedBackend.get_both(CApiBackend.get_arg_list_keywords(), HPyBackend.get_arg_list_keywords())

    @staticmethod
    def get_arg_list_fastcall():
        return "\n%s\n" % CombinedBackend.get_both(CApiBackend.get_arg_list_fastcall(), HPyBackend.get_arg_list_fastcall())

    # Expression generation methods

    @staticmethod
    def get_is_null_cond(expr):
        """
        Generates a null-check condition.
        """
        return "__PYX_IS_NULL(%s)" % expr

    @staticmethod
    def get_is_not_null_cond(expr):
        """
        Generates a not-null condition.
        """
        # macro '__PYX_IS_NOT_NULL' is define in ModuleSetupCode::ApiBackendInitCode
        return "__PYX_IS_NOT_NULL(%s)" % expr

    @staticmethod
    def get_global_is_null_cond(expr):
        """
        Generates a null-check condition for global variables.
        """
        # macro '__PYX_GLOBAL_IS_NULL' is define in ModuleSetupCode::ApiBackendInitCode
        return "__PYX_GLOBAL_IS_NULL(%s)" % expr

    @staticmethod
    def get_global_is_not_null_cond(expr):
        """
        Generates a not-null condition for global variables.
        """
        return "__PYX_GLOBAL_IS_NOT_NULL(%s)" % expr

    # Backend selection methods

    @staticmethod
    def get_both(cpy_code, hpy_code):
        """
        Print code with structure:
        #if !HPY_GUARD
        cpy_code
        #else /* HPY_GUARD */
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        return "#if !%s\n%s\n#else /* %s */\n%s\n#endif /* %s */" % (
            hpy_guard, cpy_code, hpy_guard, hpy_code, hpy_guard)

    @staticmethod
    def get_hpy(hpy_code):
        """
        Print code with structure:
        #if HPY_GUARD
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        return "#if %s\n%s\n#endif /* %s */" % (
            hpy_guard, hpy_code, hpy_guard)

    @staticmethod
    def get_cpy(cpy_code):
        """
        Print code with structure:
        #if HPY_GUARD
        cpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        return "#if !%s\n%s\n#endif /* %s */" % (
            hpy_guard, cpy_code, hpy_guard)

    @staticmethod
    def put_cpy(code, cpy_code):
        return code.putln(CombinedBackend.get_cpy(cpy_code))

    @staticmethod
    def put_hpy(code, hpy_code):
        return code.putln(CombinedBackend.get_hpy(hpy_code))

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        """
        Print code with structure:
        #if !HPY_GUARD
        cpy_code
        #else /* HPY_GUARD */
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        code.putln("#if !" + hpy_guard)
        code.putln(cpy_code)
        code.putln("#else /* %s */" % hpy_guard)
        code.putln(hpy_code)
        code.putln("#endif /* %s */" % hpy_guard)


backend = CApiBackend
