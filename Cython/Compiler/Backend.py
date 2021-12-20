from . import Naming


class APIBackend:
    hpy_guard = "HPY"
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
    pyobject_init_value = "NULL"
    pyobject_global_ctype = "PyObject *"
    pytype_global_ctype = "PyTypeObject *"
    pyobject_global_init_value = "NULL"
    pymoduledef_ctype = "PyModuleDef"
    pyssizet_ctype = "Py_ssize_t"

    # tuple building
    tuple_builder_ctype = pyobject_ctype
    tuple_builder_new = "PyTuple_New"
    tuple_builder_set_item = "PyTuple_SET_ITEM"
    tuple_builder_build = ""
    tuple_pack = "PyTuple_Pack"

    # list building
    list_builder_ctype = pyobject_ctype
    list_builder_new = "PyList_New"
    list_builder_set_item = "PyList_SET_ITEM"
    list_builder_build = ""

    @staticmethod
    def get_arg_list(*args):
        return ", ".join(args)

    @staticmethod
    def get_args(*args):
        return ", ".join(args)

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "Py_CLEAR(%s)" % var_cname

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return cexpr

    @staticmethod
    def get_visit_global(var_cname):
        return "Py_VISIT(%s);" % var_cname

    # Expression generation methods

    @staticmethod
    def get_is_null_cond(expr):
        """
        Generates a is-null condition (e.g. "!something").
        """
        return "!(%s)" % expr

    @staticmethod
    def get_is_null_cond(expr):
        """
        Generates a null-check condition (e.g. "!something").
        """
        return "!(%s)" % expr

    # Backend selection methods

    @staticmethod
    def get_hpy(hpy_code):
        return ""

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(cpy_code)


class HPyBackend(APIBackend):
    name = "hpy"
    pyobject_ctype = "HPy"
    pyobject_init_value = "HPy_NULL"
    pyobject_global_ctype = "HPyField"
    pytype_global_ctype = "HPyField"
    pyobject_global_init_value = "HPyField_NULL"
    pymoduledef_ctype = "HPyModuleDef"
    pyssizet_ctype = "HPy_ssize_t"

    # tuple building
    tuple_builder_ctype = "HPyTupleBuilder"
    tuple_builder_new = "HPyTupleBuilder_New"
    tuple_builder_set_item = "HPyTupleBuilder_Set"
    tuple_builder_build = "HPyTupleBuilder_Build"
    tuple_pack = "HPyTuple_Pack"

    # list building
    list_builder_ctype = "HPyListBuilder"
    list_builder_new = "HPyListBuilder_New"
    list_builder_set_item = "HPyListBuilder_Set"
    list_builder_build = "HPyListBuilder_Build"

    @staticmethod
    def get_arg_list(*args):
        return ", ".join(("HPyContext *" + Naming.hpy_context_cname,) + args)

    @staticmethod
    def get_args(*args):
        return ", ".join((Naming.hpy_context_cname,) + args)

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "HPyField_Store(%s, %s->h_None, &(%s), HPy_NULL);" % (
            Naming.hpy_context_cname, Naming.hpy_context_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "HPyField_Load(%s, %s->h_None, %s)" % (
            Naming.hpy_context_cname, Naming.hpy_context_cname, cexpr)

    @staticmethod
    def get_visit_global(var_cname):
        return "HPy_VISIT(&(%s));" % var_cname

    @staticmethod
    def get_pyobject_var_decl(var_name):
        return "HPy " + var_name

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


    # Backend selection methods

    @staticmethod
    def get_hpy(hpy_code):
        return hpy_code

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(hpy_code)


class CombinedBackend(APIBackend):
    name = "combined"
    pyobject_ctype = "__PYX_OBJECT_CTYPE"
    pyobject_init_value = "__PYX_NULL"
    pyobject_global_ctype = "__PYX_GLOBAL_OBJECT_CTYPE"
    pytype_global_ctype = "__PYX_GLOBAL_TYPE_CTYPE"
    pyobject_global_init_value = "__PYX_GLOBAL_NULL"
    pymoduledef_ctype = "__PYX_MODULEDEF_CTYPE"
    pyssizet_ctype = "__PYX_SSIZE_T"

    # tuple building
    tuple_builder_ctype = "__PYX_TUPLE_BUILDER_CTYPE"
    tuple_builder_new = "__PYX_TUPLE_BUILDER_NEW"
    tuple_builder_set_item = "__PYX_TUPLE_BUILDER_SET_ITEM"
    tuple_builder_build = "__PYX_TUPLE_BUILDER_BUILD"
    tuple_pack = "__PYX_TUPLE_PACK"

    # list building
    list_builder_ctype = "__PYX_LIST_BUILDER_CTYPE"
    list_builder_new = "__PYX_LIST_BUILDER_NEW"
    list_builder_set_item = "__PYX_LIST_BUILDER_SET_ITEM"
    list_builder_build = "__PYX_LIST_BUILDER_BUILD"

    @staticmethod
    def put_init_code(code):
        hpy_guard = CApiBackend.hpy_guard
        code.putln("#ifndef " + hpy_guard)
        code.putln("#define __PYX_OBJECT_CTYPE PyObject *")
        code.putln("#define __PYX_GLOBAL_OBJECT_CTYPE PyObject *")
        code.putln("#define __PYX_GLOBAL_TYPE_CTYPE PyTypeObject *")
        code.putln("#define __Pyx_CLEAR_GLOBAL(m, v) Py_CLEAR((v))")
        code.putln("#define __PYX_READ_GLOBAL(m, v) (v)")
        code.putln("#define __PYX_VISIT(x) Py_VISIT((x))")
        code.putln("#define __PYX_CONTEXT_DECL")
        code.putln("#define __PYX_CONTEXT")
        code.putln("#define __PYX_NULL NULL")
        code.putln("#define __PYX_GLOBAL_NULL NULL")
        code.putln("#define __PYX_MODULEDEF_CTYPE %s" % CApiBackend.pymoduledef_ctype)
        code.putln("#define __PYX_SSIZE_T %s" % CApiBackend.pyssizet_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_CTYPE %s" % CApiBackend.tuple_builder_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_NEW %s" % CApiBackend.tuple_builder_new)
        code.putln("#define __PYX_TUPLE_BUILDER_SET_ITEM %s" % CApiBackend.tuple_builder_set_item)
        code.putln("#define __PYX_TUPLE_BUILDER_BUILD %s" % CApiBackend.tuple_builder_build)
        code.putln("#define __PYX_TUPLE_PACK %s" % CApiBackend.tuple_pack)
        code.putln("#define __PYX_LIST_BUILDER_CTYPE %s" % CApiBackend.list_builder_ctype)
        code.putln("#define __PYX_LIST_BUILDER_NEW %s" % CApiBackend.list_builder_new)
        code.putln("#define __PYX_LIST_BUILDER_SET_ITEM %s" % CApiBackend.list_builder_set_item)
        code.putln("#define __PYX_LIST_BUILDER_BUILD %s" % CApiBackend.list_builder_build)
        code.putln("#define __PYX_IS_NULL(x) !(x)")
        code.putln("#define __PYX_IS_NOT_NULL(x) (x)")

        code.putln("#else /* %s */" % hpy_guard)

        code.putln("#define __PYX_OBJECT_CTYPE HPy")
        code.putln("#define __PYX_GLOBAL_OBJECT_CTYPE HPyField")
        code.putln("#define __PYX_GLOBAL_TYPE_CTYPE HPyField")
        code.putln("#define __Pyx_CLEAR_GLOBAL(m, v) HPyField_Store(%s, %s->h_None, &(v), HPy_NULL)" %
                   (Naming.hpy_context_cname, Naming.hpy_context_cname))
        code.putln("#define __PYX_READ_GLOBAL(m, v) HPyField_Load(%s, %s->h_None, (v))" %
                   (Naming.hpy_context_cname, Naming.hpy_context_cname))
        code.putln("#define __PYX_VISIT(x) HPy_VISIT(&(x))")
        code.putln("#define __PYX_CONTEXT_DECL HPyContext *%s, " % Naming.hpy_context_cname)
        code.putln("#define __PYX_CONTEXT %s, " % Naming.hpy_context_cname)
        code.putln("#define __PYX_NULL HPy_NULL")
        code.putln("#define __PYX_GLOBAL_NULL HPyField_NULL")
        code.putln("#define __PYX_MODULEDEF_CTYPE %s" % HPyBackend.pymoduledef_ctype)
        code.putln("#define __PYX_SSIZE_T %s" % HPyBackend.pyssizet_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_CTYPE %s" % HPyBackend.tuple_builder_ctype)
        code.putln("#define __PYX_TUPLE_BUILDER_NEW %s" % HPyBackend.tuple_builder_new)
        code.putln("#define __PYX_TUPLE_BUILDER_SET_ITEM %s" % HPyBackend.tuple_builder_set_item)
        code.putln("#define __PYX_TUPLE_BUILDER_BUILD %s" % HPyBackend.tuple_builder_build)
        code.putln("#define __PYX_TUPLE_PACK %s" % HPyBackend.tuple_pack)
        code.putln("#define __PYX_LIST_BUILDER_CTYPE %s" % HPyBackend.list_builder_ctype)
        code.putln("#define __PYX_LIST_BUILDER_NEW %s" % HPyBackend.list_builder_new)
        code.putln("#define __PYX_LIST_BUILDER_SET_ITEM %s" % HPyBackend.list_builder_set_item)
        code.putln("#define __PYX_LIST_BUILDER_BUILD %s" % HPyBackend.list_builder_build)
        code.putln("#define __PYX_IS_NULL(x) HPy_IsNull(x)")
        code.putln("#define __PYX_IS_NOT_NULL(x) !HPy_IsNull(x)")
        code.putln("#endif /* %s */" % hpy_guard)

    @staticmethod
    def get_arg_list(*args):
        return "__PYX_CONTEXT_DECL " + ", ".join(args)

    @staticmethod
    def get_args(*args):
        return "__PYX_CONTEXT " + ", ".join(args)

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "__Pyx_CLEAR_GLOBAL(%s, %s);" % (module_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "__PYX_READ_GLOBAL(%s, %s)" % (module_cname, cexpr)

    @staticmethod
    def get_visit_global(var_cname):
        return "__PYX_VISIT(%s);" % var_cname

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
        return "__PYX_IS_NOT_NULL(%s)" % expr

    # Backend selection methods

    @staticmethod
    def get_both(cpy_code, hpy_code):
        """
        Print code with structure:
        #ifndef HPY_GUARD
        cpy_code
        #else /* HPY_GUARD */
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        return "#ifdef %s\n%s\n#else /* %s */\n%s\n#endif /* %s */" % (
            hpy_guard, cpy_code, hpy_guard, hpy_code, hpy_guard)

    @staticmethod
    def get_hpy(hpy_code):
        """
        Print code with structure:
        #ifdef HPY_GUARD
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        return "#ifdef %s\n%s\n#endif /* %s */" % (
            hpy_guard, hpy_code, hpy_guard)

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        """
        Print code with structure:
        #ifndef HPY_GUARD
        cpy_code
        #else /* HPY_GUARD */
        hpy_code
        #endif /* HPY_GUARD */
        """
        hpy_guard = CApiBackend.hpy_guard
        code.putln("#ifndef " + hpy_guard)
        code.putln(cpy_code)
        code.putln("#else /* %s */" % hpy_guard)
        code.putln(hpy_code)
        code.putln("#endif /* %s */" % hpy_guard)
