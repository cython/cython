#
#   Pyrex - Code output module
#

import Naming
from Pyrex.Utils import open_new_file
from PyrexTypes import py_object_type, typecast

class CCodeWriter:
    # f                file            output file
    # level            int             indentation level
    # bol              bool            beginning of line?
    # marker           string          comment to emit before next line
    # return_label     string          function return point label
    # error_label      string          error catch point label
    # continue_label   string          loop continue point label
    # break_label      string          loop break point label
    # label_counter    integer         counter for naming labels
    # in_try_finally   boolean         inside try of try...finally
    # filename_table   {string : int}  for finding filename table indexes
    # filename_list    [string]        filenames in filename table order
    
    in_try_finally = 0
    
    def __init__(self, f):
        #self.f = open_new_file(outfile_name)
        self.f = f
        self.level = 0
        self.bol = 1
        self.marker = None
        self.label_counter = 1
        self.error_label = None
        self.filename_table = {}
        self.filename_list = []
    
    def putln(self, code = ""):
        if self.marker and self.bol:
            self.emit_marker()
        if code:
            self.put(code)
        self.f.write("\n");
        self.bol = 1
    
    def emit_marker(self):
        self.f.write("\n");
        self.indent()
        self.f.write("/* %s */\n" % self.marker)
        self.marker = None

    def put(self, code):
        dl = code.count("{") - code.count("}")
        if dl < 0:
            self.level += dl
        if self.bol:
            self.indent()
        self.f.write(code)
        self.bol = 0
        if dl > 0:
            self.level += dl
    
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
        self.f.write("  " * self.level)
    
    def mark_pos(self, pos):
        file, line, col = pos
        self.marker = '"%s":%s' % (file, line)

    def init_labels(self):
        self.label_counter = 0
        self.labels_used = {}
        self.return_label = self.new_label()
        self.new_error_label()
        self.continue_label = None
        self.break_label = None
    
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

    def put_label(self, lbl):
        if lbl in self.labels_used:
            self.putln("%s:;" % lbl)
    
    def put_goto(self, lbl):
        self.use_label(lbl)
        self.putln("goto %s;" % lbl)
    
    def put_var_declarations(self, entries, static = 0, dll_linkage = None,
            definition = True):
        for entry in entries:
            if not entry.in_cinclude:
                self.put_var_declaration(entry, static, dll_linkage, definition)
    
    def put_var_declaration(self, entry, static = 0, dll_linkage = None,
            definition = True):
        #print "Code.put_var_declaration:", entry.name, "definition =", definition ###
        visibility = entry.visibility
        if visibility == 'private' and not definition:
            return
        if not entry.used and visibility == "private":
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
        if visibility <> 'public':
            dll_linkage = None
        self.put(entry.type.declaration_code(entry.cname,
            dll_linkage = dll_linkage))
        if entry.init is not None:
            self.put(" = %s" % entry.type.literal_code(entry.init))
        self.putln(";")
    
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
        self.putln(
            '{"%s", (PyCFunction)%s, METH_VARARGS|METH_KEYWORDS, %s}%s' % (
                entry.name, 
                entry.func_cname, 
                doc_code,
                term))
    
    def error_goto(self, pos):
        lbl = self.error_label
        self.use_label(lbl)
        return "{%s = %s[%s]; %s = %s; goto %s;}" % (
            Naming.filename_cname,
            Naming.filetable_cname,
            self.lookup_filename(pos[0]),
            Naming.lineno_cname,
            pos[1],
            lbl)
    
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

