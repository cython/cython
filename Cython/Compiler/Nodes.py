#
#   Pyrex - Parse tree nodes
#

import os, string, sys, time

import Code
from Errors import error, warning, InternalError
import Naming
import PyrexTypes
from PyrexTypes import py_object_type, error_type, CTypedefType
from Symtab import ModuleScope, LocalScope, \
    StructOrUnionScope, PyClassScope, CClassScope
import TypeSlots
import Version
from Pyrex.Utils import open_new_file, replace_suffix
import Options

from DebugFlags import debug_disposal_code

absolute_path_length = len(os.path.abspath('.')) 

def relative_position(pos):
    """
    We embed the relative filename in the generated C file, since we
    don't want to have to regnerate and compile all the source code
    whenever the Python install directory moves (which could happen,
    e.g,. when distributing binaries.)
    
    INPUT:
        a position tuple -- (absolute filename, line number column position)

    OUTPUT:
        relative filename
        line number

    AUTHOR: William Stein
    """
    return (pos[0][absolute_path_length+1:], pos[1])
        

class Node:
    #  pos         (string, int, int)   Source file position
    #  is_name     boolean              Is a NameNode
    #  is_literal  boolean              Is a ConstNode
    
    is_name = 0
    is_literal = 0
    
    def __init__(self, pos, **kw):
        self.pos = pos
        self.__dict__.update(kw)
    
    #
    #  There are 3 phases of parse tree processing, applied in order to
    #  all the statements in a given scope-block:
    #
    #  (1) analyse_declarations
    #        Make symbol table entries for all declarations at the current
    #        level, both explicit (def, cdef, etc.) and implicit (assignment
    #        to an otherwise undeclared name).
    #
    #		(2)	analyse_expressions
    #         Determine the result types of expressions and fill in the
    #         'type' attribute of each ExprNode. Insert coercion nodes into the
    #         tree where needed to convert to and from Python objects. 
    #         Allocate temporary locals for intermediate results. Fill
    #         in the 'result_code' attribute of each ExprNode with a C code
    #         fragment.
    #
    #   (3) generate_code
    #         Emit C code for all declarations, statements and expressions.
    #         Recursively applies the 3 processing phases to the bodies of
    #         functions.
    #
    
    def analyse_declarations(self, env):
        pass
    
    def analyse_expressions(self, env):
        raise InternalError("analyse_expressions not implemented for %s" % \
            self.__class__.__name__)
    
    def generate_code(self, code):
        raise InternalError("generate_code not implemented for %s" % \
            self.__class__.__name__)


class BlockNode:
    #  Mixin class for nodes representing a declaration block.

    def generate_const_definitions(self, env, code):
        if env.const_entries:
            code.putln("")
            for entry in env.const_entries:
                if not entry.is_interned:
                    code.put_var_declaration(entry, static = 1)
    
    def generate_interned_name_decls(self, env, code):
        #  Flush accumulated interned names from the global scope
        #  and generate declarations for them.
        genv = env.global_scope()
        intern_map = genv.intern_map
        names = genv.interned_names
        if names:
            code.putln("")
            for name in names:
                code.putln(
                    "static PyObject *%s;" % intern_map[name])
            del names[:]
    
    def generate_py_string_decls(self, env, code):
        entries = env.pystring_entries
        if entries:
            code.putln("")
            for entry in entries:
                code.putln(
                    "static PyObject *%s;" % entry.pystring_cname)
        
    def generate_cached_builtins_decls(self, env, code):
        entries = env.builtin_scope().undeclared_cached_entries
        if len(entries) > 0:
            code.putln("")
        for entry in entries:
            code.putln("static PyObject *%s;" % entry.cname)
        del entries[:]
        

class ModuleNode(Node, BlockNode):
    #  doc       string or None
    #  body      StatListNode
    
    def analyse_declarations(self, env):
        if Options.embed_pos_in_docstring:
            env.doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
            if not self.doc is None:
                env.doc = env.doc + '\\n' + self.doc
        else:
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
            h_code = Code.CCodeWriter(result.h_file)
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
        code = Code.CCodeWriter(result.c_file)
        code.init_labels()
        self.generate_module_preamble(env, modules, code)
        for module in modules:
            self.generate_declarations_for_module(module, code,
                definition = module is env)
        code.putln("")
        code.putln("/* Implementation of %s */" % env.qualified_name)
        self.generate_const_definitions(env, code)
        self.generate_interned_name_decls(env, code)
        self.generate_py_string_decls(env, code)
        self.generate_cached_builtins_decls(env, code)
        self.body.generate_function_definitions(env, code)
        self.generate_interned_name_table(env, code)
        self.generate_py_string_table(env, code)
        self.generate_typeobj_definitions(env, code)
        self.generate_method_table(env, code)
        self.generate_filename_init_prototype(code)
        self.generate_module_init_func(modules[:-1], env, code)
        self.generate_filename_table(code)
        self.generate_utility_functions(env, code)
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
        code.putln('#define PY_SSIZE_T_CLEAN')
        for filename in env.python_include_files:
            code.putln('#include "%s"' % filename)
        code.putln("#ifndef PY_LONG_LONG")
        code.putln("  #define PY_LONG_LONG LONG_LONG")
        code.putln("#endif")
        code.putln("#if PY_VERSION_HEX < 0x02050000")
        code.putln("  typedef int Py_ssize_t;")
        code.putln("  #define PY_SSIZE_T_MAX INT_MAX")
        code.putln("  #define PY_SSIZE_T_MIN INT_MIN")
        code.putln("  #define PyInt_FromSsize_t(z) PyInt_FromLong(z)")
        code.putln("  #define PyInt_AsSsize_t(o)   PyInt_AsLong(o)")
        code.putln("#endif")
        self.generate_extern_c_macro_definition(code)
        code.putln("%s double pow(double, double);" % Naming.extern_c_macro)
        self.generate_includes(env, cimported_modules, code)
        #for filename in env.include_files:
        #	code.putln('#include "%s"' % filename)
        code.putln('')
        code.put(utility_function_predeclarations)
        if Options.intern_names:
            code.putln(get_name_interned_predeclaration)
        else:
            code.putln(get_name_predeclaration)
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
        for value_entry in enum_values:
            if value_entry.value == value_entry.name:
                code.putln(
                    "%s," % 
                        value_entry.cname)
            else:
                code.putln(
                    "%s = %s," % (
                        value_entry.cname,
                        value_entry.value))
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
        self.generate_self_cast(scope, code)
        type = scope.parent_type
        if type.vtabslot_cname:
            code.putln("*(struct %s **)&p->%s = %s;" % (
                type.vtabstruct_cname,
                type.vtabslot_cname,
                type.vtabptr_cname))
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                if entry.name == "__weakref__":
                    code.putln("p->%s = NULL;" % entry.cname)
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
        self.generate_self_cast(scope, code)
        self.generate_usr_dealloc_call(scope, code)
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                if entry.name == "__weakref__":
                    code.putln(
                        "if (p->%s) PyObject_ClearWeakRefs(o);" %
                            entry.cname)
                else:
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
        code.putln(
                "int e;")
        self.generate_self_cast(scope, code)
        if base_type:
            code.putln(
                    "e = %s->tp_traverse(o, v, a); if (e) return e;" %
                        base_type.typeptr_cname)
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry.name != "__weakref__":
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
        self.generate_self_cast(scope, code)
        if base_type:
            code.putln(
                "%s->tp_clear(o);" %
                    base_type.typeptr_cname)
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry.name != "__weakref__":
                name = "p->%s" % entry.cname
                code.put_xdecref(name, entry.type)
                #code.put_init_to_py_none(name)
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
            "static PyObject *%s(PyObject *o, Py_ssize_t i) {" %
                scope.mangle_internal("sq_item"))
        code.putln(
                "PyObject *r;")
        code.putln(
                "PyObject *x = PyInt_FromSsize_t(i); if(!x) return 0;")
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
            "static int %s(PyObject *o, Py_ssize_t i, Py_ssize_t j, PyObject *v) {" %
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
            self.full_module_name, scope.class_name))
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
        #code.putln("/*--- Builtin init code ---*/")
        self.generate_builtin_init_code(env, code)
        #code.putln("/*--- Global init code ---*/")
        self.generate_global_init_code(env, code)
        #code.putln("/*--- Type import code ---*/")
        for module in imported_modules:
            self.generate_type_import_code_for_module(module, env, code)
        #code.putln("/*--- Type init code ---*/")
        self.generate_type_init_code(env, code)
        #code.putln("/*--- Execution code ---*/")
        self.body.generate_execution_code(code)
        code.putln("return;")
        code.put_label(code.error_label)
        code.put_var_xdecrefs(env.temp_entries)
        code.putln('__Pyx_AddTraceback("%s");' % (env.qualified_name))
        env.use_utility_code(traceback_utility_code)
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
            env.use_utility_code(init_intern_tab_utility_code);
            code.putln(
                "if (__Pyx_InternStrings(%s) < 0) %s;" % (
                    Naming.intern_tab_cname,
                    code.error_goto(self.pos)))
    
    def generate_string_init_code(self, env, code):
        if env.all_pystring_entries:
            env.use_utility_code(init_string_tab_utility_code)
            code.putln(
                "if (__Pyx_InitStrings(%s) < 0) %s;" % (
                    Naming.stringtab_cname,
                    code.error_goto(self.pos)))
    
    def generate_builtin_init_code(self, env, code):
        # Lookup and cache builtin objects.
        if Options.cache_builtins:
            for entry in env.builtin_scope().cached_entries:
                if Options.intern_names:
                    #assert entry.interned_cname is not None
                    code.putln(
                        '%s = __Pyx_GetName(%s, %s); if (!%s) %s' % (
                        entry.cname,
                        Naming.builtins_cname,
                        entry.interned_cname,
                        entry.cname, 
                        code.error_goto(entry.pos)))
                else:
                    code.putln(
                        '%s = __Pyx_GetName(%s, "%s"); if (!%s) %s' % (
                        entry.cname,
                        Naming.builtins_cname,
                        self.entry.name,
                        entry.cname, 
                        code.error_goto(entry.pos)))

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
                self.generate_type_import_code(env, entry, code)
    
    def generate_type_init_code(self, env, code):
        # Generate type import code for extern extension types
        # and type ready code for non-extern ones.
        for entry in env.c_class_entries:
            if entry.visibility == 'extern':
                self.generate_type_import_code(env, entry, code)
            else:
                self.generate_exttype_vtable_init_code(entry, code)
                self.generate_type_ready_code(env, entry, code)
                self.generate_typeptr_assignment_code(entry, code)
    
    def use_type_import_utility_code(self, env):
        import ExprNodes
        env.use_utility_code(type_import_utility_code)
        env.use_utility_code(ExprNodes.import_utility_code)
    
    def generate_type_import_code(self, env, entry, code):
        # Generate code to import the typeobject of an
        # extension type defined in another module, and
        # extract its C method table pointer if any.
        type = entry.type
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
            code.error_goto(entry.pos)))
        self.use_type_import_utility_code(env)
        if type.vtabptr_cname:
            code.putln(
                "if (__Pyx_GetVtable(%s->tp_dict, &%s) < 0) %s" % (
                    type.typeptr_cname,
                    type.vtabptr_cname,
                    code.error_goto(entry.pos)))
            env.use_utility_code(get_vtable_utility_code)
    
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
                    env.use_utility_code(set_vtable_utility_code)
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
                        "*(void **)&%s.%s = (void *)%s;" % (
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
            code.put(utility_code)


class StatListNode(Node):
    # stats     a list of StatNode
    
    def analyse_declarations(self, env):
        #print "StatListNode.analyse_declarations" ###
        for stat in self.stats:
            stat.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        #print "StatListNode.analyse_expressions" ###
        for stat in self.stats:
            stat.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        #print "StatListNode.generate_function_definitions" ###
        for stat in self.stats:
            stat.generate_function_definitions(env, code)
            
    def generate_execution_code(self, code):
        #print "StatListNode.generate_execution_code" ###
        for stat in self.stats:
            code.mark_pos(stat.pos)
            stat.generate_execution_code(code)
    

class StatNode(Node):
    #
    #  Code generation for statements is split into the following subphases:
    #
    #  (1) generate_function_definitions
    #        Emit C code for the definitions of any structs,
    #        unions, enums and functions defined in the current
    #        scope-block.
    #
    #  (2) generate_execution_code
    #        Emit C code for executable statements.
    #
    
    def generate_function_definitions(self, env, code):
        pass
    
    def generate_execution_code(self, code):
        raise InternalError("generate_execution_code not implemented for %s" % \
            self.__class__.__name__)


class CDefExternNode(StatNode):
    #  include_file   string or None
    #  body           StatNode
    
    def analyse_declarations(self, env):
        if self.include_file:
            env.add_include_file(self.include_file)
        old_cinclude_flag = env.in_cinclude
        env.in_cinclude = 1
        self.body.analyse_declarations(env)
        env.in_cinclude = old_cinclude_flag
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass
        

class CDeclaratorNode(Node):
    # Part of a C declaration.
    #
    # Processing during analyse_declarations phase:
    #
    #   analyse
    #      Returns (name, type) pair where name is the
    #      CNameDeclaratorNode of the name being declared 
    #      and type is the type it is being declared as.
    #
        
    def analyse_expressions(self, env):
        pass

    def generate_execution_code(self, env):
        pass


class CNameDeclaratorNode(CDeclaratorNode):
    #  name   string           The Pyrex name being declared
    #  cname  string or None   C name, if specified
    
    def analyse(self, base_type, env):
        self.type = base_type
        return self, base_type
        
    def analyse_expressions(self, env):
        self.entry = env.lookup(self.name)
        if self.rhs is not None:
            if self.type.is_pyobject:
                self.entry.init_to_none = False
                self.entry.init = 0
            self.rhs.analyse_types(env)
            self.rhs = self.rhs.coerce_to(self.type, env)
            self.rhs.allocate_temps(env)
            self.rhs.release_temp(env)

    def generate_execution_code(self, code):
        if self.rhs is not None:
            self.rhs.generate_evaluation_code(code)
            if self.type.is_pyobject:
                self.rhs.make_owned_reference(code)
            code.putln('%s = %s;' % (self.entry.cname, self.rhs.result_as(self.entry.type)))
            self.rhs.generate_post_assignment_code(code)
            code.putln()

class CPtrDeclaratorNode(CDeclaratorNode):
    # base     CDeclaratorNode
    
    def analyse(self, base_type, env):
        if base_type.is_pyobject:
            error(self.pos,
                "Pointer base type cannot be a Python object")
        ptr_type = PyrexTypes.c_ptr_type(base_type)
        return self.base.analyse(ptr_type, env)
        
    def analyse_expressions(self, env):
        self.base.analyse_expressions(env)

    def generate_execution_code(self, env):
        self.base.generate_execution_code(env)

class CArrayDeclaratorNode(CDeclaratorNode):
    # base        CDeclaratorNode
    # dimension   ExprNode
    
    def analyse(self, base_type, env):
        if self.dimension:
            self.dimension.analyse_const_expression(env)
            if not self.dimension.type.is_int:
                error(self.dimension.pos, "Array dimension not integer")
            #size = self.dimension.value
            size = self.dimension.result_code
        else:
            size = None
        if not base_type.is_complete():
            error(self.pos,
                "Array element type '%s' is incomplete" % base_type)
        if base_type.is_pyobject:
            error(self.pos,
                "Array element cannot be a Python object")
        array_type = PyrexTypes.c_array_type(base_type, size)
        return self.base.analyse(array_type, env)


class CFuncDeclaratorNode(CDeclaratorNode):
    # base             CDeclaratorNode
    # args             [CArgDeclNode]
    # has_varargs      boolean
    # exception_value  ConstNode
    # exception_check  boolean    True if PyErr_Occurred check needed

    def analyse(self, return_type, env):
        func_type_args = []
        for arg_node in self.args:
            name_declarator, type = arg_node.analyse(env)
            name = name_declarator.name
            if name_declarator.cname:
                error(self.pos, 
                    "Function argument cannot have C name specification")
            # Turn *[] argument into **
            if type.is_array:
                type = PyrexTypes.c_ptr_type(type.base_type)
            # Catch attempted C-style func(void) decl
            if type.is_void:
                error(arg_node.pos, "Function argument cannot be void")
            func_type_args.append(
                PyrexTypes.CFuncTypeArg(name, type, arg_node.pos))
            if arg_node.default:
                error(arg_node.pos, "C function argument cannot have default value")
        exc_val = None
        exc_check = 0
        if return_type.is_pyobject \
            and (self.exception_value or self.exception_check):
                error(self.pos,
                    "Exception clause not allowed for function returning Python object")
        else:
            if self.exception_value:
                self.exception_value.analyse_const_expression(env)
                exc_val = self.exception_value.result_code
                if not return_type.assignable_from(self.exception_value.type):
                    error(self.exception_value.pos,
                        "Exception value incompatible with function return type")
            exc_check = self.exception_check
        func_type = PyrexTypes.CFuncType(
            return_type, func_type_args, self.has_varargs, 
            exception_value = exc_val, exception_check = exc_check)
        return self.base.analyse(func_type, env)


class CArgDeclNode(Node):
    # Item in a function declaration argument list.
    #
    # base_type      CBaseTypeNode
    # declarator     CDeclaratorNode
    # not_none       boolean            Tagged with 'not None'
    # default        ExprNode or None
    # default_entry  Symtab.Entry       Entry for the variable holding the default value
    # is_self_arg    boolean            Is the "self" arg of an extension type method
    
    is_self_arg = 0
    
    def analyse(self, env):
        base_type = self.base_type.analyse(env)
        return self.declarator.analyse(base_type, env)


class CBaseTypeNode(Node):
    # Abstract base class for C base type nodes.
    #
    # Processing during analyse_declarations phase:
    #
    #   analyse
    #     Returns the type.
    
    pass


class CSimpleBaseTypeNode(CBaseTypeNode):
    # name             string
    # module_path      [string]     Qualifying name components
    # is_basic_c_type  boolean
    # signed           boolean
    # longness         integer
    # is_self_arg      boolean      Is self argument of C method

    def analyse(self, env):
        # Return type descriptor.
        type = None
        if self.is_basic_c_type:
            type = PyrexTypes.simple_c_type(self.signed, self.longness, self.name)
            if not type:
                error(self.pos, "Unrecognised type modifier combination")
        elif self.name == "object" and not self.module_path:
            type = py_object_type
        elif self.name is None:
            if self.is_self_arg and env.is_c_class_scope:
                type = env.parent_type
            else:
                type = py_object_type
        else:
            scope = env
            for name in self.module_path:
                entry = scope.find(name, self.pos)
                if entry and entry.as_module:
                    scope = entry.as_module
                else:
                    if entry:
                        error(self.pos, "'%s' is not a cimported module" % name)
                    scope = None
                    break
            if scope:
                entry = scope.find(self.name, self.pos)
                if entry and entry.is_type:
                    type = entry.type
                else:
                    error(self.pos, "'%s' is not a type identifier" % self.name)
        if type:
            return type
        else:
            return PyrexTypes.error_type


class CComplexBaseTypeNode(CBaseTypeNode):
    # base_type   CBaseTypeNode
    # declarator  CDeclaratorNode
    
    def analyse(self, env):
        base = self.base_type.analyse(env)
        _, type = self.declarator.analyse(base, env)
        return type


class CVarDefNode(StatNode):
    #  C variable definition or forward/extern function declaration.
    #
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarators   [CDeclaratorNode]
    
    def analyse_declarations(self, env, dest_scope = None):
        if not dest_scope:
            dest_scope = env
        base_type = self.base_type.analyse(env)
        for declarator in self.declarators:
            name_declarator, type = declarator.analyse(base_type, env)
            if not type.is_complete():
                if not (self.visibility == 'extern' and type.is_array):
                    error(declarator.pos,
                        "Variable type '%s' is incomplete" % type)
            if self.visibility == 'extern' and type.is_pyobject:
                error(declarator.pos,
                    "Python object cannot be declared extern")
            name = name_declarator.name
            cname = name_declarator.cname
            if type.is_cfunction:
                dest_scope.declare_cfunction(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility)
            else:
                dest_scope.declare_var(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility, is_cdef = 1)
    
    def analyse_expressions(self, env):
        for declarator in self.declarators:
            declarator.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        for declarator in self.declarators:
            declarator.generate_execution_code(code)


class CStructOrUnionDefNode(StatNode):
    #  name          string
    #  cname         string or None
    #  kind          "struct" or "union"
    #  typedef_flag  boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    
    def analyse_declarations(self, env):
        scope = None
        if self.attributes is not None:
            scope = StructOrUnionScope()
        self.entry = env.declare_struct_or_union(
            self.name, self.kind, scope, self.typedef_flag, self.pos,
            self.cname)
        if self.attributes is not None:
            for attr in self.attributes:
                attr.analyse_declarations(env, scope)
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class CEnumDefNode(StatNode):
    #  name           string or None
    #  cname          string or None
    #  items          [CEnumDefItemNode]
    #  typedef_flag   boolean
    #  entry          Entry
    
    def analyse_declarations(self, env):
        self.entry = env.declare_enum(self.name, self.pos,
            cname = self.cname, typedef_flag = self.typedef_flag)
        for item in self.items:
            item.analyse_declarations(env, self.entry)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class CEnumDefItemNode(StatNode):
    #  name     string
    #  cname    string or None
    #  value    ExprNode or None
    
    def analyse_declarations(self, env, enum_entry):
        if self.value:
            self.value.analyse_const_expression(env)
            value = self.value.result_code
        else:
            value = self.name
        entry = env.declare_const(self.name, enum_entry.type, 
            value, self.pos, cname = self.cname)
        enum_entry.enum_values.append(entry)


class CTypeDefNode(StatNode):
    #  base_type   CBaseTypeNode
    #  declarator  CDeclaratorNode
    
    def analyse_declarations(self, env):
        base = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base, env)
        name = name_declarator.name
        cname = name_declarator.cname
        if env.in_cinclude:
            type = CTypedefType(cname or name, type)
        env.declare_type(name, type, self.pos, cname = cname)
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class FuncDefNode(StatNode, BlockNode):
    #  Base class for function definition nodes.
    #
    #  return_type     PyrexType
    #  #filename        string        C name of filename string const
    #  entry           Symtab.Entry
    
    def analyse_expressions(self, env):
        pass
                
    def generate_function_definitions(self, env, code):
        # Generate C code for header and body of function
        genv = env.global_scope()
        lenv = LocalScope(name = self.entry.name, outer_scope = genv)
        #lenv.function_name = self.function_name()
        lenv.return_type = self.return_type
        #self.filename = lenv.get_filename_const(self.pos)
        code.init_labels()
        self.declare_arguments(lenv)
        self.body.analyse_declarations(lenv)
        self.body.analyse_expressions(lenv)
        # Code for nested function definitions would go here
        # if we supported them, which we probably won't.
        # ----- Top-level constants used by this function
        self.generate_interned_name_decls(lenv, code)
        self.generate_py_string_decls(lenv, code)
        self.generate_cached_builtins_decls(lenv, code)
        #code.putln("")
        #code.put_var_declarations(lenv.const_entries, static = 1)
        self.generate_const_definitions(lenv, code)
        # ----- Function header
        code.putln("")
        self.generate_function_header(code,
            with_pymethdef = env.is_py_class_scope)
        # ----- Local variable declarations
        self.generate_argument_declarations(lenv, code)
        code.put_var_declarations(lenv.var_entries)
        init = ""
        if not self.return_type.is_void:
            code.putln(
                "%s%s;" % 
                    (self.return_type.declaration_code(
                        Naming.retval_cname),
                    init))
        code.put_var_declarations(lenv.temp_entries)
        self.generate_keyword_list(code)
        # ----- Extern library function declarations
        lenv.generate_library_function_declarations(code)
        # ----- Fetch arguments
        self.generate_argument_parsing_code(code)
        self.generate_argument_increfs(lenv, code)
        #self.generate_stararg_getting_code(code)
        self.generate_argument_conversion_code(code)
        # ----- Initialise local variables
        for entry in lenv.var_entries:
            if entry.type.is_pyobject and entry.init_to_none:
                code.put_init_var_to_py_none(entry)
        # ----- Check types of arguments
        self.generate_argument_type_tests(code)
        # ----- Function body
        self.body.generate_execution_code(code)
        # ----- Default return value
        code.putln("")
        if self.return_type.is_pyobject:
            #if self.return_type.is_extension_type:
            #	lhs = "(PyObject *)%s" % Naming.retval_cname
            #else:
            lhs = Naming.retval_cname
            code.put_init_to_py_none(lhs, self.return_type)
        else:
            val = self.return_type.default_value
            if val:
                code.putln("%s = %s;" % (Naming.retval_cname, val))
        code.putln("goto %s;" % code.return_label)
        # ----- Error cleanup
        code.put_label(code.error_label)
        code.put_var_xdecrefs(lenv.temp_entries)
        err_val = self.error_value()
        exc_check = self.caller_will_check_exceptions()
        if err_val is not None or exc_check:
            code.putln(
                '__Pyx_AddTraceback("%s");' % 
                    self.entry.qualified_name)
            if err_val is not None:
                code.putln(
                    "%s = %s;" % (
                        Naming.retval_cname, 
                        err_val))
        else:
            code.putln(
                '__Pyx_WriteUnraisable("%s");' % 
                    self.entry.qualified_name)
            env.use_utility_code(unraisable_exception_utility_code)
        # ----- Return cleanup
        code.put_label(code.return_label)
        code.put_var_decrefs(lenv.var_entries)
        code.put_var_decrefs(lenv.arg_entries)
        self.put_stararg_decrefs(code)
        if not self.return_type.is_void:
            retval_code = Naming.retval_cname
            #if self.return_type.is_extension_type:
            #	retval_code = "((%s)%s) " % (
            #		self.return_type.declaration_code(""),
            #		retval_code)
            code.putln("return %s;" % retval_code)
        code.putln("}")
    
    def put_stararg_decrefs(self, code):
        pass

    def declare_argument(self, env, arg):
        if arg.type.is_void:
            error(arg.pos, "Invalid use of 'void'")
        elif not arg.type.is_complete() and not arg.type.is_array:
            error(arg.pos,
                "Argument type '%s' is incomplete" % arg.type)
        return env.declare_arg(arg.name, arg.type, arg.pos)
    
    def generate_argument_increfs(self, env, code):
        # Turn borrowed argument refs into owned refs.
        # This is necessary, because if the argument is
        # assigned to, it will be decrefed.
        for entry in env.arg_entries:
            code.put_var_incref(entry)

    def generate_execution_code(self, code):
        pass
        

class CFuncDefNode(FuncDefNode):
    #  C function definition.
    #
    #  modifiers     'inline ' or ''
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarator    CDeclaratorNode
    #  body          StatListNode
    #
    #  type          CFuncType
    
    def unqualified_name(self):
        return self.entry.name
        
    def analyse_declarations(self, env):
        base_type = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base_type, env)
        # Remember the actual type according to the function header
        # written here, because the type in the symbol table entry
        # may be different if we're overriding a C method inherited
        # from the base type of an extension type.
        self.type = type
        if not type.is_cfunction:
            error(self.pos, 
                "Suite attached to non-function declaration")
        name = name_declarator.name
        cname = name_declarator.cname
        self.entry = env.declare_cfunction(
            name, type, self.pos, 
            cname = cname, visibility = self.visibility,
            defining = self.body is not None)
        self.return_type = type.return_type
    
    def declare_arguments(self, env):
        for arg in self.type.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            self.declare_argument(env, arg)
            
    def generate_function_header(self, code, with_pymethdef):
        arg_decls = []
        type = self.type
        for arg in type.args:
            arg_decls.append(arg.declaration_code())
        if type.has_varargs:
            arg_decls.append("...")
        if not arg_decls:
            arg_decls = ["void"]
        entity = "%s(%s)" % (self.entry.func_cname,
            string.join(arg_decls, ","))
        if self.visibility == 'public':
            dll_linkage = "DL_EXPORT"
        else:
            dll_linkage = None
        header = self.return_type.declaration_code(entity,
            dll_linkage = dll_linkage)
        if self.visibility <> 'private':
            storage_class = "%s " % Naming.extern_c_macro
        else:
            storage_class = "static "
        code.putln("%s%s%s {" % (
            storage_class,
            self.modifiers, 
            header))

    def generate_argument_declarations(self, env, code):
        # Arguments already declared in function header
        pass
    
    def generate_keyword_list(self, code):
        pass
        
    def generate_argument_parsing_code(self, code):
        pass
    
# 	def generate_stararg_getting_code(self, code):
# 		pass
    
    def generate_argument_conversion_code(self, code):
        pass
    
    def generate_argument_type_tests(self, code):
        pass
    
    def error_value(self):
        if self.return_type.is_pyobject:
            return "0"
        else:
            #return None
            return self.entry.type.exception_value
            
    def caller_will_check_exceptions(self):
        return self.entry.type.exception_check


class PyArgDeclNode(Node):
    # Argument which must be a Python object (used
    # for * and ** arguments).
    #
    # name   string
    # entry  Symtab.Entry
    
    pass
    

class DefNode(FuncDefNode):
    # A Python function definition.
    #
    # name          string                 the Python name of the function
    # args          [CArgDeclNode]         formal arguments
    # star_arg      PyArgDeclNode or None  * argument
    # starstar_arg  PyArgDeclNode or None  ** argument
    # doc           string or None
    # body          StatListNode
    #
    #  The following subnode is constructed internally
    #  when the def statement is inside a Python class definition.
    #
    #  assmt   AssignmentNode   Function construction/assignment
    
    assmt = None
    
    def analyse_declarations(self, env):
        for arg in self.args:
            base_type = arg.base_type.analyse(env)
            name_declarator, type = \
                arg.declarator.analyse(base_type, env)
            arg.name = name_declarator.name
            if name_declarator.cname:
                error(self.pos,
                    "Python function argument cannot have C name specification")
            arg.type = type.as_argument_type()
            arg.hdr_type = None
            arg.needs_conversion = 0
            arg.needs_type_test = 0
            arg.is_generic = 1
            if arg.not_none and not arg.type.is_extension_type:
                error(self.pos,
                    "Only extension type arguments can have 'not None'")
        self.declare_pyfunction(env)
        self.analyse_signature(env)
        self.return_type = self.entry.signature.return_type()
        if self.star_arg or self.starstar_arg:
            env.use_utility_code(get_starargs_utility_code)
    
    def analyse_signature(self, env):
        any_type_tests_needed = 0
        sig = self.entry.signature
        nfixed = sig.num_fixed_args()
        for i in range(nfixed):
            if i < len(self.args):
                arg = self.args[i]
                arg.is_generic = 0
                if sig.is_self_arg(i):
                    arg.is_self_arg = 1
                    arg.hdr_type = arg.type = env.parent_type
                    arg.needs_conversion = 0
                else:
                    arg.hdr_type = sig.fixed_arg_type(i)
                    if not arg.type.same_as(arg.hdr_type):
                        if arg.hdr_type.is_pyobject and arg.type.is_pyobject:
                            arg.needs_type_test = 1
                            any_type_tests_needed = 1
                        else:
                            arg.needs_conversion = 1
                if arg.needs_conversion:
                    arg.hdr_cname = Naming.arg_prefix + arg.name
                else:
                    arg.hdr_cname = Naming.var_prefix + arg.name
            else:
                self.bad_signature()
                return
        if nfixed < len(self.args):
            if not sig.has_generic_args:
                self.bad_signature()
            for arg in self.args:
                if arg.is_generic and arg.type.is_extension_type:
                    arg.needs_type_test = 1
                    any_type_tests_needed = 1
        if any_type_tests_needed:
            env.use_utility_code(arg_type_test_utility_code)
    
    def bad_signature(self):
        sig = self.entry.signature
        expected_str = "%d" % sig.num_fixed_args()
        if sig.has_generic_args:
            expected_str = expected_str + " or more"
        name = self.name
        if name.startswith("__") and name.endswith("__"):
            desc = "Special method"
        else:
            desc = "Method"
        error(self.pos,
            "%s %s has wrong number of arguments "
            "(%d declared, %s expected)" % (
                desc, self.name, len(self.args), expected_str))
    
    def declare_pyfunction(self, env):
        self.entry = env.declare_pyfunction(self.name, self.pos)
        if Options.embed_pos_in_docstring:
            self.entry.doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
            if not self.doc is None:
                self.entry.doc = self.entry.doc + '\\n' + self.doc
        else:
            self.entry.doc = self.doc
        self.entry.func_cname = \
            Naming.func_prefix + env.scope_prefix + self.name
        self.entry.doc_cname = \
            Naming.funcdoc_prefix + env.scope_prefix + self.name
        self.entry.pymethdef_cname = \
            Naming.pymethdef_prefix + env.scope_prefix + self.name
        
    def declare_arguments(self, env):
        for arg in self.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            if arg.needs_conversion:
                arg.entry = env.declare_var(arg.name, arg.type, arg.pos)
                if arg.type.is_pyobject:
                    arg.entry.init = "0"
                arg.entry.init_to_none = 0
            else:
                arg.entry = self.declare_argument(env, arg)
            arg.entry.is_self_arg = arg.is_self_arg
            if arg.hdr_type:
                if arg.is_self_arg or \
                    (arg.type.is_extension_type and not arg.hdr_type.is_extension_type):
                        arg.entry.is_declared_generic = 1
        self.declare_python_arg(env, self.star_arg)
        self.declare_python_arg(env, self.starstar_arg)

    def declare_python_arg(self, env, arg):
        if arg:
            arg.entry = env.declare_var(arg.name, 
                PyrexTypes.py_object_type, arg.pos)
            arg.entry.init = "0"
            arg.entry.init_to_none = 0
            arg.entry.xdecref_cleanup = 1
            
    def analyse_expressions(self, env):
        self.analyse_default_values(env)
        if env.is_py_class_scope:
            self.synthesize_assignment_node(env)
    
    def analyse_default_values(self, env):
        for arg in self.args:
            if arg.default:
                if arg.is_generic:
                    arg.default.analyse_types(env)
                    arg.default = arg.default.coerce_to(arg.type, env)
                    arg.default.allocate_temps(env)
                    arg.default_entry = env.add_default_value(arg.type)
                else:
                    error(arg.pos,
                        "This argument cannot have a default value")
                    arg.default = None
    
    def synthesize_assignment_node(self, env):
        import ExprNodes
        self.assmt = SingleAssignmentNode(self.pos,
            lhs = ExprNodes.NameNode(self.pos, name = self.name),
            rhs = ExprNodes.UnboundMethodNode(self.pos, 
                class_cname = env.class_obj_cname,
                function = ExprNodes.PyCFunctionNode(self.pos,
                    pymethdef_cname = self.entry.pymethdef_cname)))
        self.assmt.analyse_declarations(env)
        self.assmt.analyse_expressions(env)
            
    def generate_function_header(self, code, with_pymethdef):
        arg_code_list = []
        sig = self.entry.signature
        if sig.has_dummy_arg:
            arg_code_list.append(
                "PyObject *%s" % Naming.self_cname)
        for arg in self.args:
            if not arg.is_generic:
                if arg.is_self_arg:
                    arg_code_list.append("PyObject *%s" % arg.hdr_cname)
                else:
                    arg_code_list.append(
                        arg.hdr_type.declaration_code(arg.hdr_cname))
        if sig.has_generic_args:
            arg_code_list.append(
                "PyObject *%s, PyObject *%s"
                    % (Naming.args_cname, Naming.kwds_cname))
        arg_code = ", ".join(arg_code_list)
        dc = self.return_type.declaration_code(self.entry.func_cname)
        header = "static %s(%s)" % (dc, arg_code)
        code.putln("%s; /*proto*/" % header)
        if self.entry.doc:
            code.putln(
                'static char %s[] = "%s";' % (
                    self.entry.doc_cname,
                    self.entry.doc))
        if with_pymethdef:
            code.put(
                "static PyMethodDef %s = " % 
                    self.entry.pymethdef_cname)
            code.put_pymethoddef(self.entry, ";")
        code.putln("%s {" % header)

    def generate_argument_declarations(self, env, code):
        for arg in self.args:
            if arg.is_generic: # or arg.needs_conversion:
                code.put_var_declaration(arg.entry)
    
    def generate_keyword_list(self, code):
        if self.entry.signature.has_generic_args:
            code.put(
                "static char *%s[] = {" %
                    Naming.kwdlist_cname)
            for arg in self.args:
                if arg.is_generic:
                    code.put(
                        '"%s",' % 
                            arg.name)
            code.putln(
                "0};")
    
    def generate_argument_parsing_code(self, code):
        # Generate PyArg_ParseTuple call for generic
        # arguments, if any.
        if self.entry.signature.has_generic_args:
            arg_addrs = []
            arg_formats = []
            default_seen = 0
            for arg in self.args:
                arg_entry = arg.entry
                if arg.is_generic:
                    if arg.default:
                        code.putln(
                            "%s = %s;" % (
                                arg_entry.cname,
                                arg.default_entry.cname))
                        if not default_seen:
                            arg_formats.append("|")
                        default_seen = 1
                    elif default_seen:
                        error(arg.pos, "Non-default argument following default argument")
                    arg_addrs.append("&" + arg_entry.cname)
                    format = arg_entry.type.parsetuple_format
                    if format:
                        arg_formats.append(format)
                    else:
                        error(arg.pos, 
                            "Cannot convert Python object argument to type '%s' (when parsing input arguments)" 
                                % arg.type)
            argformat = '"%s"' % string.join(arg_formats, "")
            has_starargs = self.star_arg is not None or self.starstar_arg is not None
            if has_starargs:
                self.generate_stararg_getting_code(code)
            pt_arglist = [Naming.args_cname, Naming.kwds_cname, argformat,
                    Naming.kwdlist_cname] + arg_addrs
            pt_argstring = string.join(pt_arglist, ", ")
            code.put(
                'if (!PyArg_ParseTupleAndKeywords(%s)) ' %
                    pt_argstring)
            error_return_code = "return %s;" % self.error_value()
            if has_starargs:
                code.putln("{")
                code.put_xdecref(Naming.args_cname, py_object_type)
                code.put_xdecref(Naming.kwds_cname, py_object_type)
                self.generate_arg_xdecref(self.star_arg, code)
                self.generate_arg_xdecref(self.starstar_arg, code)
                code.putln(error_return_code)
                code.putln("}")
            else:
                code.putln(error_return_code)
            
    def put_stararg_decrefs(self, code):
        if self.star_arg or self.starstar_arg:
            code.put_xdecref(Naming.args_cname, py_object_type)
            code.put_xdecref(Naming.kwds_cname, py_object_type)
    
    def generate_arg_xdecref(self, arg, code):
        if arg:
            code.put_var_xdecref(arg.entry)
    
    def arg_address(self, arg):
        if arg:
            return "&%s" % arg.entry.cname
        else:
            return 0

    def generate_stararg_getting_code(self, code):
        if self.star_arg or self.starstar_arg:
            if not self.entry.signature.has_generic_args:
                error(self.pos, "This method cannot have * or ** arguments")
            star_arg_addr = self.arg_address(self.star_arg)
            starstar_arg_addr = self.arg_address(self.starstar_arg)
            code.putln(
                "if (__Pyx_GetStarArgs(&%s, &%s, %s, %s, %s, %s) < 0) return %s;" % (
                    Naming.args_cname,
                    Naming.kwds_cname,
                    Naming.kwdlist_cname,
                    len(self.args) - self.entry.signature.num_fixed_args(),
                    star_arg_addr,
                    starstar_arg_addr,
                    self.error_value()))
    
    def generate_argument_conversion_code(self, code):
        # Generate code to convert arguments from
        # signature type to declared type, if needed.
        for arg in self.args:
            if arg.needs_conversion:
                self.generate_arg_conversion(arg, code)

    def generate_arg_conversion(self, arg, code):
        # Generate conversion code for one argument.
        old_type = arg.hdr_type
        new_type = arg.type
        if old_type.is_pyobject:
            self.generate_arg_conversion_from_pyobject(arg, code)
        elif new_type.is_pyobject:
            self.generate_arg_conversion_to_pyobject(arg, code)
        else:
            if new_type.assignable_from(old_type):
                code.putln(
                    "%s = %s;" % (arg.entry.cname, arg.hdr_cname))
            else:
                error(arg.pos,
                    "Cannot convert 1 argument from '%s' to '%s'" %
                        (old_type, new_type))
    
    def generate_arg_conversion_from_pyobject(self, arg, code):
        new_type = arg.type
        func = new_type.from_py_function
        if func:
            code.putln("%s = %s(%s); if (PyErr_Occurred()) %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                code.error_goto(arg.pos)))
        else:
            error(arg.pos, 
                "Cannot convert Python object argument to type '%s'" 
                    % new_type)
    
    def generate_arg_conversion_to_pyobject(self, arg, code):
        old_type = arg.hdr_type
        func = old_type.to_py_function
        if func:
            code.putln("%s = %s(%s); if (!%s) %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                arg.entry.cname,
                code.error_goto(arg.pos)))
        else:
            error(arg.pos,
                "Cannot convert argument of type '%s' to Python object"
                    % old_type)

    def generate_argument_type_tests(self, code):
        # Generate type tests for args whose signature
        # type is PyObject * and whose declared type is
        # a subtype thereof.
        for arg in self.args:
            if arg.needs_type_test:
                self.generate_arg_type_test(arg, code)
    
    def generate_arg_type_test(self, arg, code):
        # Generate type test for one argument.
        if arg.type.typeobj_is_available():
            typeptr_cname = arg.type.typeptr_cname
            arg_code = "((PyObject *)%s)" % arg.entry.cname
            code.putln(
                'if (!__Pyx_ArgTypeTest(%s, %s, %d, "%s")) %s' % (
                    arg_code, 
                    typeptr_cname,
                    not arg.not_none,
                    arg.name,
                    code.error_goto(arg.pos)))
        else:
            error(arg.pos, "Cannot test type of extern C class "
                "without type object name specification")
    
    def generate_execution_code(self, code):
        # Evaluate and store argument default values
        for arg in self.args:
            default = arg.default
            if default:
                default.generate_evaluation_code(code)
                default.make_owned_reference(code)
                code.putln(
                    "%s = %s;" % (
                        arg.default_entry.cname,
                        default.result_as(arg.default_entry.type)))
                if default.is_temp and default.type.is_pyobject:
                    code.putln(
                        "%s = 0;" %
                            default.result_code)
        # For Python class methods, create and store function object
        if self.assmt:
            self.assmt.generate_execution_code(code)
    
    def error_value(self):
        return self.entry.signature.error_value
    
    def caller_will_check_exceptions(self):
        return 1
            

class PyClassDefNode(StatNode, BlockNode):
    #  A Python class definition.
    #
    #  name     string          Name of the class
    #  doc      string or None
    #  body     StatNode        Attribute definition code
    #  entry    Symtab.Entry
    #  scope    PyClassScope
    #
    #  The following subnodes are constructed internally:
    #
    #  dict     DictNode   Class dictionary
    #  classobj ClassNode  Class object
    #  target   NameNode   Variable to assign class object to
    
    def __init__(self, pos, name, bases, doc, body):
        StatNode.__init__(self, pos)
        self.name = name
        self.doc = doc
        self.body = body
        import ExprNodes
        self.dict = ExprNodes.DictNode(pos, key_value_pairs = [])
        if self.doc:
            if Options.embed_pos_in_docstring:
                doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
            doc = doc + '\\n' + self.doc
            doc_node = ExprNodes.StringNode(pos, value = doc)
        else:
            doc_node = None
        self.classobj = ExprNodes.ClassNode(pos,
            name = ExprNodes.StringNode(pos, value = name), 
            bases = bases, dict = self.dict, doc = doc_node)
        self.target = ExprNodes.NameNode(pos, name = name)
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        self.dict.analyse_expressions(env)
        self.classobj.analyse_expressions(env)
        genv = env.global_scope()
        cenv = PyClassScope(name = self.name, outer_scope = genv)
        cenv.class_dict_cname = self.dict.result_code
        cenv.class_obj_cname = self.classobj.result_code
        self.scope = cenv
        self.body.analyse_declarations(cenv)
        self.body.analyse_expressions(cenv)
        self.target.analyse_target_expression(env)
        self.dict.release_temp(env)
        self.classobj.release_temp(env)
        self.target.release_target_temp(env)
        #env.recycle_pending_temps()
    
    def generate_function_definitions(self, env, code):
        self.generate_py_string_decls(self.scope, code)
        self.body.generate_function_definitions(
            self.scope, code)
    
    def generate_execution_code(self, code):
        self.dict.generate_evaluation_code(code)
        self.classobj.generate_evaluation_code(code)
        self.body.generate_execution_code(code)
        self.target.generate_assignment_code(self.classobj, code)
        self.dict.generate_disposal_code(code)


class CClassDefNode(StatNode):
    #  An extension type definition.
    #
    #  visibility         'private' or 'public' or 'extern'
    #  typedef_flag       boolean
    #  module_name        string or None    For import of extern type objects
    #  class_name         string            Unqualified name of class
    #  as_name            string or None    Name to declare as in this scope
    #  base_class_module  string or None    Module containing the base class
    #  base_class_name    string or None    Name of the base class
    #  objstruct_name     string or None    Specified C name of object struct
    #  typeobj_name       string or None    Specified C name of type object
    #  in_pxd             boolean           Is in a .pxd file
    #  doc                string or None
    #  body               StatNode or None
    #  entry              Symtab.Entry
    #  base_type          PyExtensionType or None
    
    def analyse_declarations(self, env):
        #print "CClassDefNode.analyse_declarations:", self.class_name
        #print "...visibility =", self.visibility
        #print "...module_name =", self.module_name
        if env.in_cinclude and not self.objstruct_name:
            error(self.pos, "Object struct name specification required for "
                "C class defined in 'extern from' block")
        self.base_type = None
        if self.base_class_name:
            if self.base_class_module:
                base_class_scope = env.find_module(self.base_class_module, self.pos)
            else:
                base_class_scope = env
            if base_class_scope:
                base_class_entry = base_class_scope.find(self.base_class_name, self.pos)
                if base_class_entry:
                    if not base_class_entry.is_type:
                        error(self.pos, "'%s' is not a type name" % self.base_class_name)
                    elif not base_class_entry.type.is_extension_type:
                        error(self.pos, "'%s' is not an extension type" % self.base_class_name)
                    elif not base_class_entry.type.is_complete():
                        error(self.pos, "Base class '%s' is incomplete" % self.base_class_name)
                    else:
                        self.base_type = base_class_entry.type
        has_body = self.body is not None
        self.entry = env.declare_c_class(
            name = self.class_name, 
            pos = self.pos,
            defining = has_body and self.in_pxd,
            implementing = has_body and not self.in_pxd,
            module_name = self.module_name,
            base_type = self.base_type,
            objstruct_cname = self.objstruct_name,
            typeobj_cname = self.typeobj_name,
            visibility = self.visibility,
            typedef_flag = self.typedef_flag)
        scope = self.entry.type.scope
        
        if self.doc:
            if Options.embed_pos_in_docstring:
                scope.doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
                scope.doc = scope.doc + '\\n' + self.doc
            else:
                scope.doc = self.doc
            
        if has_body:
            self.body.analyse_declarations(scope)
            if self.in_pxd:
                scope.defined = 1
            else:
                scope.implemented = 1
        env.allocate_vtable_names(self.entry)
        
    def analyse_expressions(self, env):
        if self.body:
            self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        if self.body:
            self.body.generate_function_definitions(
                self.entry.type.scope, code)
    
    def generate_execution_code(self, code):
        # This is needed to generate evaluation code for
        # default values of method arguments.
        if self.body:
            self.body.generate_execution_code(code)


class PropertyNode(StatNode):
    #  Definition of a property in an extension type.
    #
    #  name   string
    #  doc    string or None    Doc string
    #  body   StatListNode
    
    def analyse_declarations(self, env):
        entry = env.declare_property(self.name, self.doc, self.pos)
        if entry:
            if self.doc:
                doc_entry = env.get_string_const(self.doc)
                entry.doc_cname = doc_entry.cname
            self.body.analyse_declarations(entry.scope)
        
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)

    def generate_execution_code(self, code):
        pass


class GlobalNode(StatNode):
    # Global variable declaration.
    #
    # names    [string]
    
    def analyse_declarations(self, env):
        for name in self.names:
            env.declare_global(name, self.pos)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class ExprStatNode(StatNode):
    #  Expression used as a statement.
    #
    #  expr   ExprNode
    
    def analyse_expressions(self, env):
        self.expr.analyse_expressions(env)
        self.expr.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
    
    def generate_execution_code(self, code):
        self.expr.generate_evaluation_code(code)
        if not self.expr.is_temp and self.expr.result_code:
            code.putln("%s;" % self.expr.result_code)
        self.expr.generate_disposal_code(code)


class AssignmentNode(StatNode):
    #  Abstract base class for assignment nodes.
    #
    #  The analyse_expressions and generate_execution_code
    #  phases of assignments are split into two sub-phases
    #  each, to enable all the right hand sides of a
    #  parallel assignment to be evaluated before assigning
    #  to any of the left hand sides.

    def analyse_expressions(self, env):
        self.analyse_expressions_1(env)
        self.analyse_expressions_2(env)

    def generate_execution_code(self, code):
        self.generate_rhs_evaluation_code(code)
        self.generate_assignment_code(code)


class SingleAssignmentNode(AssignmentNode):
    #  The simplest case:
    #
    #    a = b
    #
    #  lhs      ExprNode      Left hand side
    #  rhs      ExprNode      Right hand side

    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)
    
    def analyse_expressions_1(self, env, use_temp = 0):
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
        self.rhs = self.rhs.coerce_to(self.lhs.type, env)
        if use_temp:
            self.rhs = self.rhs.coerce_to_temp(env)
        self.rhs.allocate_temps(env)
    
    def analyse_expressions_2(self, env):
        self.lhs.allocate_target_temps(env)
        self.lhs.release_target_temp(env)
        self.rhs.release_temp(env)		

    def generate_rhs_evaluation_code(self, code):
        self.rhs.generate_evaluation_code(code)
    
    def generate_assignment_code(self, code):
        self.lhs.generate_assignment_code(self.rhs, code)


class CascadedAssignmentNode(AssignmentNode):
    #  An assignment with multiple left hand sides:
    #
    #    a = b = c
    #
    #  lhs_list   [ExprNode]   Left hand sides
    #  rhs        ExprNode     Right hand sides
    #
    #  Used internally:
    #
    #  coerced_rhs_list   [ExprNode]   RHS coerced to type of each LHS
    
    def analyse_declarations(self, env):
        for lhs in self.lhs_list:
            lhs.analyse_target_declaration(env)
    
#	def analyse_expressions(self, env):
#		import ExprNodes
#		self.rhs.analyse_types(env)
#		self.rhs = self.rhs.coerce_to_temp(env)
#		self.rhs.allocate_temps(env)
#		self.coerced_rhs_list = []
#		for lhs in self.lhs_list:
#			lhs.analyse_target_types(env)
#			coerced_rhs = ExprNodes.CloneNode(self.rhs).coerce_to(lhs.type, env)
#			self.coerced_rhs_list.append(coerced_rhs)
#			coerced_rhs.allocate_temps(env)
#			lhs.allocate_target_temps(env)
#			coerced_rhs.release_temp(env)
#			lhs.release_target_temp(env)
#		self.rhs.release_temp(env)

    def analyse_expressions_1(self, env, use_temp = 0):
        self.rhs.analyse_types(env)
        if use_temp:
            self.rhs = self.rhs.coerce_to_temp(env)
        else:
            self.rhs = self.rhs.coerce_to_simple(env)
        self.rhs.allocate_temps(env)
    
    def analyse_expressions_2(self, env):
        from ExprNodes import CloneNode
        self.coerced_rhs_list = []
        for lhs in self.lhs_list:
            lhs.analyse_target_types(env)
            rhs = CloneNode(self.rhs)
            rhs = rhs.coerce_to(lhs.type, env)
            self.coerced_rhs_list.append(rhs)
            rhs.allocate_temps(env)
            lhs.allocate_target_temps(env)
            lhs.release_target_temp(env)
            rhs.release_temp(env)
        self.rhs.release_temp(env)
            
#	def generate_execution_code(self, code):
#		self.rhs.generate_evaluation_code(code)
#		for i in range(len(self.lhs_list)):
#			lhs = self.lhs_list[i]
#			rhs = self.coerced_rhs_list[i]
#			rhs.generate_evaluation_code(code)
#			lhs.generate_assignment_code(rhs, code)
#			# Assignment has already disposed of the cloned RHS
#		self.rhs.generate_disposal_code(code)
    
    def generate_rhs_evaluation_code(self, code):
        self.rhs.generate_evaluation_code(code)
    
    def generate_assignment_code(self, code):
        for i in range(len(self.lhs_list)):
            lhs = self.lhs_list[i]
            rhs = self.coerced_rhs_list[i]
            rhs.generate_evaluation_code(code)
            lhs.generate_assignment_code(rhs, code)
            # Assignment has disposed of the cloned RHS
        self.rhs.generate_disposal_code(code)

class ParallelAssignmentNode(AssignmentNode):
    #  A combined packing/unpacking assignment:
    #
    #    a, b, c =  d, e, f
    #
    #  This has been rearranged by the parser into
    #
    #    a = d ; b = e ; c = f
    #
    #  but we must evaluate all the right hand sides
    #  before assigning to any of the left hand sides.
    #
    #  stats     [AssignmentNode]   The constituent assignments
    
    def analyse_declarations(self, env):
        for stat in self.stats:
            stat.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        for stat in self.stats:
            stat.analyse_expressions_1(env, use_temp = 1)
        for stat in self.stats:
            stat.analyse_expressions_2(env)
    
    def generate_execution_code(self, code):
        for stat in self.stats:
            stat.generate_rhs_evaluation_code(code)
        for stat in self.stats:
            stat.generate_assignment_code(code)

class InPlaceAssignmentNode(AssignmentNode):
    #  An in place arithmatic operand:
    #
    #    a += b
    #    a -= b
    #    ...
    #
    #  lhs      ExprNode      Left hand side
    #  rhs      ExprNode      Right hand side
    #  op       char          one of "+-*/%^&|"
    #  dup     (ExprNode)     copy of lhs used for operation (auto-generated)
    #
    #  This code is a bit tricky because in order to obey Python 
    #  semantics the sub-expressions (e.g. indices) of the lhs must 
    #  not be evaluated twice. So we must re-use the values calculated 
    #  in evaluation phase for the assignment phase as well. 
    #  Fortunately, the type of the lhs node is fairly constrained 
    #  (it must be a NameNode, AttributeNode, or IndexNode).     
    
    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)
    
    def analyse_expressions_1(self, env, use_temp = 0):
        import ExprNodes
        self.create_dup_node(env) # re-assigns lhs to a shallow copy
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
        if self.lhs.type.is_pyobject or self.rhs.type.is_pyobject:
            self.rhs = self.rhs.coerce_to(self.lhs.type, env)
        if self.lhs.type.is_pyobject:
             self.result = ExprNodes.PyTempNode(self.pos, env)
             self.result.allocate_temps(env)
        if use_temp:
            self.rhs = self.rhs.coerce_to_temp(env)
        self.rhs.allocate_temps(env)
        self.dup.allocate_subexpr_temps(env)
        self.dup.allocate_temp(env)
    
    def analyse_expressions_2(self, env):
        self.lhs.allocate_target_temps(env)
        self.lhs.release_target_temp(env)
        self.dup.release_temp(env)
        if self.dup.is_temp:
            self.dup.release_subexpr_temps(env)
        self.rhs.release_temp(env)
        if self.lhs.type.is_pyobject:
            self.result.release_temp(env)

    def generate_execution_code(self, code):
        self.rhs.generate_evaluation_code(code)
        self.dup.generate_subexpr_evaluation_code(code)
        self.dup.generate_result_code(code)
        if self.lhs.type.is_pyobject:
            code.putln(
                "%s = %s(%s, %s); if (!%s) %s" % (
                    self.result.result_code, 
                    self.py_operation_function(), 
                    self.dup.py_result(),
                    self.rhs.py_result(),
                    self.result.py_result(),
                    code.error_goto(self.pos)))
            self.rhs.generate_disposal_code(code)
            self.dup.generate_disposal_code(code)
            self.lhs.generate_assignment_code(self.result, code)
        else: 
            # have to do assignment directly to avoid side-effects
            code.putln("%s %s= %s;" % (self.lhs.result_code, self.operator, self.rhs.result_code) )
            self.rhs.generate_disposal_code(code)
        if self.dup.is_temp:
            self.dup.generate_subexpr_disposal_code(code)
            
    def create_dup_node(self, env): 
        import ExprNodes
        self.dup = self.lhs
        self.dup.analyse_types(env)
        if isinstance(self.lhs, ExprNodes.NameNode):
            target_lhs = ExprNodes.NameNode(self.dup.pos, name = self.dup.name, is_temp = self.dup.is_temp, entry = self.dup.entry)
        elif isinstance(self.lhs, ExprNodes.AttributeNode):
            target_lhs = ExprNodes.AttributeNode(self.dup.pos, obj = ExprNodes.CloneNode(self.lhs.obj), attribute = self.dup.attribute, is_temp = self.dup.is_temp)
        elif isinstance(self.lhs, ExprNodes.IndexNode):
            target_lhs = ExprNodes.IndexNode(self.dup.pos, base = ExprNodes.CloneNode(self.dup.base), index = ExprNodes.CloneNode(self.lhs.index), is_temp = self.dup.is_temp)
        self.lhs = target_lhs
    
    def py_operation_function(self):
        return self.py_functions[self.operator]

    py_functions = {
        "|":		"PyNumber_InPlaceOr",
        "^":		"PyNumber_InPlaceXor",
        "&":		"PyNumber_InPlaceAnd",
        "+":		"PyNumber_InPlaceAdd",
        "-":		"PyNumber_InPlaceSubtract",
        "*":		"PyNumber_InPlaceMultiply",
        "/":		"PyNumber_InPlaceDivide",
        "%":		"PyNumber_InPlaceRemainder",
    }


class PrintStatNode(StatNode):
    #  print statement
    #
    #  args              [ExprNode]
    #  ends_with_comma   boolean
    
    def analyse_expressions(self, env):
        for i in range(len(self.args)):
            arg = self.args[i]
            arg.analyse_types(env)
            arg = arg.coerce_to_pyobject(env)
            arg.allocate_temps(env)
            arg.release_temp(env)
            self.args[i] = arg
            #env.recycle_pending_temps() # TEMPORARY
        env.use_utility_code(printing_utility_code)
    
    def generate_execution_code(self, code):
        for arg in self.args:
            arg.generate_evaluation_code(code)
            code.putln(
                "if (__Pyx_PrintItem(%s) < 0) %s" % (
                    arg.py_result(),
                    code.error_goto(self.pos)))
            arg.generate_disposal_code(code)
        if not self.ends_with_comma:
            code.putln(
                "if (__Pyx_PrintNewline() < 0) %s" %
                    code.error_goto(self.pos))


class DelStatNode(StatNode):
    #  del statement
    #
    #  args     [ExprNode]
    
    def analyse_declarations(self, env):
        for arg in self.args:
            arg.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        for arg in self.args:
            arg.analyse_target_expression(env)
            if not arg.type.is_pyobject:
                error(arg.pos, "Deletion of non-Python object")
            #env.recycle_pending_temps() # TEMPORARY
    
    def generate_execution_code(self, code):
        for arg in self.args:
            if arg.type.is_pyobject:
                arg.generate_deletion_code(code)
            # else error reported earlier


class PassStatNode(StatNode):
    #  pass statement
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class BreakStatNode(StatNode):

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        if not code.break_label:
            error(self.pos, "break statement not inside loop")
        else:
            code.putln(
                "goto %s;" %
                    code.break_label)


class ContinueStatNode(StatNode):

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        if code.in_try_finally:
            error(self.pos, "continue statement inside try of try...finally")
        elif not code.continue_label:
            error(self.pos, "continue statement not inside loop")
        else:
            code.putln(
                "goto %s;" %
                    code.continue_label)


class ReturnStatNode(StatNode):
    #  return statement
    #
    #  value         ExprNode or None
    #  return_type   PyrexType
    #  temps_in_use  [Entry]            Temps in use at time of return
    
    def analyse_expressions(self, env):
        return_type = env.return_type
        self.return_type = return_type
        self.temps_in_use = env.temps_in_use()
        if not return_type:
            error(self.pos, "Return not inside a function body")
            return
        if self.value:
            self.value.analyse_types(env)
            if return_type.is_void or return_type.is_returncode:
                error(self.value.pos, 
                    "Return with value in void function")
            else:
                self.value = self.value.coerce_to(env.return_type, env)
            self.value.allocate_temps(env)
            self.value.release_temp(env)
        else:
            if (not return_type.is_void
                and not return_type.is_pyobject
                and not return_type.is_returncode):
                    error(self.pos, "Return value required")
    
    def generate_execution_code(self, code):
        if not self.return_type:
            # error reported earlier
            return
        if self.value:
            self.value.generate_evaluation_code(code)
            self.value.make_owned_reference(code)
            code.putln(
                "%s = %s;" % (
                    Naming.retval_cname,
                    self.value.result_as(self.return_type)))
            self.value.generate_post_assignment_code(code)
        else:
            if self.return_type.is_pyobject:
                code.put_init_to_py_none(Naming.retval_cname, self.return_type)
            elif self.return_type.is_returncode:
                code.putln(
                    "%s = %s;" % (
                        Naming.retval_cname,
                        self.return_type.default_value))
        for entry in self.temps_in_use:
            code.put_var_decref_clear(entry)
        code.putln(
            "goto %s;" %
                code.return_label)


class RaiseStatNode(StatNode):
    #  raise statement
    #
    #  exc_type    ExprNode or None
    #  exc_value   ExprNode or None
    #  exc_tb      ExprNode or None
    
    def analyse_expressions(self, env):
        if self.exc_type:
            self.exc_type.analyse_types(env)
            self.exc_type = self.exc_type.coerce_to_pyobject(env)
            self.exc_type.allocate_temps(env)
        if self.exc_value:
            self.exc_value.analyse_types(env)
            self.exc_value = self.exc_value.coerce_to_pyobject(env)
            self.exc_value.allocate_temps(env)
        if self.exc_tb:
            self.exc_tb.analyse_types(env)
            self.exc_tb = self.exc_tb.coerce_to_pyobject(env)
            self.exc_tb.allocate_temps(env)
        if self.exc_type:
            self.exc_type.release_temp(env)
        if self.exc_value:
            self.exc_value.release_temp(env)
        if self.exc_tb:
            self.exc_tb.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        if not (self.exc_type or self.exc_value or self.exc_tb):
            env.use_utility_code(reraise_utility_code)
        else:
            env.use_utility_code(raise_utility_code)
    
    def generate_execution_code(self, code):
        if self.exc_type:
            self.exc_type.generate_evaluation_code(code)
            type_code = self.exc_type.py_result()
        else:
            type_code = 0
        if self.exc_value:
            self.exc_value.generate_evaluation_code(code)
            value_code = self.exc_value.py_result()
        else:
            value_code = "0"
        if self.exc_tb:
            self.exc_tb.generate_evaluation_code(code)
            tb_code = self.exc_tb.py_result()
        else:
            tb_code = "0"
        if self.exc_type or self.exc_value or self.exc_tb:
            code.putln(
                "__Pyx_Raise(%s, %s, %s);" % (
                    type_code,
                    value_code,
                    tb_code))
        else:
            code.putln(
                "__Pyx_ReRaise();")
        if self.exc_type:
            self.exc_type.generate_disposal_code(code)
        if self.exc_value:
            self.exc_value.generate_disposal_code(code)
        if self.exc_tb:
            self.exc_tb.generate_disposal_code(code)
        code.putln(
            code.error_goto(self.pos))


class AssertStatNode(StatNode):
    #  assert statement
    #
    #  cond    ExprNode
    #  value   ExprNode or None
    
    def analyse_expressions(self, env):
        self.cond = self.cond.analyse_boolean_expression(env)
        if self.value:
            self.value.analyse_types(env)
            self.value = self.value.coerce_to_pyobject(env)
            self.value.allocate_temps(env)
        self.cond.release_temp(env)
        if self.value:
            self.value.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
    
    def generate_execution_code(self, code):
        self.cond.generate_evaluation_code(code)
        if self.value:
            self.value.generate_evaluation_code(code)
        code.putln(
            "if (!%s) {" %
                self.cond.result_code)
        if self.value:
            code.putln(
                "PyErr_SetObject(PyExc_AssertionError, %s);" %
                    self.value.py_result())
        else:
            code.putln(
                "PyErr_SetNone(PyExc_AssertionError);")
        code.putln(
                code.error_goto(self.pos))
        code.putln(
            "}")
        self.cond.generate_disposal_code(code)
        if self.value:
            self.value.generate_disposal_code(code)


class IfStatNode(StatNode):
    #  if statement
    #
    #  if_clauses   [IfClauseNode]
    #  else_clause  StatNode or None
    
    def analyse_declarations(self, env):
        for if_clause in self.if_clauses:
            if_clause.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        for if_clause in self.if_clauses:
            if_clause.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        end_label = code.new_label()
        for if_clause in self.if_clauses:
            if_clause.generate_execution_code(code, end_label)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(end_label)


class IfClauseNode(Node):
    #  if or elif clause in an if statement
    #
    #  condition   ExprNode
    #  body        StatNode
    
    def analyse_declarations(self, env):
        self.condition.analyse_declarations(env)
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.condition.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
    
    def generate_execution_code(self, code, end_label):
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (%s) {" %
                self.condition.result_code)
        self.body.generate_execution_code(code)
        code.putln(
            "goto %s;" %
                end_label)
        code.putln("}")
        
    
class WhileStatNode(StatNode):
    #  while statement
    #
    #  condition    ExprNode
    #  body         StatNode
    #  else_clause  StatNode
    
    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.condition.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        code.putln(
            "while (1) {")
        code.put_label(code.continue_label)
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (!%s) break;" %
                self.condition.result_code)
        self.body.generate_execution_code(code)
        code.putln("}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)


def ForStatNode(pos, **kw):
    if kw.has_key('iterator'):
        return ForInStatNode(pos, **kw)
    else:
        return ForFromStatNode(pos, **kw)

class ForInStatNode(StatNode):
    #  for statement
    #
    #  target        ExprNode
    #  iterator      IteratorNode
    #  body          StatNode
    #  else_clause   StatNode
    #  item          NextNode       used internally
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.iterator.analyse_expressions(env)
        self.target.analyse_target_types(env)
        self.item = ExprNodes.NextNode(self.iterator, env)
        self.item = self.item.coerce_to(self.target.type, env)
        self.item.allocate_temps(env)
        self.target.allocate_target_temps(env)
        self.item.release_temp(env)
        self.target.release_target_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
        #env.recycle_pending_temps() # TEMPORARY
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
        self.iterator.release_temp(env)

    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.iterator.generate_evaluation_code(code)
        code.putln(
            "for (;;) {")
        code.put_label(code.continue_label)
        self.item.generate_evaluation_code(code)
        self.target.generate_assignment_code(self.item, code)
        self.body.generate_execution_code(code)
        code.putln(
            "}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)
        self.iterator.generate_disposal_code(code)


class ForFromStatNode(StatNode):
    #  for name from expr rel name rel expr
    #
    #  target        NameNode
    #  bound1        ExprNode
    #  relation1     string
    #  relation2     string
    #  bound2        ExprNode
    #  step          ExprNode or None
    #  body          StatNode
    #  else_clause   StatNode or None
    #
    #  Used internally:
    #
    #  loopvar_name       string
    #  py_loopvar_node    PyTempNode or None
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)

    def analyse_expressions(self, env):
        import ExprNodes
        self.target.analyse_target_types(env)
        self.bound1.analyse_types(env)
        self.bound2.analyse_types(env)
        self.bound1 = self.bound1.coerce_to_integer(env)
        self.bound2 = self.bound2.coerce_to_integer(env)
        if self.step is not None:
            if isinstance(self.step, ExprNodes.UnaryMinusNode):
                warning(self.step.pos, "Probable infinite loop in for-from-by statment. Consider switching the directions of the relations.", 2)
            self.step.analyse_types(env)
            self.step = self.step.coerce_to_integer(env)
        if not (self.bound2.is_name or self.bound2.is_literal):
            self.bound2 = self.bound2.coerce_to_temp(env)
        target_type = self.target.type
        if not (target_type.is_pyobject
            or target_type.assignable_from(PyrexTypes.c_int_type)):
                error(self.target.pos,
                    "Cannot assign integer to variable of type '%s'" % target_type)
        if target_type.is_int:
            self.loopvar_name = self.target.entry.cname
            self.py_loopvar_node = None
        else:
            c_loopvar_node = ExprNodes.TempNode(self.pos, 
                PyrexTypes.c_long_type, env)
            c_loopvar_node.allocate_temps(env)
            self.loopvar_name = c_loopvar_node.result_code
            self.py_loopvar_node = \
                ExprNodes.CloneNode(c_loopvar_node).coerce_to_pyobject(env)
        self.bound1.allocate_temps(env)
        self.bound2.allocate_temps(env)
        if self.step is not None:
            self.step.allocate_temps(env)
        if self.py_loopvar_node:
            self.py_loopvar_node.allocate_temps(env)
        self.target.allocate_target_temps(env)
        self.target.release_target_temp(env)
        if self.py_loopvar_node:
            self.py_loopvar_node.release_temp(env)
        self.body.analyse_expressions(env)
        if self.py_loopvar_node:
            c_loopvar_node.release_temp(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
        self.bound1.release_temp(env)
        self.bound2.release_temp(env)
        if self.step is not None:
            self.step.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
            
    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.bound1.generate_evaluation_code(code)
        self.bound2.generate_evaluation_code(code)
        offset, incop = self.relation_table[self.relation1]
        if self.step is not None:
            self.step.generate_evaluation_code(code)
            incop = "%s=%s" % (incop[0], self.step.result_code)
        code.putln(
            "for (%s = %s%s; %s %s %s; %s%s) {" % (
                self.loopvar_name,
                self.bound1.result_code, offset,
                self.loopvar_name, self.relation2, self.bound2.result_code,
                self.loopvar_name, incop))
        if self.py_loopvar_node:
            self.py_loopvar_node.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.py_loopvar_node, code)
        self.body.generate_execution_code(code)
        code.put_label(code.continue_label)
        code.putln("}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)
        self.bound1.generate_disposal_code(code)
        self.bound2.generate_disposal_code(code)
        if self.step is not None:
            self.step.generate_disposal_code(code)
    
    relation_table = {
        # {relop : (initial offset, increment op)}
        '<=': ("",   "++"),
        '<' : ("+1", "++"),
        '>=': ("",   "--"),
        '>' : ("-1", "--")
    }


class TryExceptStatNode(StatNode):
    #  try .. except statement
    #
    #  body             StatNode
    #  except_clauses   [ExceptClauseNode]
    #  else_clause      StatNode or None
    #  cleanup_list     [Entry]            temps to clean up on error
    
    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        for except_clause in self.except_clauses:
            except_clause.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        for except_clause in self.except_clauses:
            except_clause.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        end_label = code.new_label()
        code.putln(
            "/*try:*/ {")
        self.body.generate_execution_code(code)
        code.putln(
            "}")
        code.error_label = old_error_label
        if self.else_clause:
            code.putln(
                "/*else:*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln(
                "}")
        code.putln(
            "goto %s;" %
                end_label)
        code.put_label(our_error_label)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        default_clause_seen = 0
        for except_clause in self.except_clauses:
            if not except_clause.pattern:
                default_clause_seen = 1
            else:
                if default_clause_seen:
                    error(except_clause.pos, "Default except clause not last")
            except_clause.generate_handling_code(code, end_label)
        if not default_clause_seen:
            code.putln(
                "goto %s;" %
                    code.error_label)
        code.put_label(end_label)


class ExceptClauseNode(Node):
    #  Part of try ... except statement.
    #
    #  pattern        ExprNode
    #  target         ExprNode or None
    #  body           StatNode
    #  match_flag     string             result of exception match
    #  exc_value      ExcValueNode       used internally
    #  function_name  string             qualified name of enclosing function
    
    def analyse_declarations(self, env):
        if self.target:
            self.target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        genv = env.global_scope()
        self.function_name = env.qualified_name
        if self.pattern:
            self.pattern.analyse_expressions(env)
            self.pattern = self.pattern.coerce_to_pyobject(env)
            self.match_flag = env.allocate_temp(PyrexTypes.c_int_type)
            self.pattern.release_temp(env)
            env.release_temp(self.match_flag)
        self.exc_value = ExprNodes.ExcValueNode(self.pos, env)
        self.exc_value.allocate_temps(env)
        if self.target:
            self.target.analyse_target_expression(env)
        self.exc_value.release_temp(env)
        if self.target:
            self.target.release_target_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
    
    def generate_handling_code(self, code, end_label):
        code.mark_pos(self.pos)
        if self.pattern:
            self.pattern.generate_evaluation_code(code)
            code.putln(
                "%s = PyErr_ExceptionMatches(%s);" % (
                    self.match_flag,
                    self.pattern.py_result()))
            self.pattern.generate_disposal_code(code)
            code.putln(
                "if (%s) {" %
                    self.match_flag)
        else:
            code.putln(
                "/*except:*/ {")
        code.putln(
            '__Pyx_AddTraceback("%s");' % (self.function_name))
        # We always have to fetch the exception value even if
        # there is no target, because this also normalises the 
        # exception and stores it in the thread state.
        self.exc_value.generate_evaluation_code(code)
        if self.target:
            self.target.generate_assignment_code(self.exc_value, code)
        else:
            self.exc_value.generate_disposal_code(code)
        self.body.generate_execution_code(code)
        code.putln(
            "goto %s;"
                % end_label)
        code.putln(
            "}")


class TryFinallyStatNode(StatNode):
    #  try ... finally statement
    #
    #  body             StatNode
    #  finally_clause   StatNode
    #  cleanup_list     [Entry]      temps to clean up on error
    #  exc_vars         3*(string,)  temps to hold saved exception
    #
    #  The plan is that we funnel all continue, break
    #  return and error gotos into the beginning of the
    #  finally block, setting a variable to remember which
    #  one we're doing. At the end of the finally block, we
    #  switch on the variable to figure out where to go.
    #  In addition, if we're doing an error, we save the
    #  exception on entry to the finally block and restore
    #  it on exit.
    
    disallow_continue_in_try_finally = 0
    # There doesn't seem to be any point in disallowing
    # continue in the try block, since we have no problem
    # handling it.
    
    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        self.finally_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        self.exc_vars = (
            env.allocate_temp(PyrexTypes.py_object_type),
            env.allocate_temp(PyrexTypes.py_object_type),
            env.allocate_temp(PyrexTypes.py_object_type))
        self.lineno_var = \
            env.allocate_temp(PyrexTypes.c_int_type)
        self.finally_clause.analyse_expressions(env)
        for var in self.exc_vars:
            env.release_temp(var)
    
    def generate_execution_code(self, code):
        old_error_label = code.error_label
        old_labels = code.all_new_labels()
        new_labels = code.get_all_labels()
        new_error_label = code.error_label
        catch_label = code.new_label()
        code.putln(
            "/*try:*/ {")
        if self.disallow_continue_in_try_finally:
            was_in_try_finally = code.in_try_finally
            code.in_try_finally = 1
        self.body.generate_execution_code(code)
        if self.disallow_continue_in_try_finally:
            code.in_try_finally = was_in_try_finally
        code.putln(
            "}")
        code.putln(
            "/*finally:*/ {")
        code.putln(
                "int __pyx_why;")
        #code.putln(
        #		"PyObject *%s, *%s, *%s;" %
        #			self.exc_vars)
        #code.putln(
        #		"int %s;" %
        #			self.lineno_var)
        code.putln(
                "__pyx_why = 0; goto %s;" %
                    catch_label)
        for i in range(len(new_labels)):
            if new_labels[i] and new_labels[i] <> "<try>":
                if new_labels[i] == new_error_label:
                    self.put_error_catcher(code, 
                        new_error_label, i+1, catch_label)
                else:
                    code.putln(
                        "%s: __pyx_why = %s; goto %s;" % (
                            new_labels[i],
                            i+1,
                            catch_label))
        code.put_label(catch_label)
        code.set_all_labels(old_labels)
        self.finally_clause.generate_execution_code(code)
        code.putln(
                "switch (__pyx_why) {")
        for i in range(len(old_labels)):
            if old_labels[i]:
                if old_labels[i] == old_error_label:
                    self.put_error_uncatcher(code, i+1, old_error_label)
                else:
                    code.putln(
                        "case %s: goto %s;" % (
                            i+1,
                            old_labels[i]))
        code.putln(
                "}")		
        code.putln(
            "}")

    def put_error_catcher(self, code, error_label, i, catch_label):
        code.putln(
            "%s: {" %
                error_label)
        code.putln(
                "__pyx_why = %s;" %
                    i)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        code.putln(
                "PyErr_Fetch(&%s, &%s, &%s);" %
                    self.exc_vars)
        code.putln(
                "%s = %s;" % (
                    self.lineno_var, Naming.lineno_cname))
        code.putln(
                "goto %s;" %
                    catch_label)
        code.putln(
            "}")
            
    def put_error_uncatcher(self, code, i, error_label):
        code.putln(
            "case %s: {" %
                i)
        code.putln(
                "PyErr_Restore(%s, %s, %s);" %
                    self.exc_vars)
        code.putln(
                "%s = %s;" % (
                    Naming.lineno_cname, self.lineno_var))
        for var in self.exc_vars:
            code.putln(
                "%s = 0;" %
                    var)
        code.putln(
                "goto %s;" %
                    error_label)
        code.putln(
            "}")


class CImportStatNode(StatNode):
    #  cimport statement
    #
    #  module_name   string           Qualified name of module being imported
    #  as_name       string or None   Name specified in "as" clause, if any
    
    def analyse_declarations(self, env):
        module_scope = env.find_module(self.module_name, self.pos)
        if "." in self.module_name:
            names = self.module_name.split(".")
            top_name = names[0]
            top_module_scope = env.context.find_submodule(top_name)
            module_scope = top_module_scope
            for name in names[1:]:
                submodule_scope = module_scope.find_submodule(name)
                module_scope.declare_module(name, submodule_scope, self.pos)
                module_scope = submodule_scope
            if self.as_name:
                env.declare_module(self.as_name, module_scope, self.pos)
            else:
                env.declare_module(top_name, top_module_scope, self.pos)
        else:
            name = self.as_name or self.module_name
            env.declare_module(name, module_scope, self.pos)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass
    

class FromCImportStatNode(StatNode):
    #  from ... cimport statement
    #
    #  module_name     string                  Qualified name of module
    #  imported_names  [(pos, name, as_name)]  Names to be imported
    
    def analyse_declarations(self, env):
        module_scope = env.find_module(self.module_name, self.pos)
        env.add_imported_module(module_scope)
        for pos, name, as_name in self.imported_names:
            entry = module_scope.find(name, pos)
            if entry:
                local_name = as_name or name
                env.add_imported_entry(local_name, entry, pos)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class FromImportStatNode(StatNode):
    #  from ... import statement
    #
    #  module           ImportNode
    #  items            [(string, NameNode)]
    #  interned_items   [(string, NameNode)]
    #  item             PyTempNode            used internally
    
    def analyse_declarations(self, env):
        for _, target in self.items:
            target.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.module.analyse_expressions(env)
        self.item = ExprNodes.PyTempNode(self.pos, env)
        self.item.allocate_temp(env)
        self.interned_items = []
        for name, target in self.items:
            if Options.intern_names:
                self.interned_items.append((env.intern(name), target))
            target.analyse_target_expression(env)
            target.release_temp(env)
        self.module.release_temp(env)
        self.item.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
    
    def generate_execution_code(self, code):
        self.module.generate_evaluation_code(code)
        if Options.intern_names:
            for cname, target in self.interned_items:
                code.putln(
                    '%s = PyObject_GetAttr(%s, %s); if (!%s) %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        cname,
                        self.item.result_code,
                        code.error_goto(self.pos)))
                target.generate_assignment_code(self.item, code)
        else:
            for name, target in self.items:
                code.putln(
                    '%s = PyObject_GetAttrString(%s, "%s"); if (!%s) %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        name,
                        self.item.result_code,
                        code.error_goto(self.pos)))
                target.generate_assignment_code(self.item, code)
        self.module.generate_disposal_code(code)

#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

utility_function_predeclarations = \
"""
typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/
static PyObject *__Pyx_UnpackItem(PyObject *, Py_ssize_t); /*proto*/
static int __Pyx_EndUnpack(PyObject *, Py_ssize_t); /*proto*/
static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static void __Pyx_ReRaise(void); /*proto*/
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
static PyObject *__Pyx_GetExcValue(void); /*proto*/
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
static int __Pyx_GetStarArgs(PyObject **args, PyObject **kwds,\
 char *kwd_list[], Py_ssize_t nargs, PyObject **args2, PyObject **kwds2); /*proto*/
static void __Pyx_WriteUnraisable(char *name); /*proto*/
static void __Pyx_AddTraceback(char *funcname); /*proto*/
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr); /*proto*/
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, char *modname); /*proto*/
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/
"""

get_name_predeclaration = \
"static PyObject *__Pyx_GetName(PyObject *dict, char *name); /*proto*/"

get_name_interned_predeclaration = \
"static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/"

#------------------------------------------------------------------------------------

printing_utility_code = \
r"""
static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject("stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_PrintItem(PyObject *v) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_SoftSpace(f, 1)) {
        if (PyFile_WriteString(" ", f) < 0)
            return -1;
    }
    if (PyFile_WriteObject(v, f, Py_PRINT_RAW) < 0)
        return -1;
    if (PyString_Check(v)) {
        char *s = PyString_AsString(v);
        Py_ssize_t len = PyString_Size(v);
        if (len > 0 &&
            isspace(Py_CHARMASK(s[len-1])) &&
            s[len-1] != ' ')
                PyFile_SoftSpace(f, 0);
    }
    return 0;
}

static int __Pyx_PrintNewline(void) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_WriteString("\n", f) < 0)
        return -1;
    PyFile_SoftSpace(f, 0);
    return 0;
}
"""

#------------------------------------------------------------------------------------

# The following function is based on do_raise() from ceval.c.

raise_utility_code = \
"""
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    /* First, check the traceback argument, replacing None with NULL. */
    if (tb == Py_None) {
        Py_DECREF(tb);
        tb = 0;
    }
    else if (tb != NULL && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto raise_error;
    }
    /* Next, replace a missing value with None */
    if (value == NULL) {
        value = Py_None;
        Py_INCREF(value);
    }
    /* Next, repeatedly, replace a tuple exception with its first item */
    while (PyTuple_Check(type) && PyTuple_Size(type) > 0) {
        PyObject *tmp = type;
        type = PyTuple_GET_ITEM(type, 0);
        Py_INCREF(type);
        Py_DECREF(tmp);
    }
    if (PyString_Check(type))
        ;
/*    else if (PyClass_Check(type)) */
    else if (PyType_Check(type) || PyClass_Check(type))
        ; /*PyErr_NormalizeException(&type, &value, &tb);*/
    else if (PyInstance_Check(type)) {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
              "instance exception may not have a separate value");
            goto raise_error;
        }
        else {
            /* Normalize to raise <class>, <instance> */
            Py_DECREF(value);
            value = type;
            type = (PyObject*) ((PyInstanceObject*)type)->in_class;
            Py_INCREF(type);
        }
    }
    else {
        /* Not something you can raise.  You get an exception
           anyway, just not what you specified :-) */
        PyErr_Format(PyExc_TypeError,
                 "exceptions must be strings, classes, or "
                 "instances, not %s", type->ob_type->tp_name);
        goto raise_error;
    }
    PyErr_Restore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}
"""

#------------------------------------------------------------------------------------

reraise_utility_code = \
"""
static void __Pyx_ReRaise(void) {
    PyThreadState *tstate = PyThreadState_Get();
    PyObject *type = tstate->exc_type;
    PyObject *value = tstate->exc_value;
    PyObject *tb = tstate->exc_traceback;
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    PyErr_Restore(type, value, tb);
}
"""

#------------------------------------------------------------------------------------

arg_type_test_utility_code = \
"""
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if ((none_allowed && obj == Py_None) || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError,
        "Argument '%s' has incorrect type (expected %s, got %s)",
        name, type->tp_name, obj->ob_type->tp_name);
    return 0;
}
"""

#------------------------------------------------------------------------------------
#
#  __Pyx_GetStarArgs splits the args tuple and kwds dict into two parts
#  each, one part suitable for passing to PyArg_ParseTupleAndKeywords,
#  and the other containing any extra arguments. On success, replaces
#  the borrowed references *args and *kwds with references to a new
#  tuple and dict, and passes back new references in *args2 and *kwds2.
#  Does not touch any of its arguments on failure.
#
#  Any of *kwds, args2 and kwds2 may be 0 (but not args or kwds). If
#  *kwds == 0, it is not changed. If kwds2 == 0 and *kwds != 0, a new
#  reference to the same dictionary is passed back in *kwds.
#

get_starargs_utility_code = \
"""
static int __Pyx_GetStarArgs(
    PyObject **args, 
    PyObject **kwds,
    char *kwd_list[], 
    Py_ssize_t nargs,
    PyObject **args2, 
    PyObject **kwds2)
{
    PyObject *x = 0, *args1 = 0, *kwds1 = 0;
    
    if (args2)
        *args2 = 0;
    if (kwds2)
        *kwds2 = 0;
    
    if (args2) {
        args1 = PyTuple_GetSlice(*args, 0, nargs);
        if (!args1)
            goto bad;
        *args2 = PyTuple_GetSlice(*args, nargs, PyTuple_Size(*args));
        if (!*args2)
            goto bad;
    }
    else {
        args1 = *args;
        Py_INCREF(args1);
    }
    
    if (kwds2) {
        if (*kwds) {
            char **p;
            kwds1 = PyDict_New();
            if (!kwds)
                goto bad;
            *kwds2 = PyDict_Copy(*kwds);
            if (!*kwds2)
                goto bad;
            for (p = kwd_list; *p; p++) {
                x = PyDict_GetItemString(*kwds, *p);
                if (x) {
                    if (PyDict_SetItemString(kwds1, *p, x) < 0)
                        goto bad;
                    if (PyDict_DelItemString(*kwds2, *p) < 0)
                        goto bad;
                }
            }
        }
        else {
            *kwds2 = PyDict_New();
            if (!*kwds2)
                goto bad;
        }
    }
    else {
        kwds1 = *kwds;
        Py_XINCREF(kwds1);
    }
    
    *args = args1;
    *kwds = kwds1;
    return 0;
bad:
    Py_XDECREF(args1);
    Py_XDECREF(kwds1);
    Py_XDECREF(*args2);
    Py_XDECREF(*kwds2);
    return -1;
}
"""

#------------------------------------------------------------------------------------

unraisable_exception_utility_code = \
"""
static void __Pyx_WriteUnraisable(char *name) {
    PyObject *old_exc, *old_val, *old_tb;
    PyObject *ctx;
    PyErr_Fetch(&old_exc, &old_val, &old_tb);
    ctx = PyString_FromString(name);
    PyErr_Restore(old_exc, old_val, old_tb);
    if (!ctx)
        ctx = Py_None;
    PyErr_WriteUnraisable(ctx);
}
"""

#------------------------------------------------------------------------------------

traceback_utility_code = \
"""
#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(%(FILENAME)s);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(%(GLOBALS)s);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        %(LINENO)s,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = %(LINENO)s;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
""" % {
    'FILENAME': Naming.filename_cname,
    'LINENO':  Naming.lineno_cname,
    'GLOBALS': Naming.module_cname
}

#------------------------------------------------------------------------------------

type_import_utility_code = \
"""
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, 
    long size) 
{
    PyObject *py_module_name = 0;
    PyObject *py_class_name = 0;
    PyObject *py_name_list = 0;
    PyObject *py_module = 0;
    PyObject *result = 0;
    
    py_module_name = PyString_FromString(module_name);
    if (!py_module_name)
        goto bad;
    py_class_name = PyString_FromString(class_name);
    if (!py_class_name)
        goto bad;
    py_name_list = PyList_New(1);
    if (!py_name_list)
        goto bad;
    Py_INCREF(py_class_name);
    if (PyList_SetItem(py_name_list, 0, py_class_name) < 0)
        goto bad;
    py_module = __Pyx_Import(py_module_name, py_name_list);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttr(py_module, py_class_name);
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError, 
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError, 
            "%s.%s does not appear to be the correct type object",
            module_name, class_name);
        goto bad;
    }
    goto done;
bad:
    Py_XDECREF(result);
    result = 0;
done:
    Py_XDECREF(py_module_name);
    Py_XDECREF(py_class_name);
    Py_XDECREF(py_name_list);
    return (PyTypeObject *)result;
}
"""

#------------------------------------------------------------------------------------

set_vtable_utility_code = \
"""
static int __Pyx_SetVtable(PyObject *dict, void *vtable) {
    PyObject *pycobj = 0;
    int result;
    
    pycobj = PyCObject_FromVoidPtr(vtable, 0);
    if (!pycobj)
        goto bad;
    if (PyDict_SetItemString(dict, "__pyx_vtable__", pycobj) < 0)
        goto bad;
    result = 0;
    goto done;

bad:
    result = -1;
done:
    Py_XDECREF(pycobj);
    return result;
}
"""

#------------------------------------------------------------------------------------

get_vtable_utility_code = \
r"""
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr) {
    int result;
    PyObject *pycobj;
    
    pycobj = PyMapping_GetItemString(dict, "__pyx_vtable__");
    if (!pycobj)
        goto bad;
    *(void **)vtabptr = PyCObject_AsVoidPtr(pycobj);
    if (!*(void **)vtabptr)
        goto bad;
    result = 0;
    goto done;

bad:
    result = -1;
done:
    Py_XDECREF(pycobj);
    return result;
}
"""

#------------------------------------------------------------------------------------

init_intern_tab_utility_code = \
"""
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
""";

#------------------------------------------------------------------------------------

init_string_tab_utility_code = \
"""
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
""";

#------------------------------------------------------------------------------------
