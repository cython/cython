#
#   Pyrex - Code output module
#

import codecs
import Naming
import Options
from Cython.Utils import open_new_file, open_source_file
from PyrexTypes import py_object_type, typecast
from TypeSlots import method_coexist
from Scanning import SourceDescriptor
from Cython.StringIOTree import StringIOTree
from sets import Set as set

class FunctionContext(object):
    # Not used for now, perhaps later
    def __init__(self, names_taken=set()):
        self.names_taken = names_taken
        
        self.error_label = None
        self.label_counter = 0
        self.labels_used = {}
        self.return_label = self.new_label()
        self.new_error_label()
        self.continue_label = None
        self.break_label = None

        self.temps_allocated = [] # of (name, type)
        self.temps_free = {} # type -> list of free vars
        self.temps_used_type = {} # name -> type
        self.temp_counter = 0

    def new_label(self):
        n = self.label_counter
        self.label_counter = n + 1
        return "%s%d" % (Naming.label_prefix, n)
    
    def new_error_label(self):
        old_err_lbl = self.error_label
        self.error_label = self.new_label()
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
            (self.new_label(), 
             self.new_label()))
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

    def allocate_temp(self, type):
        """
        Allocates a temporary (which may create a new one or get a previously
        allocated and released one of the same type). Type is simply registered
        and handed back, but will usually be a PyrexType.

        A C string referring to the variable is returned.
        """
        freelist = self.temps_free.get(type)
        if freelist is not None and len(freelist) > 0:
            result = freelist.pop()
        else:
            while True:
                self.temp_counter += 1
                result = "%s%d" % (Naming.codewriter_temp_prefix, self.temp_counter)
                if not result in self.names_taken: break
            self.temps_allocated.append((result, type))
        self.temps_used_type[result] = type
        return result

    def release_temp(self, name):
        """
        Releases a temporary so that it can be reused by other code needing
        a temp of the same type.
        """
        type = self.temps_used_type[name]
        freelist = self.temps_free.get(type)
        if freelist is None:
            freelist = []
            self.temps_free[type] = freelist
        freelist.append(name)

def funccontext_property(name):
    def get(self):
        return getattr(self.func, name)
    def set(self, value):
        setattr(self.func, name, value)
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
    # return_label     string          function return point label
    # error_label      string          error catch point label
    # continue_label   string          loop continue point label
    # break_label      string          loop break point label
    # return_from_error_cleanup_label string
    # label_counter    integer         counter for naming labels
    # in_try_finally   boolean         inside try of try...finally
    # filename_table   {string : int}  for finding filename table indexes
    # filename_list    [string]        filenames in filename table order
    # exc_vars         (string * 3)    exception variables for reraise, or None
    # input_file_contents dict         contents (=list of lines) of any file that was used as input
    #                                  to create this output C code.  This is
    #                                  used to annotate the comments.
    # func             FunctionContext contains labels and temps context info
   
    in_try_finally = 0
    
    def __init__(self, create_from=None, buffer=None):
        if buffer is None: buffer = StringIOTree()
        self.buffer = buffer
        self.marker = None
        self.last_marker_line = 0
        self.func = None
        if create_from is None:
            # Root CCodeWriter
            self.level = 0
            self.bol = 1
            self.filename_table = {}
            self.filename_list = []
            self.exc_vars = None
            self.input_file_contents = {}
        else:
            # Clone formatting state
            c = create_from
            self.level = c.level
            self.bol = c.bol
            # Note: NOT copying but sharing instance
            self.filename_table = c.filename_table
            self.filename_list = []
            self.input_file_contents = c.input_file_contents
            # Leave other state alone

    def create_new(self, create_from, buffer):
        # polymorphic constructor -- very slightly more versatile
        # than using __class__
        return CCodeWriter(create_from, buffer)

    def copyto(self, f):
        self.buffer.copyto(f)

    def getvalue(self):
        return self.buffer.getvalue()

    def write(self, s):
        self.buffer.write(s)

    def insertion_point(self):
        other = self.create_new(create_from=self, buffer=self.buffer.insertion_point())
        return other


    # Properties delegated to function scope
    label_counter = funccontext_property("label_counter")
    return_label = funccontext_property("return_label")
    error_label = funccontext_property("error_label")
    labels_used = funccontext_property("labels_used")
    continue_label = funccontext_property("continue_label")
    break_label = funccontext_property("break_label")


    # Functions delegated to function scope
    def new_label(self):               return self.func.new_label()
    def new_error_label(self):         return self.func.new_error_label()
    def get_loop_labels(self):         return self.func.get_loop_labels()
    def set_loop_labels(self, labels): return self.func.set_loop_labels(labels)
    def new_loop_labels(self):         return self.func.new_loop_labels()
    def get_all_labels(self):          return self.func.get_all_labels()
    def set_all_labels(self, labels):  return self.func.set_all_labels(labels)
    def all_new_labels(self):          return self.func.all_new_labels()
    def use_label(self, lbl):          return self.func.use_label(lbl)
    def label_used(self, lbl):         return self.func.label_used(lbl)


    def enter_cfunc_scope(self):
        self.func = FunctionContext()
    
    def exit_cfunc_scope(self):
        self.func = None

    def putln(self, code = ""):
        if self.marker and self.bol:
            self.emit_marker()
        if code:
            self.put(code)
        self.write("\n");
        self.bol = 1
    
    def emit_marker(self):
        self.write("\n");
        self.indent()
        self.write("/* %s */\n" % self.marker[1])
        self.last_marker_line = self.marker[0]
        self.marker = None

    def put(self, code):
        dl = code.count("{") - code.count("}")
        if dl < 0:
            self.level += dl
        elif dl == 0 and code.startswith('}'):
            self.level -= 1
        if self.bol:
            self.indent()
        self.write(code)
        self.bol = 0
        if dl > 0:
            self.level += dl
        elif dl == 0 and code.startswith('}'):
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

    def commented_file_contents(self, source_desc):
        try:
            return self.input_file_contents[source_desc]
        except KeyError:
            F = [u' * ' + line.rstrip().replace(
                    u'*/', u'*[inserted by cython to avoid comment closer]/'
                    ).encode('ASCII', 'replace') # + Py2 auto-decode to unicode
                 for line in source_desc.get_lines()]
            self.input_file_contents[source_desc] = F
            return F

    def mark_pos(self, pos):
        if pos is None:
            return
        source_desc, line, col = pos
        if self.last_marker_line == line:
            return
        assert isinstance(source_desc, SourceDescriptor)
        contents = self.commented_file_contents(source_desc)

        lines = contents[max(0,line-3):line] # line numbers start at 1
        lines[-1] += u'             # <<<<<<<<<<<<<<'
        lines += contents[line:line+2]

        marker = u'"%s":%d\n%s\n' % (
            source_desc.get_escaped_description(), line, u'\n'.join(lines))
        self.marker = (line, marker)

        
    def put_label(self, lbl):
        if lbl in self.func.labels_used:
            self.putln("%s:;" % lbl)
    
    def put_goto(self, lbl):
        self.func.use_label(lbl)
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
            self.put(" = %s" % entry.type.literal_code(entry.init))
        self.putln(";")

    def put_temp_declarations(self, func_context):
        for name, type in func_context.temps_allocated:
            decl = type.declaration_code(name)
            if type.is_pyobject:
                self.putln("%s = NULL;" % decl)
            else:
                self.putln("%s;" % decl)

    def entry_as_pyobject(self, entry):
        type = entry.type
        if (not entry.is_self_arg and not entry.type.is_complete()) \
            or (entry.type.is_extension_type and entry.type.base_type):
            return "(PyObject *)" + entry.cname
        else:
            return entry.cname
    
    def as_pyobject(self, cname, type):
        return typecast(py_object_type, type, cname)
    
    def put_incref(self, cname, type):
        self.putln("Py_INCREF(%s);" % self.as_pyobject(cname, type))
    
    def put_decref(self, cname, type):
        self.putln("Py_DECREF(%s);" % self.as_pyobject(cname, type))
    
    def put_var_incref(self, entry):
        if entry.type.is_pyobject:
            self.putln("Py_INCREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_decref_clear(self, cname, type):
        self.putln("Py_DECREF(%s); %s = 0;" % (
            typecast(py_object_type, type, cname), cname))
            #self.as_pyobject(cname, type), cname))
    
    def put_xdecref(self, cname, type):
        self.putln("Py_XDECREF(%s);" % self.as_pyobject(cname, type))
    
    def put_xdecref_clear(self, cname, type):
        self.putln("Py_XDECREF(%s); %s = 0;" % (
            self.as_pyobject(cname, type), cname))

    def put_var_decref(self, entry):
        if entry.type.is_pyobject:
            if entry.init_to_none is False:
                self.putln("Py_XDECREF(%s);" % self.entry_as_pyobject(entry))
            else:
                self.putln("Py_DECREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_var_decref_clear(self, entry):
        if entry.type.is_pyobject:
            self.putln("Py_DECREF(%s); %s = 0;" % (
                self.entry_as_pyobject(entry), entry.cname))
    
    def put_var_xdecref(self, entry):
        if entry.type.is_pyobject:
            self.putln("Py_XDECREF(%s);" % self.entry_as_pyobject(entry))
    
    def put_var_xdecref_clear(self, entry):
        if entry.type.is_pyobject:
            self.putln("Py_XDECREF(%s); %s = 0;" % (
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
    
    def put_init_to_py_none(self, cname, type):
        py_none = typecast(type, py_object_type, "Py_None")
        self.putln("%s = %s; Py_INCREF(Py_None);" % (cname, py_none))
    
    def put_init_var_to_py_none(self, entry, template = "%s"):
        code = template % entry.cname
        #if entry.type.is_extension_type:
        #	code = "((PyObject*)%s)" % code
        self.put_init_to_py_none(code, entry.type)

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
                '{"%s", (PyCFunction)%s, %s, %s}%s' % (
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
        
    def error_goto(self, pos):
        lbl = self.func.error_label
        self.func.use_label(lbl)
        if Options.c_line_in_traceback:
            cinfo = " %s = %s;" % (Naming.clineno_cname, Naming.line_c_macro)
        else:
            cinfo = ""
        return "{%s = %s[%s]; %s = %s;%s goto %s;}" % (
            Naming.filename_cname,
            Naming.filetable_cname,
            self.lookup_filename(pos[0]),
            Naming.lineno_cname,
            pos[1],
            cinfo,
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
        try:
            index = self.filename_table[filename]
        except KeyError:
            index = len(self.filename_list)
            self.filename_list.append(filename)
            self.filename_table[filename] = index
        return index


class PyrexCodeWriter:
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

