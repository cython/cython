from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Utils import EncodedString
from Cython.Compiler.Errors import CompileError
import PyrexTypes
from sets import Set as set

def used_buffer_aux_vars(entry):
    buffer_aux = entry.buffer_aux
    buffer_aux.buffer_info_var.used = True
    for s in buffer_aux.shapevars: s.used = True
    for s in buffer_aux.stridevars: s.used = True

def put_unpack_buffer_aux_into_scope(buffer_aux, code):
    bufstruct = buffer_aux.buffer_info_var.cname

    code.putln(" ".join(["%s = %s.strides[%d];" %
                         (s.cname, bufstruct, idx)
                         for idx, s in enumerate(buffer_aux.stridevars)]))
    code.putln(" ".join(["%s = %s.shape[%d];" %
                         (s.cname, bufstruct, idx)
                         for idx, s in enumerate(buffer_aux.shapevars)]))

def put_zero_buffer_aux_into_scope(buffer_aux, code):
    # If new buffer is None, set up to access 0
    # for a "safer segfault" on access
    code.putln("%s.buf = 0;" % buffer_aux.buffer_info_var.cname) 
    code.putln(" ".join(["%s = 0;" % s.cname
                         for s in buffer_aux.stridevars]))
    code.putln(" ".join(["%s = 0;" % s.cname
                         for s in buffer_aux.shapevars]))    

def put_acquire_arg_buffer(entry, code, pos):
    buffer_aux = entry.buffer_aux
    cname  = entry.cname
    bufstruct = buffer_aux.buffer_info_var.cname
    flags = '0'
    # Acquire any new buffer
    code.put('if (%s != Py_None) ' % cname)
    code.begin_block()
    code.putln('%s.buf = 0;' % bufstruct) # PEP requirement
    code.put(code.error_goto_if(
        'PyObject_GetBuffer(%s, &%s, %s) == -1' % (
        cname, bufstruct, flags), pos))
    # An exception raised in arg parsing cannot be catched, so no
    # need to do care about the buffer then.
    put_unpack_buffer_aux_into_scope(buffer_aux, code)
    code.end_block()

def put_release_buffer(entry, code):
    code.putln("if (%s != Py_None) PyObject_ReleaseBuffer(%s, &%s);" % (
        entry.cname, entry.cname, entry.buffer_aux.buffer_info_var.cname))

def put_assign_to_buffer(lhs_cname, rhs_cname, buffer_aux, is_initialized, pos, code):
    bufstruct = buffer_aux.buffer_info_var.cname
    flags = '0'

    if is_initialized:
        # Release any existing buffer
        code.put('if (%s != Py_None) ' % lhs_cname)
        code.begin_block();
        code.putln('PyObject_ReleaseBuffer(%s, &%s);' % (
            lhs_cname, bufstruct))
        code.end_block()
    # Acquire any new buffer
    code.put('if (%s != Py_None) ' % rhs_cname)
    code.begin_block()
    code.putln('%s.buf = 0;' % bufstruct) # PEP requirement
    code.put('if (%s) ' % code.unlikely(
        'PyObject_GetBuffer(%s, &%s, %s) == -1' % (
            rhs_cname,
            bufstruct,
            flags)
         + ' || %s((char*)%s.format) == NULL' % (
            buffer_aux.tschecker.cname, bufstruct
        )))
    code.begin_block()
    # If acquisition failed, attempt to reacquire the old buffer
    # before raising the exception. A failure of reacquisition
    # will cause the reacquisition exception to be reported, one
    # can consider working around this later.
    if is_initialized:
        put_zero_buffer_aux_into_scope(buffer_aux, code)
        code.put('if (%s != Py_None && PyObject_GetBuffer(%s, &%s, %s) == -1) ' % (
            lhs_cname, lhs_cname, bufstruct, flags))
        code.begin_block()
        put_zero_buffer_aux_into_scope(buffer_aux, code)
        code.end_block()
    else:
        # our entry had no previous value, so set to None when acquisition fails
        code.putln('%s = Py_None; Py_INCREF(Py_None);' % lhs_cname)
    code.putln(code.error_goto(pos))
    code.end_block() # acquisition failure
    # Unpack indices
    put_unpack_buffer_aux_into_scope(buffer_aux, code)
    code.putln('} else {')
    # If new buffer is None, set up to access 0
    # for a "safer segfault" on access
    put_zero_buffer_aux_into_scope(buffer_aux, code)
    code.end_block()

    # Everything is ok, assign object variable
    code.putln("%s = %s;" % (lhs_cname, rhs_cname))


def put_access(entry, index_types, index_cnames, tmp_cname, pos, code):
    """Returns a c string which can be used to access the buffer
    for reading or writing"""
    bufaux = entry.buffer_aux
    bufstruct = bufaux.buffer_info_var.cname
    # Check bounds and fix negative indices
    boundscheck = True
    nonegs = True
    if boundscheck:
        code.putln("%s = -1;" % tmp_cname)
    for idx, (type, cname, shape) in enumerate(zip(index_types, index_cnames,
                                  bufaux.shapevars)):
        if type.signed != 0:
            nonegs = False
            # not unsigned, deal with negative index
            code.putln("if (%s < 0) {" % cname)
            code.putln("%s += %s;" % (cname, shape.cname))
            if boundscheck:
                code.putln("if (%s) %s = %d;" % (
                    code.unlikely("%s < 0" % cname), tmp_cname, idx))
            code.put("} else ")
        else:
            if idx > 0: code.put("} else ")
        if boundscheck:
            # check bounds in positive direction
            code.putln("if (%s) %s = %d;" % (
                code.unlikely("%s >= %s" % (cname, shape.cname)),
                tmp_cname, idx))
#    if boundscheck or not nonegs:
#        code.putln("}")
    if boundscheck:  
        code.put("if (%s) " % code.unlikely("%s != -1" % tmp_cname))
        code.begin_block()
        code.putln('__Pyx_BufferIndexError(%s);' % tmp_cname)
        code.putln(code.error_goto(pos))
        code.end_block() 
        
    # Create buffer lookup and return it

    offset = " + ".join(["%s * %s" % (idx, stride.cname)
                         for idx, stride in
                         zip(index_cnames, bufaux.stridevars)])
    ptrcode = "(%s.buf + %s)" % (bufstruct, offset)
    valuecode = "*%s" % entry.type.buffer_ptr_type.cast_code(ptrcode)
    return valuecode


# Utility function to set the right exception
# The caller should immediately goto_error
buffer_boundsfail_error_utility_code = [
"""
static void __Pyx_BufferIndexError(int axis); /*proto*/
""","""
static void __Pyx_BufferIndexError(int axis) {
  PyErr_Format(PyExc_IndexError,
     "Out of bounds on buffer access (axis %d)", axis);
}
"""]


class PureCFuncNode(Node):
    child_attrs = []
    
    def __init__(self, pos, cname, type, c_code, visibility='private'):
        self.pos = pos
        self.cname = cname
        self.type = type
        self.c_code = c_code
        self.visibility = visibility
        self.entry = None

    def analyse_expressions(self, env):
        if not self.entry:
            self.entry = env.declare_cfunction(
                            "<pure c function:%s>" % self.cname,
                            self.type, self.pos, cname=self.cname,
                            defining=True, visibility=self.visibility)

    def generate_function_definitions(self, env, code, transforms):
        assert self.type.optional_arg_count == 0
        visibility = self.entry.visibility
        if visibility != 'private':
            storage_class = "%s " % Naming.extern_c_macro
        else:
            storage_class = "static "
        arg_decls = [arg.declaration_code() for arg in self.type.args]
        sig = self.type.return_type.declaration_code(
            self.type.function_header_code(self.cname, ", ".join(arg_decls)))
        code.putln("")
        code.putln("%s%s {" % (storage_class, sig))
        code.put(self.c_code)
        code.putln("}")

    def generate_execution_code(self, code):
        pass


tschecker_functype = PyrexTypes.CFuncType(
    PyrexTypes.c_char_ptr_type,
    [PyrexTypes.CFuncTypeArg(EncodedString("ts"), PyrexTypes.c_char_ptr_type,
                             (0, 0, None), cname="ts")],
    exception_value = "NULL"
)  

tsprefix = "__Pyx_tsc"

class IntroduceBufferAuxiliaryVars(CythonTransform):

    #
    # Entry point
    #

    def __call__(self, node):
        assert isinstance(node, ModuleNode)
        try:
            cymod = self.context.modules[u'__cython__']
        except KeyError:
            # No buffer fun for this module
            return node
        self.bufstruct_type = cymod.entries[u'Py_buffer'].type
        self.tscheckers = {}
        self.ts_funcs = []
        self.ts_item_checkers = {}
        self.module_scope = node.scope
        self.module_pos = node.pos
        result = super(IntroduceBufferAuxiliaryVars, self).__call__(node)
        # Register ts stuff
        if "endian.h" not in node.scope.include_files:
            node.scope.include_files.append("endian.h")
        result.body.stats += self.ts_funcs
        return result


    #
    # Basic operations for transforms
    #
    def handle_scope(self, node, scope):
        # For all buffers, insert extra variables in the scope.
        # The variables are also accessible from the buffer_info
        # on the buffer entry
        bufvars = [entry for name, entry
                   in scope.entries.iteritems()
                   if entry.type.is_buffer]

        if isinstance(node, ModuleNode) and len(bufvars) > 0:
            # for now...note that pos is wrong 
            raise CompileError(node.pos, "Buffer vars not allowed in module scope")
        for entry in bufvars:
            name = entry.name
            buftype = entry.type

            # Get or make a type string checker
            tschecker = self.tschecker(buftype.dtype)

            # Declare auxiliary vars
            cname = scope.mangle(Naming.bufstruct_prefix, name)
            bufinfo = scope.declare_var(name="$%s" % cname, cname=cname,
                                        type=self.bufstruct_type, pos=node.pos)

            bufinfo.used = True

            def var(prefix, idx):
                cname = scope.mangle(prefix, "%d_%s" % (idx, name))
                result = scope.declare_var("$%s" % cname, PyrexTypes.c_py_ssize_t_type,
                                         node.pos, cname=cname, is_cdef=True)
                result.init = "0"
                if entry.is_arg:
                    result.used = True
                return result
            
            stridevars = [var(Naming.bufstride_prefix, i) for i in range(entry.type.ndim)]
            shapevars = [var(Naming.bufshape_prefix, i) for i in range(entry.type.ndim)]            
            entry.buffer_aux = Symtab.BufferAux(bufinfo, stridevars, shapevars, tschecker)
            
        scope.buffer_entries = bufvars
        self.scope = scope

    def visit_ModuleNode(self, node):
        node.scope.use_utility_code(buffer_boundsfail_error_utility_code)
        self.handle_scope(node, node.scope)
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        self.handle_scope(node, node.local_scope)
        self.visitchildren(node)
        return node

    #
    # Utils for creating type string checkers
    #
    
    def new_ts_func(self, name, code):
        cname = "%s_%s" % (tsprefix, name)
        funcnode = PureCFuncNode(self.module_pos, cname, tschecker_functype, code)
        funcnode.analyse_expressions(self.module_scope)
        self.ts_funcs.append(funcnode)
        return funcnode        
    
    def mangle_dtype_name(self, dtype):
        # Use prefixes to seperate user defined types from builtins
        # (consider "typedef float unsigned_int")
        return dtype.declaration_code("").replace(" ", "_")
        
    def get_ts_check_item(self, dtype):
        # See if we can consume one (unnamed) dtype as next item
        funcnode = self.ts_item_checkers.get(dtype)
        if funcnode is None:
            char = dtype.typestring
            if char is not None and len(char) == 1:
                # Can use direct comparison
                funcnode = self.new_ts_func("natitem_%s" % self.mangle_dtype_name(dtype), """\
  if (*ts != '%s') {
    PyErr_Format(PyExc_TypeError, "Buffer datatype mismatch (rejecting on '%%s')", ts);
  return NULL;
  } else return ts + 1;
""" % char)
            else:
                # Must deduce sign and length; rely on int vs. float to be correctly declared
                ctype = dtype.declaration_code("")
                
                code = """\
  int ok;
  switch (*ts) {"""
                if dtype.is_int:
                    types = [
                        ('b', 'char'), ('h', 'short'), ('i', 'int'),
                        ('l', 'long'), ('q', 'long long')
                    ]
                    code += "".join(["""\
    case '%s': ok = (sizeof(%s) == sizeof(%s) && (%s)-1 < 0); break;
    case '%s': ok = (sizeof(%s) == sizeof(%s) && (%s)-1 > 0); break;
""" % (char, ctype, against, ctype, char.upper(), ctype, "unsigned " + against, ctype) for
                                     char, against in types])
                    code += """\
    default: ok = 0;
  }
  if (!ok) {
    PyErr_Format(PyExc_TypeError, "Buffer datatype mismatch (rejecting on '%s')", ts);
    return NULL;
  } else return ts + 1;
"""
                
                funcnode = self.new_ts_func("tdefitem_%s" % self.mangle_dtype_name(dtype), code)
                
            self.ts_item_checkers[dtype] = funcnode
        return funcnode.entry.cname

    ts_consume_whitespace_cname = None
    ts_check_endian_cname = None

    def ensure_ts_utils(self):
        # Makes sure that the typechecker utils are in scope
        # (and constructs them if not)
        if self.ts_consume_whitespace_cname is None:
            self.ts_consume_whitespace_cname = self.new_ts_func("consume_whitespace", """\
  while (1) {
    switch (*ts) {
      case 10:
      case 13:
      case ' ':
        ++ts;
      default:
        return ts;
    }
  }
""").entry.cname
        if self.ts_check_endian_cname is None:
            self.ts_check_endian_cname = self.new_ts_func("check_endian", """\
  int ok = 1;
  switch (*ts) {
    case '@':
    case '=':
      ++ts; break;
    case '<':
      if (__BYTE_ORDER == __LITTLE_ENDIAN) ++ts;
      else ok = 0;
      break;
    case '>':
    case '!':
      if (__BYTE_ORDER == __BIG_ENDIAN) ++ts;
      else ok = 0;
      break;
  }
  if (!ok) {
    PyErr_Format(PyExc_TypeError, "Data has wrong endianness (rejecting on '%s')", ts);
    return NULL;
  }
  return ts;
""").entry.cname
            
    def create_ts_check_simple(self, dtype):
        # Check whole string for single unnamed item
        consume_whitespace = self.ts_consume_whitespace_cname
        check_endian = self.ts_check_endian_cname
        check_item = self.get_ts_check_item(dtype)
        return self.new_ts_func("simple_%s" % self.mangle_dtype_name(dtype), """\
  ts = %(consume_whitespace)s(ts);
  ts = %(check_endian)s(ts);
  if (!ts) return NULL;
  ts = %(consume_whitespace)s(ts);
  ts = %(check_item)s(ts);
  if (!ts) return NULL;
  ts = %(consume_whitespace)s(ts);
  if (*ts != 0) {
    PyErr_Format(PyExc_TypeError, "Data too long (rejecting on '%%s')", ts);
    return NULL;
  }
  return ts;
""" % locals())

    def tschecker(self, dtype):
        # Creates a type string checker function for the given type.
        # Each checker is created as a function entry in the module scope
        # and a PureCNode and put in the self.ts_checkers dict.
        # Also the entry is returned.
        #
        # TODO: __eq__ and __hash__ for types

        self.ensure_ts_utils()
        funcnode = self.tscheckers.get(dtype)
        if funcnode is None:
            if dtype.is_struct_or_union:
                assert False
            elif dtype.is_int or dtype.is_float:
                # This includes simple typedef-ed types
                funcnode = self.create_ts_check_simple(dtype)
            else:
                assert False
            self.tscheckers[dtype] = funcnode
        return funcnode.entry

    

class BufferTransform(CythonTransform):
    """
    Run after type analysis. Takes care of the buffer functionality.

    Expects to be run on the full module. If you need to process a fragment
    one should look into refactoring this transform.
    """
    # Abbreviations:
    # "ts" means typestring and/or typestring checking stuff
    
    scope = None

    #
    # Entry point
    #

    def __call__(self, node):
        assert isinstance(node, ModuleNode)
        
        try:
            cymod = self.context.modules[u'__cython__']
        except KeyError:
            # No buffer fun for this module
            return node
        self.bufstruct_type = cymod.entries[u'Py_buffer'].type
        self.tscheckers = {}
        self.ts_funcs = []
        self.ts_item_checkers = {}
        self.module_scope = node.scope
        self.module_pos = node.pos
        result = super(BufferTransform, self).__call__(node)
        # Register ts stuff
        if "endian.h" not in node.scope.include_files:
            node.scope.include_files.append("endian.h")
        result.body.stats += self.ts_funcs
        return result



    acquire_buffer_fragment = TreeFragment(u"""
        __cython__.PyObject_GetBuffer(<__cython__.PyObject*>SUBJECT, &BUFINFO, 0)
        TSCHECKER(<char*>BUFINFO.format)
    """)
    fetch_strides = TreeFragment(u"""
        TARGET = BUFINFO.strides[IDX]
    """)

    fetch_shape = TreeFragment(u"""
        TARGET = BUFINFO.shape[IDX]
    """)

    def acquire_buffer_stats(self, entry, buffer_aux, pos):
        # Just the stats for acquiring and unpacking the buffer auxiliaries
        auxass = []
        for idx, strideentry in enumerate(buffer_aux.stridevars):
            strideentry.used = True
            ass = self.fetch_strides.substitute({
                u"TARGET": NameNode(pos, name=strideentry.name),
                u"BUFINFO": NameNode(pos, name=buffer_aux.buffer_info_var.name),
                u"IDX": IntNode(pos, value=EncodedString(idx)),
            })
            auxass += ass.stats

        for idx, shapeentry in enumerate(buffer_aux.shapevars):
            shapeentry.used = True
            ass = self.fetch_shape.substitute({
                u"TARGET": NameNode(pos, name=shapeentry.name),
                u"BUFINFO": NameNode(pos, name=buffer_aux.buffer_info_var.name),
                u"IDX": IntNode(pos, value=EncodedString(idx))
            })
            auxass += ass.stats
        buffer_aux.buffer_info_var.used = True
        acq = self.acquire_buffer_fragment.substitute({
            u"SUBJECT" : NameNode(pos, name=entry.name),
            u"BUFINFO": NameNode(pos, name=buffer_aux.buffer_info_var.name),
            u"TSCHECKER": NameNode(pos, name=buffer_aux.tschecker.name)
        }, pos=pos)
        return acq.stats + auxass
                
    def acquire_argument_buffer_stats(self, entry, pos):
        # On function entry, not getting a buffer is an uncatchable
        # exception, so we don't need to worry about what happens if
        # we don't get a buffer.
        stats = self.acquire_buffer_stats(entry, entry.buffer_aux, pos)
        for s in stats:
            s.analyse_declarations(self.scope)
            #s.analyse_expressions(self.scope)
        return stats

    # Notes: The cast to <char*> gets around Cython not supporting const types
    reacquire_buffer_fragment = TreeFragment(u"""
        TMP = LHS
        if TMP is not None:
            __cython__.PyObject_ReleaseBuffer(<__cython__.PyObject*>TMP, &BUFINFO)
        TMP = RHS
        if TMP is not None:
            ACQUIRE
        LHS = TMP
    """)

    def reacquire_buffer(self, node):
        buffer_aux = node.lhs.entry.buffer_aux
        acquire_stats = self.acquire_buffer_stats(buffer_aux.temp_var, buffer_aux, node.pos)
        acq = self.reacquire_buffer_fragment.substitute({
            u"TMP" : NameNode(pos=node.pos, name=buffer_aux.temp_var.name),
            u"LHS" : node.lhs,
            u"RHS": node.rhs,
            u"ACQUIRE": StatListNode(node.pos, stats=acquire_stats),
            u"BUFINFO": NameNode(pos=node.pos, name=buffer_aux.buffer_info_var.name)
        }, pos=node.pos)
        # Preserve first assignment info on LHS
        if node.first:
            # TODO: Prettier code
            acq.stats[4].first = True
            del acq.stats[0]
            del acq.stats[0]
        # Note: The below should probably be refactored into something
        # like fragment.substitute(..., context=self.context), with
        # TreeFragment getting context.pipeline_until_now() and
        # applying it on the fragment.
        acq.analyse_declarations(self.scope)
        acq.analyse_expressions(self.scope)
        stats = acq.stats
        return stats

    def assign_into_buffer(self, node):
        result = SingleAssignmentNode(node.pos,
                                      rhs=self.visit(node.rhs),
                                      lhs=self.buffer_index(node.lhs))
        result.analyse_expressions(self.scope)
        return result
        

    buffer_cleanup_fragment = TreeFragment(u"""
        if BUF is not None:
            __cython__.PyObject_ReleaseBuffer(<__cython__.PyObject*>BUF, &BUFINFO)
    """)
    def funcdef_buffer_cleanup(self, node, pos):
        env = node.local_scope
        cleanups = [self.buffer_cleanup_fragment.substitute({
                u"BUF" : NameNode(pos, name=entry.name),
                u"BUFINFO": NameNode(pos, name=entry.buffer_aux.buffer_info_var.name)
                }, pos=pos)
            for entry in node.local_scope.buffer_entries]
        cleanup_stats = []
        for c in cleanups: cleanup_stats += c.stats
        cleanup = StatListNode(pos, stats=cleanup_stats)
        cleanup.analyse_expressions(env) 
        result = TryFinallyStatNode.create_analysed(pos, env, body=node.body, finally_clause=cleanup)
        node.body = StatListNode.create_analysed(pos, env, stats=[result])
        return node
        
    #
    # Transforms
    #
    
    def visit_ModuleNode(self, node):
        self.handle_scope(node, node.scope)
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        self.handle_scope(node, node.local_scope)
        self.visitchildren(node)
        node = self.funcdef_buffer_cleanup(node, node.pos)
        stats = []
        for arg in node.local_scope.arg_entries:
            if arg.type.is_buffer:
                stats += self.acquire_argument_buffer_stats(arg, node.pos)
        node.body.stats = stats + node.body.stats
        return node


# TODO:
# - buf must be NULL before getting new buffer

