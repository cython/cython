#
#   Pyrex - Symbol Table
#

import re
from Errors import error, InternalError
import Options
import Naming
from PyrexTypes import c_int_type, \
    py_object_type, c_char_array_type, \
    CEnumType, CStructOrUnionType, PyExtensionType
from TypeSlots import \
    pyfunction_signature, pymethod_signature, \
    get_special_method_signature, get_property_accessor_signature

identifier_pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*$")

class Entry:
    # A symbol table entry in a Scope or ModuleNamespace.
    #
    # name             string     Python name of entity
    # cname            string     C name of entity
    # type             PyrexType  Type of entity
    # doc              string     Doc string
    # init             string     Initial value
    # visibility       'private' or 'public' or 'extern'
    # is_builtin       boolean    Is a Python builtin name
    # is_cglobal       boolean    Is a C global variable
    # is_pyglobal      boolean    Is a Python module-level variable
    #                               or class attribute during
    #                               class construction
    # is_variable      boolean    Is a variable
    # is_cfunction     boolean    Is a C function
    # is_cmethod       boolean    Is a C method of an extension type
    # is_type          boolean    Is a type definition
    # is_const         boolean    Is a constant
    # is_property      boolean    Is a property of an extension type:
    # doc_cname        string or None  C const holding the docstring
    # getter_cname     string          C func for getting property
    # setter_cname     string          C func for setting or deleting property
    # is_self_arg      boolean    Is the "self" arg of an exttype method
    # is_readonly      boolean    Can't be assigned to
    # func_cname       string     C func implementing Python func
    # pos              position   Source position where declared
    # namespace_cname  string     If is_pyglobal, the C variable
    #                               holding its home namespace
    # pymethdef_cname  string     PyMethodDef structure
    # signature        Signature  Arg & return types for Python func
    # init_to_none     boolean    True if initial value should be None
    # as_variable      Entry      Alternative interpretation of extension
    #                               type name as a variable
    # xdecref_cleanup  boolean    Use Py_XDECREF for error cleanup
    # in_cinclude      boolean    Suppress C declaration code
    # enum_values      [Entry]    For enum types, list of values
    # qualified_name   string     "modname.funcname" or "modname.classname"
    #                               or "modname.classname.funcname"
    # is_declared_generic  boolean  Is declared as PyObject * even though its
    #                                 type is an extension type
    # as_module        None       Module scope, if a cimported module
    # is_inherited     boolean    Is an inherited attribute of an extension type
    # interned_cname   string     C name of interned name string
    # pystring_cname   string     C name of Python version of string literal
    # is_interned      boolean    For string const entries, value is interned
    # used             boolean

    borrowed = 0
    init = ""
    visibility = 'private'
    is_builtin = 0
    is_cglobal = 0
    is_pyglobal = 0
    is_variable = 0
    is_cfunction = 0
    is_cmethod = 0
    is_type = 0
    is_const = 0
    is_property = 0
    doc_cname = None
    getter_cname = None
    setter_cname = None
    is_self_arg = 0
    is_declared_generic = 0
    is_readonly = 0
    func_cname = None
    doc = None
    init_to_none = 0
    as_variable = None
    xdecref_cleanup = 0
    in_cinclude = 0
    as_module = None
    is_inherited = 0
    interned_cname = None
    pystring_cname = None
    is_interned = 0
    used = 0
    
    def __init__(self, name, cname, type, pos = None, init = None):
        self.name = name
        self.cname = cname
        self.type = type
        self.pos = pos
        self.init = init


class Scope:
    # name              string             Unqualified name
    # outer_scope       Scope or None      Enclosing scope
    # entries           {string : Entry}   Python name to entry, non-types
    # const_entries     [Entry]            Constant entries
    # sue_entries       [Entry]            Struct/union/enum entries
    # arg_entries       [Entry]            Function argument entries
    # var_entries       [Entry]            User-defined variable entries
    # pyfunc_entries    [Entry]            Python function entries
    # cfunc_entries     [Entry]            C function entries
    # c_class_entries   [Entry]            All extension type entries
    # temp_entries      [Entry]            Temporary variable entries
    # free_temp_entries [Entry]            Temp variables currently unused
    # temp_counter      integer            Counter for naming temp vars
    # cname_to_entry    {string : Entry}   Temp cname to entry mapping
    # pow_function_used boolean            The C pow() function is used
    # return_type       PyrexType or None  Return type of function owning scope
    # is_py_class_scope boolean            Is a Python class scope
    # is_c_class_scope  boolean            Is an extension type scope
    # scope_prefix      string             Disambiguator for C names
    # in_cinclude       boolean            Suppress C declaration code
    # qualified_name    string             "modname" or "modname.classname"
    # pystring_entries  [Entry]            String const entries newly used as
    #                                        Python strings in this scope

    is_py_class_scope = 0
    is_c_class_scope = 0
    scope_prefix = ""
    in_cinclude = 0
    
    def __init__(self, name, outer_scope, parent_scope):
        # The outer_scope is the next scope in the lookup chain.
        # The parent_scope is used to derive the qualified name of this scope.
        self.name = name
        self.outer_scope = outer_scope
        self.parent_scope = parent_scope
        mangled_name = "%d%s_" % (len(name), name)
        qual_scope = self.qualifying_scope()
        if qual_scope:
            self.qualified_name = qual_scope.qualify_name(name)
            self.scope_prefix = qual_scope.scope_prefix + mangled_name
        else:
            self.qualified_name = name
            self.scope_prefix = mangled_name
        self.entries = {}
        self.const_entries = []
        self.sue_entries = []
        self.arg_entries = []
        self.var_entries = []
        self.pyfunc_entries = []
        self.cfunc_entries = []
        self.c_class_entries = []
        self.defined_c_classes = []
        self.imported_c_classes = {}
        self.temp_entries = []
        self.free_temp_entries = []
        #self.pending_temp_entries = [] # TEMPORARY
        self.temp_counter = 1
        self.cname_to_entry = {}
        self.pow_function_used = 0
        self.string_to_entry = {}
        self.pystring_entries = []
    
    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.qualified_name)
    
    def intern(self, name):
        return self.global_scope().intern(name)
    
    def qualifying_scope(self):
        return self.parent_scope
    
    def mangle(self, prefix, name = None):
        if name:
            return "%s%s%s" % (prefix, self.scope_prefix, name)
        else:
            return self.parent_scope.mangle(prefix, self.name)
    
    def mangle_internal(self, name):
        # Mangle an internal name so as not to clash with any
        # user-defined name in this scope.
        prefix = "%s%s_" % (Naming.pyrex_prefix, name)
        return self.mangle(prefix)
        #return self.parent_scope.mangle(prefix, self.name)
    
    def global_scope(self):
        # Return the module-level scope containing this scope.
        return self.outer_scope.global_scope()
    
    def declare(self, name, cname, type, pos):
        # Create new entry, and add to dictionary if
        # name is not None. Reports an error if already 
        # declared.
        dict = self.entries
        if name and dict.has_key(name):
            error(pos, "'%s' redeclared" % name)
        entry = Entry(name, cname, type, pos = pos)
        entry.in_cinclude = self.in_cinclude
        if name:
            entry.qualified_name = self.qualify_name(name)
            dict[name] = entry
        return entry
    
    def qualify_name(self, name):
        return "%s.%s" % (self.qualified_name, name)
    
    def declare_const(self, name, type, value, pos, cname = None):
        # Add an entry for a named constant.
        if not cname:
            if self.in_cinclude:
                cname = name
            else:
                cname = self.mangle(Naming.enum_prefix, name)
        entry = self.declare(name, cname, type, pos)
        entry.is_const = 1
        entry.value = value
        return entry
    
    def declare_type(self, name, type, pos, 
            cname = None, visibility = 'private'):
        # Add an entry for a type definition.
        if not cname:
            cname = name
        entry = self.declare(name, cname, type, pos)
        entry.visibility = visibility
        entry.is_type = 1
        return entry
        
    def declare_struct_or_union(self, name, kind, scope, 
            typedef_flag, pos, cname = None):
        # Add an entry for a struct or union definition.
        if not cname:
            if self.in_cinclude:
                cname = name
            else:
                cname = self.mangle(Naming.type_prefix, name)
        entry = self.lookup_here(name)
        if not entry:
            type = CStructOrUnionType(name, kind, scope, typedef_flag, cname)
            entry = self.declare_type(name, type, pos, cname)
            self.sue_entries.append(entry)
        else:
            if not (entry.is_type and entry.type.is_struct_or_union):
                error(pos, "'%s' redeclared" % name)
            elif scope and entry.type.scope:
                error(pos, "'%s' already defined" % name)
            else:
                self.check_previous_typedef_flag(entry, typedef_flag, pos)
                if scope:
                    entry.type.scope = scope
        if not scope and not entry.type.scope:
            self.check_for_illegal_incomplete_ctypedef(typedef_flag, pos)
        return entry
    
    def check_previous_typedef_flag(self, entry, typedef_flag, pos):
        if typedef_flag <> entry.type.typedef_flag:
            error(pos, "'%s' previously declared using '%s'" % (
                entry.name, ("cdef", "ctypedef")[entry.type.typedef_flag]))
    
    def declare_enum(self, name, pos, cname, typedef_flag):
        if name:
            if not cname:
                if self.in_cinclude:
                    cname = name
                else:
                    cname = self.mangle(Naming.type_prefix, name)
            type = CEnumType(name, cname, typedef_flag)
        else:
            type = c_int_type
        entry = self.declare_type(name, type, pos, cname = cname)
        entry.enum_values = []
        self.sue_entries.append(entry)
        return entry	
    
    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for a variable.
        if not cname:
            if visibility <> 'private':
                cname = name
            else:
                cname = self.mangle(Naming.var_prefix, name)
        entry = self.declare(name, cname, type, pos)
        entry.is_variable = 1
        entry.visibility = visibility
        return entry
        
    def declare_builtin(self, name, pos):
        return self.outer_scope.declare_builtin(name, pos)
    
    def declare_pyfunction(self, name, pos):
        # Add an entry for a Python function.
        entry = self.declare_var(name, py_object_type, pos)
        entry.signature = pyfunction_signature
        self.pyfunc_entries.append(entry)
        return entry
    
    def register_pyfunction(self, entry):
        self.pyfunc_entries.append(entry)
    
    def declare_cfunction(self, name, type, pos, 
            cname = None, visibility = 'private', defining = 0):
        # Add an entry for a C function.
        if not cname:
            if visibility <> 'private':
                cname = name
            else:
                cname = self.mangle(Naming.func_prefix, name)
        entry = self.add_cfunction(name, type, pos, cname, visibility)
        entry.func_cname = cname
        return entry
    
    def add_cfunction(self, name, type, pos, cname, visibility):
        # Add a C function entry without giving it a func_cname.
        entry = self.declare(name, cname, type, pos)
        entry.is_cfunction = 1
        entry.visibility = visibility
        self.cfunc_entries.append(entry)
        return entry
    
    def find(self, name, pos):
        # Look up name, report error if not found.
        entry = self.lookup(name)
        if entry:
            return entry
        else:
            error(pos, "'%s' is not declared" % name)
    
    def lookup(self, name):
        # Look up name in this scope or an enclosing one.
        # Return None if not found.
        return (self.lookup_here(name)
            or (self.outer_scope and self.outer_scope.lookup(name))
            or None)

    def lookup_here(self, name):
        # Look up in this scope only, return None if not found.
        return self.entries.get(name, None)
        
    def lookup_target(self, name):
        # Look up name in this scope only. Declare as Python
        # variable if not found.
        entry = self.lookup_here(name)
        if not entry:
            entry = self.declare_var(name, py_object_type, None)
        return entry
    
    def add_string_const(self, value):
        # Add an entry for a string constant.
        cname = self.new_const_cname()
        entry = Entry("", cname, c_char_array_type, init = value)
        entry.used = 1
        self.const_entries.append(entry)
        return entry
    
    def get_string_const(self, value):
        # Get entry for string constant. Returns an existing
        # one if possible, otherwise creates a new one.
        genv = self.global_scope()
        entry = genv.string_to_entry.get(value)
        if not entry:
            entry = self.add_string_const(value)
            genv.string_to_entry[value] = entry
        return entry
    
    def add_py_string(self, entry):
        # If not already done, allocate a C name for a Python version of
        # a string literal, and add it to the list of Python strings to
        # be created at module init time. If the string resembles a
        # Python identifier, it will be interned.
        if not entry.pystring_cname:
            value = entry.init
            if identifier_pattern.match(value):
                entry.pystring_cname = self.intern(value)
                entry.is_interned = 1
            else:
                entry.pystring_cname = entry.cname + "p"
                self.pystring_entries.append(entry)
                self.global_scope().all_pystring_entries.append(entry)
    
    def new_const_cname(self):
        # Create a new globally-unique name for a constant.
        return self.global_scope().new_const_cname()

    def allocate_temp(self, type):
        # Allocate a temporary variable of the given type from the 
        # free list if available, otherwise create a new one.
        # Returns the cname of the variable.
        for entry in self.free_temp_entries:
            if entry.type == type:
                self.free_temp_entries.remove(entry)
                return entry.cname
        n = self.temp_counter
        self.temp_counter = n + 1
        cname = "%s%d" % (Naming.pyrex_prefix, n)
        entry = Entry("", cname, type)
        entry.used = 1
        if type.is_pyobject:
            entry.init = "0"
        self.cname_to_entry[entry.cname] = entry
        self.temp_entries.append(entry)
        return entry.cname
    
    def allocate_temp_pyobject(self):
        # Allocate a temporary PyObject variable.
        return self.allocate_temp(py_object_type)

    def release_temp(self, cname):
        # Release a temporary variable for re-use.
        if not cname: # can happen when type of an expr is void
            return
        entry = self.cname_to_entry[cname]
        if entry in self.free_temp_entries:
            raise InternalError("Temporary variable %s released more than once"
                % cname)
        self.free_temp_entries.append(entry)
    
    def temps_in_use(self):
        # Return a new list of temp entries currently in use.
        return [entry for entry in self.temp_entries
            if entry not in self.free_temp_entries]
    
    #def recycle_pending_temps(self):
    #	# Obsolete
    #	pass

    def use_utility_code(self, new_code):
        self.global_scope().use_utility_code(new_code)
    
    def generate_library_function_declarations(self, code):
        # Generate extern decls for C library funcs used.
        #if self.pow_function_used:
        #	code.putln("%s double pow(double, double);" % Naming.extern_c_macro)
        pass
        
    def defines_any(self, names):
        # Test whether any of the given names are
        # defined in this scope.
        for name in names:
            if name in self.entries:	
                return 1
        return 0


class BuiltinScope(Scope):
    #  The builtin namespace.
    
    def __init__(self):
        Scope.__init__(self, "__builtin__", None, None)
    
    def declare_builtin(self, name, pos):
        entry = self.declare(name, name, py_object_type, pos)
        entry.is_builtin = 1
        return entry
    

class ModuleScope(Scope):
    # module_name          string             Python name of the module
    # module_cname         string             C name of Python module object
    # #module_dict_cname   string             C name of module dict object
    # method_table_cname   string             C name of method table
    # doc                  string             Module doc string
    # doc_cname            string             C name of module doc string
    # const_counter        integer            Counter for naming constants
    # utility_code_used    [string]           Utility code to be included
    # default_entries      [Entry]            Function argument default entries
    # python_include_files [string]           Standard  Python headers to be included
    # include_files        [string]           Other C headers to be included
    # string_to_entry      {string : Entry}   Map string const to entry
    # context              Context
    # parent_module        Scope              Parent in the import namespace
    # module_entries       {string : Entry}   For cimport statements
    # type_names           {string : 1}       Set of type names (used during parsing)
    # pxd_file_loaded      boolean            Corresponding .pxd file has been processed
    # cimported_modules    [ModuleScope]      Modules imported with cimport
    # intern_map           {string : string}  Mapping from Python names to interned strs
    # interned_names       [string]           Interned names pending generation of declarations
    # all_pystring_entries [Entry]            Python string consts from all scopes
    # types_imported       {PyrexType : 1}    Set of types for which import code generated

    def __init__(self, name, parent_module, context):
        self.parent_module = parent_module
        outer_scope = context.find_submodule("__builtin__")
        Scope.__init__(self, name, outer_scope, parent_module)
        self.module_name = name
        self.context = context
        self.module_cname = Naming.module_cname
        self.module_dict_cname = Naming.moddict_cname
        self.method_table_cname = Naming.methtable_cname
        self.doc = ""
        self.doc_cname = Naming.moddoc_cname
        self.const_counter = 1
        self.utility_code_used = []
        self.default_entries = []
        self.module_entries = {}
        self.python_include_files = ["Python.h", "structmember.h"]
        self.include_files = []
        self.type_names = {}
        self.pxd_file_loaded = 0
        self.cimported_modules = []
        self.intern_map = {}
        self.interned_names = []
        self.all_pystring_entries = []
        self.types_imported = {}
    
    def qualifying_scope(self):
        return self.parent_module
    
    def global_scope(self):
        return self
    
    def declare_builtin(self, name, pos):
        entry = Scope.declare_builtin(self, name, pos)
        entry.interned_cname = self.intern(name)
        return entry
    
    def intern(self, name):
        intern_map = self.intern_map
        cname = intern_map.get(name)
        if not cname:
            cname = Naming.interned_prefix + name
            intern_map[name] = cname
            self.interned_names.append(name)
        return cname

    def find_module(self, module_name, pos):
        # Find a module in the import namespace, interpreting
        # relative imports relative to this module's parent.
        # Finds and parses the module's .pxd file if the module
        # has not been referenced before.
        return self.global_scope().context.find_module(
            module_name, relative_to = self.parent_module, pos = pos)
    
    def find_submodule(self, name):
        # Find and return scope for a submodule of this module,
        # creating a new empty one if necessary. Doesn't parse .pxd.
        scope = self.lookup_submodule(name)
        if not scope:
            scope = ModuleScope(name, 
                parent_module = self, context = self.context)
            self.module_entries[name] = scope
        return scope
    
    def lookup_submodule(self, name):
        # Return scope for submodule of this module, or None.
        return self.module_entries.get(name, None)
    
    def add_include_file(self, filename):
        if filename not in self.python_include_files \
            and filename not in self.include_files:
                self.include_files.append(filename)
    
    def add_imported_module(self, scope):
        if scope not in self.cimported_modules:
            self.cimported_modules.append(scope)
    
    def add_imported_entry(self, name, entry, pos):
        if entry not in self.entries:
            self.entries[name] = entry
        else:
            error(pos, "'%s' redeclared" % name)
    
    def declare_module(self, name, scope, pos):
        # Declare a cimported module. This is represented as a
        # Python module-level variable entry with a module
        # scope attached to it. Reports an error and returns
        # None if previously declared as something else.
        entry = self.lookup_here(name)
        if entry:
            if entry.is_pyglobal and entry.as_module is scope:
                return entry # Already declared as the same module
            if not (entry.is_pyglobal and not entry.as_module):
                error(pos, "'%s' redeclared" % name)
                return None
        else:
            entry = self.declare_var(name, py_object_type, pos)
        entry.as_module = scope
        self.cimported_modules.append(scope)
        return entry
    
    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for a global variable. If it is a Python
        # object type, and not declared with cdef, it will live 
        # in the module dictionary, otherwise it will be a C 
        # global variable.
        entry = Scope.declare_var(self, name, type, pos, 
            cname, visibility, is_cdef)
        if not visibility in ('private', 'public', 'extern'):
            error(pos, "Module-level variable cannot be declared %s" % visibility)
        if not is_cdef:
            if not (type.is_pyobject and not type.is_extension_type):
                raise InternalError(
                    "Non-cdef global variable is not a generic Python object")
            entry.is_pyglobal = 1
            entry.namespace_cname = self.module_cname
            if Options.intern_names:
                entry.interned_cname = self.intern(name)
        else:
            entry.is_cglobal = 1
            self.var_entries.append(entry)
        return entry
    
    def declare_global(self, name, pos):
        entry = self.lookup_here(name)
        if not entry:
            self.declare_var(name, py_object_type, pos)
    
    def add_default_value(self, type):
        # Add an entry for holding a function argument
        # default value.
        cname = self.new_const_cname()
        entry = Entry("", cname, type)
        self.default_entries.append(entry)
        return entry
        
    def new_const_cname(self):
        # Create a new globally-unique name for a constant.
        n = self.const_counter
        self.const_counter = n + 1
        return "%s%d" % (Naming.const_prefix, n)
    
    def use_utility_code(self, new_code):
        #  Add string to list of utility code to be included,
        #  if not already there (tested using 'is').
        for old_code in self.utility_code_used:
            if old_code is new_code:
                return
        self.utility_code_used.append(new_code)
    
    def declare_c_class(self, name, pos, defining, implementing,
        module_name, base_type, objstruct_cname, typeobj_cname,
        visibility, typedef_flag):
        #
        #print "declare_c_class:", name
        #print "...visibility =", visibility
        #
        # Look for previous declaration as a type
        #
        entry = self.lookup_here(name)
        if entry:
            type = entry.type
            if not (entry.is_type and type.is_extension_type):
                entry = None # Will cause an error when we redeclare it
            else:
                self.check_previous_typedef_flag(entry, typedef_flag, pos)
                if base_type <> type.base_type:
                    error(pos, "Base type does not match previous declaration")
        #
        # Make a new entry if needed
        #
        if not entry:
            type = PyExtensionType(name, typedef_flag, base_type)
            if visibility == 'extern':
                type.module_name = module_name
            else:
                type.module_name = self.qualified_name
            type.typeptr_cname = self.mangle(Naming.typeptr_prefix, name)
            entry = self.declare_type(name, type, pos, visibility = visibility)
            if objstruct_cname:
                type.objstruct_cname = objstruct_cname
            elif not entry.in_cinclude:
                type.objstruct_cname = self.mangle(Naming.objstruct_prefix, name)				
            else:
                error(entry.pos, 
                    "Object name required for 'public' or 'extern' C class")
            self.attach_var_entry_to_c_class(entry)
            self.c_class_entries.append(entry)
        #
        # Check for re-definition and create scope if needed
        #
        if not type.scope:
            if defining or implementing:
                scope = CClassScope(name = name, outer_scope = self,
                    visibility = visibility)
                if base_type:
                    scope.declare_inherited_c_attributes(base_type.scope)
                type.set_scope(scope)
            else:
                self.check_for_illegal_incomplete_ctypedef(typedef_flag, pos)
        else:
            if defining and type.scope.defined:
                error(pos, "C class '%s' already defined" % name)
            elif implementing and type.scope.implemented:
                error(pos, "C class '%s' already implemented" % name)
        #
        # Fill in options, checking for compatibility with any previous declaration
        #
        if implementing:   # So that filenames in runtime exceptions refer to
            entry.pos = pos  # the .pyx file and not the .pxd file
        if entry.visibility <> visibility:
            error(pos, "Declaration of '%s' as '%s' conflicts with previous "
                "declaration as '%s'" % (class_name, visibility, entry.visibility))
        if objstruct_cname:
            if type.objstruct_cname and type.objstruct_cname <> objstruct_cname:
                error(pos, "Object struct name differs from previous declaration")
            type.objstruct_cname = objstruct_cname		
        if typeobj_cname:
            if type.typeobj_cname and type.typeobj_cname <> typeobj_cname:
                    error(pos, "Type object name differs from previous declaration")
            type.typeobj_cname = typeobj_cname
        #
        # Return new or existing entry	
        #
        return entry
    
    def check_for_illegal_incomplete_ctypedef(self, typedef_flag, pos):
        if typedef_flag and not self.in_cinclude:
            error(pos, "Forward-referenced type must use 'cdef', not 'ctypedef'")
    
    def allocate_vtable_names(self, entry):
        #  If extension type has a vtable, allocate vtable struct and
        #  slot names for it.
        type = entry.type
        if type.base_type and type.base_type.vtabslot_cname:
            #print "...allocating vtabslot_cname because base type has one" ###
            type.vtabslot_cname = "%s.%s" % (
                Naming.obj_base_cname, type.base_type.vtabslot_cname)
        elif type.scope and type.scope.cfunc_entries:
            #print "...allocating vtabslot_cname because there are C methods" ###
            type.vtabslot_cname = Naming.vtabslot_cname
        if type.vtabslot_cname:
            #print "...allocating other vtable related cnames" ###
            type.vtabstruct_cname = self.mangle(Naming.vtabstruct_prefix, entry.name)
            type.vtabptr_cname = self.mangle(Naming.vtabptr_prefix, entry.name)

    def check_c_classes(self):
        # Performs post-analysis checking and finishing up of extension types
        # being implemented in this module. This is called only for the main
        # .pyx file scope, not for cimported .pxd scopes.
        #
        # Checks all extension types declared in this scope to
        # make sure that:
        #
        #    * The extension type is implemented
        #    * All required object and type names have been specified or generated
        #    * All non-inherited C methods are implemented
        #
        # Also allocates a name for the vtable if needed.
        #
        debug_check_c_classes = 0
        if debug_check_c_classes:
            print "Scope.check_c_classes: checking scope", self.qualified_name
        for entry in self.c_class_entries:
            if debug_check_c_classes:
                print "...entry", entry.name, entry
                print "......type =", entry.type
                print "......visibility =", entry.visibility
            type = entry.type
            name = entry.name
            visibility = entry.visibility
            # Check defined
            if not type.scope:
                error(entry.pos, "C class '%s' is declared but not defined" % name)
            # Generate typeobj_cname
            if visibility <> 'extern' and not type.typeobj_cname:
                type.typeobj_cname = self.mangle(Naming.typeobj_prefix, name)
            ## Generate typeptr_cname
            #type.typeptr_cname = self.mangle(Naming.typeptr_prefix, name)
            # Check C methods defined
            if type.scope:
                for method_entry in type.scope.cfunc_entries:
                    if not method_entry.is_inherited and not method_entry.func_cname:
                        error(method_entry.pos, "C method '%s' is declared but not defined" %
                            method_entry.name)
            # Allocate vtable name if necessary
            if type.vtabslot_cname:
                #print "ModuleScope.check_c_classes: allocating vtable cname for", self ###
                type.vtable_cname = self.mangle(Naming.vtable_prefix, entry.name)
    
    def attach_var_entry_to_c_class(self, entry):
        # The name of an extension class has to serve as both a type
        # name and a variable name holding the type object. It is
        # represented in the symbol table by a type entry with a
        # variable entry attached to it. For the variable entry,
        # we use a read-only C global variable whose name is an
        # expression that refers to the type object.
        var_entry = Entry(name = entry.name,
            type = py_object_type,
            pos = entry.pos,
            cname = "((PyObject*)%s)" % entry.type.typeptr_cname)
        var_entry.is_variable = 1
        var_entry.is_cglobal = 1
        var_entry.is_readonly = 1
        entry.as_variable = var_entry
        

class LocalScope(Scope):

    def __init__(self, name, outer_scope):
        Scope.__init__(self, name, outer_scope, outer_scope)
    
    def mangle(self, prefix, name):
        return prefix + name

    def declare_arg(self, name, type, pos):
        # Add an entry for an argument of a function.
        cname = self.mangle(Naming.var_prefix, name)
        entry = self.declare(name, cname, type, pos)
        entry.is_variable = 1
        if type.is_pyobject:
            entry.init = "0"
        #entry.borrowed = 1 # Not using borrowed arg refs for now
        self.arg_entries.append(entry)
        return entry
    
    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for a local variable.
        if visibility in ('public', 'readonly'):
            error(pos, "Local variable cannot be declared %s" % visibility)
        entry = Scope.declare_var(self, name, type, pos, 
            cname, visibility, is_cdef)
        entry.init_to_none = type.is_pyobject
        self.var_entries.append(entry)
        return entry
    
    def declare_global(self, name, pos):
        # Pull entry from global scope into local scope.
        if self.lookup_here(name):
            error(pos, "'%s' redeclared")
        else:
            entry = self.global_scope().lookup_target(name)
            self.entries[name] = entry
        

class StructOrUnionScope(Scope):
    #  Namespace of a C struct or union.

    def __init__(self):
        Scope.__init__(self, "?", None, None)

    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for an attribute.
        if not cname:
            cname = name
        entry = self.declare(name, cname, type, pos)
        entry.is_variable = 1
        self.var_entries.append(entry)
        if type.is_pyobject:
            error(pos,
                "C struct/union member cannot be a Python object")
        if visibility <> 'private':
            error(pos,
                "C struct/union member cannot be declared %s" % visibility)
        return entry


class ClassScope(Scope):
    #  Abstract base class for namespace of
    #  Python class or extension type.
    #
    #  class_name     string   Pyrex name of the class
    #  scope_prefix   string   Additional prefix for names
    #                          declared in the class
    #  doc    string or None   Doc string

    def __init__(self, name, outer_scope):
        Scope.__init__(self, name, outer_scope, outer_scope)
        self.class_name = name
        self.doc = None

    def add_string_const(self, value):
        return self.outer_scope.add_string_const(value)


class PyClassScope(ClassScope):
    #  Namespace of a Python class.
    #
    #  class_dict_cname    string   C variable holding class dict
    #  class_obj_cname     string   C variable holding class object

    is_py_class_scope = 1
    
    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for a class attribute.
        entry = Scope.declare_var(self, name, type, pos, 
            cname, visibility, is_cdef)
        entry.is_pyglobal = 1
        entry.namespace_cname = self.class_obj_cname
        if Options.intern_names:
            entry.interned_cname = self.intern(name)
        return entry

    def allocate_temp(self, type):
        return self.outer_scope.allocate_temp(type)

    def release_temp(self, cname):
        self.outer_scope.release_temp(cname)

    #def recycle_pending_temps(self):
    #	self.outer_scope.recycle_pending_temps()

    def add_default_value(self, type):
        return self.outer_scope.add_default_value(type)


class CClassScope(ClassScope):
    #  Namespace of an extension type.
    #
    #  parent_type           CClassType
    #  #typeobj_cname        string or None
    #  #objstruct_cname      string
    #  method_table_cname    string
    #  member_table_cname    string
    #  getset_table_cname    string
    #  has_pyobject_attrs    boolean  Any PyObject attributes?
    #  public_attr_entries   boolean  public/readonly attrs
    #  property_entries      [Entry]
    #  defined               boolean  Defined in .pxd file
    #  implemented           boolean  Defined in .pyx file
    #  inherited_var_entries [Entry]  Adapted var entries from base class
    
    is_c_class_scope = 1
    
    def __init__(self, name, outer_scope, visibility):
        ClassScope.__init__(self, name, outer_scope)
        if visibility <> 'extern':
            self.method_table_cname = outer_scope.mangle(Naming.methtab_prefix, name)
            self.member_table_cname = outer_scope.mangle(Naming.memtab_prefix, name)
            self.getset_table_cname = outer_scope.mangle(Naming.gstab_prefix, name)
        self.has_pyobject_attrs = 0
        self.public_attr_entries = []
        self.property_entries = []
        self.inherited_var_entries = []
        self.defined = 0
        self.implemented = 0
    
    def needs_gc(self):
        # If the type or any of its base types have Python-valued
        # C attributes, then it needs to participate in GC.
        return self.has_pyobject_attrs or \
            (self.parent_type.base_type and \
                self.parent_type.base_type.scope.needs_gc())

    def declare_var(self, name, type, pos, 
            cname = None, visibility = 'private', is_cdef = 0):
        # Add an entry for an attribute.
        if self.defined:
            error(pos,
                "C attributes cannot be added in implementation part of"
                " extension type")
        if get_special_method_signature(name):
            error(pos, 
                "The name '%s' is reserved for a special method."
                    % name)
        if not cname:
            cname = name
        entry = self.declare(name, cname, type, pos)
        entry.visibility = visibility
        entry.is_variable = 1
        self.var_entries.append(entry)
        if type.is_pyobject:
            self.has_pyobject_attrs = 1
        if visibility not in ('private', 'public', 'readonly'):
            error(pos,
                "Attribute of extension type cannot be declared %s" % visibility)
        if visibility in ('public', 'readonly'):
            if type.pymemberdef_typecode:
                self.public_attr_entries.append(entry)
                if name == "__weakref__":
                    error(pos, "Special attribute __weakref__ cannot be exposed to Python")
            else:
                error(pos,
                    "C attribute of type '%s' cannot be accessed from Python" % type)
        if visibility == 'public' and type.is_extension_type:
            error(pos,
                "Non-generic Python attribute cannot be exposed for writing from Python")
        return entry

    def declare_pyfunction(self, name, pos):
        # Add an entry for a method.
        entry = self.declare(name, name, py_object_type, pos)
        special_sig = get_special_method_signature(name)
        if special_sig:
            entry.signature = special_sig
            # Special methods don't get put in the method table
        else:
            entry.signature = pymethod_signature
            self.pyfunc_entries.append(entry)
        return entry
            
    def declare_cfunction(self, name, type, pos,
            cname = None, visibility = 'private', defining = 0):
        if get_special_method_signature(name):
            error(pos, "Special methods must be declared with 'def', not 'cdef'")
        args = type.args
        if not args:
            error(pos, "C method has no self argument")
        elif not args[0].type.same_as(self.parent_type):
            error(pos, "Self argument of C method does not match parent type")
        entry = self.lookup_here(name)
        if entry:
            if not entry.is_cfunction:
                error(pos, "'%s' redeclared" % name)
            else:
                if defining and entry.func_cname:
                    error(pos, "'%s' already defined" % name)
                if not entry.type.same_as(type, as_cmethod = 1):
                    error(pos, "Signature does not match previous declaration")
        else:
            if self.defined:
                error(pos,
                    "C method '%s' not previously declared in definition part of"
                    " extension type" % name)
            entry = self.add_cfunction(name, type, pos, cname or name, visibility)
        if defining:
            entry.func_cname = self.mangle(Naming.func_prefix, name)
        return entry
        
    def add_cfunction(self, name, type, pos, cname, visibility):
        # Add a cfunction entry without giving it a func_cname.
        entry = ClassScope.add_cfunction(self, name, type, pos, cname, visibility)
        entry.is_cmethod = 1
        return entry
    
    def declare_property(self, name, doc, pos):
        entry = self.declare(name, name, py_object_type, pos)
        entry.is_property = 1
        entry.doc = doc
        entry.scope = PropertyScope(name, 
            outer_scope = self.global_scope(), parent_scope = self)
        entry.scope.parent_type = self.parent_type
        self.property_entries.append(entry)
        return entry
    
    def declare_inherited_c_attributes(self, base_scope):
        # Declare entries for all the C attributes of an
        # inherited type, with cnames modified appropriately
        # to work with this type.
        def adapt(cname):
            return "%s.%s" % (Naming.obj_base_cname, base_entry.cname)
        for base_entry in \
            base_scope.inherited_var_entries + base_scope.var_entries:
                entry = self.declare(base_entry.name, adapt(base_entry.cname), 
                    base_entry.type, None)
                entry.is_variable = 1
                self.inherited_var_entries.append(entry)
        for base_entry in base_scope.cfunc_entries:
            entry = self.add_cfunction(base_entry.name, base_entry.type, None,
                adapt(base_entry.cname), base_entry.visibility)
            entry.is_inherited = 1
    

class PropertyScope(Scope):
    #  Scope holding the __get__, __set__ and __del__ methods for
    #  a property of an extension type.
    #
    #  parent_type   PyExtensionType   The type to which the property belongs
    
    def declare_pyfunction(self, name, pos):
        # Add an entry for a method.
        signature = get_property_accessor_signature(name)
        if signature:
            entry = self.declare(name, name, py_object_type, pos)
            entry.signature = signature
            return entry
        else:
            error(pos, "Only __get__, __set__ and __del__ methods allowed "
                "in a property declaration")
            return None
