#
#   Pyrex - Code output module
#

import codecs
import Naming
import Options
from Cython.Utils import open_new_file, open_source_file
from PyrexTypes import py_object_type, typecast
import PyrexTypes
from TypeSlots import method_coexist
from Scanning import SourceDescriptor
from Cython.StringIOTree import StringIOTree
import DebugFlags
try:
    set
except NameError:
    from sets import Set as set
import DebugFlags

class FunctionState(object):
    # return_label     string          function return point label
    # error_label      string          error catch point label
    # continue_label   string          loop continue point label
    # break_label      string          loop break point label
    # return_from_error_cleanup_label string
    # label_counter    integer         counter for naming labels
    # in_try_finally   boolean         inside try of try...finally
    # exc_vars         (string * 3)    exception variables for reraise, or None

    # Not used for now, perhaps later
    def __init__(self, owner, names_taken=set()):
        self.names_taken = names_taken
        self.owner = owner
        
        self.error_label = None
        self.label_counter = 0
        self.labels_used = {}
        self.return_label = self.new_label()
        self.new_error_label()
        self.continue_label = None
        self.break_label = None

        self.in_try_finally = 0
        self.exc_vars = None

        self.temps_allocated = [] # of (name, type, manage_ref)
        self.temps_free = {} # (type, manage_ref) -> list of free vars with same type/managed status
        self.temps_used_type = {} # name -> (type, manage_ref)
        self.temp_counter = 0

    def new_label(self, name=None):
        n = self.label_counter
        self.label_counter = n + 1
        label = "%s%d" % (Naming.label_prefix, n)
        if name is not None:
            label += '_' + name
        return label
    
    def new_error_label(self):
        old_err_lbl = self.error_label
        self.error_label = self.new_label('error')
        return old_err_lbl
    
    def get_loop_labels(self):
        return (
            self.continue_label,
            self.break_label)
    
    def set_loop_labels(self, labels):
        (self.continue_label,
         self.break_label) = labels
    
    def new_loop_labels(self):
        old_labels = self.get_loop_labels()
        self.set_loop_labels(
            (self.new_label("continue"), 
             self.new_label("break")))
        return old_labels
    
    def get_all_labels(self):
        return (
            self.continue_label,
            self.break_label,
            self.return_label,
            self.error_label)

    def set_all_labels(self, labels):
        (self.continue_label,
         self.break_label,
         self.return_label,
         self.error_label) = labels

    def all_new_labels(self):
        old_labels = self.get_all_labels()
        new_labels = []
        for old_label in old_labels:
            if old_label:
                new_labels.append(self.new_label())
            else:
                new_labels.append(old_label)
        self.set_all_labels(new_labels)
        return old_labels
    
    def use_label(self, lbl):
        self.labels_used[lbl] = 1
        
    def label_used(self, lbl):
        return lbl in self.labels_used

    def allocate_temp(self, type, manage_ref):
        """
        Allocates a temporary (which may create a new one or get a previously
        allocated and released one of the same type). Type is simply registered
        and handed back, but will usually be a PyrexType.

        If type.is_pyobject, manage_ref comes into play. If manage_ref is set to
        True, the temp will be decref-ed on return statements and in exception
        handling clauses. Otherwise the caller has to deal with any reference
        counting of the variable.

        If not type.is_pyobject, then manage_ref will be ignored, but it
        still has to be passed. It is recommended to pass False by convention
        if it is known that type will never be a Python object.

        A C string referring to the variable is returned.
        """
        if not type.is_pyobject:
            # Make manage_ref canonical, so that manage_ref will always mean
            # a decref is needed.
            manage_ref = False
        freelist = self.temps_free.get((type, manage_ref))
        if freelist is not None and len(freelist) > 0:
            result = freelist.pop()
        else:
            while True:
                self.temp_counter += 1
                result = "%s%d" % (Naming.codewriter_temp_prefix, self.temp_counter)
                if not result in self.names_taken: break
            self.temps_allocated.append((result, type, manage_ref))
        self.temps_used_type[result] = (type, manage_ref)
        if DebugFlags.debug_temp_code_comments:
            self.owner.putln("/* %s allocated */" % result)
        return result

    def release_temp(self, name):
        """
        Releases a temporary so that it can be reused by other code needing
        a temp of the same type.
        """
        type, manage_ref = self.temps_used_type[name]
        freelist = self.temps_free.get((type, manage_ref))
        if freelist is None:
            freelist = []
            self.temps_free[(type, manage_ref)] = freelist
        if name in freelist:
            raise RuntimeError("Temp %s freed twice!" % name)
        freelist.append(name)
        if DebugFlags.debug_temp_code_comments:
            self.owner.putln("/* %s released */" % name)

    def temps_in_use(self):
        """Return a list of (cname,type,manage_ref) tuples of temp names and their type
        that are currently in use.
        """
        used = []
        for name, type, manage_ref in self.temps_allocated:
            freelist = self.temps_free.get((type, manage_ref))
            if freelist is None or name not in freelist:
                used.append((name, type, manage_ref))
        return used

    def temps_holding_reference(self):
        """Return a list of (cname,type) tuples of temp names and their type
        that are currently in use. This includes only temps of a
        Python object type which owns its reference.
        """
        return [(name, type)
                for name, type, manage_ref in self.temps_in_use()
                if manage_ref]

    def all_managed_temps(self):
        """Return a list of (cname, type) tuples of refcount-managed Python objects.
        """
        return [(cname, type)
                for cname, type, manage_ref in self.temps_allocated
                if manage_ref]

    def all_free_managed_temps(self):
        """Return a list of (cname, type) tuples of refcount-managed Python
        objects that are not currently in use.  This is used by
        try-except and try-finally blocks to clean up temps in the
        error case.
        """
        return [(cname, type)
                for (type, manage_ref), freelist in self.temps_free.iteritems()
                if manage_ref
                for cname in freelist]

class GlobalState(object):
    # filename_table   {string : int}  for finding filename table indexes
    # filename_list    [string]        filenames in filename table order
    # input_file_contents dict         contents (=list of lines) of any file that was used as input
    #                                  to create this output C code.  This is
    #                                  used to annotate the comments.
    #
    # utility_codes   set                IDs of used utility code (to avoid reinsertion)
    #
    # declared_cnames  {string:Entry}  used in a transition phase to merge pxd-declared
    #                                  constants etc. into the pyx-declared ones (i.e,
    #                                  check if constants are already added).
    #                                  In time, hopefully the literals etc. will be
    #                                  supplied directly instead.

    # parts            {string:CCodeWriter}

    
    # interned_strings
    # consts
    # py_string_decls
    # interned_nums
    # cached_builtins

    # directives       set             Temporary variable used to track
    #                                  the current set of directives in the code generation
    #                                  process.

    directives = {}

    code_layout = [
        'h_code',
        'utility_code_proto',
        'type_declarations',
        'module_declarations',
        'typeinfo',
        'before_global_var',
        'global_var',
        'all_the_rest',
        'utility_code_def'
    ]
    

    def __init__(self, writer, emit_linenums=False):
        self.filename_table = {}
        self.filename_list = []
        self.input_file_contents = {}
        self.utility_codes = set()
        self.declared_cnames = {}
        self.pystring_table_needed = False
        self.in_utility_code_generation = False
        self.emit_linenums = emit_linenums
        self.parts = {}

        assert writer.globalstate is None
        writer.globalstate = self
        self.rootwriter = writer

    def initialize_main_c_code(self):
        rootwriter = self.rootwriter
        for part in self.code_layout:
            self.parts[part] = rootwriter.insertion_point()

        self.decls_writer = rootwriter.new_writer()
        self.pystring_table = rootwriter.new_writer()
        self.init_cached_builtins_writer = rootwriter.new_writer()
        self.initwriter = rootwriter.new_writer()
        self.cleanupwriter = rootwriter.new_writer()

        if Options.cache_builtins:
            self.init_cached_builtins_writer.enter_cfunc_scope()
            self.init_cached_builtins_writer.putln("static int __Pyx_InitCachedBuiltins(void) {")

        self.initwriter.enter_cfunc_scope()
        self.initwriter.putln("")
        self.initwriter.putln("static int __Pyx_InitGlobals(void) {")

        self.cleanupwriter.enter_cfunc_scope()
        self.cleanupwriter.putln("")
        self.cleanupwriter.putln("static void __Pyx_CleanupGlobals(void) {")

        self.pystring_table.putln("")
        self.pystring_table.putln("static __Pyx_StringTabEntry %s[] = {" %
                Naming.stringtab_cname)


        #
        # utility_code_def
        #
        code = self.parts['utility_code_def']
        if self.emit_linenums:
            code.write('\n#line 1 "cython_utility"\n')
        code.putln("")
        code.putln("/* Runtime support code */")
        code.putln("")
        code.putln("static void %s(void) {" % Naming.fileinit_cname)
        code.putln("%s = %s;" % 
            (Naming.filetable_cname, Naming.filenames_cname))
        code.putln("}")

    def finalize_main_c_code(self):
        self.close_global_decls()

        #
        # utility_code_def
        #
        code = self.parts['utility_code_def']
        code.put(PyrexTypes.type_conversion_functions)
        code.putln("")

    def __getitem__(self, key):
        return self.parts[key]

    #
    # Global constants, interned objects, etc.
    #
    def close_global_decls(self):
        # This is called when it is known that no more global declarations will
        # declared (but can be called before or after insert_XXX).
        if self.pystring_table_needed:
            self.pystring_table.putln("{0, 0, 0, 0, 0, 0}")
            self.pystring_table.putln("};")
            import Nodes
            self.use_utility_code(Nodes.init_string_tab_utility_code)
            self.initwriter.putln(
                "if (__Pyx_InitStrings(%s) < 0) %s;" % (
                    Naming.stringtab_cname,
                    self.initwriter.error_goto(self.module_pos)))

        if Options.cache_builtins:
            w = self.init_cached_builtins_writer
            w.putln("return 0;")
            w.put_label(w.error_label)
            w.putln("return -1;")
            w.putln("}")
            w.exit_cfunc_scope()

        w = self.initwriter
        w.putln("return 0;")
        w.put_label(w.error_label)
        w.putln("return -1;")
        w.putln("}")
        w.exit_cfunc_scope()

        w = self.cleanupwriter
        w.putln("}")
        w.exit_cfunc_scope()
         
    def insert_initcode_into(self, code):
        if self.pystring_table_needed:
            code.insert(self.pystring_table)
        if Options.cache_builtins:
            code.insert(self.init_cached_builtins_writer)
        code.insert(self.initwriter)

    def insert_cleanupcode_into(self, code):
        code.insert(self.cleanupwriter)

    def put_pyobject_decl(self, entry):
        self['global_var'].putln("static PyObject *%s;" % entry.cname)

    # The functions below are there in a transition phase only
    # and will be deprecated. They are called from Nodes.BlockNode.
    # The copy&paste duplication is intentional in order to be able
    # to see quickly how BlockNode worked, until this is replaced.    

    def should_declare(self, cname, entry):
        if cname in self.declared_cnames:
            other = self.declared_cnames[cname]
            assert str(entry.type) == str(other.type)
            assert entry.init == other.init
            return False
        else:
            self.declared_cnames[cname] = entry
            return True

    def add_const_definition(self, entry):
        if self.should_declare(entry.cname, entry):
            self['global_var'].put_var_declaration(entry, static = 1)

    def add_interned_string_decl(self, entry):
        if self.should_declare(entry.cname, entry):
            self['global_var'].put_var_declaration(entry, static = 1)
        self.add_py_string_decl(entry)

    def add_py_string_decl(self, entry):
        if self.should_declare(entry.pystring_cname, entry):
            self['global_var'].putln("static PyObject *%s;" % entry.pystring_cname)
            self.pystring_table_needed = True
            self.pystring_table.putln("{&%s, %s, sizeof(%s), %d, %d, %d}," % (
                entry.pystring_cname,
                entry.cname,
                entry.cname,
                entry.type.is_unicode,
                entry.is_interned,
                entry.is_identifier
                ))
                       
    def add_interned_num_decl(self, entry):
        if self.should_declare(entry.cname, entry):
            if entry.init[-1] == "L":
                self.initwriter.putln('%s = PyLong_FromString((char *)"%s", 0, 0); %s;' % (
                    entry.cname,
                    entry.init[:-1], # strip 'L' for Py3 compatibility
                    self.initwriter.error_goto_if_null(entry.cname, self.module_pos)))
            else:
                self.initwriter.putln("%s = PyInt_FromLong(%s); %s;" % (
                    entry.cname,
                    entry.init,
                    self.initwriter.error_goto_if_null(entry.cname, self.module_pos)))
            
            self.put_pyobject_decl(entry)
        
    def add_cached_builtin_decl(self, entry):
        if Options.cache_builtins:
            if self.should_declare(entry.cname, entry):
                self.put_pyobject_decl(entry)
                self.init_cached_builtins_writer.putln('%s = __Pyx_GetName(%s, %s); if (!%s) %s' % (
                    entry.cname,
                    Naming.builtins_cname,
                    entry.interned_cname,
                    entry.cname,
                    self.init_cached_builtins_writer.error_goto(entry.pos)))


    #
    # File name state
    #

    def lookup_filename(self, filename):
        try:
            index = self.filename_table[filename]
        except KeyError:
            index = len(self.filename_list)
            self.filename_list.append(filename)
            self.filename_table[filename] = index
        return index

    def commented_file_contents(self, source_desc):
        try:
            return self.input_file_contents[source_desc]
        except KeyError:
            F = [u' * ' + line.rstrip().replace(
                    u'*/', u'*[inserted by cython to avoid comment closer]/'
                    ).replace(
                    u'/*', u'/[inserted by cython to avoid comment start]*'
                    ).encode('ASCII', 'replace') # + Py2 auto-decode to unicode
                 for line in source_desc.get_lines()]
            if len(F) == 0: F.append(u'')
            self.input_file_contents[source_desc] = F
            return F

    #
    # Utility code state
    #
    
    def use_utility_code(self, utility_code, name=None):
        """
        Adds the given utility code to the C file if needed.

        codetup should unpack into one prototype code part and one
        definition code part, both strings inserted directly in C.

        If name is provided, it is used as an identifier to avoid inserting
        code twice. Otherwise, id(codetup) is used as such an identifier.
        """
        if name is None: name = id(utility_code)
        if name not in self.utility_codes:
            self.utility_codes.add(name)
            if utility_code.requires:
                for dependency in utility_code.requires:
                    self.use_utility_code(dependency)
            if utility_code.proto:
                self.parts['utility_code_proto'].put(utility_code.proto)
            if utility_code.impl:
                self.parts['utility_code_def'].put(utility_code.impl)
            utility_code.write_init_code(self.initwriter, self.module_pos)
            utility_code.write_cleanup_code(self.cleanupwriter, self.module_pos)


def funccontext_property(name):
    def get(self):
        return getattr(self.funcstate, name)
    def set(self, value):
        setattr(self.funcstate, name, value)
    return property(get, set)

class CCodeWriter(object):
    """
    Utility class to output C code.

    When creating an insertion point one must care about the state that is
    kept:
    - formatting state (level, bol) is cloned and used in insertion points
      as well
    - labels, temps, exc_vars: One must construct a scope in which these can
      exist by calling enter_cfunc_scope/exit_cfunc_scope (these are for
      sanity checking and forward compatabilty). Created insertion points
      looses this scope and cannot access it.
    - marker: Not copied to insertion point
    - filename_table, filename_list, input_file_contents: All codewriters
      coming from the same root share the same instances simultaneously.
    """
    
    # f                file            output file
    # buffer           StringIOTree
    
    # level            int             indentation level
    # bol              bool            beginning of line?
    # marker           string          comment to emit before next line
    # funcstate        FunctionState   contains state local to a C function used for code
    #                                  generation (labels and temps state etc.)
    # globalstate      GlobalState     contains state global for a C file (input file info,
    #                                  utility code, declared constants etc.)
    # emit_linenums    boolean         whether or not to write #line pragmas 

    globalstate = None
    
    def __init__(self, create_from=None, buffer=None, copy_formatting=False, emit_linenums=None):
        if buffer is None: buffer = StringIOTree()
        self.buffer = buffer
        self.marker = None
        self.last_marker_line = 0
        self.source_desc = ""
        
        self.funcstate = None
        self.level = 0
        self.call_level = 0
        self.bol = 1

        if create_from is not None:
            # Use same global state
            self.globalstate = create_from.globalstate
            # Clone formatting state
            if copy_formatting:
                self.level = create_from.level
                self.bol = create_from.bol
                self.call_level = create_from.call_level
        if emit_linenums is None and self.globalstate:
            self.emit_linenums = self.globalstate.emit_linenums
        else:
            self.emit_linenums = emit_linenums

    def create_new(self, create_from, buffer, copy_formatting):
        # polymorphic constructor -- very slightly more versatile
        # than using __class__
        result = CCodeWriter(create_from, buffer, copy_formatting)
        return result

    def copyto(self, f):
        self.buffer.copyto(f)

    def getvalue(self):
        return self.buffer.getvalue()

    def write(self, s):
        self.buffer.write(s)

    def insertion_point(self):
        other = self.create_new(create_from=self, buffer=self.buffer.insertion_point(), copy_formatting=True)
        return other

    def new_writer(self):
        """
        Creates a new CCodeWriter connected to the same global state, which
        can later be inserted using insert.
        """
        return CCodeWriter(create_from=self)

    def insert(self, writer):
        """
        Inserts the contents of another code writer (created with
        the same global state) in the current location.

        It is ok to write to the inserted writer also after insertion.
        """
        assert writer.globalstate is self.globalstate
        self.buffer.insert(writer.buffer)

    # Properties delegated to function scope
    label_counter = funccontext_property("label_counter")
    return_label = funccontext_property("return_label")
    error_label = funccontext_property("error_label")
    labels_used = funccontext_property("labels_used")
    continue_label = funccontext_property("continue_label")
    break_label = funccontext_property("break_label")
    return_from_error_cleanup_label = funccontext_property("return_from_error_cleanup_label")

    # Functions delegated to function scope
    def new_label(self, name=None):    return self.funcstate.new_label(name)
    def new_error_label(self):         return self.funcstate.new_error_label()
    def get_loop_labels(self):         return self.funcstate.get_loop_labels()
    def set_loop_labels(self, labels): return self.funcstate.set_loop_labels(labels)
    def new_loop_labels(self):         return self.funcstate.new_loop_labels()
    def get_all_labels(self):          return self.funcstate.get_all_labels()
    def set_all_labels(self, labels):  return self.funcstate.set_all_labels(labels)
    def all_new_labels(self):          return self.funcstate.all_new_labels()
    def use_label(self, lbl):          return self.funcstate.use_label(lbl)
    def label_used(self, lbl):         return self.funcstate.label_used(lbl)


    def enter_cfunc_scope(self):
        self.funcstate = FunctionState(self)
    
    def exit_cfunc_scope(self):
        self.funcstate = None

    def putln(self, code = "", safe=False):
        if self.marker and self.bol:
            self.emit_marker()
        if self.emit_linenums and self.last_marker_line != 0:
            self.write('\n#line %s "%s"\n' % (self.last_marker_line, self.source_desc))
        if code:
            if safe:
                self.put_safe(code)
            else:
                self.put(code)
        self.write("\n");
        self.bol = 1
    
    def emit_marker(self):
        self.write("\n");
        self.indent()
        self.write("/* %s */\n" % self.marker[1])
        self.last_marker_line = self.marker[0]
        self.marker = None

    def put_safe(self, code):
        # put code, but ignore {}
        self.write(code)
        self.bol = 0

    def put(self, code):
        fix_indent = False
        if "{" in code:
            dl = code.count("{")
        else:
            dl = 0
        if "}" in code:
            dl -= code.count("}")
            if dl < 0:
                self.level += dl
            elif dl == 0 and code[0] == "}":
                # special cases like "} else {" need a temporary dedent
                fix_indent = True
                self.level -= 1
        if self.bol:
            self.indent()
        self.write(code)
        self.bol = 0
        if dl > 0:
            self.level += dl
        elif fix_indent:
            self.level += 1

    def increase_indent(self):
        self.level = self.level + 1
    
    def decrease_indent(self):
        self.level = self.level - 1
    
    def begin_block(self):
        self.putln("{")
        self.increase_indent()
    
    def end_block(self):
        self.decrease_indent()
        self.putln("}")
    
    def indent(self):
        self.write("  " * self.level)

    def get_py_version_hex(self, pyversion):
        return "0x%02X%02X%02X%02X" % (tuple(pyversion) + (0,0,0,0))[:4]

    def mark_pos(self, pos):
        if pos is None:
            return
        source_desc, line, col = pos
        if self.last_marker_line == line:
            return
        assert isinstance(source_desc, SourceDescriptor)
        contents = self.globalstate.commented_file_contents(source_desc)
        lines = contents[max(0,line-3):line] # line numbers start at 1
        lines[-1] += u'             # <<<<<<<<<<<<<<'
        lines += contents[line:line+2]

        marker = u'"%s":%d\n%s\n' % (
            source_desc.get_escaped_description(), line, u'\n'.join(lines))
        self.marker = (line, marker)
        if self.emit_linenums:
            self.source_desc = source_desc.get_escaped_description()
        
    def put_label(self, lbl):
        if lbl in self.funcstate.labels_used:
            self.putln("%s:;" % lbl)
    
    def put_goto(self, lbl):
        self.funcstate.use_label(lbl)
        self.putln("goto %s;" % lbl)
    
    def put_var_declarations(self, entries, static = 0, dll_linkage = None,
            definition = True):
        for entry in entries:
            if not entry.in_cinclude:
                self.put_var_declaration(entry, static, dll_linkage, definition)
    
    def put_var_declaration(self, entry, static = 0, dll_linkage = None,
            definition = True):
        #print "Code.put_var_declaration:", entry.name, "definition =", definition ###
        if entry.in_closure:
            return
        visibility = entry.visibility
        if visibility == 'private' and not definition:
            #print "...private and not definition, skipping" ###
            return
        if not entry.used and visibility == "private":
            #print "not used and private, skipping", entry.cname ###
            return
        storage_class = ""
        if visibility == 'extern':
            storage_class = Naming.extern_c_macro
        elif visibility == 'public':
            if not definition:
                storage_class = Naming.extern_c_macro
        elif visibility == 'private':
            if static:
                storage_class = "static"
        if storage_class:
            self.put("%s " % storage_class)
        if visibility != 'public':
            dll_linkage = None
        self.put(entry.type.declaration_code(entry.cname,
            dll_linkage = dll_linkage))
        if entry.init is not None:
            self.put_safe(" = %s" % entry.type.literal_code(entry.init))
        self.putln(";")

    def put_temp_declarations(self, func_context):
        for name, type, manage_ref in func_context.temps_allocated:
            decl = type.declaration_code(name)
            if type.is_pyobject:
                self.putln("%s = NULL;" % decl)
            else:
                self.putln("%s;" % decl)

    def entry_as_pyobject(self, entry):
        type = entry.type
        if (not entry.is_self_arg and not entry.type.is_complete()
            or entry.type.is_extension_type):
            return "(PyObject *)" + entry.cname
        else:
            return entry.cname
    
    def as_pyobject(self, cname, type):
        return typecast(py_object_type, type, cname)
    
    def put_gotref(self, cname):
        self.putln("__Pyx_GOTREF(%s);" % cname)
    
    def put_giveref(self, cname):
        self.putln("__Pyx_GIVEREF(%s);" % cname)
    
    def put_xgiveref(self, cname):
        self.putln("__Pyx_XGIVEREF(%s);" % cname)

    def put_xgotref(self, cname):
        self.putln("__Pyx_XGOTREF(%s);" % cname)

    def put_incref(self, cname, type, nanny=True):
        if nanny:
            self.putln("__Pyx_INCREF(%s);" % self.as_pyobject(cname, type))
        else:
            self.putln("Py_INCREF(%s);" % self.as_pyobject(cname, type))
    
    def put_decref(self, cname, type, nanny=True):
        if nanny:
            self.putln("__Pyx_DECREF(%s);" % self.as_pyobject(cname, type))
        else:
            self.putln("Py_DECREF(%s);" % self.as_pyobject(cname, type))

    def put_var_gotref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_GOTREF(%s);" % self.entry_as_pyobject(entry))
        
    def put_var_giveref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_GIVEREF(%s);" % self.entry_as_pyobject(entry))

    def put_var_xgotref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_XGOTREF(%s);" % self.entry_as_pyobject(entry))

    def put_var_xgiveref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_XGIVEREF(%s);" % self.entry_as_pyobject(entry))

    def put_var_incref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_INCREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_decref_clear(self, cname, type, nanny=True):
        if nanny:
            self.putln("__Pyx_DECREF(%s); %s = 0;" % (
                typecast(py_object_type, type, cname), cname))
        else:
            self.putln("Py_DECREF(%s); %s = 0;" % (
                typecast(py_object_type, type, cname), cname))
    
    def put_xdecref(self, cname, type, nanny=True):
        if nanny:
            self.putln("__Pyx_XDECREF(%s);" % self.as_pyobject(cname, type))
        else:
            self.putln("Py_XDECREF(%s);" % self.as_pyobject(cname, type))
    
    def put_xdecref_clear(self, cname, type, nanny=True):
        if nanny:
            self.putln("__Pyx_XDECREF(%s); %s = 0;" % (
                self.as_pyobject(cname, type), cname))
        else:
            self.putln("Py_XDECREF(%s); %s = 0;" % (
                self.as_pyobject(cname, type), cname))

    def put_var_decref(self, entry):
        if entry.type.is_pyobject:
            if entry.init_to_none is False:
                self.putln("__Pyx_XDECREF(%s);" % self.entry_as_pyobject(entry))
            else:
                self.putln("__Pyx_DECREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_var_decref_clear(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_DECREF(%s); %s = 0;" % (
                self.entry_as_pyobject(entry), entry.cname))
    
    def put_var_xdecref(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_XDECREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_var_xdecref_clear(self, entry):
        if entry.type.is_pyobject:
            self.putln("__Pyx_XDECREF(%s); %s = 0;" % (
                self.entry_as_pyobject(entry), entry.cname))
    
    def put_var_decrefs(self, entries, used_only = 0):
        for entry in entries:
            if not used_only or entry.used:
                if entry.xdecref_cleanup:
                    self.put_var_xdecref(entry)
                else:
                    self.put_var_decref(entry)
    
    def put_var_xdecrefs(self, entries):
        for entry in entries:
            self.put_var_xdecref(entry)
    
    def put_var_xdecrefs_clear(self, entries):
        for entry in entries:
            self.put_var_xdecref_clear(entry)
    
    def put_init_to_py_none(self, cname, type, nanny=True):
        py_none = typecast(type, py_object_type, "Py_None")
        if nanny:
            self.putln("%s = %s; __Pyx_INCREF(Py_None);" % (cname, py_none))
        else:
            self.putln("%s = %s; Py_INCREF(Py_None);" % (cname, py_none))
    
    def put_init_var_to_py_none(self, entry, template = "%s", nanny=True):
        code = template % entry.cname
        #if entry.type.is_extension_type:
        #    code = "((PyObject*)%s)" % code
        self.put_init_to_py_none(code, entry.type, nanny)

    def put_pymethoddef(self, entry, term):
        if entry.doc:
            doc_code = entry.doc_cname
        else:
            doc_code = 0
        method_flags = entry.signature.method_flags()
        if method_flags:
            if entry.is_special:
                method_flags += [method_coexist]
            self.putln(
                '{__Pyx_NAMESTR("%s"), (PyCFunction)%s, %s, __Pyx_DOCSTR(%s)}%s' % (
                    entry.name, 
                    entry.func_cname,
                    "|".join(method_flags),
                    doc_code,
                    term))

    def put_error_if_neg(self, pos, value):
#        return self.putln("if (unlikely(%s < 0)) %s" % (value, self.error_goto(pos)))  # TODO this path is almost _never_ taken, yet this macro makes is slower!
        return self.putln("if (%s < 0) %s" % (value, self.error_goto(pos)))

    def put_h_guard(self, guard):
        self.putln("#ifndef %s" % guard)
        self.putln("#define %s" % guard)
    
    def unlikely(self, cond):
        if Options.gcc_branch_hints:
            return 'unlikely(%s)' % cond
        else:
            return cond

    def set_error_info(self, pos):
        if Options.c_line_in_traceback:
            cinfo = " %s = %s;" % (Naming.clineno_cname, Naming.line_c_macro)
        else:
            cinfo = ""
        return "%s = %s[%s]; %s = %s;%s" % (
            Naming.filename_cname,
            Naming.filetable_cname,
            self.lookup_filename(pos[0]),
            Naming.lineno_cname,
            pos[1],
            cinfo)
        
    def error_goto(self, pos):
        lbl = self.funcstate.error_label
        self.funcstate.use_label(lbl)
        return "{%s goto %s;}" % (
            self.set_error_info(pos),
            lbl)

    def error_goto_if(self, cond, pos):
        return "if (%s) %s" % (self.unlikely(cond), self.error_goto(pos))
            
    def error_goto_if_null(self, cname, pos):
        return self.error_goto_if("!%s" % cname, pos)
    
    def error_goto_if_neg(self, cname, pos):
        return self.error_goto_if("%s < 0" % cname, pos)
    
    def error_goto_if_PyErr(self, pos):
        return self.error_goto_if("PyErr_Occurred()", pos)
    
    def lookup_filename(self, filename):
        return self.globalstate.lookup_filename(filename)

    def put_setup_refcount_context(self, name):
        self.putln('__Pyx_SetupRefcountContext("%s");' % name)

    def put_finish_refcount_context(self):
        self.putln("__Pyx_FinishRefcountContext();")


class PyrexCodeWriter(object):
    # f                file      output file
    # level            int       indentation level

    def __init__(self, outfile_name):
        self.f = open_new_file(outfile_name)
        self.level = 0
    
    def putln(self, code):
        self.f.write("%s%s\n" % (" " * self.level, code))
    
    def indent(self):
        self.level += 1
    
    def dedent(self):
        self.level -= 1

