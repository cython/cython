#
#   Pyrex - Module parse tree node
#

import os, time
from cStringIO import StringIO

import Code
import Naming
import Nodes
import Options
import PyrexTypes
import TypeSlots
import Version

from Errors import error
from PyrexTypes import py_object_type
from Pyrex.Utils import open_new_file, replace_suffix

class ModuleNode(Nodes.Node, Nodes.BlockNode):
    #  doc       string or None
    #  body      StatListNode
    
    def analyse_declarations(self, env):
        env.doc = self.doc
        self.body.analyse_declarations(env)
    
    def process_implementation(self, env, result):
        self.analyse_declarations(env)
        env.check_c_classes()
        self.body.analyse_expressions(env)
        env.return_type = PyrexTypes.c_void_type
        self.generate_c_code(env, result)
        self.generate_h_code(env, result)
    
    def generate_h_code(self, env, result):
        public_vars_and_funcs = []
        public_extension_types = []
        for entry in env.var_entries:
            if entry.visibility == 'public':
                public_vars_and_funcs.append(entry)
        for entry in env.cfunc_entries:
            if entry.visibility == 'public':
                public_vars_and_funcs.append(entry)
        for entry in env.c_class_entries:
            if entry.visibility == 'public':
                public_extension_types.append(entry)
        if public_vars_and_funcs or public_extension_types:
            result.h_file = replace_suffix(result.c_file, ".h")
            result.i_file = replace_suffix(result.c_file, ".pxi")
            h_code = Code.CCodeWriter(open_new_file(result.h_file))
            i_code = Code.PyrexCodeWriter(result.i_file)
            self.generate_extern_c_macro_definition(h_code)
            for entry in public_vars_and_funcs:
                h_code.putln("%s %s;" % (
                    Naming.extern_c_macro,
                    entry.type.declaration_code(
                        entry.cname, dll_linkage = "DL_IMPORT")))
                i_code.putln("cdef extern %s" % 
                    entry.type.declaration_code(entry.cname, pyrex = 1))
            for entry in public_extension_types:
                self.generate_cclass_header_code(entry.type, h_code)
                self.generate_cclass_include_code(entry.type, i_code)
            h_code.putln("PyMODINIT_FUNC init%s(void);" % env.module_name)
    
    def generate_cclass_header_code(self, type, h_code):
        #h_code.putln("extern DL_IMPORT(PyTypeObject) %s;" % type.typeobj_cname)
        h_code.putln("%s DL_IMPORT(PyTypeObject) %s;" % (
            Naming.extern_c_macro,
            type.typeobj_cname))
        self.generate_obj_struct_definition(type, h_code)
    
    def generate_cclass_include_code(self, type, i_code):
        i_code.putln("cdef extern class %s.%s:" % (
            type.module_name, type.name))
        i_code.indent()
        var_entries = type.scope.var_entries
        if var_entries:
            for entry in var_entries:
                i_code.putln("cdef %s" % 
                    entry.type.declaration_code(entry.cname, pyrex = 1))
        else:
            i_code.putln("pass")
        i_code.dedent()
    
    def generate_c_code(self, env, result):
        modules = []
        self.find_referenced_modules(env, modules, {})
        #code = Code.CCodeWriter(result.c_file)
        code = Code.CCodeWriter(StringIO())
        code.h = Code.CCodeWriter(StringIO())
        code.init_labels()
        self.generate_module_preamble(env, modules, code.h)

        code.putln("")
        code.putln("/* Implementation of %s */" % env.qualified_name)
        self.generate_const_definitions(env, code)
        self.generate_interned_name_decls(env, code)
        self.generate_py_string_decls(env, code)
        self.body.generate_function_definitions(env, code)
        self.generate_interned_name_table(env, code)
        self.generate_py_string_table(env, code)
        self.generate_typeobj_definitions(env, code)
        self.generate_method_table(env, code)
        self.generate_filename_init_prototype(code)
        self.generate_module_init_func(modules[:-1], env, code)
        self.generate_filename_table(code)
        self.generate_utility_functions(env, code)

        for module in modules:
            self.generate_declarations_for_module(module, code.h,
                definition = module is env)

        f = open_new_file(result.c_file)
        f.write(code.h.f.getvalue())
        f.write("\n")
        f.write(code.f.getvalue())
        f.close()
        result.c_file_generated = 1
    
    def find_referenced_modules(self, env, module_list, modules_seen):
        if env not in modules_seen:
            modules_seen[env] = 1
            for imported_module in env.cimported_modules:
                self.find_referenced_modules(imported_module, module_list, modules_seen)
            module_list.append(env)
        
    def generate_module_preamble(self, env, cimported_modules, code):
        code.putln('/* Generated by Pyrex %s on %s */' % (
            Version.version, time.asctime()))
        code.putln('')
        for filename in env.python_include_files:
            code.putln('#include "%s"' % filename)
        code.putln("#ifndef PY_LONG_LONG")
        code.putln("  #define PY_LONG_LONG LONG_LONG")
        code.putln("#endif")
        self.generate_extern_c_macro_definition(code)
        code.putln("%s double pow(double, double);" % Naming.extern_c_macro)
        self.generate_includes(env, cimported_modules, code)
        #for filename in env.include_files:
        #	code.putln('#include "%s"' % filename)
        code.putln('')
        code.put(Nodes.utility_function_predeclarations)
        #if Options.intern_names:
        #	code.putln(Nodes.get_name_interned_predeclaration)
        #else:
        #	code.putln(get_name_predeclaration)
        code.putln('')
        code.putln('static PyObject *%s;' % env.module_cname)
        code.putln('static PyObject *%s;' % Naming.builtins_cname)
        code.putln('static int %s;' % Naming.lineno_cname)
        code.putln('static char *%s;' % Naming.filename_cname)
        code.putln('static char **%s;' % Naming.filetable_cname)
        if env.doc:
            code.putln('')
            code.putln('static char %s[] = "%s";' % (env.doc_cname, env.doc))
    
    def generate_extern_c_macro_definition(self, code):
        name = Naming.extern_c_macro
        code.putln("#ifdef __cplusplus")
        code.putln('#define %s extern "C"' % name)
        code.putln("#else")
        code.putln("#define %s extern" % name)
        code.putln("#endif")

    def generate_includes(self, env, cimported_modules, code):
        includes = env.include_files[:]
        for module in cimported_modules:
            for filename in module.include_files:
                if filename not in includes:
                    includes.append(filename)
        for filename in includes:
            code.putln('#include "%s"' % filename)
    
    def generate_filename_table(self, code):
        code.putln("")
        code.putln("static char *%s[] = {" % Naming.filenames_cname)
        if code.filename_list:
            for filename in code.filename_list:
                filename = os.path.basename(filename)
                escaped_filename = filename.replace("\\", "\\\\").replace('"', r'\"')
                code.putln('"%s",' % 
                    escaped_filename)
        else:
            # Some C compilers don't like an empty array
            code.putln("0")
        code.putln("};")
    
    def generate_declarations_for_module(self, env, code, definition):
        code.putln("")
        code.putln("/* Declarations from %s */" % env.qualified_name)
        self.generate_type_predeclarations(env, code)
        self.generate_type_definitions(env, code)
        self.generate_global_declarations(env, code, definition)
        self.generate_cfunction_predeclarations(env, code)

    def generate_type_predeclarations(self, env, code):
        pass
    
    def generate_type_definitions(self, env, code):
        # Generate definitions of structs/unions/enums.
        for entry in env.sue_entries:
            if not entry.in_cinclude:
                type = entry.type
                if type.is_struct_or_union:
                    self.generate_struct_union_definition(entry, code)
                else:
                    self.generate_enum_definition(entry, code)
        # Generate extension type object struct definitions.
        for entry in env.c_class_entries:
            if not entry.in_cinclude:
                self.generate_typeobject_predeclaration(entry, code)
                self.generate_obj_struct_definition(entry.type, code)
                self.generate_exttype_vtable_struct(entry, code)
                self.generate_exttype_vtabptr_declaration(entry, code)
    
    def sue_header_footer(self, type, kind, name):
        if type.typedef_flag:
            header = "typedef %s {" % kind
            footer = "} %s;" % name
        else:
            header = "%s %s {" % (kind, name)
            footer = "};"
        return header, footer
    
    def generate_struct_union_definition(self, entry, code):
        type = entry.type
        scope = type.scope
        if scope:
            header, footer = \
                self.sue_header_footer(type, type.kind, type.cname)
            code.putln("")
            code.putln(header)
            var_entries = scope.var_entries
            if not var_entries:
                error(entry.pos,
                    "Empty struct or union definition not allowed outside a"
                    " 'cdef extern from' block")
            for attr in var_entries:
                code.putln(
                    "%s;" %
                        attr.type.declaration_code(attr.cname))
            code.putln(footer)

    def generate_enum_definition(self, entry, code):
        type = entry.type
        name = entry.cname or entry.name or ""
        header, footer = \
            self.sue_header_footer(type, "enum", name)
        code.putln("")
        code.putln(header)
        enum_values = entry.enum_values
        if not enum_values:
            error(entry.pos,
                "Empty enum definition not allowed outside a"
                " 'cdef extern from' block")
        else:
            last_entry = enum_values[-1]
            for value_entry in enum_values:
                if value_entry.value == value_entry.name:
                    value_code = value_entry.cname
                else:
                    value_code = ("%s = %s" % (
                        value_entry.cname,
                        value_entry.value))
                if value_entry is not last_entry:
                    value_code += ","
                code.putln(value_code)
        code.putln(footer)
    
    def generate_typeobject_predeclaration(self, entry, code):
        code.putln("")
        name = entry.type.typeobj_cname
        if name:
            if entry.visibility == 'extern' and not entry.in_cinclude:
                code.putln("%s DL_IMPORT(PyTypeObject) %s;" % (
                    Naming.extern_c_macro,
                    name))
            elif entry.visibility == 'public':
                #code.putln("DL_EXPORT(PyTypeObject) %s;" % name)
                code.putln("%s DL_EXPORT(PyTypeObject) %s;" % (
                    Naming.extern_c_macro,
                    name))
            # ??? Do we really need the rest of this? ???
            #else:
            #	code.putln("staticforward PyTypeObject %s;" % name)
    
    def generate_exttype_vtable_struct(self, entry, code):
        # Generate struct declaration for an extension type's vtable.
        type = entry.type
        scope = type.scope
        if type.vtabstruct_cname:
            code.putln("")
            code.putln(
                "struct %s {" %
                    type.vtabstruct_cname)
            if type.base_type and type.base_type.vtabstruct_cname:
                code.putln("struct %s %s;" % (
                    type.base_type.vtabstruct_cname,
                    Naming.obj_base_cname))
            for method_entry in scope.cfunc_entries:
                if not method_entry.is_inherited:
                    code.putln(
                        "%s;" % method_entry.type.declaration_code("(*%s)" % method_entry.name))
            code.putln(
                "};")
    
    def generate_exttype_vtabptr_declaration(self, entry, code):
        # Generate declaration of pointer to an extension type's vtable.
        type = entry.type
        if type.vtabptr_cname:
            code.putln("static struct %s *%s;" % (
                type.vtabstruct_cname,
                type.vtabptr_cname))
    
    def generate_obj_struct_definition(self, type, code):
        # Generate object struct definition for an
        # extension type.
        if not type.scope:
            return # Forward declared but never defined
        header, footer = \
            self.sue_header_footer(type, "struct", type.objstruct_cname)
        code.putln("")
        code.putln(header)
        base_type = type.base_type
        if base_type:
            code.putln(
                "%s%s %s;" % (
                    ("struct ", "")[base_type.typedef_flag],
                    base_type.objstruct_cname,
                    Naming.obj_base_cname))
        else:
            code.putln(
                "PyObject_HEAD")
        if type.vtabslot_cname and not (type.base_type and type.base_type.vtabslot_cname):
            code.putln(
                "struct %s *%s;" % (
                    type.vtabstruct_cname,
                    type.vtabslot_cname))
        for attr in type.scope.var_entries:
            code.putln(
                "%s;" %
                    attr.type.declaration_code(attr.cname))
        code.putln(footer)

    def generate_global_declarations(self, env, code, definition):
        code.putln("")
        for entry in env.c_class_entries:
            code.putln("static PyTypeObject *%s = 0;" % 
                entry.type.typeptr_cname)
        code.put_var_declarations(env.var_entries, static = 1, 
            dll_linkage = "DL_EXPORT", definition = definition)
        code.put_var_declarations(env.default_entries, static = 1)
    
    def generate_cfunction_predeclarations(self, env, code):
        for entry in env.cfunc_entries:
            if not entry.in_cinclude:
                if entry.visibility == 'public':
                    dll_linkage = "DL_EXPORT"
                else:
                    dll_linkage = None
                header = entry.type.declaration_code(entry.cname, 
                    dll_linkage = dll_linkage)
                if entry.visibility <> 'private':
                    storage_class = "%s " % Naming.extern_c_macro
                else:
                    storage_class = "static "
                code.putln("%s%s; /*proto*/" % (
                    storage_class,
                    header))
    
    def generate_typeobj_definitions(self, env, code):
        full_module_name = env.qualified_name
        for entry in env.c_class_entries:
            #print "generate_typeobj_definitions:", entry.name
            #print "...visibility =", entry.visibility
            if entry.visibility <> 'extern':
                type = entry.type
                scope = type.scope
                if scope: # could be None if there was an error
                    self.generate_exttype_vtable(scope, code)
                    self.generate_new_function(scope, code)
                    self.generate_dealloc_function(scope, code)
                    self.generate_traverse_function(scope, code)
                    self.generate_clear_function(scope, code)
                    if scope.defines_any(["__getitem__"]):
                        self.generate_getitem_int_function(scope, code)
                    if scope.defines_any(["__setitem__", "__delitem__"]):
                        self.generate_ass_subscript_function(scope, code)
                    if scope.defines_any(["__setslice__", "__delslice__"]):
                        self.generate_ass_slice_function(scope, code)
                    if scope.defines_any(["__getattr__"]):
                        self.generate_getattro_function(scope, code)
                    if scope.defines_any(["__setattr__", "__delattr__"]):
                        self.generate_setattro_function(scope, code)
                    if scope.defines_any(["__get__"]):
                        self.generate_descr_get_function(scope, code)
                    if scope.defines_any(["__set__", "__delete__"]):
                        self.generate_descr_set_function(scope, code)
                    self.generate_property_accessors(scope, code)
                    self.generate_method_table(scope, code)
                    self.generate_member_table(scope, code)
                    self.generate_getset_table(scope, code)
                    self.generate_typeobj_definition(full_module_name, entry, code)
    
    def generate_exttype_vtable(self, scope, code):
        # Generate the definition of an extension type's vtable.
        type = scope.parent_type
        if type.vtable_cname:
            code.putln("static struct %s %s;" % (
                type.vtabstruct_cname,
                type.vtable_cname))
        
    def generate_self_cast(self, scope, code):
        type = scope.parent_type
        code.putln(
            "%s = (%s)o;" % (
                type.declaration_code("p"),
                type.declaration_code("")))
    
    def generate_new_function(self, scope, code):
        base_type = scope.parent_type.base_type
        code.putln("")
        code.putln(
            "static PyObject *%s(PyTypeObject *t, PyObject *a, PyObject *k) {"
                % scope.mangle_internal("tp_new"))
        if base_type:
            code.putln(
                "PyObject *o = %s->tp_new(t, a, k);" %
                    base_type.typeptr_cname)
        else:
            code.putln(
                "PyObject *o = (*t->tp_alloc)(t, 0);")
        type = scope.parent_type
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                py_attrs.append(entry)
        if type.vtabslot_cname or py_attrs:
            self.generate_self_cast(scope, code)
        if type.vtabslot_cname:
            code.putln("*(struct %s **)&p->%s = %s;" % (
                type.vtabstruct_cname,
                type.vtabslot_cname,
                type.vtabptr_cname))
        for entry in py_attrs:
            if entry.name == "__weakref__":
                code.putln("p->%s = 0;" % entry.cname)
            else:
                code.put_init_var_to_py_none(entry, "p->%s")
        entry = scope.lookup_here("__new__")
        if entry:
            code.putln(
                "if (%s(o, a, k) < 0) {" % 
                    entry.func_cname)
            code.put_decref_clear("o", py_object_type);
            code.putln(
                "}")
        code.putln(
            "return o;")
        code.putln(
            "}")
    
    def generate_dealloc_function(self, scope, code):
        base_type = scope.parent_type.base_type
        code.putln("")
        code.putln(
            "static void %s(PyObject *o) {"
                % scope.mangle_internal("tp_dealloc"))
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry.name <> "__weakref__":
                py_attrs.append(entry)
        if py_attrs:
            self.generate_self_cast(scope, code)
        self.generate_usr_dealloc_call(scope, code)
        if scope.lookup_here("__weakref__"):
            code.putln("PyObject_ClearWeakRefs(o);")
        for entry in py_attrs:
            code.put_xdecref("p->%s" % entry.cname, entry.type)
        if base_type:
            code.putln(
                "%s->tp_dealloc(o);" %
                    base_type.typeptr_cname)
        else:
            code.putln(
                "(*o->ob_type->tp_free)(o);")
        code.putln(
            "}")
    
    def generate_usr_dealloc_call(self, scope, code):
        entry = scope.lookup_here("__dealloc__")
        if entry:
            code.putln(
                "{")
            code.putln(
                    "PyObject *etype, *eval, *etb;")
            code.putln(
                    "PyErr_Fetch(&etype, &eval, &etb);")
            code.putln(
                    "++o->ob_refcnt;")
            code.putln(
                    "%s(o);" % 
                        entry.func_cname)
            code.putln(
                    "if (PyErr_Occurred()) PyErr_WriteUnraisable(o);")
            code.putln(
                    "--o->ob_refcnt;")
            code.putln(
                    "PyErr_Restore(etype, eval, etb);")
            code.putln(
                "}")
    
    def generate_traverse_function(self, scope, code):
        base_type = scope.parent_type.base_type
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, visitproc v, void *a) {"
                % scope.mangle_internal("tp_traverse"))
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                py_attrs.append(entry)
        if base_type or py_attrs:
            code.putln(
                    "int e;")
        if py_attrs:
            self.generate_self_cast(scope, code)
        if base_type:
            code.putln(
                    "e = %s->tp_traverse(o, v, a); if (e) return e;" %
                        base_type.typeptr_cname)
        for entry in py_attrs:
            var_code = "p->%s" % entry.cname
            code.putln(
                    "if (%s) {"
                        % var_code)
            if entry.type.is_extension_type:
                var_code = "((PyObject*)%s)" % var_code
            code.putln(
                        "e = (*v)(%s, a); if (e) return e;" 
                            % var_code)
            code.putln(
                    "}")
        code.putln(
                "return 0;")
        code.putln(
            "}")
    
    def generate_clear_function(self, scope, code):
        base_type = scope.parent_type.base_type
        code.putln("")
        code.putln(
            "static int %s(PyObject *o) {"
                % scope.mangle_internal("tp_clear"))
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                py_attrs.append(entry)
        if py_attrs:
            self.generate_self_cast(scope, code)
        if base_type:
            code.putln(
                "%s->tp_clear(o);" %
                    base_type.typeptr_cname)
        for entry in py_attrs:
            name = "p->%s" % entry.cname
            code.put_xdecref(name, entry.type)
            code.put_init_var_to_py_none(entry, "p->%s")
        code.putln(
            "return 0;")
        code.putln(
            "}")
        
    def generate_getitem_int_function(self, scope, code):
        # This function is put into the sq_item slot when
        # a __getitem__ method is present. It converts its
        # argument to a Python integer and calls mp_subscript.
        code.putln(
            "static PyObject *%s(PyObject *o, int i) {" %
                scope.mangle_internal("sq_item"))
        code.putln(
                "PyObject *r;")
        code.putln(
                "PyObject *x = PyInt_FromLong(i); if(!x) return 0;")
        code.putln(
                "r = o->ob_type->tp_as_mapping->mp_subscript(o, x);")
        code.putln(
                "Py_DECREF(x);")
        code.putln(
                "return r;")
        code.putln(
            "}")

    def generate_ass_subscript_function(self, scope, code):
        # Setting and deleting an item are both done through
        # the ass_subscript method, so we dispatch to user's __setitem__
        # or __delitem__, or raise an exception.
        base_type = scope.parent_type.base_type
        set_entry = scope.lookup_here("__setitem__")
        del_entry = scope.lookup_here("__delitem__")
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, PyObject *i, PyObject *v) {" %
                scope.mangle_internal("mp_ass_subscript"))
        code.putln(
                "if (v) {")
        if set_entry:
            code.putln(
                    "return %s(o, i, v);" %
                        set_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, "tp_as_mapping", "mp_ass_subscript", "o, i, v", code)
            code.putln(
                    "PyErr_Format(PyExc_NotImplementedError,")
            code.putln(
                    '  "Subscript assignment not supported by %s", o->ob_type->tp_name);')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
                "else {")
        if del_entry:
            code.putln(
                    "return %s(o, i);" %
                        del_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, "tp_as_mapping", "mp_ass_subscript", "o, i, v", code)
            code.putln(
                    "PyErr_Format(PyExc_NotImplementedError,")
            code.putln(
                    '  "Subscript deletion not supported by %s", o->ob_type->tp_name);')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
            "}")
    
    def generate_guarded_basetype_call(
            self, base_type, substructure, slot, args, code):
        if base_type:
            base_tpname = base_type.typeptr_cname
            if substructure:
                code.putln(
                    "if (%s->%s && %s->%s->%s)" % (
                        base_tpname, substructure, base_tpname, substructure, slot))
                code.putln(
                    "  return %s->%s->%s(%s);" % (
                        base_tpname, substructure, slot, args))
            else:
                code.putln(
                    "if (%s->%s)" % (
                        base_tpname, slot))
                code.putln(
                    "  return %s->%s(%s);" % (
                        base_tpname, slot, args))

    def generate_ass_slice_function(self, scope, code):
        # Setting and deleting a slice are both done through
        # the ass_slice method, so we dispatch to user's __setslice__
        # or __delslice__, or raise an exception.
        base_type = scope.parent_type.base_type
        set_entry = scope.lookup_here("__setslice__")
        del_entry = scope.lookup_here("__delslice__")
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, int i, int j, PyObject *v) {" %
                scope.mangle_internal("sq_ass_slice"))
        code.putln(
                "if (v) {")
        if set_entry:
            code.putln(
                    "return %s(o, i, j, v);" %
                        set_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, "tp_as_sequence", "sq_ass_slice", "o, i, j, v", code)
            code.putln(
                    "PyErr_Format(PyExc_NotImplementedError,")
            code.putln(
                    '  "2-element slice assignment not supported by %s", o->ob_type->tp_name);')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
                "else {")
        if del_entry:
            code.putln(
                    "return %s(o, i, j);" %
                        del_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, "tp_as_sequence", "sq_ass_slice", "o, i, j, v", code)
            code.putln(
                    "PyErr_Format(PyExc_NotImplementedError,")
            code.putln(
                    '  "2-element slice deletion not supported by %s", o->ob_type->tp_name);')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
            "}")

    def generate_getattro_function(self, scope, code):
        # First try to get the attribute using PyObject_GenericGetAttr.
        # If that raises an AttributeError, call the user's __getattr__
        # method.
        entry = scope.lookup_here("__getattr__")
        code.putln("")
        code.putln(
            "static PyObject *%s(PyObject *o, PyObject *n) {"
                % scope.mangle_internal("tp_getattro"))
        code.putln(
                "PyObject *v = PyObject_GenericGetAttr(o, n);")
        code.putln(
                "if (!v && PyErr_ExceptionMatches(PyExc_AttributeError)) {")
        code.putln(
                    "PyErr_Clear();")
        code.putln(
                    "v = %s(o, n);" %
                        entry.func_cname)
        code.putln(
                "}")
        code.putln(
                "return v;")
        code.putln(
            "}")
    
    def generate_setattro_function(self, scope, code):
        # Setting and deleting an attribute are both done through
        # the setattro method, so we dispatch to user's __setattr__
        # or __delattr__ or fall back on PyObject_GenericSetAttr.
        base_type = scope.parent_type.base_type
        set_entry = scope.lookup_here("__setattr__")
        del_entry = scope.lookup_here("__delattr__")
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, PyObject *n, PyObject *v) {" %
                scope.mangle_internal("tp_setattro"))
        code.putln(
                "if (v) {")
        if set_entry:
            code.putln(
                    "return %s(o, n, v);" %
                        set_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, None, "tp_setattro", "o, n, v", code)
            code.putln(
                    "return PyObject_GenericSetAttr(o, n, v);")
        code.putln(
                "}")
        code.putln(
                "else {")
        if del_entry:
            code.putln(
                    "return %s(o, n);" %
                        del_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, None, "tp_setattro", "o, n, v", code)
            code.putln(
                    "return PyObject_GenericSetAttr(o, n, 0);")
        code.putln(
                "}")
        code.putln(
            "}")
    
    def generate_descr_get_function(self, scope, code):
        # The __get__ function of a descriptor object can be
        # called with NULL for the second or third arguments
        # under some circumstances, so we replace them with
        # None in that case.
        user_get_entry = scope.lookup_here("__get__")
        code.putln("")
        code.putln(
            "static PyObject *%s(PyObject *o, PyObject *i, PyObject *c) {" %
                scope.mangle_internal("tp_descr_get"))
        code.putln(
            "PyObject *r = 0;")
        code.putln(
            "if (!i) i = Py_None;")
        code.putln(
            "if (!c) c = Py_None;")
        #code.put_incref("i", py_object_type)
        #code.put_incref("c", py_object_type)
        code.putln(
            "r = %s(o, i, c);" %
                user_get_entry.func_cname)
        #code.put_decref("i", py_object_type)
        #code.put_decref("c", py_object_type)
        code.putln(
            "return r;")
        code.putln(
            "}")
    
    def generate_descr_set_function(self, scope, code):
        # Setting and deleting are both done through the __set__
        # method of a descriptor, so we dispatch to user's __set__
        # or __delete__ or raise an exception.
        base_type = scope.parent_type.base_type
        user_set_entry = scope.lookup_here("__set__")
        user_del_entry = scope.lookup_here("__delete__")
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, PyObject *i, PyObject *v) {" %
                scope.mangle_internal("tp_descr_set"))
        code.putln(
                "if (v) {")
        if user_set_entry:
            code.putln(
                    "return %s(o, i, v);" %
                        user_set_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, None, "tp_descr_set", "o, i, v", code)
            code.putln(
                    'PyErr_SetString(PyExc_NotImplementedError, "__set__");')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
                "else {")
        if user_del_entry:
            code.putln(
                    "return %s(o, i);" %
                        user_del_entry.func_cname)
        else:
            self.generate_guarded_basetype_call(
                base_type, None, "tp_descr_set", "o, i, v", code)
            code.putln(
                    'PyErr_SetString(PyExc_NotImplementedError, "__delete__");')
            code.putln(
                    "return -1;")
        code.putln(
                "}")		
        code.putln(
            "}")
    
    def generate_property_accessors(self, cclass_scope, code):
        for entry in cclass_scope.property_entries:
            property_scope = entry.scope
            if property_scope.defines_any(["__get__"]):
                self.generate_property_get_function(entry, code)
            if property_scope.defines_any(["__set__", "__del__"]):
                self.generate_property_set_function(entry, code)
    
    def generate_property_get_function(self, property_entry, code):
        property_scope = property_entry.scope
        property_entry.getter_cname = property_scope.parent_scope.mangle(
            Naming.prop_get_prefix, property_entry.name)
        get_entry = property_scope.lookup_here("__get__")
        code.putln("")
        code.putln(
            "static PyObject *%s(PyObject *o, void *x) {" %
                property_entry.getter_cname)
        code.putln(
                "return %s(o);" %
                    get_entry.func_cname)
        code.putln(
            "}")
    
    def generate_property_set_function(self, property_entry, code):
        property_scope = property_entry.scope
        property_entry.setter_cname = property_scope.parent_scope.mangle(
            Naming.prop_set_prefix, property_entry.name)
        set_entry = property_scope.lookup_here("__set__")
        del_entry = property_scope.lookup_here("__del__")
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, PyObject *v, void *x) {" %
                property_entry.setter_cname)
        code.putln(
                "if (v) {")
        if set_entry:
            code.putln(
                    "return %s(o, v);" %
                        set_entry.func_cname)
        else:
            code.putln(
                    'PyErr_SetString(PyExc_NotImplementedError, "__set__");')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
                "else {")
        if del_entry:
            code.putln(
                    "return %s(o);" %
                        del_entry.func_cname)
        else:
            code.putln(
                    'PyErr_SetString(PyExc_NotImplementedError, "__del__");')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
            "}")

    def generate_typeobj_definition(self, modname, entry, code):
        type = entry.type
        scope = type.scope
        for suite in TypeSlots.substructures:
            suite.generate_substructure(scope, code)
        code.putln("")
        if entry.visibility == 'public':
            header = "DL_EXPORT(PyTypeObject) %s = {"
        else:
            #header = "statichere PyTypeObject %s = {"
            header = "PyTypeObject %s = {"
        #code.putln(header % scope.parent_type.typeobj_cname)
        code.putln(header % type.typeobj_cname)
        code.putln(
            "PyObject_HEAD_INIT(0)")
        code.putln(
            "0, /*ob_size*/")
        code.putln(
            '"%s.%s", /*tp_name*/' % (
                modname, scope.class_name))
        if type.typedef_flag:
            objstruct = type.objstruct_cname
        else:
            #objstruct = "struct %s" % scope.parent_type.objstruct_cname
            objstruct = "struct %s" % type.objstruct_cname
        code.putln(
            "sizeof(%s), /*tp_basicsize*/" %
                objstruct)
        code.putln(
            "0, /*tp_itemsize*/")
        for slot in TypeSlots.slot_table:
            slot.generate(scope, code)
        code.putln(
            "};")
    
    def generate_method_table(self, env, code):
        code.putln("")
        code.putln(
            "static struct PyMethodDef %s[] = {" % 
                env.method_table_cname)
        for entry in env.pyfunc_entries:
                code.put_pymethoddef(entry, ",")
        code.putln(
                "{0, 0, 0, 0}")
        code.putln(
            "};")
    
    def generate_member_table(self, env, code):
        #print "ModuleNode.generate_member_table: scope =", env ###
        if env.public_attr_entries:
            code.putln("")
            code.putln(
                "static struct PyMemberDef %s[] = {" %
                    env.member_table_cname)
            type = env.parent_type
            if type.typedef_flag:
                objstruct = type.objstruct_cname
            else:
                objstruct = "struct %s" % type.objstruct_cname
            for entry in env.public_attr_entries:
                type_code = entry.type.pymemberdef_typecode
                if entry.visibility == 'readonly':
                    flags = "READONLY"
                else:
                    flags = "0"
                code.putln('{"%s", %s, %s, %s, 0},' % (
                    entry.name,
                    type_code,
                    "offsetof(%s, %s)" % (objstruct, entry.name),
                    flags))
            code.putln(
                    "{0, 0, 0, 0, 0}")
            code.putln(
                "};")
    
    def generate_getset_table(self, env, code):
        if env.property_entries:
            code.putln("")
            code.putln(
                "static struct PyGetSetDef %s[] = {" %
                    env.getset_table_cname)
            for entry in env.property_entries:
                code.putln(
                    '{"%s", %s, %s, %s, 0},' % (
                        entry.name,
                        entry.getter_cname or "0",
                        entry.setter_cname or "0",
                        entry.doc_cname or "0"))
            code.putln(
                    "{0, 0, 0, 0, 0}")
            code.putln(
                "};")
    
    def generate_interned_name_table(self, env, code):
        items = env.intern_map.items()
        if items:
            items.sort()
            code.putln("")
            code.putln(
                "static __Pyx_InternTabEntry %s[] = {" %
                    Naming.intern_tab_cname)
            for (name, cname) in items:
                code.putln(
                    '{&%s, "%s"},' % (
                        cname,
                        name))
            code.putln(
                "{0, 0}")
            code.putln(
                "};")
    
    def generate_py_string_table(self, env, code):
        entries = env.all_pystring_entries
        if entries:
            code.putln("")
            code.putln(
                "static __Pyx_StringTabEntry %s[] = {" %
                    Naming.stringtab_cname)
            for entry in entries:
                code.putln(
                    "{&%s, %s, sizeof(%s)}," % (
                        entry.pystring_cname,
                        entry.cname,
                        entry.cname))
            code.putln(
                "{0, 0, 0}")
            code.putln(
                "};")
    
    def generate_filename_init_prototype(self, code):
        code.putln("");
        code.putln("static void %s(void); /*proto*/" % Naming.fileinit_cname)

    def generate_module_init_func(self, imported_modules, env, code):
        code.putln("")
        header = "PyMODINIT_FUNC init%s(void)" % env.module_name
        code.putln("%s; /*proto*/" % header)
        code.putln("%s {" % header)
        code.put_var_declarations(env.temp_entries)
        #code.putln("/*--- Libary function declarations ---*/")
        env.generate_library_function_declarations(code)
        self.generate_filename_init_call(code)
        #code.putln("/*--- Module creation code ---*/")
        self.generate_module_creation_code(env, code)
        #code.putln("/*--- Intern code ---*/")
        self.generate_intern_code(env, code)
        #code.putln("/*--- String init code ---*/")
        self.generate_string_init_code(env, code)
        #code.putln("/*--- Global init code ---*/")
        self.generate_global_init_code(env, code)

        #code.putln("/*--- Type init code ---*/")
        self.generate_type_init_code(env, code)

        #code.putln("/*--- Type import code ---*/")
        for module in imported_modules:
            self.generate_type_import_code_for_module(module, env, code)

        #code.putln("/*--- Execution code ---*/")
        self.body.generate_execution_code(code)
        code.putln("return;")
        code.put_label(code.error_label)
        code.put_var_xdecrefs(env.temp_entries)
        code.putln('__Pyx_AddTraceback("%s");' % (env.qualified_name))
        env.use_utility_code(Nodes.traceback_utility_code)
        code.putln('}')
    
    def generate_filename_init_call(self, code):
        code.putln("%s();" % Naming.fileinit_cname)
    
    def generate_module_creation_code(self, env, code):
        # Generate code to create the module object and
        # install the builtins.
        if env.doc:
            doc = env.doc_cname
        else:
            doc = "0"
        code.putln(
            '%s = Py_InitModule4("%s", %s, %s, 0, PYTHON_API_VERSION);' % (
                env.module_cname, 
                env.module_name, 
                env.method_table_cname, 
                doc))
        code.putln(
            "if (!%s) %s;" % (
                env.module_cname,
                code.error_goto(self.pos)));
        code.putln(
            '%s = PyImport_AddModule("__builtin__");' %
                Naming.builtins_cname)
        code.putln(
            "if (!%s) %s;" % (
                Naming.builtins_cname,
                code.error_goto(self.pos)));
        code.putln(
            'if (PyObject_SetAttrString(%s, "__builtins__", %s) < 0) %s;' % (
                env.module_cname,
                Naming.builtins_cname,
                code.error_goto(self.pos)))
    
    def generate_intern_code(self, env, code):
        if env.intern_map:
            env.use_utility_code(Nodes.init_intern_tab_utility_code);
            code.putln(
                "if (__Pyx_InternStrings(%s) < 0) %s;" % (
                    Naming.intern_tab_cname,
                    code.error_goto(self.pos)))
    
    def generate_string_init_code(self, env, code):
        if env.all_pystring_entries:
            env.use_utility_code(Nodes.init_string_tab_utility_code)
            code.putln(
                "if (__Pyx_InitStrings(%s) < 0) %s;" % (
                    Naming.stringtab_cname,
                    code.error_goto(self.pos)))
    
    def generate_global_init_code(self, env, code):
        # Generate code to initialise global PyObject *
        # variables to None.
        for entry in env.var_entries:
            if entry.visibility <> 'extern':
                if entry.type.is_pyobject:
                    code.put_init_var_to_py_none(entry)
    
    def generate_type_import_code_for_module(self, module, env, code):
        # Generate type import code for all extension types in
        # an imported module.
        if module.c_class_entries:
            for entry in module.c_class_entries:
                self.generate_type_import_code(env, entry.type, entry.pos, code)
    
    def generate_type_init_code(self, env, code):
        # Generate type import code for extern extension types
        # and type ready code for non-extern ones.
        for entry in env.c_class_entries:
            if entry.visibility == 'extern':
                self.generate_type_import_code(env, entry.type, entry.pos, code)
            else:
                self.generate_base_type_import_code(env, entry, code)
                self.generate_exttype_vtable_init_code(entry, code)
                self.generate_type_ready_code(env, entry, code)
                self.generate_typeptr_assignment_code(entry, code)
    
    def generate_base_type_import_code(self, env, entry, code):
        base_type = entry.type.base_type
        if base_type and base_type.module_name <> env.qualified_name:
            self.generate_type_import_code(env, base_type, self.pos, code)
    
    def use_type_import_utility_code(self, env):
        import ExprNodes
        env.use_utility_code(Nodes.type_import_utility_code)
        env.use_utility_code(ExprNodes.import_utility_code)
    
    def generate_type_import_code(self, env, type, pos, code):
        # If not already done, generate code to import the typeobject of an
        # extension type defined in another module, and extract its C method
        # table pointer if any.
        if type in env.types_imported:
            return
        if type.typedef_flag:
            objstruct = type.objstruct_cname
        else:
            objstruct = "struct %s" % type.objstruct_cname
        code.putln('%s = __Pyx_ImportType("%s", "%s", sizeof(%s)); if (!%s) %s' % (
            type.typeptr_cname,
            type.module_name, 
            type.name,
            objstruct,
            type.typeptr_cname,
            code.error_goto(pos)))
        self.use_type_import_utility_code(env)
        if type.vtabptr_cname:
            code.putln(
                "if (__Pyx_GetVtable(%s->tp_dict, &%s) < 0) %s" % (
                    type.typeptr_cname,
                    type.vtabptr_cname,
                    code.error_goto(pos)))
            env.use_utility_code(Nodes.get_vtable_utility_code)
        env.types_imported[type] = 1
    
    def generate_type_ready_code(self, env, entry, code):
        # Generate a call to PyType_Ready for an extension
        # type defined in this module.
        type = entry.type
        typeobj_cname = type.typeobj_cname
        scope = type.scope
        if scope: # could be None if there was an error
            if entry.visibility <> 'extern':
                for slot in TypeSlots.slot_table:
                    slot.generate_dynamic_init_code(scope, code)
                code.putln(
                    "if (PyType_Ready(&%s) < 0) %s" % (
                        typeobj_cname,
                        code.error_goto(entry.pos)))
                if type.vtable_cname:
                    code.putln(
                        "if (__Pyx_SetVtable(%s.tp_dict, %s) < 0) %s" % (
                            typeobj_cname,
                            type.vtabptr_cname,
                            code.error_goto(entry.pos)))
                    env.use_utility_code(Nodes.set_vtable_utility_code)
                code.putln(
                    'if (PyObject_SetAttrString(%s, "%s", (PyObject *)&%s) < 0) %s' % (
                        Naming.module_cname,
                        scope.class_name,
                        typeobj_cname,
                        code.error_goto(entry.pos)))
                weakref_entry = scope.lookup_here("__weakref__")
                if weakref_entry:
                    if weakref_entry.type is py_object_type:
                        tp_weaklistoffset = "%s.tp_weaklistoffset" % typeobj_cname
                        code.putln("if (%s == 0) %s = offsetof(struct %s, %s);" % (
                            tp_weaklistoffset,
                            tp_weaklistoffset,
                            type.objstruct_cname,
                            weakref_entry.cname))
                    else:
                        error(weakref_entry.pos, "__weakref__ slot must be of type 'object'")
    
    def generate_exttype_vtable_init_code(self, entry, code):
        # Generate code to initialise the C method table of an
        # extension type.
        type = entry.type
        if type.vtable_cname:
            code.putln(
                "%s = &%s;" % (
                    type.vtabptr_cname,
                    type.vtable_cname))
            if type.base_type and type.base_type.vtabptr_cname:
                code.putln(
                    "%s.%s = *%s;" % (
                        type.vtable_cname,
                        Naming.obj_base_cname,
                        type.base_type.vtabptr_cname))
            for meth_entry in type.scope.cfunc_entries:
                if meth_entry.func_cname:
                    code.putln(
                        "*(void(**)())&%s.%s = (void(*)())%s;" % (
                            type.vtable_cname,
                            meth_entry.cname,
                            meth_entry.func_cname))
    
    def generate_typeptr_assignment_code(self, entry, code):
        # Generate code to initialise the typeptr of an extension
        # type defined in this module to point to its type object.
        type = entry.type
        if type.typeobj_cname:
            code.putln(
                "%s = &%s;" % (
                    type.typeptr_cname, type.typeobj_cname))
    
    def generate_utility_functions(self, env, code):
        code.putln("")
        code.putln("/* Runtime support code */")
        code.putln("")
        code.putln("static void %s(void) {" % Naming.fileinit_cname)
        code.putln("%s = %s;" % 
            (Naming.filetable_cname, Naming.filenames_cname))
        code.putln("}")
        for utility_code in env.utility_code_used:
            code.h.put(utility_code[0])
            code.put(utility_code[1])
