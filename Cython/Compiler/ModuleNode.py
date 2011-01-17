#
#   Pyrex - Module parse tree node
#

import cython
from cython import set
cython.declare(Naming=object, Options=object, PyrexTypes=object, TypeSlots=object,
               error=object, warning=object, py_object_type=object, UtilityCode=object,
               EncodedString=object)

import os, time
from PyrexTypes import CPtrType
import Future

import Annotate
import Code
import Naming
import Nodes
import Options
import PyrexTypes
import TypeSlots
import Version
import DebugFlags

from Errors import error, warning
from PyrexTypes import py_object_type
from Cython.Utils import open_new_file, replace_suffix
from Code import UtilityCode
from StringEncoding import EncodedString


def check_c_declarations_pxd(module_node):
    module_node.scope.check_c_classes_pxd()
    return module_node

def check_c_declarations(module_node):
    module_node.scope.check_c_classes()
    module_node.scope.check_c_functions()
    return module_node

class ModuleNode(Nodes.Node, Nodes.BlockNode):
    #  doc       string or None
    #  body      StatListNode
    #
    #  referenced_modules   [ModuleScope]
    #  full_module_name     string
    #
    #  scope                The module scope.
    #  compilation_source   A CompilationSource (see Main)
    #  directives           Top-level compiler directives

    child_attrs = ["body"]
    directives = None

    def analyse_declarations(self, env):
        if Options.embed_pos_in_docstring:
            env.doc = EncodedString(u'File: %s (starting at line %s)' % Nodes.relative_position(self.pos))
            if not self.doc is None:
                env.doc = EncodedString(env.doc + u'\n' + self.doc)
                env.doc.encoding = self.doc.encoding
        else:
            env.doc = self.doc
        env.directives = self.directives
        self.body.analyse_declarations(env)

    def process_implementation(self, options, result):
        env = self.scope
        env.return_type = PyrexTypes.c_void_type
        self.referenced_modules = []
        self.find_referenced_modules(env, self.referenced_modules, {})
        if options.recursive:
            self.generate_dep_file(env, result)
        self.generate_c_code(env, options, result)
        self.generate_h_code(env, options, result)
        self.generate_api_code(env, result)

    def has_imported_c_functions(self):
        for module in self.referenced_modules:
            for entry in module.cfunc_entries:
                if entry.defined_in_pxd:
                    return 1
        return 0

    def generate_dep_file(self, env, result):
        modules = self.referenced_modules
        if len(modules) > 1 or env.included_files:
            dep_file = replace_suffix(result.c_file, ".dep")
            f = open(dep_file, "w")
            try:
                for module in modules:
                    if module is not env:
                        f.write("cimport %s\n" % module.qualified_name)
                    for path in module.included_files:
                        f.write("include %s\n" % path)
            finally:
                f.close()

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
            h_code = Code.CCodeWriter()
            Code.GlobalState(h_code)
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

            f = open_new_file(result.h_file)
            try:
                h_code.copyto(f)
            finally:
                f.close()

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
            h_code = Code.CCodeWriter()
            Code.GlobalState(h_code)
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
            h_code.put(import_module_utility_code.impl)
            h_code.putln("")
            h_code.putln("#endif")
            if api_funcs:
                h_code.putln("")
                h_code.put(function_import_utility_code.impl)
            if public_extension_types:
                h_code.putln("")
                h_code.put(type_import_utility_code.impl)
            h_code.putln("")
            h_code.putln("static int import_%s(void) {" % name)
            h_code.putln("PyObject *module = 0;")
            h_code.putln('module = __Pyx_ImportModule("%s");' % env.qualified_name)
            h_code.putln("if (!module) goto bad;")
            for entry in api_funcs:
                sig = entry.type.signature_string()
                h_code.putln(
                    'if (__Pyx_ImportFunction(module, "%s", (void (**)(void))&%s, "%s") < 0) goto bad;' % (
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

            f = open_new_file(result.api_file)
            try:
                h_code.copyto(f)
            finally:
                f.close()

    def generate_cclass_header_code(self, type, h_code):
        h_code.putln("%s DL_IMPORT(PyTypeObject) %s;" % (
            Naming.extern_c_macro,
            type.typeobj_cname))

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

        if Options.annotate or options.annotate:
            emit_linenums = False
            rootwriter = Annotate.AnnotationCCodeWriter()
        else:
            emit_linenums = options.emit_linenums
            rootwriter = Code.CCodeWriter(emit_linenums=emit_linenums, c_line_in_traceback=options.c_line_in_traceback)
        globalstate = Code.GlobalState(rootwriter, emit_linenums)
        globalstate.initialize_main_c_code()
        h_code = globalstate['h_code']

        self.generate_module_preamble(env, modules, h_code)

        globalstate.module_pos = self.pos
        globalstate.directives = self.directives

        globalstate.use_utility_code(refnanny_utility_code)

        code = globalstate['before_global_var']
        code.putln('#define __Pyx_MODULE_NAME "%s"' % self.full_module_name)
        code.putln("static int %s%s = 0;" % (Naming.module_is_main, self.full_module_name.replace('.', '__')))
        code.putln("")
        code.putln("/* Implementation of %s */" % env.qualified_name)

        code = globalstate['all_the_rest']

        self.generate_cached_builtins_decls(env, code)
        self.generate_lambda_definitions(env, code)
        # generate normal function definitions
        self.body.generate_function_definitions(env, code)
        code.mark_pos(None)
        self.generate_typeobj_definitions(env, code)
        self.generate_method_table(env, code)
        if env.has_import_star:
            self.generate_import_star(env, code)
        self.generate_pymoduledef_struct(env, code)

        # init_globals is inserted before this
        self.generate_module_init_func(modules[:-1], env, globalstate['init_module'])
        self.generate_module_cleanup_func(env, globalstate['cleanup_module'])
        if Options.embed:
            self.generate_main_method(env, globalstate['main_method'])
        self.generate_filename_table(globalstate['filename_table'])

        self.generate_declarations_for_modules(env, modules, globalstate)
        h_code.write('\n')

        for utilcode in env.utility_code_list:
            globalstate.use_utility_code(utilcode)
        globalstate.finalize_main_c_code()

        f = open_new_file(result.c_file)
        rootwriter.copyto(f)
        if options.gdb_debug:
            self._serialize_lineno_map(env, rootwriter)
        f.close()
        result.c_file_generated = 1
        if Options.annotate or options.annotate:
            self.annotate(rootwriter)
            rootwriter.save_annotation(result.main_source_file, result.c_file)

    def _serialize_lineno_map(self, env, ccodewriter):
        tb = env.context.gdb_debug_outputwriter
        markers = ccodewriter.buffer.allmarkers()

        d = {}
        for c_lineno, cython_lineno in enumerate(markers):
            if cython_lineno > 0:
                d.setdefault(cython_lineno, []).append(c_lineno + 1)

        tb.start('LineNumberMapping')
        for cython_lineno, c_linenos in sorted(d.iteritems()):
                attrs = {
                    'c_linenos': ' '.join(map(str, c_linenos)),
                    'cython_lineno': str(cython_lineno),
                }
                tb.start('LineNumber', attrs)
                tb.end('LineNumber')
        tb.end('LineNumberMapping')
        tb.serialize()

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
                        self.generate_objstruct_definition(type, code)
        for entry in vtabslot_list:
            self.generate_objstruct_definition(entry.type, code)
        for entry in vtab_list:
            self.generate_typeobject_predeclaration(entry, code)
            self.generate_exttype_vtable_struct(entry, code)
            self.generate_exttype_vtabptr_declaration(entry, code)

    def generate_declarations_for_modules(self, env, modules, globalstate):
        typecode = globalstate['type_declarations']
        typecode.putln("")
        typecode.putln("/* Type declarations */")
        vtab_list, vtabslot_list = self.sort_type_hierarchy(modules, env)
        self.generate_type_definitions(
            env, modules, vtab_list, vtabslot_list, typecode)
        modulecode = globalstate['module_declarations']
        for module in modules:
            defined_here = module is env
            modulecode.putln("/* Module declarations from %s */" %
                             module.qualified_name)
            self.generate_global_declarations(module, modulecode, defined_here)
            self.generate_cfunction_predeclarations(module, modulecode, defined_here)

    def generate_module_preamble(self, env, cimported_modules, code):
        code.putln("/* Generated by Cython %s on %s */" % (
            Version.version, time.asctime()))
        code.putln("")
        code.putln("#define PY_SSIZE_T_CLEAN")
        for filename in env.python_include_files:
            code.putln('#include "%s"' % filename)
        code.putln("#ifndef Py_PYTHON_H")
        code.putln("    #error Python headers needed to compile C extensions, please install development version of Python.")
        code.putln("#else")
        code.globalstate["end"].putln("#endif /* Py_PYTHON_H */")

        code.put("""
#include <stddef.h> /* For offsetof */
#ifndef offsetof
#define offsetof(type, member) ( (size_t) & ((type*)0) -> member )
#endif

#if !defined(WIN32) && !defined(MS_WINDOWS)
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
  #ifndef __fastcall
    #define __fastcall
  #endif
#endif

#ifndef DL_IMPORT
  #define DL_IMPORT(t) t
#endif
#ifndef DL_EXPORT
  #define DL_EXPORT(t) t
#endif

#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif

#if PY_VERSION_HEX < 0x02040000
  #define METH_COEXIST 0
  #define PyDict_CheckExact(op) (Py_TYPE(op) == &PyDict_Type)
  #define PyDict_Contains(d,o)   PySequence_Contains(d,o)
#endif

#if PY_VERSION_HEX < 0x02050000
  typedef int Py_ssize_t;
  #define PY_SSIZE_T_MAX INT_MAX
  #define PY_SSIZE_T_MIN INT_MIN
  #define PY_FORMAT_SIZE_T \"\"
  #define PyInt_FromSsize_t(z) PyInt_FromLong(z)
  #define PyInt_AsSsize_t(o)   PyInt_AsLong(o)
  #define PyNumber_Index(o)    PyNumber_Int(o)
  #define PyIndex_Check(o)     PyNumber_Check(o)
  #define PyErr_WarnEx(category, message, stacklevel) PyErr_Warn(category, message)
#endif

#if PY_VERSION_HEX < 0x02060000
  #define Py_REFCNT(ob) (((PyObject*)(ob))->ob_refcnt)
  #define Py_TYPE(ob)   (((PyObject*)(ob))->ob_type)
  #define Py_SIZE(ob)   (((PyVarObject*)(ob))->ob_size)
  #define PyVarObject_HEAD_INIT(type, size) \\
          PyObject_HEAD_INIT(type) size,
  #define PyType_Modified(t)

  typedef struct {
     void *buf;
     PyObject *obj;
     Py_ssize_t len;
     Py_ssize_t itemsize;
     int readonly;
     int ndim;
     char *format;
     Py_ssize_t *shape;
     Py_ssize_t *strides;
     Py_ssize_t *suboffsets;
     void *internal;
  } Py_buffer;

  #define PyBUF_SIMPLE 0
  #define PyBUF_WRITABLE 0x0001
  #define PyBUF_FORMAT 0x0004
  #define PyBUF_ND 0x0008
  #define PyBUF_STRIDES (0x0010 | PyBUF_ND)
  #define PyBUF_C_CONTIGUOUS (0x0020 | PyBUF_STRIDES)
  #define PyBUF_F_CONTIGUOUS (0x0040 | PyBUF_STRIDES)
  #define PyBUF_ANY_CONTIGUOUS (0x0080 | PyBUF_STRIDES)
  #define PyBUF_INDIRECT (0x0100 | PyBUF_STRIDES)

#endif

#if PY_MAJOR_VERSION < 3
  #define __Pyx_BUILTIN_MODULE_NAME "__builtin__"
#else
  #define __Pyx_BUILTIN_MODULE_NAME "builtins"
#endif

#if PY_MAJOR_VERSION >= 3
  #define Py_TPFLAGS_CHECKTYPES 0
  #define Py_TPFLAGS_HAVE_INDEX 0
#endif

#if (PY_VERSION_HEX < 0x02060000) || (PY_MAJOR_VERSION >= 3)
  #define Py_TPFLAGS_HAVE_NEWBUFFER 0
#endif

#if PY_MAJOR_VERSION >= 3
  #define PyBaseString_Type            PyUnicode_Type
  #define PyStringObject               PyUnicodeObject
  #define PyString_Type                PyUnicode_Type
  #define PyString_Check               PyUnicode_Check
  #define PyString_CheckExact          PyUnicode_CheckExact
#endif

#if PY_VERSION_HEX < 0x02060000
  #define PyBytesObject                PyStringObject
  #define PyBytes_Type                 PyString_Type
  #define PyBytes_Check                PyString_Check
  #define PyBytes_CheckExact           PyString_CheckExact
  #define PyBytes_FromString           PyString_FromString
  #define PyBytes_FromStringAndSize    PyString_FromStringAndSize
  #define PyBytes_FromFormat           PyString_FromFormat
  #define PyBytes_DecodeEscape         PyString_DecodeEscape
  #define PyBytes_AsString             PyString_AsString
  #define PyBytes_AsStringAndSize      PyString_AsStringAndSize
  #define PyBytes_Size                 PyString_Size
  #define PyBytes_AS_STRING            PyString_AS_STRING
  #define PyBytes_GET_SIZE             PyString_GET_SIZE
  #define PyBytes_Repr                 PyString_Repr
  #define PyBytes_Concat               PyString_Concat
  #define PyBytes_ConcatAndDel         PyString_ConcatAndDel
#endif

#if PY_VERSION_HEX < 0x02060000
  #define PySet_Check(obj)             PyObject_TypeCheck(obj, &PySet_Type)
  #define PyFrozenSet_Check(obj)       PyObject_TypeCheck(obj, &PyFrozenSet_Type)
#endif
#ifndef PySet_CheckExact
  #define PySet_CheckExact(obj)        (Py_TYPE(obj) == &PySet_Type)
#endif

#define __Pyx_TypeCheck(obj, type) PyObject_TypeCheck(obj, (PyTypeObject *)type)

#if PY_MAJOR_VERSION >= 3
  #define PyIntObject                  PyLongObject
  #define PyInt_Type                   PyLong_Type
  #define PyInt_Check(op)              PyLong_Check(op)
  #define PyInt_CheckExact(op)         PyLong_CheckExact(op)
  #define PyInt_FromString             PyLong_FromString
  #define PyInt_FromUnicode            PyLong_FromUnicode
  #define PyInt_FromLong               PyLong_FromLong
  #define PyInt_FromSize_t             PyLong_FromSize_t
  #define PyInt_FromSsize_t            PyLong_FromSsize_t
  #define PyInt_AsLong                 PyLong_AsLong
  #define PyInt_AS_LONG                PyLong_AS_LONG
  #define PyInt_AsSsize_t              PyLong_AsSsize_t
  #define PyInt_AsUnsignedLongMask     PyLong_AsUnsignedLongMask
  #define PyInt_AsUnsignedLongLongMask PyLong_AsUnsignedLongLongMask
#endif

#if PY_MAJOR_VERSION >= 3
  #define PyBoolObject                 PyLongObject
#endif

""")

        code.put("""
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_TrueDivide(x,y)
  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceTrueDivide(x,y)
#else
""")
        if Future.division in env.context.future_directives:
            code.putln("  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_TrueDivide(x,y)")
            code.putln("  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceTrueDivide(x,y)")
        else:
            code.putln("  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_Divide(x,y)")
            code.putln("  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceDivide(x,y)")
        code.putln("#endif")

        code.put("""
#if (PY_MAJOR_VERSION < 3) || (PY_VERSION_HEX >= 0x03010300)
  #define __Pyx_PySequence_GetSlice(obj, a, b) PySequence_GetSlice(obj, a, b)
  #define __Pyx_PySequence_SetSlice(obj, a, b, value) PySequence_SetSlice(obj, a, b, value)
  #define __Pyx_PySequence_DelSlice(obj, a, b) PySequence_DelSlice(obj, a, b)
#else
  #define __Pyx_PySequence_GetSlice(obj, a, b) (unlikely(!(obj)) ? \\
        (PyErr_SetString(PyExc_SystemError, "null argument to internal routine"), (PyObject*)0) : \\
        (likely((obj)->ob_type->tp_as_mapping) ? (PySequence_GetSlice(obj, a, b)) : \\
            (PyErr_Format(PyExc_TypeError, "'%.200s' object is unsliceable", (obj)->ob_type->tp_name), (PyObject*)0)))
  #define __Pyx_PySequence_SetSlice(obj, a, b, value) (unlikely(!(obj)) ? \\
        (PyErr_SetString(PyExc_SystemError, "null argument to internal routine"), -1) : \\
        (likely((obj)->ob_type->tp_as_mapping) ? (PySequence_SetSlice(obj, a, b, value)) : \\
            (PyErr_Format(PyExc_TypeError, "'%.200s' object doesn't support slice assignment", (obj)->ob_type->tp_name), -1)))
  #define __Pyx_PySequence_DelSlice(obj, a, b) (unlikely(!(obj)) ? \\
        (PyErr_SetString(PyExc_SystemError, "null argument to internal routine"), -1) : \\
        (likely((obj)->ob_type->tp_as_mapping) ? (PySequence_DelSlice(obj, a, b)) : \\
            (PyErr_Format(PyExc_TypeError, "'%.200s' object doesn't support slice deletion", (obj)->ob_type->tp_name), -1)))
#endif

#if PY_MAJOR_VERSION >= 3
  #define PyMethod_New(func, self, klass) ((self) ? PyMethod_New(func, self) : PyInstanceMethod_New(func))
#endif

#if PY_VERSION_HEX < 0x02050000
  #define __Pyx_GetAttrString(o,n)   PyObject_GetAttrString((o),((char *)(n)))
  #define __Pyx_SetAttrString(o,n,a) PyObject_SetAttrString((o),((char *)(n)),(a))
  #define __Pyx_DelAttrString(o,n)   PyObject_DelAttrString((o),((char *)(n)))
#else
  #define __Pyx_GetAttrString(o,n)   PyObject_GetAttrString((o),(n))
  #define __Pyx_SetAttrString(o,n,a) PyObject_SetAttrString((o),(n),(a))
  #define __Pyx_DelAttrString(o,n)   PyObject_DelAttrString((o),(n))
#endif

#if PY_VERSION_HEX < 0x02050000
  #define __Pyx_NAMESTR(n) ((char *)(n))
  #define __Pyx_DOCSTR(n)  ((char *)(n))
#else
  #define __Pyx_NAMESTR(n) (n)
  #define __Pyx_DOCSTR(n)  (n)
#endif
""")

        code.putln("")
        self.generate_extern_c_macro_definition(code)
        code.putln("")
        code.putln("#if defined(WIN32) || defined(MS_WINDOWS)")
        code.putln("#define _USE_MATH_DEFINES")
        code.putln("#endif")
        code.putln("#include <math.h>")
        code.putln("#define %s" % Naming.api_guard_prefix + self.api_name(env))
        self.generate_includes(env, cimported_modules, code)
        code.putln("")
        code.putln("#ifdef PYREX_WITHOUT_ASSERTIONS")
        code.putln("#define CYTHON_WITHOUT_ASSERTIONS")
        code.putln("#endif")
        code.putln("")
        if env.directives['ccomplex']:
            code.putln("")
            code.putln("#if !defined(CYTHON_CCOMPLEX)")
            code.putln("#define CYTHON_CCOMPLEX 1")
            code.putln("#endif")
            code.putln("")
        code.put(Nodes.utility_function_predeclarations)
        code.put(PyrexTypes.type_conversion_predeclarations)
        code.put(Nodes.branch_prediction_macros)
        code.putln('')
        code.putln('static PyObject *%s;' % env.module_cname)
        code.putln('static PyObject *%s;' % Naming.builtins_cname)
        code.putln('static PyObject *%s;' % Naming.empty_tuple)
        code.putln('static PyObject *%s;' % Naming.empty_bytes)
        if Options.pre_import is not None:
            code.putln('static PyObject *%s;' % Naming.preimport_cname)
        code.putln('static int %s;' % Naming.lineno_cname)
        code.putln('static int %s = 0;' % Naming.clineno_cname)
        code.putln('static const char * %s= %s;' % (Naming.cfilenm_cname, Naming.file_c_macro))
        code.putln('static const char *%s;' % Naming.filename_cname)

        # XXX this is a mess
        for utility_code in PyrexTypes.c_int_from_py_function.specialize_list:
            env.use_utility_code(utility_code)
        for utility_code in PyrexTypes.c_long_from_py_function.specialize_list:
            env.use_utility_code(utility_code)

    def generate_extern_c_macro_definition(self, code):
        name = Naming.extern_c_macro
        code.putln("#ifdef __cplusplus")
        code.putln('#define %s extern "C"' % name)
        code.putln("#else")
        code.putln("#define %s extern" % name)
        code.putln("#endif")

    def generate_includes(self, env, cimported_modules, code):
        includes = []
        for filename in env.include_files:
            byte_decoded_filenname = str(filename)
            if byte_decoded_filenname[0] == '<' and byte_decoded_filenname[-1] == '>':
                code.putln('#include %s' % byte_decoded_filenname)
            else:
                code.putln('#include "%s"' % byte_decoded_filenname)

    def generate_filename_table(self, code):
        code.putln("")
        code.putln("static const char *%s[] = {" % Naming.filetable_cname)
        if code.globalstate.filename_list:
            for source_desc in code.globalstate.filename_list:
                filename = os.path.basename(source_desc.get_filenametable_entry())
                escaped_filename = filename.replace("\\", "\\\\").replace('"', r'\"')
                code.putln('"%s",' % escaped_filename)
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
                    self.generate_objstruct_definition(type, code)

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
        if base_type.is_numeric:
            writer = code.globalstate['numeric_typedefs']
        else:
            writer = code
        writer.putln("")
        writer.putln("typedef %s;" % base_type.declaration_code(entry.cname))

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
            kind = type.kind
            packed = type.is_struct and type.packed
            if packed:
                kind = "%s %s" % (type.kind, "__Pyx_PACKED")
                code.globalstate.use_utility_code(packed_struct_utility_code)
            header, footer = \
                self.sue_header_footer(type, kind, type.cname)
            code.putln("")
            if packed:
                code.putln("#if defined(__SUNPRO_C)")
                code.putln("  #pragma pack(1)")
                code.putln("#elif !defined(__GNUC__)")
                code.putln("  #pragma pack(push, 1)")
                code.putln("#endif")
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
            if packed:
                code.putln("#if defined(__SUNPRO_C)")
                code.putln("  #pragma pack()")
                code.putln("#elif !defined(__GNUC__)")
                code.putln("  #pragma pack(pop)")
                code.putln("#endif")

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
            # this does not really generate code, just builds the result value
            for value_entry in enum_values:
                if value_entry.value_node is not None:
                    value_entry.value_node.generate_evaluation_code(code)

            for value_entry in enum_values:
                if value_entry.value_node is None:
                    value_code = value_entry.cname
                else:
                    value_code = ("%s = %s" % (
                        value_entry.cname,
                        value_entry.value_node.result()))
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
                code.putln("%s DL_EXPORT(PyTypeObject) %s;" % (
                    Naming.extern_c_macro,
                    name))
            # ??? Do we really need the rest of this? ???
            #else:
            #    code.putln("staticforward PyTypeObject %s;" % name)

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

    def generate_objstruct_definition(self, type, code):
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
        if type.objtypedef_cname is not None:
            # Only for exposing public typedef name.
            code.putln("typedef struct %s %s;" % (type.objstruct_cname, type.objtypedef_cname))

    def generate_global_declarations(self, env, code, definition):
        code.putln("")
        for entry in env.c_class_entries:
            if definition or entry.defined_in_pxd:
                code.putln("static PyTypeObject *%s = 0;" %
                    entry.type.typeptr_cname)
        code.put_var_declarations(env.var_entries, static = 1,
            dll_linkage = "DL_EXPORT", definition = definition)

    def generate_cfunction_predeclarations(self, env, code, definition):
        for entry in env.cfunc_entries:
            if entry.inline_func_in_pxd or (not entry.in_cinclude and (definition
                    or entry.defined_in_pxd or entry.visibility == 'extern')):
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
                elif entry.visibility == 'public':
                    storage_class = ""
                else:
                    storage_class = "%s " % Naming.extern_c_macro
                if entry.func_modifiers:
                    modifiers = '%s ' % ' '.join([
                            modifier.upper() for modifier in entry.func_modifiers])
                else:
                    modifiers = ''
                code.putln("%s%s%s; /*proto*/" % (
                    storage_class,
                    modifiers,
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
                    if scope.defines_any(["__getslice__", "__setslice__", "__delslice__"]):
                        warning(self.pos, "__getslice__, __setslice__, and __delslice__ are not supported by Python 3, use __getitem__, __setitem__, and __delitem__ instead", 1)
                        code.putln("#if PY_MAJOR_VERSION >= 3")
                        code.putln("#error __getslice__, __setslice__, and __delslice__ not supported in Python 3.")
                        code.putln("#endif")
                    if scope.defines_any(["__setslice__", "__delslice__"]):
                        self.generate_ass_slice_function(scope, code)
                    if scope.defines_any(["__getattr__","__getattribute__"]):
                        self.generate_getattro_function(scope, code)
                    if scope.defines_any(["__setattr__", "__delattr__"]):
                        self.generate_setattro_function(scope, code)
                    if scope.defines_any(["__get__"]):
                        self.generate_descr_get_function(scope, code)
                    if scope.defines_any(["__set__", "__delete__"]):
                        self.generate_descr_set_function(scope, code)
                    self.generate_property_accessors(scope, code)
                    self.generate_method_table(scope, code)
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
        #    self.generate_self_cast(scope, code)
        if type.vtabslot_cname:
            vtab_base_type = type
            while vtab_base_type.base_type and vtab_base_type.base_type.vtabstruct_cname:
                vtab_base_type = vtab_base_type.base_type
            if vtab_base_type is not type:
                struct_type_cast = "(struct %s*)" % vtab_base_type.vtabstruct_cname
            else:
                struct_type_cast = ""
            code.putln("p->%s = %s%s;" % (
                type.vtabslot_cname,
                struct_type_cast, type.vtabptr_cname))
        for entry in py_attrs:
            if scope.is_internal or entry.name == "__weakref__":
                # internal classes do not need None inits
                code.putln("p->%s = 0;" % entry.cname)
            else:
                code.put_init_var_to_py_none(entry, "p->%s", nanny=False)
        entry = scope.lookup_here("__new__")
        if entry and entry.is_special:
            if entry.trivial_signature:
                cinit_args = "o, %s, NULL" % Naming.empty_tuple
            else:
                cinit_args = "o, a, k"
            code.putln(
                "if (%s(%s) < 0) {" %
                    (entry.func_cname, cinit_args))
            code.put_decref_clear("o", py_object_type, nanny=False);
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
            code.put_xdecref("p->%s" % entry.cname, entry.type, nanny=False)
        if base_type:
            tp_dealloc = TypeSlots.get_base_slot_function(scope, tp_slot)
            if tp_dealloc is None:
                tp_dealloc = "%s->tp_dealloc" % base_type.typeptr_cname
            code.putln(
                    "%s(o);" % tp_dealloc)
        else:
            code.putln(
                    "(*Py_TYPE(o)->tp_free)(o);")
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
                    "++Py_REFCNT(o);")
            code.putln(
                    "%s(o);" %
                        entry.func_cname)
            code.putln(
                    "if (PyErr_Occurred()) PyErr_WriteUnraisable(o);")
            code.putln(
                    "--Py_REFCNT(o);")
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
            code.put_init_to_py_none(name, entry.type, nanny=False)
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
                "r = Py_TYPE(o)->tp_as_mapping->mp_subscript(o, x);")
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
                    '  "Subscript assignment not supported by %s", Py_TYPE(o)->tp_name);')
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
                    '  "Subscript deletion not supported by %s", Py_TYPE(o)->tp_name);')
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
                    '  "2-element slice assignment not supported by %s", Py_TYPE(o)->tp_name);')
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
                    '  "2-element slice deletion not supported by %s", Py_TYPE(o)->tp_name);')
            code.putln(
                    "return -1;")
        code.putln(
                "}")
        code.putln(
            "}")

    def generate_getattro_function(self, scope, code):
        # First try to get the attribute using __getattribute__, if defined, or
        # PyObject_GenericGetAttr.
        #
        # If that raises an AttributeError, call the __getattr__ if defined.
        #
        # In both cases, defined can be in this class, or any base class.
        def lookup_here_or_base(n,type=None):
            # Recursive lookup
            if type is None:
                type = scope.parent_type
            r = type.scope.lookup_here(n)
            if r is None and \
               type.base_type is not None:
                return lookup_here_or_base(n,type.base_type)
            else:
                return r
        getattr_entry = lookup_here_or_base("__getattr__")
        getattribute_entry = lookup_here_or_base("__getattribute__")
        code.putln("")
        code.putln(
            "static PyObject *%s(PyObject *o, PyObject *n) {"
                % scope.mangle_internal("tp_getattro"))
        if getattribute_entry is not None:
            code.putln(
                "PyObject *v = %s(o, n);" %
                    getattribute_entry.func_cname)
        else:
            code.putln(
                "PyObject *v = PyObject_GenericGetAttr(o, n);")
        if getattr_entry is not None:
            code.putln(
                "if (!v && PyErr_ExceptionMatches(PyExc_AttributeError)) {")
            code.putln(
                "PyErr_Clear();")
            code.putln(
                "v = %s(o, n);" %
                    getattr_entry.func_cname)
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
            header = "static PyTypeObject %s = {"
        #code.putln(header % scope.parent_type.typeobj_cname)
        code.putln(header % type.typeobj_cname)
        code.putln(
            "PyVarObject_HEAD_INIT(0, 0)")
        code.putln(
            '__Pyx_NAMESTR("%s.%s"), /*tp_name*/' % (
                self.full_module_name, scope.class_name))
        if type.typedef_flag:
            objstruct = type.objstruct_cname
        else:
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
            "static PyMethodDef %s[] = {" %
                env.method_table_cname)
        for entry in env.pyfunc_entries:
            code.put_pymethoddef(entry, ",")
        code.putln(
                "{0, 0, 0, 0}")
        code.putln(
            "};")

    def generate_getset_table(self, env, code):
        if env.property_entries:
            code.putln("")
            code.putln(
                "static struct PyGetSetDef %s[] = {" %
                    env.getset_table_cname)
            for entry in env.property_entries:
                if entry.doc:
                    doc_code = "__Pyx_DOCSTR(%s)" % code.get_string_const(entry.doc)
                else:
                    doc_code = "0"
                code.putln(
                    '{(char *)"%s", %s, %s, %s, 0},' % (
                        entry.name,
                        entry.getter_cname or "0",
                        entry.setter_cname or "0",
                        doc_code))
            code.putln(
                    "{0, 0, 0, 0, 0}")
            code.putln(
                "};")

    def generate_import_star(self, env, code):
        env.use_utility_code(streq_utility_code)
        code.putln()
        code.putln("char* %s_type_names[] = {" % Naming.import_star)
        for name, entry in env.entries.items():
            if entry.is_type:
                code.putln('"%s",' % name)
        code.putln("0")
        code.putln("};")
        code.putln()
        code.enter_cfunc_scope() # as we need labels
        code.putln("static int %s(PyObject *o, PyObject* py_name, char *name) {" % Naming.import_star_set)
        code.putln("char** type_name = %s_type_names;" % Naming.import_star)
        code.putln("while (*type_name) {")
        code.putln("if (__Pyx_StrEq(name, *type_name)) {")
        code.putln('PyErr_Format(PyExc_TypeError, "Cannot overwrite C type %s", name);')
        code.putln('goto bad;')
        code.putln("}")
        code.putln("type_name++;")
        code.putln("}")
        old_error_label = code.new_error_label()
        code.putln("if (0);") # so the first one can be "else if"
        for name, entry in env.entries.items():
            if entry.is_cglobal and entry.used:
                code.putln('else if (__Pyx_StrEq(name, "%s")) {' % name)
                if entry.type.is_pyobject:
                    if entry.type.is_extension_type or entry.type.is_builtin_type:
                        code.putln("if (!(%s)) %s;" % (
                            entry.type.type_test_code("o"),
                            code.error_goto(entry.pos)))
                    code.putln("Py_INCREF(o);")
                    code.put_decref(entry.cname, entry.type, nanny=False)
                    code.putln("%s = %s;" % (
                        entry.cname,
                        PyrexTypes.typecast(entry.type, py_object_type, "o")))
                elif entry.type.from_py_function:
                    rhs = "%s(o)" % entry.type.from_py_function
                    if entry.type.is_enum:
                        rhs = PyrexTypes.typecast(entry.type, PyrexTypes.c_long_type, rhs)
                    code.putln("%s = %s; if (%s) %s;" % (
                        entry.cname,
                        rhs,
                        entry.type.error_condition(entry.cname),
                        code.error_goto(entry.pos)))
                else:
                    code.putln('PyErr_Format(PyExc_TypeError, "Cannot convert Python object %s to %s");' % (name, entry.type))
                    code.putln(code.error_goto(entry.pos))
                code.putln("}")
        code.putln("else {")
        code.putln("if (PyObject_SetAttr(%s, py_name, o) < 0) goto bad;" % Naming.module_cname)
        code.putln("}")
        code.putln("return 0;")
        if code.label_used(code.error_label):
            code.put_label(code.error_label)
            # This helps locate the offending name.
            code.putln('__Pyx_AddTraceback("%s");' % self.full_module_name);
        code.error_label = old_error_label
        code.putln("bad:")
        code.putln("return -1;")
        code.putln("}")
        code.putln(import_star_utility_code)
        code.exit_cfunc_scope() # done with labels

    def generate_module_init_func(self, imported_modules, env, code):
        code.enter_cfunc_scope()
        code.putln("")
        header2 = "PyMODINIT_FUNC init%s(void)" % env.module_name
        header3 = "PyMODINIT_FUNC PyInit_%s(void)" % env.module_name
        code.putln("#if PY_MAJOR_VERSION < 3")
        code.putln("%s; /*proto*/" % header2)
        code.putln(header2)
        code.putln("#else")
        code.putln("%s; /*proto*/" % header3)
        code.putln(header3)
        code.putln("#endif")
        code.putln("{")
        tempdecl_code = code.insertion_point()

        code.putln("#if CYTHON_REFNANNY")
        code.putln("void* __pyx_refnanny = NULL;")
        code.putln("__Pyx_RefNanny = __Pyx_RefNannyImportAPI(\"refnanny\");")
        code.putln("if (!__Pyx_RefNanny) {")
        code.putln("  PyErr_Clear();")
        code.putln("  __Pyx_RefNanny = __Pyx_RefNannyImportAPI(\"Cython.Runtime.refnanny\");")
        code.putln("  if (!__Pyx_RefNanny)")
        code.putln("      Py_FatalError(\"failed to import 'refnanny' module\");")
        code.putln("}")
        code.putln("__pyx_refnanny = __Pyx_RefNanny->SetupContext(\"%s\", __LINE__, __FILE__);"% header3)
        code.putln("#endif")

        code.putln("%s = PyTuple_New(0); %s" % (Naming.empty_tuple, code.error_goto_if_null(Naming.empty_tuple, self.pos)));
        code.putln("%s = PyBytes_FromStringAndSize(\"\", 0); %s" % (Naming.empty_bytes, code.error_goto_if_null(Naming.empty_bytes, self.pos)));

        code.putln("#ifdef %s_USED" % Naming.binding_cfunc)
        code.putln("if (%s_init() < 0) %s" % (Naming.binding_cfunc, code.error_goto(self.pos)))
        code.putln("#endif")

        code.putln("/*--- Library function declarations ---*/")
        env.generate_library_function_declarations(code)

        code.putln("/*--- Threads initialization code ---*/")
        code.putln("#if defined(__PYX_FORCE_INIT_THREADS) && __PYX_FORCE_INIT_THREADS")
        code.putln("#ifdef WITH_THREAD /* Python build with threading support? */")
        code.putln("PyEval_InitThreads();")
        code.putln("#endif")
        code.putln("#endif")

        code.putln("/*--- Module creation code ---*/")
        self.generate_module_creation_code(env, code)

        code.putln("/*--- Initialize various global constants etc. ---*/")
        code.putln(code.error_goto_if_neg("__Pyx_InitGlobals()", self.pos))

        __main__name = code.globalstate.get_py_string_const(
            EncodedString("__main__"), identifier=True)
        code.putln("if (%s%s) {" % (Naming.module_is_main, self.full_module_name.replace('.', '__')))
        code.putln(
            'if (__Pyx_SetAttrString(%s, "__name__", %s) < 0) %s;' % (
                env.module_cname,
                __main__name.cname,
                code.error_goto(self.pos)))
        code.putln("}")

        if Options.cache_builtins:
            code.putln("/*--- Builtin init code ---*/")
            code.putln(code.error_goto_if_neg("__Pyx_InitCachedBuiltins()", self.pos))

        code.putln("/*--- Constants init code ---*/")
        code.putln(code.error_goto_if_neg("__Pyx_InitCachedConstants()", self.pos))

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
            # this should be replaced by the module's tp_clear in Py3
            env.use_utility_code(import_module_utility_code)
            code.putln("if (__Pyx_RegisterCleanup()) %s;" % code.error_goto(self.pos))

        code.put_goto(code.return_label)
        code.put_label(code.error_label)
        for cname, type in code.funcstate.all_managed_temps():
            code.put_xdecref(cname, type)
        code.putln('if (%s) {' % env.module_cname)
        code.putln('__Pyx_AddTraceback("init %s");' % env.qualified_name)
        env.use_utility_code(Nodes.traceback_utility_code)
        code.put_decref_clear(env.module_cname, py_object_type, nanny=False)
        code.putln('} else if (!PyErr_Occurred()) {')
        code.putln('PyErr_SetString(PyExc_ImportError, "init %s");' % env.qualified_name)
        code.putln('}')
        code.put_label(code.return_label)

        code.put_finish_refcount_context()

        code.putln("#if PY_MAJOR_VERSION < 3")
        code.putln("return;")
        code.putln("#else")
        code.putln("return %s;" % env.module_cname)
        code.putln("#endif")
        code.putln('}')

        tempdecl_code.put_temp_declarations(code.funcstate)

        code.exit_cfunc_scope()

    def generate_module_cleanup_func(self, env, code):
        if not Options.generate_cleanup_code:
            return
        code.globalstate.use_utility_code(register_cleanup_utility_code)
        code.putln('static PyObject *%s(CYTHON_UNUSED PyObject *self, CYTHON_UNUSED PyObject *unused) {' %
                   Naming.cleanup_cname)
        if Options.generate_cleanup_code >= 2:
            code.putln("/*--- Global cleanup code ---*/")
            rev_entries = list(env.var_entries)
            rev_entries.reverse()
            for entry in rev_entries:
                if entry.visibility != 'extern':
                    if entry.type.is_pyobject and entry.used:
                        code.putln("Py_DECREF(%s); %s = 0;" % (
                            code.entry_as_pyobject(entry), entry.cname))
        code.putln("__Pyx_CleanupGlobals();")
        if Options.generate_cleanup_code >= 3:
            code.putln("/*--- Type import cleanup code ---*/")
            for type, _ in env.types_imported.items():
                code.putln("Py_DECREF((PyObject *)%s);" % type.typeptr_cname)
        if Options.cache_builtins:
            code.putln("/*--- Builtin cleanup code ---*/")
            for entry in env.cached_builtins:
                code.put_decref_clear(entry.cname,
                                      PyrexTypes.py_object_type,
                                      nanny=False)
        code.putln("/*--- Intern cleanup code ---*/")
        code.put_decref_clear(Naming.empty_tuple,
                              PyrexTypes.py_object_type,
                              nanny=False)
#        for entry in env.pynum_entries:
#            code.put_decref_clear(entry.cname,
#                                  PyrexTypes.py_object_type,
#                                  nanny=False)
#        for entry in env.all_pystring_entries:
#            if entry.is_interned:
#                code.put_decref_clear(entry.pystring_cname,
#                                      PyrexTypes.py_object_type,
#                                      nanny=False)
#        for entry in env.default_entries:
#            if entry.type.is_pyobject and entry.used:
#                code.putln("Py_DECREF(%s); %s = 0;" % (
#                    code.entry_as_pyobject(entry), entry.cname))
        code.putln("Py_INCREF(Py_None); return Py_None;")

    def generate_main_method(self, env, code):
        module_is_main = "%s%s" % (Naming.module_is_main, self.full_module_name.replace('.', '__'))
        code.globalstate.use_utility_code(main_method.specialize(module_name=env.module_name, module_is_main=module_is_main))

    def generate_pymoduledef_struct(self, env, code):
        if env.doc:
            doc = "__Pyx_DOCSTR(%s)" % code.get_string_const(env.doc)
        else:
            doc = "0"
        code.putln("")
        code.putln("#if PY_MAJOR_VERSION >= 3")
        code.putln("static struct PyModuleDef %s = {" % Naming.pymoduledef_cname)
        code.putln("  PyModuleDef_HEAD_INIT,")
        code.putln('  __Pyx_NAMESTR("%s"),' % env.module_name)
        code.putln("  %s, /* m_doc */" % doc)
        code.putln("  -1, /* m_size */")
        code.putln("  %s /* m_methods */," % env.method_table_cname)
        code.putln("  NULL, /* m_reload */")
        code.putln("  NULL, /* m_traverse */")
        code.putln("  NULL, /* m_clear */")
        code.putln("  NULL /* m_free */")
        code.putln("};")
        code.putln("#endif")

    def generate_module_creation_code(self, env, code):
        # Generate code to create the module object and
        # install the builtins.
        if env.doc:
            doc = "__Pyx_DOCSTR(%s)" % code.get_string_const(env.doc)
        else:
            doc = "0"
        code.putln("#if PY_MAJOR_VERSION < 3")
        code.putln(
            '%s = Py_InitModule4(__Pyx_NAMESTR("%s"), %s, %s, 0, PYTHON_API_VERSION);' % (
                env.module_cname,
                env.module_name,
                env.method_table_cname,
                doc))
        code.putln("#else")
        code.putln(
            "%s = PyModule_Create(&%s);" % (
                env.module_cname,
                Naming.pymoduledef_cname))
        code.putln("#endif")
        code.putln(
            "if (!%s) %s;" % (
                env.module_cname,
                code.error_goto(self.pos)));
        code.putln("#if PY_MAJOR_VERSION < 3")
        code.putln(
            "Py_INCREF(%s);" %
                env.module_cname)
        code.putln("#endif")
        code.putln(
            '%s = PyImport_AddModule(__Pyx_NAMESTR(__Pyx_BUILTIN_MODULE_NAME));' %
                Naming.builtins_cname)
        code.putln(
            "if (!%s) %s;" % (
                Naming.builtins_cname,
                code.error_goto(self.pos)));
        code.putln(
            'if (__Pyx_SetAttrString(%s, "__builtins__", %s) < 0) %s;' % (
                env.module_cname,
                Naming.builtins_cname,
                code.error_goto(self.pos)))
        if Options.pre_import is not None:
            code.putln(
                '%s = PyImport_AddModule(__Pyx_NAMESTR("%s"));' % (
                    Naming.preimport_cname,
                    Options.pre_import))
            code.putln(
                "if (!%s) %s;" % (
                    Naming.preimport_cname,
                    code.error_goto(self.pos)));

    def generate_global_init_code(self, env, code):
        # Generate code to initialise global PyObject *
        # variables to None.
        for entry in env.var_entries:
            if entry.visibility != 'extern':
                if entry.type.is_pyobject and entry.used:
                    code.put_init_var_to_py_none(entry, nanny=False)

    def generate_c_function_export_code(self, env, code):
        # Generate code to create PyCFunction wrappers for exported C functions.
        for entry in env.cfunc_entries:
            if entry.api or entry.defined_in_pxd:
                env.use_utility_code(function_export_utility_code)
                signature = entry.type.signature_string()
                code.putln('if (__Pyx_ExportFunction("%s", (void (*)(void))%s, "%s") < 0) %s' % (
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
            temp = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
            code.putln(
                '%s = __Pyx_ImportModule("%s"); if (!%s) %s' % (
                    temp,
                    module.qualified_name,
                    temp,
                    code.error_goto(self.pos)))
            for entry in entries:
                code.putln(
                    'if (__Pyx_ImportFunction(%s, "%s", (void (**)(void))&%s, "%s") < 0) %s' % (
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
        if base_type and base_type.module_name != env.qualified_name \
               and not base_type.is_builtin_type:
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
            env.use_utility_code(Nodes.get_vtable_utility_code)
            code.putln("%s = (struct %s*)__Pyx_GetVtable(%s->tp_dict); %s" % (
                type.vtabptr_cname,
                type.vtabstruct_cname,
                type.typeptr_cname,
                code.error_goto_if_null(type.vtabptr_cname, pos)))
        env.types_imported[type] = 1

    py3_type_name_map = {'str' : 'bytes', 'unicode' : 'str'}

    def generate_type_import_call(self, type, code, error_code):
        if type.typedef_flag:
            objstruct = type.objstruct_cname
        else:
            objstruct = "struct %s" % type.objstruct_cname
        module_name = type.module_name
        if module_name not in ('__builtin__', 'builtins'):
            module_name = '"%s"' % module_name
        else:
            module_name = '__Pyx_BUILTIN_MODULE_NAME'
        if type.name in self.py3_type_name_map:
            code.putln("#if PY_MAJOR_VERSION >= 3")
            code.putln('%s = __Pyx_ImportType(%s, "%s", sizeof(%s), 1); %s' % (
                    type.typeptr_cname,
                    module_name,
                    self.py3_type_name_map[type.name],
                    objstruct,
                    error_code))
            code.putln("#else")
        code.putln('%s = __Pyx_ImportType(%s, "%s", sizeof(%s), %i); %s' % (
                type.typeptr_cname,
                module_name,
                type.name,
                objstruct,
                not type.is_external or type.is_subclassed,
                error_code))
        if type.name in self.py3_type_name_map:
            code.putln("#endif")

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
                # Fix special method docstrings. This is a bit of a hack, but
                # unless we let PyType_Ready create the slot wrappers we have
                # a significant performance hit. (See trac #561.)
                for func in entry.type.scope.pyfunc_entries:
                    if func.is_special and Options.docstrings and func.wrapperbase_cname:
                        code.putln("{")
                        code.putln(
                            'PyObject *wrapper = __Pyx_GetAttrString((PyObject *)&%s, "%s"); %s' % (
                                typeobj_cname,
                                func.name,
                                code.error_goto_if_null('wrapper', entry.pos)))
                        code.putln(
                            "if (Py_TYPE(wrapper) == &PyWrapperDescr_Type) {")
                        code.putln(
                            "%s = *((PyWrapperDescrObject *)wrapper)->d_base;" % (
                                func.wrapperbase_cname))
                        code.putln(
                            "%s.doc = %s;" % (func.wrapperbase_cname, func.doc_cname))
                        code.putln(
                            "((PyWrapperDescrObject *)wrapper)->d_base = &%s;" % (
                                func.wrapperbase_cname))
                        code.putln("}")
                        code.putln("}")
                if type.vtable_cname:
                    code.putln(
                        "if (__Pyx_SetVtable(%s.tp_dict, %s) < 0) %s" % (
                            typeobj_cname,
                            type.vtabptr_cname,
                            code.error_goto(entry.pos)))
                    env.use_utility_code(Nodes.set_vtable_utility_code)
                if not type.scope.is_internal and not type.scope.directives['internal']:
                    # scope.is_internal is set for types defined by
                    # Cython (such as closures), the 'internal'
                    # directive is set by users
                    code.putln(
                        'if (__Pyx_SetAttrString(%s, "%s", (PyObject *)&%s) < 0) %s' % (
                            Naming.module_cname,
                            scope.class_name,
                            typeobj_cname,
                            code.error_goto(entry.pos)))
                weakref_entry = scope.lookup_here("__weakref__")
                if weakref_entry:
                    if weakref_entry.type is py_object_type:
                        tp_weaklistoffset = "%s.tp_weaklistoffset" % typeobj_cname
                        if type.typedef_flag:
                            objstruct = type.objstruct_cname
                        else:
                            objstruct = "struct %s" % type.objstruct_cname
                        code.putln("if (%s == 0) %s = offsetof(%s, %s);" % (
                            tp_weaklistoffset,
                            tp_weaklistoffset,
                            objstruct,
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

            c_method_entries = [
                entry for entry in type.scope.cfunc_entries
                if entry.func_cname ]
            if c_method_entries:
                for meth_entry in c_method_entries:
                    cast = meth_entry.type.signature_cast_string()
                    code.putln(
                        "%s.%s = %s%s;" % (
                            type.vtable_cname,
                            meth_entry.cname,
                            cast,
                            meth_entry.func_cname))

    def generate_typeptr_assignment_code(self, entry, code):
        # Generate code to initialise the typeptr of an extension
        # type defined in this module to point to its type object.
        type = entry.type
        if type.typeobj_cname:
            code.putln(
                "%s = &%s;" % (
                    type.typeptr_cname, type.typeobj_cname))

#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

streq_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE int __Pyx_StrEq(const char *, const char *); /*proto*/
""",
impl = """
static CYTHON_INLINE int __Pyx_StrEq(const char *s1, const char *s2) {
     while (*s1 != '\\0' && *s1 == *s2) { s1++; s2++; }
     return *s1 == *s2;
}
""")

#------------------------------------------------------------------------------------

import_module_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_ImportModule(const char *name); /*proto*/
""",
impl = """
#ifndef __PYX_HAVE_RT_ImportModule
#define __PYX_HAVE_RT_ImportModule
static PyObject *__Pyx_ImportModule(const char *name) {
    PyObject *py_name = 0;
    PyObject *py_module = 0;

    #if PY_MAJOR_VERSION < 3
    py_name = PyString_FromString(name);
    #else
    py_name = PyUnicode_FromString(name);
    #endif
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
""")

#------------------------------------------------------------------------------------

type_import_utility_code = UtilityCode(
proto = """
static PyTypeObject *__Pyx_ImportType(const char *module_name, const char *class_name, long size, int strict);  /*proto*/
""",
impl = """
#ifndef __PYX_HAVE_RT_ImportType
#define __PYX_HAVE_RT_ImportType
static PyTypeObject *__Pyx_ImportType(const char *module_name, const char *class_name,
    long size, int strict)
{
    PyObject *py_module = 0;
    PyObject *result = 0;
    PyObject *py_name = 0;
    char warning[200];

    py_module = __Pyx_ImportModule(module_name);
    if (!py_module)
        goto bad;
    #if PY_MAJOR_VERSION < 3
    py_name = PyString_FromString(class_name);
    #else
    py_name = PyUnicode_FromString(class_name);
    #endif
    if (!py_name)
        goto bad;
    result = PyObject_GetAttr(py_module, py_name);
    Py_DECREF(py_name);
    py_name = 0;
    Py_DECREF(py_module);
    py_module = 0;
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError,
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (!strict && ((PyTypeObject *)result)->tp_basicsize > size) {
        PyOS_snprintf(warning, sizeof(warning),
            "%s.%s size changed, may indicate binary incompatibility",
            module_name, class_name);
        #if PY_VERSION_HEX < 0x02050000
        PyErr_Warn(NULL, warning);
        #else
        PyErr_WarnEx(NULL, warning, 0);
        #endif
    }
    else if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError,
            "%s.%s has the wrong size, try recompiling",
            module_name, class_name);
        goto bad;
    }
    return (PyTypeObject *)result;
bad:
    Py_XDECREF(py_module);
    Py_XDECREF(result);
    return 0;
}
#endif
""")

#------------------------------------------------------------------------------------

function_export_utility_code = UtilityCode(
proto = """
static int __Pyx_ExportFunction(const char *name, void (*f)(void), const char *sig); /*proto*/
""",
impl = r"""
static int __Pyx_ExportFunction(const char *name, void (*f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    union {
        void (*fp)(void);
        void *p;
    } tmp;

    d = PyObject_GetAttrString(%(MODULE)s, (char *)"%(API)s");
    if (!d) {
        PyErr_Clear();
        d = PyDict_New();
        if (!d)
            goto bad;
        Py_INCREF(d);
        if (PyModule_AddObject(%(MODULE)s, (char *)"%(API)s", d) < 0)
            goto bad;
    }
    tmp.fp = f;
#if PY_VERSION_HEX >= 0x02070000 && !(PY_MAJOR_VERSION==3&&PY_MINOR_VERSION==0)
    cobj = PyCapsule_New(tmp.p, sig, 0);
#else
    cobj = PyCObject_FromVoidPtrAndDesc(tmp.p, (void *)sig, 0);
#endif
    if (!cobj)
        goto bad;
    if (PyDict_SetItemString(d, name, cobj) < 0)
        goto bad;
    Py_DECREF(cobj);
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(cobj);
    Py_XDECREF(d);
    return -1;
}
""" % {'MODULE': Naming.module_cname, 'API': Naming.api_name}
)

function_import_utility_code = UtilityCode(
proto = """
static int __Pyx_ImportFunction(PyObject *module, const char *funcname, void (**f)(void), const char *sig); /*proto*/
""",
impl = """
#ifndef __PYX_HAVE_RT_ImportFunction
#define __PYX_HAVE_RT_ImportFunction
static int __Pyx_ImportFunction(PyObject *module, const char *funcname, void (**f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    union {
        void (*fp)(void);
        void *p;
    } tmp;

    d = PyObject_GetAttrString(module, (char *)"%(API)s");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, funcname);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%%s does not export expected C function %%s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
#if PY_VERSION_HEX >= 0x02070000 && !(PY_MAJOR_VERSION==3&&PY_MINOR_VERSION==0)
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C function %%s.%%s has wrong signature (expected %%s, got %%s)",
             PyModule_GetName(module), funcname, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    tmp.p = PyCapsule_GetPointer(cobj, sig);
#else
    {const char *desc, *s1, *s2;
    desc = (const char *)PyCObject_GetDesc(cobj);
    if (!desc)
        goto bad;
    s1 = desc; s2 = sig;
    while (*s1 != '\\0' && *s1 == *s2) { s1++; s2++; }
    if (*s1 != *s2) {
        PyErr_Format(PyExc_TypeError,
            "C function %%s.%%s has wrong signature (expected %%s, got %%s)",
             PyModule_GetName(module), funcname, sig, desc);
        goto bad;
    }
    tmp.p = PyCObject_AsVoidPtr(cobj);}
#endif
    *f = tmp.fp;
    if (!(*f))
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif
""" % dict(API = Naming.api_name)
)

#------------------------------------------------------------------------------------

register_cleanup_utility_code = UtilityCode(
proto = """
static int __Pyx_RegisterCleanup(void); /*proto*/
static PyObject* %(module_cleanup)s(CYTHON_UNUSED PyObject *self, CYTHON_UNUSED PyObject *unused); /*proto*/
static PyMethodDef cleanup_def = {__Pyx_NAMESTR("__cleanup"), (PyCFunction)&%(module_cleanup)s, METH_NOARGS, 0};
""" % {'module_cleanup': Naming.cleanup_cname},
impl = """
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
    reg = __Pyx_GetAttrString(atexit, "register");
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
""")

import_star_utility_code = """

/* import_all_from is an unexposed function from ceval.c */

static int
__Pyx_import_all_from(PyObject *locals, PyObject *v)
{
    PyObject *all = __Pyx_GetAttrString(v, "__all__");
    PyObject *dict, *name, *value;
    int skip_leading_underscores = 0;
    int pos, err;

    if (all == NULL) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError))
            return -1; /* Unexpected error */
        PyErr_Clear();
        dict = __Pyx_GetAttrString(v, "__dict__");
        if (dict == NULL) {
            if (!PyErr_ExceptionMatches(PyExc_AttributeError))
                return -1;
            PyErr_SetString(PyExc_ImportError,
            "from-import-* object has no __dict__ and no __all__");
            return -1;
        }
        all = PyMapping_Keys(dict);
        Py_DECREF(dict);
        if (all == NULL)
            return -1;
        skip_leading_underscores = 1;
    }

    for (pos = 0, err = 0; ; pos++) {
        name = PySequence_GetItem(all, pos);
        if (name == NULL) {
            if (!PyErr_ExceptionMatches(PyExc_IndexError))
                err = -1;
            else
                PyErr_Clear();
            break;
        }
        if (skip_leading_underscores &&
#if PY_MAJOR_VERSION < 3
            PyString_Check(name) &&
            PyString_AS_STRING(name)[0] == '_')
#else
            PyUnicode_Check(name) &&
            PyUnicode_AS_UNICODE(name)[0] == '_')
#endif
        {
            Py_DECREF(name);
            continue;
        }
        value = PyObject_GetAttr(v, name);
        if (value == NULL)
            err = -1;
        else if (PyDict_CheckExact(locals))
            err = PyDict_SetItem(locals, name, value);
        else
            err = PyObject_SetItem(locals, name, value);
        Py_DECREF(name);
        Py_XDECREF(value);
        if (err != 0)
            break;
    }
    Py_DECREF(all);
    return err;
}


static int %(IMPORT_STAR)s(PyObject* m) {

    int i;
    int ret = -1;
    char* s;
    PyObject *locals = 0;
    PyObject *list = 0;
#if PY_MAJOR_VERSION >= 3
    PyObject *utf8_name = 0;
#endif
    PyObject *name;
    PyObject *item;

    locals = PyDict_New();              if (!locals) goto bad;
    if (__Pyx_import_all_from(locals, m) < 0) goto bad;
    list = PyDict_Items(locals);        if (!list) goto bad;

    for(i=0; i<PyList_GET_SIZE(list); i++) {
        name = PyTuple_GET_ITEM(PyList_GET_ITEM(list, i), 0);
        item = PyTuple_GET_ITEM(PyList_GET_ITEM(list, i), 1);
#if PY_MAJOR_VERSION >= 3
        utf8_name = PyUnicode_AsUTF8String(name);
        if (!utf8_name) goto bad;
        s = PyBytes_AS_STRING(utf8_name);
        if (%(IMPORT_STAR_SET)s(item, name, s) < 0) goto bad;
        Py_DECREF(utf8_name); utf8_name = 0;
#else
        s = PyString_AsString(name);
        if (!s) goto bad;
        if (%(IMPORT_STAR_SET)s(item, name, s) < 0) goto bad;
#endif
    }
    ret = 0;

bad:
    Py_XDECREF(locals);
    Py_XDECREF(list);
#if PY_MAJOR_VERSION >= 3
    Py_XDECREF(utf8_name);
#endif
    return ret;
}
""" % {'IMPORT_STAR'     : Naming.import_star,
       'IMPORT_STAR_SET' : Naming.import_star_set }

refnanny_utility_code = UtilityCode(proto="""
#ifndef CYTHON_REFNANNY
  #define CYTHON_REFNANNY 0
#endif

#if CYTHON_REFNANNY
  typedef struct {
    void (*INCREF)(void*, PyObject*, int);
    void (*DECREF)(void*, PyObject*, int);
    void (*GOTREF)(void*, PyObject*, int);
    void (*GIVEREF)(void*, PyObject*, int);
    void* (*SetupContext)(const char*, int, const char*);
    void (*FinishContext)(void**);
  } __Pyx_RefNannyAPIStruct;
  static __Pyx_RefNannyAPIStruct *__Pyx_RefNanny = NULL;
  static __Pyx_RefNannyAPIStruct * __Pyx_RefNannyImportAPI(const char *modname) {
    PyObject *m = NULL, *p = NULL;
    void *r = NULL;
    m = PyImport_ImportModule((char *)modname);
    if (!m) goto end;
    p = PyObject_GetAttrString(m, (char *)\"RefNannyAPI\");
    if (!p) goto end;
    r = PyLong_AsVoidPtr(p);
  end:
    Py_XDECREF(p);
    Py_XDECREF(m);
    return (__Pyx_RefNannyAPIStruct *)r;
  }
  #define __Pyx_RefNannySetupContext(name) \
          void *__pyx_refnanny = __Pyx_RefNanny->SetupContext((name), __LINE__, __FILE__)
  #define __Pyx_RefNannyFinishContext() \
          __Pyx_RefNanny->FinishContext(&__pyx_refnanny)
  #define __Pyx_INCREF(r) __Pyx_RefNanny->INCREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_DECREF(r) __Pyx_RefNanny->DECREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_GOTREF(r) __Pyx_RefNanny->GOTREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_GIVEREF(r) __Pyx_RefNanny->GIVEREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_XDECREF(r) do { if((r) != NULL) {__Pyx_DECREF(r);} } while(0)
#else
  #define __Pyx_RefNannySetupContext(name)
  #define __Pyx_RefNannyFinishContext()
  #define __Pyx_INCREF(r) Py_INCREF(r)
  #define __Pyx_DECREF(r) Py_DECREF(r)
  #define __Pyx_GOTREF(r)
  #define __Pyx_GIVEREF(r)
  #define __Pyx_XDECREF(r) Py_XDECREF(r)
#endif /* CYTHON_REFNANNY */
#define __Pyx_XGIVEREF(r) do { if((r) != NULL) {__Pyx_GIVEREF(r);} } while(0)
#define __Pyx_XGOTREF(r) do { if((r) != NULL) {__Pyx_GOTREF(r);} } while(0)
""")


main_method = UtilityCode(
impl = """
#ifdef __FreeBSD__
#include <floatingpoint.h>
#endif

#if PY_MAJOR_VERSION < 3
int main(int argc, char** argv) {
#elif defined(WIN32) || defined(MS_WINDOWS)
int wmain(int argc, wchar_t **argv) {
#else
static int __Pyx_main(int argc, wchar_t **argv) {
#endif
    int r = 0;
    PyObject* m = NULL;
    /* 754 requires that FP exceptions run in "no stop" mode by default,
     * and until C vendors implement C99's ways to control FP exceptions,
     * Python requires non-stop mode.  Alas, some platforms enable FP
     * exceptions by default.  Here we disable them.
     */
#ifdef __FreeBSD__
    fp_except_t m;

    m = fpgetmask();
    fpsetmask(m & ~FP_X_OFL);
#endif
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    PySys_SetArgv(argc, argv);
    %(module_is_main)s = 1;
#if PY_MAJOR_VERSION < 3
        init%(module_name)s();
#else
        m = PyInit_%(module_name)s();
#endif
    if (PyErr_Occurred() != NULL) {
        r = 1;
        PyErr_Print(); /* This exits with the right code if SystemExit. */
#if PY_MAJOR_VERSION < 3
        if (Py_FlushLine()) PyErr_Clear();
#endif
    }
    Py_XDECREF(m);
    Py_Finalize();
    return r;
}


#if PY_MAJOR_VERSION >= 3 && !defined(WIN32) && !defined(MS_WINDOWS)
#include <locale.h>

static wchar_t*
__Pyx_char2wchar(char* arg)
{
	wchar_t *res;
#ifdef HAVE_BROKEN_MBSTOWCS
	/* Some platforms have a broken implementation of
	 * mbstowcs which does not count the characters that
	 * would result from conversion.  Use an upper bound.
	 */
	size_t argsize = strlen(arg);
#else
	size_t argsize = mbstowcs(NULL, arg, 0);
#endif
	size_t count;
	unsigned char *in;
	wchar_t *out;
#ifdef HAVE_MBRTOWC
	mbstate_t mbs;
#endif
	if (argsize != (size_t)-1) {
		res = (wchar_t *)malloc((argsize+1)*sizeof(wchar_t));
		if (!res)
			goto oom;
		count = mbstowcs(res, arg, argsize+1);
		if (count != (size_t)-1) {
			wchar_t *tmp;
			/* Only use the result if it contains no
			   surrogate characters. */
			for (tmp = res; *tmp != 0 &&
				     (*tmp < 0xd800 || *tmp > 0xdfff); tmp++)
				;
			if (*tmp == 0)
				return res;
		}
		free(res);
	}
	/* Conversion failed. Fall back to escaping with surrogateescape. */
#ifdef HAVE_MBRTOWC
	/* Try conversion with mbrtwoc (C99), and escape non-decodable bytes. */

	/* Overallocate; as multi-byte characters are in the argument, the
	   actual output could use less memory. */
	argsize = strlen(arg) + 1;
	res = malloc(argsize*sizeof(wchar_t));
	if (!res) goto oom;
	in = (unsigned char*)arg;
	out = res;
	memset(&mbs, 0, sizeof mbs);
	while (argsize) {
		size_t converted = mbrtowc(out, (char*)in, argsize, &mbs);
		if (converted == 0)
			/* Reached end of string; null char stored. */
			break;
		if (converted == (size_t)-2) {
			/* Incomplete character. This should never happen,
			   since we provide everything that we have -
			   unless there is a bug in the C library, or I
			   misunderstood how mbrtowc works. */
			fprintf(stderr, "unexpected mbrtowc result -2\\n");
			return NULL;
		}
		if (converted == (size_t)-1) {
			/* Conversion error. Escape as UTF-8b, and start over
			   in the initial shift state. */
			*out++ = 0xdc00 + *in++;
			argsize--;
			memset(&mbs, 0, sizeof mbs);
			continue;
		}
		if (*out >= 0xd800 && *out <= 0xdfff) {
			/* Surrogate character.  Escape the original
			   byte sequence with surrogateescape. */
			argsize -= converted;
			while (converted--)
				*out++ = 0xdc00 + *in++;
			continue;
		}
		/* successfully converted some bytes */
		in += converted;
		argsize -= converted;
		out++;
	}
#else
	/* Cannot use C locale for escaping; manually escape as if charset
	   is ASCII (i.e. escape all bytes > 128. This will still roundtrip
	   correctly in the locale's charset, which must be an ASCII superset. */
	res = malloc((strlen(arg)+1)*sizeof(wchar_t));
	if (!res) goto oom;
	in = (unsigned char*)arg;
	out = res;
	while(*in)
		if(*in < 128)
			*out++ = *in++;
		else
			*out++ = 0xdc00 + *in++;
	*out = 0;
#endif
	return res;
oom:
	fprintf(stderr, "out of memory\\n");
	return NULL;
}

int
main(int argc, char **argv)
{
	wchar_t **argv_copy = (wchar_t **)malloc(sizeof(wchar_t*)*argc);
	/* We need a second copies, as Python might modify the first one. */
	wchar_t **argv_copy2 = (wchar_t **)malloc(sizeof(wchar_t*)*argc);
	int i, res;
	char *oldloc;
	if (!argv_copy || !argv_copy2) {
		fprintf(stderr, "out of memory\\n");
		return 1;
	}
	oldloc = strdup(setlocale(LC_ALL, NULL));
	setlocale(LC_ALL, "");
	for (i = 0; i < argc; i++) {
		argv_copy2[i] = argv_copy[i] = __Pyx_char2wchar(argv[i]);
		if (!argv_copy[i])
			return 1;
	}
	setlocale(LC_ALL, oldloc);
	free(oldloc);
	res = __Pyx_main(argc, argv_copy);
	for (i = 0; i < argc; i++) {
		free(argv_copy2[i]);
	}
	free(argv_copy);
	free(argv_copy2);
	return res;
}
#endif
""")

packed_struct_utility_code = UtilityCode(proto="""
#if defined(__GNUC__)
#define __Pyx_PACKED __attribute__((__packed__))
#else
#define __Pyx_PACKED
#endif
""", impl="", proto_block='utility_code_proto_before_types')
