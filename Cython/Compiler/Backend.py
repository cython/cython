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
    pyobject_global_ctype = "PyObject *"
    pytype_global_ctype = "PyTypeObject *"

    @staticmethod
    def get_arg_list(*args):
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

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(cpy_code)


class HPyBackend(APIBackend):
    name = "hpy"
    pyobject_ctype = "HPy"
    pyobject_global_ctype = "HPyField"
    pytype_global_ctype = "HPyField"

    @staticmethod
    def get_arg_list(*args):
        return ", ".join(("HPyContext *" + Naming.hpy_context_cname,) + args)

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "HPyField_Store(%s, %s, &(%s), HPy_NULL);" % (Naming.hpy_context_cname, module_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "HPyField_Load(%s, %s, %s)" % (Naming.hpy_context_cname, module_cname, cexpr)

    @staticmethod
    def get_visit_global(var_cname):
        return "HPy_VISIT(&(%s));" % var_cname

    @staticmethod
    def get_pyobject_var_decl(var_name):
        return "HPy " + var_name

    @staticmethod
    def put_both(code, cpy_code, hpy_code):
        code.putln(hpy_code)


class CombinedBackend(APIBackend):
    name = "combined"
    pyobject_ctype = "__PYX_OBJECT_CTYPE"
    pyobject_global_ctype = "__PYX_GLOBAL_OBJECT_CTYPE"
    pytype_global_ctype = "__PYX_GLOBAL_TYPE_CTYPE"

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
        code.putln("#else /* %s */" % hpy_guard)
        code.putln("#define __PYX_OBJECT_CTYPE HPy")
        code.putln("#define __PYX_GLOBAL_OBJECT_CTYPE HPyField")
        code.putln("#define __PYX_GLOBAL_TYPE_CTYPE HPyField")
        code.putln("#define __Pyx_CLEAR_GLOBAL(m, v) HPyField_Store(%s, (m), &(v), HPy_NULL)" %
                   Naming.hpy_context_cname)
        code.putln("#define __PYX_READ_GLOBAL(m, v) HPyField_Load(%s, (m), (v))" % Naming.hpy_context_cname)
        code.putln("#define __PYX_VISIT(x) HPy_VISIT(&(x))")
        code.putln("#endif /* %s */" % hpy_guard)

    @staticmethod
    def get_arg_list(*args):
        return CombinedBackend.get_both(
            HPyBackend.get_arg_list(*args),
            CApiBackend.get_arg_list(*args)
        )

    @staticmethod
    def get_clear_global(module_cname, var_cname):
        return "__Pyx_CLEAR_GLOBAL(%s, %s);" % (module_cname, var_cname)

    @staticmethod
    def get_read_global(module_cname, cexpr):
        return "__PYX_READ_GLOBAL(%s, %s)" % (module_cname, cexpr)

    @staticmethod
    def get_visit_global(var_cname):
        return "__PYX_VISIT(%s);" % var_cname

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
