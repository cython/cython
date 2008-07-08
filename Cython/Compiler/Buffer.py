from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Utils import EncodedString
from Cython.Compiler.Errors import CompileError
from sets import Set as set

class BufferTransform(CythonTransform):
    """
    Run after type analysis. Takes care of the buffer functionality.
    """
    scope = None

    def __call__(self, node):
        cymod = self.context.modules[u'__cython__']
        self.buffer_type = cymod.entries[u'Py_buffer'].type
        return super(BufferTransform, self).__call__(node)

    def handle_scope(self, node, scope):
        # For all buffers, insert extra variables in the scope.
        # The variables are also accessible from the buffer_info
        # on the buffer entry
        bufvars = [(name, entry) for name, entry
                   in scope.entries.iteritems()
                   if entry.type.buffer_options is not None]
                   
        for name, entry in bufvars:
            # Variable has buffer opts, declare auxiliary vars
            bufopts = entry.type.buffer_options

            bufinfo = scope.declare_var(temp_name_handle(u"%s_bufinfo" % name),
                                        self.buffer_type, node.pos)

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
                                                shapevars)
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

    acquire_buffer_fragment = TreeFragment(u"""
        TMP = LHS
        if TMP is not None:
            __cython__.PyObject_ReleaseBuffer(<__cython__.PyObject*>TMP, &BUFINFO)
        TMP = RHS
        __cython__.PyObject_GetBuffer(<__cython__.PyObject*>TMP, &BUFINFO, 0)
        ASSIGN_AUX
        LHS = TMP
    """)

    fetch_strides = TreeFragment(u"""
        TARGET = BUFINFO.strides[IDX]
    """)

    fetch_shape = TreeFragment(u"""
        TARGET = BUFINFO.shape[IDX]
    """)

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
        
    def reacquire_buffer(self, node):
        bufaux = node.lhs.entry.buffer_aux
        auxass = []
        for idx, entry in enumerate(bufaux.stridevars):
            entry.used = True
            ass = self.fetch_strides.substitute({
                u"TARGET": NameNode(node.pos, name=entry.name),
                u"BUFINFO": NameNode(node.pos, name=bufaux.buffer_info_var.name),
                u"IDX": IntNode(node.pos, value=EncodedString(idx))
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
            u"BUFINFO": NameNode(pos=node.pos, name=bufaux.buffer_info_var.name)
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

    def visit_CallNode(self, node):
###        print node.dump()
        return node
    
#    def visit_FuncDefNode(self, node):
#        print node.dump()
    
