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
    def __init__(self, pos, cname, type, c_code):
        self.pos = pos
        self.cname = cname
        self.type = type
        self.c_code = c_code

    def analyse_types(self, env):
        self.entry = env.declare_cfunction(
            "<pure c function:%s>" % self.cname,
            self.type, self.pos, cname=self.cname,
            defining=True)

    def generate_function_definitions(self, env, code, transforms):
        # TODO: Fix constness, don't hack it
        assert self.type.optional_arg_count == 0
        arg_decls = [arg.declaration_code() for arg in self.type.args]
        sig = self.type.return_type.declaration_code(
            self.type.function_header_code(self.cname, ", ".join(arg_decls)))
        code.putln("")
        code.putln("%s {" % sig)
        code.put(self.c_code)
        code.putln("}")

    def generate_execution_code(self, code):
        pass

class BufferTransform(CythonTransform):
    """
    Run after type analysis. Takes care of the buffer functionality.
    """
    scope = None
    tschecker_functype = PyrexTypes.CFuncType(
        PyrexTypes.c_char_ptr_type,
        [PyrexTypes.CFuncTypeArg(EncodedString("ts"), PyrexTypes.c_char_ptr_type,
                      (0, 0, None), cname="ts")],
        exception_value = "NULL"
    )  

    def __call__(self, node):
        cymod = self.context.modules[u'__cython__']
        self.bufstruct_type = cymod.entries[u'Py_buffer'].type
        self.tscheckers = {}
        self.module_scope = node.scope
        self.module_pos = node.pos
        result = super(BufferTransform, self).__call__(node)
        result.body.stats += [node for node in self.tscheckers.values()]
        return result

    def tschecker_simple(self, dtype):
        char = dtype.typestring
        return """
  if (*ts != '%s') {
    PyErr_Format(PyExc_TypeError, "Buffer datatype mismatch");  
    return NULL;
  } else return ts + 1;
""" % char

    def tschecker(self, dtype):
        # Creates a type string checker function for the given type.
        # Each checker is created as a function entry in the module scope
        # and a PureCNode and put in the self.ts_checkers dict.
        # Also the entry is returned.
        #
        # TODO: __eq__ and __hash__ for types
        funcnode = self.tscheckers.get(dtype, None)
        if funcnode is None:
            assert dtype.is_int or dtype.is_float or dtype.is_struct_or_union
            # Use prefixes to seperate user defined types from builtins
            # (consider "typedef float unsigned_int")
            builtin = not (dtype.is_struct_or_union or dtype.is_typedef)
            if not builtin:
                prefix = "user"
            else:
                prefix = "builtin"
            cname = "check_typestring_%s_%s" % (prefix,
                       dtype.declaration_code("").replace(" ", "_"))

            if dtype.typestring is not None and len(dtype.typestring) == 1:
                code = self.tschecker_simple(dtype)
            else:
                assert False

            funcnode = PureCFuncNode(self.module_pos, cname,
                                     self.tschecker_functype, code)
            funcnode.analyse_types(self.module_scope)
            self.tscheckers[dtype] = funcnode
        return funcnode.entry

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

            
    def visit_ModuleNode(self, node):
        self.handle_scope(node, node.scope)
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        self.handle_scope(node, node.local_scope)
        self.visitchildren(node)
        return node

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
        bufaux = node.base.entry.buffer_aux
        assert bufaux is not None
        # indices * strides...
        to_sum = [ IntBinopNode(node.pos, operator='*',
                                operand1=index, #PhaseEnvelopeNode(PhaseEnvelopeNode.ANALYSED, index),
                                operand2=NameNode(node.pos, name=stride.name))
            for index, stride in zip(node.indices, bufaux.stridevars)]

        # then sum them 
        expr = to_sum[0]
        for next in to_sum[1:]:
            expr = IntBinopNode(node.pos, operator='+', operand1=expr, operand2=next)

        tmp= self.buffer_access.substitute({
            'BUF': NameNode(node.pos, name=bufaux.buffer_info_var.name),
            'OFFSET': expr
            }, pos=node.pos)

        return tmp.stats[0].expr


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
        
    buffer_access = TreeFragment(u"""
        (<unsigned char*>(BUF.buf + OFFSET))[0]
    """)
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

