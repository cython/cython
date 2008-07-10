from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Utils import EncodedString
from Cython.Compiler.Errors import CompileError
import PyrexTypes
from sets import Set as set

class PureCFuncNode(Node):
    def __init__(self, pos, cname, type, c_code, visibility='private'):
        self.pos = pos
        self.cname = cname
        self.type = type
        self.c_code = c_code
        self.visibility = visibility

    def analyse_types(self, env):
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


    #
    # Basic operations for transforms
    #
    def handle_scope(self, node, scope):
        # For all buffers, insert extra variables in the scope.
        # The variables are also accessible from the buffer_info
        # on the buffer entry
        bufvars = [(name, entry) for name, entry
                   in scope.entries.iteritems()
                   if entry.type.buffer_options is not None]
                   
        for name, entry in bufvars:
            
            bufopts = entry.type.buffer_options

            # Get or make a type string checker
            tschecker = self.tschecker(bufopts.dtype)

            # Declare auxiliary vars
            bufinfo = scope.declare_var(temp_name_handle(u"%s_bufinfo" % name),
                                        self.bufstruct_type, node.pos)

            temp_var =  scope.declare_var(temp_name_handle(u"%s_tmp" % name),
                                        entry.type, node.pos)
            
            
            stridevars = []
            shapevars = []
            for idx in range(bufopts.ndim):
                # stride
                varname = temp_name_handle(u"%s_%s%d" % (name, "stride", idx))
                var = scope.declare_var(varname, PyrexTypes.c_int_type, node.pos, is_cdef=True)
                stridevars.append(var)
                # shape
                varname = temp_name_handle(u"%s_%s%d" % (name, "shape", idx))
                var = scope.declare_var(varname, PyrexTypes.c_uint_type, node.pos, is_cdef=True)
                shapevars.append(var)
            entry.buffer_aux = Symtab.BufferAux(bufinfo, stridevars, 
                                                shapevars, tschecker)
            entry.buffer_aux.temp_var = temp_var
        self.scope = scope

    # Notes: The cast to <char*> gets around Cython not supporting const types
    acquire_buffer_fragment = TreeFragment(u"""
        TMP = LHS
        if TMP is not None:
            __cython__.PyObject_ReleaseBuffer(<__cython__.PyObject*>TMP, &BUFINFO)
        TMP = RHS
        if TMP is not None:
            __cython__.PyObject_GetBuffer(<__cython__.PyObject*>TMP, &BUFINFO, 0)
            TSCHECKER(<char*>BUFINFO.format)
            ASSIGN_AUX
        LHS = TMP
    """)

    fetch_strides = TreeFragment(u"""
        TARGET = BUFINFO.strides[IDX]
    """)

    fetch_shape = TreeFragment(u"""
        TARGET = BUFINFO.shape[IDX]
    """)

    def reacquire_buffer(self, node):
        bufaux = node.lhs.entry.buffer_aux
        auxass = []
        for idx, entry in enumerate(bufaux.stridevars):
            entry.used = True
            ass = self.fetch_strides.substitute({
                u"TARGET": NameNode(node.pos, name=entry.name),
                u"BUFINFO": NameNode(node.pos, name=bufaux.buffer_info_var.name),
                u"IDX": IntNode(node.pos, value=EncodedString(idx)),
            })
            auxass.append(ass)

        for idx, entry in enumerate(bufaux.shapevars):
            entry.used = True
            ass = self.fetch_shape.substitute({
                u"TARGET": NameNode(node.pos, name=entry.name),
                u"BUFINFO": NameNode(node.pos, name=bufaux.buffer_info_var.name),
                u"IDX": IntNode(node.pos, value=EncodedString(idx))
            })
            auxass.append(ass)

        bufaux.buffer_info_var.used = True
        acq = self.acquire_buffer_fragment.substitute({
            u"TMP" : NameNode(pos=node.pos, name=bufaux.temp_var.name),
            u"LHS" : node.lhs,
            u"RHS": node.rhs,
            u"ASSIGN_AUX": StatListNode(node.pos, stats=auxass),
            u"BUFINFO": NameNode(pos=node.pos, name=bufaux.buffer_info_var.name),
            u"TSCHECKER": NameNode(node.pos, name=bufaux.tschecker.name)
        }, pos=node.pos)
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
        

    def buffer_index(self, node):
        pos = node.pos
        bufaux = node.base.entry.buffer_aux
        assert bufaux is not None
        # indices * strides...
        to_sum = [ IntBinopNode(pos, operator='*',
                                operand1=index, #PhaseEnvelopeNode(PhaseEnvelopeNode.ANALYSED, index),
                                operand2=NameNode(node.pos, name=stride.name))
            for index, stride in zip(node.indices, bufaux.stridevars)]

        # then sum them with the buffer pointer
        expr = AttributeNode(pos,
            obj=NameNode(pos, name=bufaux.buffer_info_var.name),
            attribute=EncodedString("buf"))
        for next in to_sum:
            expr = AddNode(pos, operator='+', operand1=expr, operand2=next)

        casted = TypecastNode(pos, operand=expr,
                              type=PyrexTypes.c_ptr_type(node.base.entry.type.buffer_options.dtype))
        result = IndexNode(pos, base=casted, index=IntNode(pos, value='0'))

        return result


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
        return node

    def visit_SingleAssignmentNode(self, node):
        # On assignments, two buffer-related things can happen:
        # a) A buffer variable is assigned to (reacquisition)
        # b) Buffer access assignment: arr[...] = ...
        # Since we don't allow nested buffers, these don't overlap.
        self.visitchildren(node)
        # Only acquire buffers on vars (not attributes) for now.
        if isinstance(node.lhs, NameNode) and node.lhs.entry.buffer_aux:
            # Is buffer variable
            return self.reacquire_buffer(node)
        elif (isinstance(node.lhs, IndexNode) and
              isinstance(node.lhs.base, NameNode) and
              node.lhs.base.entry.buffer_aux is not None):
            return self.assign_into_buffer(node)
        else:
            return node
        
    def visit_IndexNode(self, node):
        # Only occurs when the IndexNode is an rvalue
        if node.is_buffer_access:
            assert node.index is None
            assert node.indices is not None
            result = self.buffer_index(node)
            result.analyse_expressions(self.scope)
            return result
        else:
            return node

    #
    # Utils for creating type string checkers
    #
    
    def new_ts_func(self, name, code):
        cname = "%s_%s" % (tsprefix, name)
        funcnode = PureCFuncNode(self.module_pos, cname, tschecker_functype, code)
        funcnode.analyse_types(self.module_scope)
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
            if char is not None and len(char) > 1:
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



# TODO:
# - buf must be NULL before getting new buffer

