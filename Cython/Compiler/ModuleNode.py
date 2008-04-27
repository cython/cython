#
#   Pyrex - Module parse tree node
#

import os, time
from cStringIO import StringIO
from PyrexTypes import CPtrType

try:
    set
except NameError: # Python 2.3
    from sets import Set as set

import Annotate
import Code
import Naming
import Nodes
import Options
import PyrexTypes
import TypeSlots
import Version

from Errors import error
from PyrexTypes import py_object_type
from Cython.Utils import open_new_file, replace_suffix


class ModuleNode(Nodes.Node, Nodes.BlockNode):
    #  doc       string or None
    #  body      StatListNode
    #
    #  referenced_modules   [ModuleScope]
    #  module_temp_cname    string
    #  full_module_name     string

    children_attrs = ["body"]
    
    def analyse_declarations(self, env):
        if Options.embed_pos_in_docstring:
            env.doc = 'File: %s (starting at line %s)'%Nodes.relative_position(self.pos)
            if not self.doc is None:
                env.doc = env.doc + '\\n' + self.doc
        else:
            env.doc = self.doc
        self.body.analyse_declarations(env)
    
    def process_implementation(self, env, options, result):
        self.analyse_declarations(env)
        env.check_c_classes()
        self.body.analyse_expressions(env)
        env.return_type = PyrexTypes.c_void_type
        self.referenced_modules = []
        self.find_referenced_modules(env, self.referenced_modules, {})
        if self.has_imported_c_functions():
            self.module_temp_cname = env.allocate_temp_pyobject()
            env.release_temp(self.module_temp_cname)
        self.generate_c_code(env, options, result)
        self.generate_h_code(env, options, result)
        self.generate_api_code(env, result)
    
    def has_imported_c_functions(self):
        for module in self.referenced_modules:
            for entry in module.cfunc_entries:
                if entry.defined_in_pxd:
                    return 1
        return 0
    
    def generate_h_code(self, env, options, result):
        def h_entries(entries, pxd = 0):
            return [entry for entry in entries
                if entry.visibility == 'public' or pxd and entry.defined_in_pxd]
        h_types = h_entries(env.type_entries)
        h_vars = h_entries(env.var_entries)
        h_funcs = h_entries(env.cfunc_entries)
        h_extension_types = h_entries(env.c_class_entries)
        if h_types or h_vars or h_funcs or h_extension_types:
            result.h_file = replace_suffix(result.c_file, ".h")
            h_code = Code.CCodeWriter(open_new_file(result.h_file))
            if options.generate_pxi:
                result.i_file = replace_suffix(result.c_file, ".pxi")
                i_code = Code.PyrexCodeWriter(result.i_file)
            else:
                i_code = None
            guard = Naming.h_guard_prefix + env.qualified_name.replace(".", "__")
            h_code.put_h_guard(guard)
            self.generate_extern_c_macro_definition(h_code)
            self.generate_type_header_code(h_types, h_code)
            h_code.putln("")
            h_code.putln("#ifndef %s" % Naming.api_guard_prefix + self.api_name(env))
            if h_vars:
                h_code.putln("")
                for entry in h_vars:
                    self.generate_public_declaration(entry, h_code, i_code)
            if h_funcs:
                h_code.putln("")
                for entry in h_funcs:
                    self.generate_public_declaration(entry, h_code, i_code)
            if h_extension_types:
                h_code.putln("")
                for entry in h_extension_types:
                    self.generate_cclass_header_code(entry.type, h_code)
                    if i_code:
                        self.generate_cclass_include_code(entry.type, i_code)
            h_code.putln("")
            h_code.putln("#endif")
            h_code.putln("")
            h_code.putln("PyMODINIT_FUNC init%s(void);" % env.module_name)
            h_code.putln("")
            h_code.putln("#endif")
    
    def generate_public_declaration(self, entry, h_code, i_code):
        h_code.putln("%s %s;" % (
            Naming.extern_c_macro,
            entry.type.declaration_code(
                entry.cname, dll_linkage = "DL_IMPORT")))
        if i_code:
            i_code.putln("cdef extern %s" % 
                entry.type.declaration_code(entry.cname, pyrex = 1))
    
    def api_name(self, env):
        return env.qualified_name.replace(".", "__")
    
    def generate_api_code(self, env, result):
        api_funcs = []
        public_extension_types = []
        has_api_extension_types = 0
        for entry in env.cfunc_entries:
            if entry.api:
                api_funcs.append(entry)
        for entry in env.c_class_entries:
            if entry.visibility == 'public':
                public_extension_types.append(entry)
            if entry.api:
                has_api_extension_types = 1
        if api_funcs or has_api_extension_types:
            result.api_file = replace_suffix(result.c_file, "_api.h")
            h_code = Code.CCodeWriter(open_new_file(result.api_file))
            name = self.api_name(env)
            guard = Naming.api_guard_prefix + name
            h_code.put_h_guard(guard)
            h_code.putln('#include "Python.h"')
            if result.h_file:
                h_code.putln('#include "%s"' % os.path.basename(result.h_file))
            for entry in public_extension_types:
                type = entry.type
                h_code.putln("")
                h_code.putln("static PyTypeObject *%s;" % type.typeptr_cname)
                h_code.putln("#define %s (*%s)" % (
                    type.typeobj_cname, type.typeptr_cname))
            if api_funcs:
                h_code.putln("")
                for entry in api_funcs:
                    type = CPtrType(entry.type)
                    h_code.putln("static %s;" % type.declaration_code(entry.cname))
            h_code.putln("")
            h_code.put_h_guard(Naming.api_func_guard + "import_module")
            h_code.put(import_module_utility_code[1])
            h_code.putln("")
            h_code.putln("#endif")
            if api_funcs:
                h_code.putln("")
                h_code.put(function_import_utility_code[1])
            if public_extension_types:
                h_code.putln("")
                h_code.put(type_import_utility_code[1])
            h_code.putln("")
            h_code.putln("static int import_%s(void) {" % name)
            h_code.putln("PyObject *module = 0;")
            h_code.putln('module = __Pyx_ImportModule("%s");' % env.qualified_name)
            h_code.putln("if (!module) goto bad;")
            for entry in api_funcs:
                sig = entry.type.signature_string()
                h_code.putln(
                    'if (__Pyx_ImportFunction(module, "%s", (void**)&%s, "%s") < 0) goto bad;' % (
                        entry.name,
                        entry.cname,
                        sig))
            h_code.putln("Py_DECREF(module); module = 0;")
            for entry in public_extension_types:
                self.generate_type_import_call(
                    entry.type, h_code,
                    "if (!%s) goto bad;" % entry.type.typeptr_cname)
            h_code.putln("return 0;")
            h_code.putln("bad:")
            h_code.putln("Py_XDECREF(module);")
            h_code.putln("return -1;")
            h_code.putln("}")
            h_code.putln("")
            h_code.putln("#endif")
    
    def generate_cclass_header_code(self, type, h_code):
        h_code.putln("%s DL_IMPORT(PyTypeObject) %s;" % (
            Naming.extern_c_macro,
            type.typeobj_cname))
        #self.generate_obj_struct_definition(type, h_code)
    
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
    
    def generate_c_code(self, env, options, result):
        modules = self.referenced_modules
        if Options.annotate:
            code = Annotate.AnnotationCCodeWriter(StringIO())
        else:
            code = Code.CCodeWriter(StringIO())
        code.h = Code.CCodeWriter(StringIO())
        code.init_labels()
        self.generate_module_preamble(env, modules, code.h)

        code.putln("")
        code.putln("/* Implementation of %s */" % env.qualified_name)
        self.generate_const_definitions(env, code)
        self.generate_interned_num_decls(env, code)
        self.generate_interned_name_decls(env, code)
        self.generate_py_string_decls(env, code)
        self.generate_cached_builtins_decls(env, code)
        self.body.generate_function_definitions(env, code, options.transforms)
        code.mark_pos(None)
        self.generate_interned_name_table(env, code)
        self.generate_py_string_table(env, code)
        self.generate_typeobj_definitions(env, code)
        self.generate_method_table(env, code)
        self.generate_filename_init_prototype(code)
        self.generate_module_init_func(modules[:-1], env, code)
        code.mark_pos(None)
        self.generate_module_cleanup_func(env, code)
        self.generate_filename_table(code)
        self.generate_utility_functions(env, code)

        self.generate_declarations_for_modules(env, modules, code.h)


        f = open_new_file(result.c_file)
        f.write(code.h.f.getvalue())
        f.write("\n")
        f.write(code.f.getvalue())
        f.close()
        result.c_file_generated = 1
        if Options.annotate:
            self.annotate(code)
            code.save_annotation(result.c_file[:-1] + "pyx") # change?
    
    def find_referenced_modules(self, env, module_list, modules_seen):
        if env not in modules_seen:
            modules_seen[env] = 1
            for imported_module in env.cimported_modules:
                self.find_referenced_modules(imported_module, module_list, modules_seen)
            module_list.append(env)

    def sort_types_by_inheritance(self, type_dict, getkey):
        # copy the types into a list moving each parent type before
        # its first child
        type_items = type_dict.items()
        type_list = []
        for i, item in enumerate(type_items):
            key, new_entry = item

            # collect all base classes to check for children
            hierarchy = set()
            base = new_entry
            while base:
                base_type = base.type.base_type
                if not base_type:
                    break
                base_key = getkey(base_type)
                hierarchy.add(base_key)
                base = type_dict.get(base_key)
            new_entry.base_keys = hierarchy

            # find the first (sub-)subclass and insert before that
            for j in range(i):
                entry = type_list[j]
                if key in entry.base_keys:
                    type_list.insert(j, new_entry)
                    break
            else:
                type_list.append(new_entry)
        return type_list

    def sort_type_hierarchy(self, module_list, env):
        vtab_dict = {}
        vtabslot_dict = {}
        for module in module_list:
            for entry in module.c_class_entries:
                if not entry.in_cinclude:
                    type = entry.type
                    if type.vtabstruct_cname:
                        vtab_dict[type.vtabstruct_cname] = entry
            all_defined_here = module is env
            for entry in module.type_entries:
                if all_defined_here or entry.defined_in_pxd:
                    type = entry.type
                    if type.is_extension_type and not entry.in_cinclude:
                        type = entry.type
                        vtabslot_dict[type.objstruct_cname] = entry
                
        def vtabstruct_cname(entry_type):
            return entry_type.vtabstruct_cname
        vtab_list = self.sort_types_by_inheritance(
            vtab_dict, vtabstruct_cname)

        def objstruct_cname(entry_type):
            return entry_type.objstruct_cname
        vtabslot_list = self.sort_types_by_inheritance(
            vtabslot_dict, objstruct_cname)

        return (vtab_list, vtabslot_list)

    def generate_type_definitions(self, env, modules, vtab_list, vtabslot_list, code):
        vtabslot_entries = set(vtabslot_list)
        for module in modules:
            definition = module is env
            if definition:
                type_entries = module.type_entries
            else:
                type_entries = []
                for entry in module.type_entries:
                    if entry.defined_in_pxd:
                        type_entries.append(entry)
            for entry in type_entries:
                if not entry.in_cinclude:
                    #print "generate_type_header_code:", entry.name, repr(entry.type) ###
                    type = entry.type
                    if type.is_typedef: # Must test this first!
                        self.generate_typedef(entry, code)
                    elif type.is_struct_or_union:
                        self.generate_struct_union_definition(entry, code)
                    elif type.is_enum:
                        self.generate_enum_definition(entry, code)
                    elif type.is_extension_type and entry not in vtabslot_entries:
                        self.generate_obj_struct_definition(type, code)
        for entry in vtabslot_list:
            self.generate_obj_struct_definition(entry.type, code)
        for entry in vtab_list:
            self.generate_typeobject_predeclaration(entry, code)
            self.generate_exttype_vtable_struct(entry, code)
            self.generate_exttype_vtabptr_declaration(entry, code)

    def generate_declarations_for_modules(self, env, modules, code):
        code.putln("")
        code.putln("/* Declarations */")
        vtab_list, vtabslot_list = self.sort_type_hierarchy(modules, env)
        self.generate_type_definitions(
            env, modules, vtab_list, vtabslot_list, code)
        for module in modules:
            defined_here = module is env
            self.generate_global_declarations(module, code, defined_here)
            self.generate_cfunction_predeclarations(module, code, defined_here)

    def generate_module_preamble(self, env, cimported_modules, code):
        code.putln('/* Generated by Cython %s on %s */' % (
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
        code.putln("  #define PyNumber_Index(o)    PyNumber_Int(o)")
        code.putln("  #define PyIndex_Check(o)     PyNumber_Check(o)")
        code.putln("#endif")
        code.putln("#if PY_VERSION_HEX < 0x02040000")
        code.putln("  #define METH_COEXIST 0")
        code.putln("#endif")
        code.putln("#ifndef __stdcall")
        code.putln("  #define __stdcall")
        code.putln("#endif")
        code.putln("#ifndef __cdecl")
        code.putln("  #define __cdecl")
        code.putln("#endif")
        self.generate_extern_c_macro_definition(code)
        code.putln("#include <math.h>")
        self.generate_includes(env, cimported_modules, code)
        code.putln('')
        code.put(Nodes.utility_function_predeclarations)
        code.put(PyrexTypes.type_conversion_predeclarations)
        code.put(Nodes.branch_prediction_macros)
        code.putln('')
        code.putln('static PyObject *%s;' % env.module_cname)
        code.putln('static PyObject *%s;' % Naming.builtins_cname)
        code.putln('static PyObject *%s;' % Naming.empty_tuple)
        if Options.pre_import is not None:
            code.putln('static PyObject *%s;' % Naming.preimport_cname)
        code.putln('static int %s;' % Naming.lineno_cname)
        code.putln('static int %s = 0;' % Naming.clineno_cname)
        code.putln('static char * %s= %s;' % (Naming.cfilenm_cname, Naming.file_c_macro))
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

    def generate_type_predeclarations(self, env, code):
        pass

    def generate_type_header_code(self, type_entries, code):
        # Generate definitions of structs/unions/enums/typedefs/objstructs.
        #self.generate_gcc33_hack(env, code) # Is this still needed?
        #for entry in env.type_entries:
        for entry in type_entries:
            if not entry.in_cinclude:
                #print "generate_type_header_code:", entry.name, repr(entry.type) ###
                type = entry.type
                if type.is_typedef: # Must test this first!
                    self.generate_typedef(entry, code)
                elif type.is_struct_or_union:
                    self.generate_struct_union_definition(entry, code)
                elif type.is_enum:
                    self.generate_enum_definition(entry, code)
                elif type.is_extension_type:
                    self.generate_obj_struct_definition(type, code)
        
    def generate_gcc33_hack(self, env, code):
        # Workaround for spurious warning generation in gcc 3.3
        code.putln("")
        for entry in env.c_class_entries:
            type = entry.type
            if not type.typedef_flag:
                name = type.objstruct_cname
                if name.startswith("__pyx_"):
                    tail = name[6:]
                else:
                    tail = name
                code.putln("typedef struct %s __pyx_gcc33_%s;" % (
                    name, tail))
    
    def generate_typedef(self, entry, code):
        base_type = entry.type.typedef_base_type
        code.putln("")
        code.putln("typedef %s;" % base_type.declaration_code(entry.cname))

    def sue_header_footer(self, type, kind, name):
        if type.typedef_flag:
            header = "typedef %s {" % kind
            footer = "} %s;" % name
        else:
            header = "%s %s {" % (kind, name)
            footer = "};"
        return header, footer
    
    def generate_struct_union_definition(self, entry, code):
        code.mark_pos(entry.pos)
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
        code.mark_pos(entry.pos)
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
        code.mark_pos(entry.pos)
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
        code.mark_pos(entry.pos)
        # Generate declaration of pointer to an extension type's vtable.
        type = entry.type
        if type.vtabptr_cname:
            code.putln("static struct %s *%s;" % (
                type.vtabstruct_cname,
                type.vtabptr_cname))
    
    def generate_obj_struct_definition(self, type, code):
        code.mark_pos(type.pos)
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
            if definition or entry.defined_in_pxd:
                code.putln("static PyTypeObject *%s = 0;" % 
                    entry.type.typeptr_cname)
        code.put_var_declarations(env.var_entries, static = 1, 
            dll_linkage = "DL_EXPORT", definition = definition)
        code.put_var_declarations(env.default_entries, static = 1,
                                  definition = definition)
    
    def generate_cfunction_predeclarations(self, env, code, definition):
        for entry in env.cfunc_entries:
            if not entry.in_cinclude and (definition
                    or entry.defined_in_pxd or entry.visibility == 'extern'):
                if entry.visibility in ('public', 'extern'):
                    dll_linkage = "DL_EXPORT"
                else:
                    dll_linkage = None
                type = entry.type
                if not definition and entry.defined_in_pxd:
                    type = CPtrType(type)
                header = type.declaration_code(entry.cname, 
                    dll_linkage = dll_linkage)
                if entry.visibility == 'private':
                    storage_class = "static "
                elif entry.visibility == 'extern':
                    storage_class = "%s " % Naming.extern_c_macro
                else:
                    storage_class = ""
                code.putln("%s%s; /*proto*/" % (
                    storage_class,
                    header))
    
    def generate_typeobj_definitions(self, env, code):
        full_module_name = env.qualified_name
        for entry in env.c_class_entries:
            #print "generate_typeobj_definitions:", entry.name
            #print "...visibility =", entry.visibility
            if entry.visibility != 'extern':
                type = entry.type
                scope = type.scope
                if scope: # could be None if there was an error
                    self.generate_exttype_vtable(scope, code)
                    self.generate_new_function(scope, code)
                    self.generate_dealloc_function(scope, code)
                    if scope.needs_gc():
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
        tp_slot = TypeSlots.ConstructorSlot("tp_new", '__new__')
        slot_func = scope.mangle_internal("tp_new")
        type = scope.parent_type
        base_type = type.base_type
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject:
                py_attrs.append(entry)
        need_self_cast = type.vtabslot_cname or py_attrs
        code.putln("")
        code.putln(
            "static PyObject *%s(PyTypeObject *t, PyObject *a, PyObject *k) {"
                % scope.mangle_internal("tp_new"))
        if need_self_cast:
            code.putln(
                "%s;"
                    % scope.parent_type.declaration_code("p"))
        if base_type:
            tp_new = TypeSlots.get_base_slot_function(scope, tp_slot)
            if tp_new is None:
                tp_new = "%s->tp_new" % base_type.typeptr_cname
            code.putln(
                "PyObject *o = %s(t, a, k);" % tp_new)
        else:
            code.putln(
                "PyObject *o = (*t->tp_alloc)(t, 0);")
        code.putln(
                "if (!o) return 0;")
        if need_self_cast:
            code.putln(
                "p = %s;"
                    % type.cast_code("o"))
        #if need_self_cast:
        #	self.generate_self_cast(scope, code)
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
            if entry.trivial_signature:
                cinit_args = "o, %s, NULL" % Naming.empty_tuple
            else:
                cinit_args = "o, a, k"
            code.putln(
                "if (%s(%s) < 0) {" % 
                    (entry.func_cname, cinit_args))
            code.put_decref_clear("o", py_object_type);
            code.putln(
                "}")
        code.putln(
            "return o;")
        code.putln(
            "}")
    
    def generate_dealloc_function(self, scope, code):
        tp_slot = TypeSlots.ConstructorSlot("tp_dealloc", '__dealloc__')
        slot_func = scope.mangle_internal("tp_dealloc")
        base_type = scope.parent_type.base_type
        if tp_slot.slot_code(scope) != slot_func:
            return # never used
        code.putln("")
        code.putln(
            "static void %s(PyObject *o) {"
                % scope.mangle_internal("tp_dealloc"))
        py_attrs = []
        weakref_slot = scope.lookup_here("__weakref__")
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry is not weakref_slot:
                py_attrs.append(entry)
        if py_attrs or weakref_slot in scope.var_entries:
            self.generate_self_cast(scope, code)
        self.generate_usr_dealloc_call(scope, code)
        if weakref_slot in scope.var_entries:
            code.putln("if (p->__weakref__) PyObject_ClearWeakRefs(o);")
        for entry in py_attrs:
            code.put_xdecref("p->%s" % entry.cname, entry.type)
        if base_type:
            tp_dealloc = TypeSlots.get_base_slot_function(scope, tp_slot)
            if tp_dealloc is None:
                tp_dealloc = "%s->tp_dealloc" % base_type.typeptr_cname
            code.putln(
                    "%s(o);" % tp_dealloc)
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
        tp_slot = TypeSlots.GCDependentSlot("tp_traverse")
        slot_func = scope.mangle_internal("tp_traverse")
        base_type = scope.parent_type.base_type
        if tp_slot.slot_code(scope) != slot_func:
            return # never used
        code.putln("")
        code.putln(
            "static int %s(PyObject *o, visitproc v, void *a) {"
                % slot_func)
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry.name != "__weakref__":
                py_attrs.append(entry)
        if base_type or py_attrs:
            code.putln("int e;")
        if py_attrs:
            self.generate_self_cast(scope, code)
        if base_type:
            # want to call it explicitly if possible so inlining can be performed
            static_call = TypeSlots.get_base_slot_function(scope, tp_slot)
            if static_call:
                code.putln("e = %s(o, v, a); if (e) return e;" % static_call)
            else:
                code.putln("if (%s->tp_traverse) {" % base_type.typeptr_cname)
                code.putln(
                        "e = %s->tp_traverse(o, v, a); if (e) return e;" %
                            base_type.typeptr_cname)
                code.putln("}")
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
        tp_slot = TypeSlots.GCDependentSlot("tp_clear")
        slot_func = scope.mangle_internal("tp_clear")
        base_type = scope.parent_type.base_type
        if tp_slot.slot_code(scope) != slot_func:
            return # never used
        code.putln("")
        code.putln("static int %s(PyObject *o) {" % slot_func)
        py_attrs = []
        for entry in scope.var_entries:
            if entry.type.is_pyobject and entry.name != "__weakref__":
                py_attrs.append(entry)
        if py_attrs:
            self.generate_self_cast(scope, code)
            code.putln("PyObject* tmp;")
        if base_type:
            # want to call it explicitly if possible so inlining can be performed
            static_call = TypeSlots.get_base_slot_function(scope, tp_slot)
            if static_call:
                code.putln("%s(o);" % static_call)
            else:
                code.putln("if (%s->tp_clear) {" % base_type.typeptr_cname)
                code.putln("%s->tp_clear(o);" % base_type.typeptr_cname)
                code.putln("}")
        for entry in py_attrs:
            name = "p->%s" % entry.cname
            code.putln("tmp = ((PyObject*)%s);" % name)
            code.put_init_to_py_none(name, entry.type)
            code.putln("Py_XDECREF(tmp);")
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
                    "offsetof(%s, %s)" % (objstruct, entry.cname),
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
        code.mark_pos(None)
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
                    "{&%s, %s, sizeof(%s), %d}," % (
                        entry.pystring_cname,
                        entry.cname,
                        entry.cname,
                        entry.type.is_unicode
                        ))
            code.putln(
                "{0, 0, 0, 0}")
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

        code.putln("/*--- Libary function declarations ---*/")
        env.generate_library_function_declarations(code)
        self.generate_filename_init_call(code)

        code.putln("/*--- Module creation code ---*/")
        self.generate_module_creation_code(env, code)

        code.putln("/*--- Intern code ---*/")
        self.generate_intern_code(env, code)

        code.putln("/*--- String init code ---*/")
        self.generate_string_init_code(env, code)

        if Options.cache_builtins:
            code.putln("/*--- Builtin init code ---*/")
            self.generate_builtin_init_code(env, code)
            
        code.putln("%s = PyTuple_New(0); %s" % (Naming.empty_tuple, code.error_goto_if_null(Naming.empty_tuple, self.pos)));
        code.putln("%s = 0;" % Naming.skip_dispatch_cname);

        code.putln("/*--- Global init code ---*/")
        self.generate_global_init_code(env, code)

        code.putln("/*--- Function export code ---*/")
        self.generate_c_function_export_code(env, code)

        code.putln("/*--- Type init code ---*/")
        self.generate_type_init_code(env, code)

        code.putln("/*--- Type import code ---*/")
        for module in imported_modules:
            self.generate_type_import_code_for_module(module, env, code)

        code.putln("/*--- Function import code ---*/")
        for module in imported_modules:
            self.generate_c_function_import_code_for_module(module, env, code)

        code.putln("/*--- Execution code ---*/")
        code.mark_pos(None)
        self.body.generate_execution_code(code)

        if Options.generate_cleanup_code:
            code.putln("if (__Pyx_RegisterCleanup()) %s;" % code.error_goto(self.pos))

        code.putln("return;")
        code.put_label(code.error_label)
        code.put_var_xdecrefs(env.temp_entries)
        code.putln('__Pyx_AddTraceback("%s");' % env.qualified_name)
        env.use_utility_code(Nodes.traceback_utility_code)
        code.putln('}')

    def generate_module_cleanup_func(self, env, code):
        if not Options.generate_cleanup_code:
            return
        env.use_utility_code(import_module_utility_code)
        env.use_utility_code(register_cleanup_utility_code)
        code.putln()
        code.putln('static PyObject* %s(PyObject *self, PyObject *unused) {' % Naming.cleanup_cname)
        if Options.generate_cleanup_code >= 2:
            code.putln("/*--- Global cleanup code ---*/")
            rev_entries = list(env.var_entries)
            rev_entries.reverse()
            for entry in rev_entries:
                if entry.visibility != 'extern':
                    if entry.type.is_pyobject:
                        code.put_var_decref_clear(entry)
        if Options.generate_cleanup_code >= 3:
            code.putln("/*--- Type import cleanup code ---*/")
            for type, _ in env.types_imported.items():
                code.put_decref("((PyObject*)%s)" % type.typeptr_cname, PyrexTypes.py_object_type)
        if Options.cache_builtins:
            code.putln("/*--- Builtin cleanup code ---*/")
            for entry in env.cached_builtins:
                code.put_var_decref_clear(entry)
        code.putln("Py_DECREF(%s); %s = 0;" % (Naming.empty_tuple, Naming.empty_tuple));
        code.putln("/*--- Intern cleanup code ---*/")
        for entry in env.pynum_entries:
            code.put_var_decref_clear(entry)
        if env.intern_map:
            for name, cname in env.intern_map.items():
                code.put_decref_clear(cname, PyrexTypes.py_object_type)
        code.putln("Py_INCREF(Py_None); return Py_None;")
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
        if Options.pre_import is not None:
            code.putln(
                '%s = PyImport_AddModule("%s");' % (
                    Naming.preimport_cname, 
                    Options.pre_import))
            code.putln(
                "if (!%s) %s;" % (
                    Naming.preimport_cname,
                    code.error_goto(self.pos)));
    
    def generate_intern_code(self, env, code):
        for entry in env.pynum_entries:
            code.putln("%s = PyInt_FromLong(%s); %s;" % (
                entry.cname,
                entry.init,
                code.error_goto_if_null(entry.cname, self.pos)))
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

    def generate_builtin_init_code(self, env, code):
        # Lookup and cache builtin objects.
        if Options.cache_builtins:
            for entry in env.cached_builtins:
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
                        entry.name,
                        entry.cname, 
                        code.error_goto(entry.pos)))
    
    def generate_global_init_code(self, env, code):
        # Generate code to initialise global PyObject *
        # variables to None.
        for entry in env.var_entries:
            if entry.visibility != 'extern':
                if entry.type.is_pyobject:
                    code.put_init_var_to_py_none(entry)

    def generate_c_function_export_code(self, env, code):
        # Generate code to create PyCFunction wrappers for exported C functions.
        for entry in env.cfunc_entries:
            if entry.api or entry.defined_in_pxd:
                env.use_utility_code(function_export_utility_code)
                signature = entry.type.signature_string()
                code.putln('if (__Pyx_ExportFunction("%s", (void*)%s, "%s") < 0) %s' % (
                    entry.name,
                    entry.cname,
                    signature, 
                    code.error_goto(self.pos)))
    
    def generate_type_import_code_for_module(self, module, env, code):
        # Generate type import code for all exported extension types in
        # an imported module.
        #if module.c_class_entries:
        for entry in module.c_class_entries:
            if entry.defined_in_pxd:
                self.generate_type_import_code(env, entry.type, entry.pos, code)
    
    def generate_c_function_import_code_for_module(self, module, env, code):
        # Generate import code for all exported C functions in a cimported module.
        entries = []
        for entry in module.cfunc_entries:
            if entry.defined_in_pxd:
                entries.append(entry)
        if entries:
            env.use_utility_code(import_module_utility_code)
            env.use_utility_code(function_import_utility_code)
            temp = self.module_temp_cname
            code.putln(
                '%s = __Pyx_ImportModule("%s"); if (!%s) %s' % (
                    temp,
                    module.qualified_name,
                    temp,
                    code.error_goto(self.pos)))
            for entry in entries:
                code.putln(
                    'if (__Pyx_ImportFunction(%s, "%s", (void**)&%s, "%s") < 0) %s' % (
                        temp,
                        entry.name,
                        entry.cname,
                        entry.type.signature_string(),
                        code.error_goto(self.pos)))
            code.putln("Py_DECREF(%s); %s = 0;" % (temp, temp))
    
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
        if base_type and base_type.module_name != env.qualified_name:
            self.generate_type_import_code(env, base_type, self.pos, code)
    
    def use_type_import_utility_code(self, env):
        env.use_utility_code(type_import_utility_code)
        env.use_utility_code(import_module_utility_code)
    
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
        self.generate_type_import_call(type, code,
                                       code.error_goto_if_null(type.typeptr_cname, pos))
        self.use_type_import_utility_code(env)
        if type.vtabptr_cname:
            code.putln(
                "if (__Pyx_GetVtable(%s->tp_dict, &%s) < 0) %s" % (
                    type.typeptr_cname,
                    type.vtabptr_cname,
                    code.error_goto(pos)))
            env.use_utility_code(Nodes.get_vtable_utility_code)
        env.types_imported[type] = 1

    def generate_type_import_call(self, type, code, error_code):
        if type.typedef_flag:
            objstruct = type.objstruct_cname
        else:
            objstruct = "struct %s" % type.objstruct_cname
        code.putln('%s = __Pyx_ImportType("%s", "%s", sizeof(%s)); %s' % (
            type.typeptr_cname,
            type.module_name, 
            type.name,
            objstruct,
            error_code))

    def generate_type_ready_code(self, env, entry, code):
        # Generate a call to PyType_Ready for an extension
        # type defined in this module.
        type = entry.type
        typeobj_cname = type.typeobj_cname
        scope = type.scope
        if scope: # could be None if there was an error
            if entry.visibility != 'extern':
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
                        "*(void(**)(void))&%s.%s = (void(*)(void))%s;" % (
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
        code.put(PyrexTypes.type_conversion_functions)

#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

import_module_utility_code = [
"""
static PyObject *__Pyx_ImportModule(char *name); /*proto*/
""","""
#ifndef __PYX_HAVE_RT_ImportModule
#define __PYX_HAVE_RT_ImportModule
static PyObject *__Pyx_ImportModule(char *name) {
    PyObject *py_name = 0;
    PyObject *py_module = 0;
    
    py_name = PyString_FromString(name);
    if (!py_name)
        goto bad;
    py_module = PyImport_Import(py_name);
    Py_DECREF(py_name);
    return py_module;
bad:
    Py_XDECREF(py_name);
    return 0;
}
#endif
"""]

#------------------------------------------------------------------------------------

type_import_utility_code = [
"""
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/
""","""
#ifndef __PYX_HAVE_RT_ImportType
#define __PYX_HAVE_RT_ImportType
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name,
    long size)
{
    PyObject *py_module = 0;
    PyObject *result = 0;
    PyObject *py_name = 0;
    
    py_name = PyString_FromString(module_name);
    if (!py_name)
        goto bad;

    py_module = __Pyx_ImportModule(module_name);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttrString(py_module, class_name);
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
    return (PyTypeObject *)result;
bad:
    Py_XDECREF(py_name);
    Py_XDECREF(result);
    return 0;
}
#endif
"""]

#------------------------------------------------------------------------------------

function_export_utility_code = [
"""
static int __Pyx_ExportFunction(char *name, void *f, char *sig); /*proto*/
""",r"""
static int __Pyx_ExportFunction(char *name, void *f, char *sig) {
    PyObject *d = 0;
    PyObject *p = 0;
    d = PyObject_GetAttrString(%(MODULE)s, "%(API)s");
    if (!d) {
        PyErr_Clear();
        d = PyDict_New();
        if (!d)
            goto bad;
        Py_INCREF(d);
        if (PyModule_AddObject(%(MODULE)s, "%(API)s", d) < 0)
            goto bad;
    }
    p = PyCObject_FromVoidPtrAndDesc(f, sig, 0);
    if (!p)
        goto bad;
    if (PyDict_SetItemString(d, name, p) < 0)
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(p);
    Py_XDECREF(d);
    return -1;
}
""" % {'MODULE': Naming.module_cname, 'API': Naming.api_name}]

#------------------------------------------------------------------------------------

function_import_utility_code = [
"""
static int __Pyx_ImportFunction(PyObject *module, char *funcname, void **f, char *sig); /*proto*/
""","""
#ifndef __PYX_HAVE_RT_ImportFunction
#define __PYX_HAVE_RT_ImportFunction
static int __Pyx_ImportFunction(PyObject *module, char *funcname, void **f, char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    char *desc;
    
    d = PyObject_GetAttrString(module, "%(API)s");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, funcname);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%%s does not export expected C function %%s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
    desc = (char *)PyCObject_GetDesc(cobj);
    if (!desc)
        goto bad;
    if (strcmp(desc, sig) != 0) {
        PyErr_Format(PyExc_TypeError,
            "C function %%s.%%s has wrong signature (expected %%s, got %%s)",
                PyModule_GetName(module), funcname, sig, desc);
        goto bad;
    }
    *f = PyCObject_AsVoidPtr(cobj);
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif
""" % dict(API = Naming.api_name)]

register_cleanup_utility_code = [
"""
static int __Pyx_RegisterCleanup(void); /*proto*/
static PyObject* __pyx_module_cleanup(PyObject *self, PyObject *unused); /*proto*/
static PyMethodDef cleanup_def = {"__cleanup", (PyCFunction)&__pyx_module_cleanup, METH_NOARGS, 0};
""","""
static int __Pyx_RegisterCleanup(void) {
    /* Don't use Py_AtExit because that has a 32-call limit 
     * and is called after python finalization. 
     */

    PyObject *cleanup_func = 0;
    PyObject *atexit = 0;
    PyObject *reg = 0;
    PyObject *args = 0;
    PyObject *res = 0;
    int ret = -1;
    
    cleanup_func = PyCFunction_New(&cleanup_def, 0);
    args = PyTuple_New(1);
    if (!cleanup_func || !args)
        goto bad;
    PyTuple_SET_ITEM(args, 0, cleanup_func);
    cleanup_func = 0;

    atexit = __Pyx_ImportModule("atexit");
    if (!atexit)
        goto bad;
    reg = PyObject_GetAttrString(atexit, "register");
    if (!reg)
        goto bad;
    res = PyObject_CallObject(reg, args);
    if (!res)
        goto bad;
    ret = 0;
bad:
    Py_XDECREF(cleanup_func);
    Py_XDECREF(atexit);
    Py_XDECREF(reg);
    Py_XDECREF(args);
    Py_XDECREF(res);
    return ret;
}
"""]
