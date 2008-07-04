
from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Utils import EncodedString
from Cython.Compiler.Errors import CompileError
from sets import Set as set

class NormalizeTree(CythonTransform):
    """
    This transform fixes up a few things after parsing
    in order to make the parse tree more suitable for
    transforms.

    a) After parsing, blocks with only one statement will
    be represented by that statement, not by a StatListNode.
    When doing transforms this is annoying and inconsistent,
    as one cannot in general remove a statement in a consistent
    way and so on. This transform wraps any single statements
    in a StatListNode containing a single statement.

    b) The PassStatNode is a noop and serves no purpose beyond
    plugging such one-statement blocks; i.e., once parsed a
`    "pass" can just as well be represented using an empty
    StatListNode. This means less special cases to worry about
    in subsequent transforms (one always checks to see if a
    StatListNode has no children to see if the block is empty).
    """

    def __init__(self, context):
        super(NormalizeTree, self).__init__(context)
        self.is_in_statlist = False
        self.is_in_expr = False

    def visit_ExprNode(self, node):
        stacktmp = self.is_in_expr
        self.is_in_expr = True
        self.visitchildren(node)
        self.is_in_expr = stacktmp
        return node

    def visit_StatNode(self, node, is_listcontainer=False):
        stacktmp = self.is_in_statlist
        self.is_in_statlist = is_listcontainer
        self.visitchildren(node)
        self.is_in_statlist = stacktmp
        if not self.is_in_statlist and not self.is_in_expr:
            return StatListNode(pos=node.pos, stats=[node])
        else:
            return node

    def visit_PassStatNode(self, node):
        if not self.is_in_statlist:
            return StatListNode(pos=node.pos, stats=[])
        else:
            return []

    def visit_StatListNode(self, node):
        self.is_in_statlist = True
        self.visitchildren(node)
        self.is_in_statlist = False
        return node

    def visit_ParallelAssignmentNode(self, node):
        return self.visit_StatNode(node, True)
    
    def visit_CEnumDefNode(self, node):
        return self.visit_StatNode(node, True)

    def visit_CStructOrUnionDefNode(self, node):
        return self.visit_StatNode(node, True)


class PostParseError(CompileError): pass

# error strings checked by unit tests, so define them
ERR_BUF_OPTION_UNKNOWN = '"%s" is not a buffer option'
ERR_BUF_TOO_MANY = 'Too many buffer options'
ERR_BUF_DUP = '"%s" buffer option already supplied'
ERR_BUF_MISSING = '"%s" missing'
ERR_BUF_INT = '"%s" must be an integer'
ERR_BUF_NONNEG = '"%s" must be non-negative'

class PostParse(CythonTransform):
    """
    Basic interpretation of the parse tree, as well as validity
    checking that can be done on a very basic level on the parse
    tree (while still not being a problem with the basic syntax,
    as such).

    Specifically:
    - CBufferAccessTypeNode has its options interpreted:
    Any first positional argument goes into the "dtype" attribute,
    any "ndim" keyword argument goes into the "ndim" attribute and
    so on. Also it is checked that the option combination is valid.

    Note: Currently Parsing.py does a lot of interpretation and
    reorganization that can be refactored into this transform
    if a more pure Abstract Syntax Tree is wanted.
    """

    buffer_options = ("dtype", "ndim") # ordered!
    def visit_CBufferAccessTypeNode(self, node):
        options = {}
        # Fetch positional arguments
        if len(node.positional_args) > len(self.buffer_options):
            self.context.error(ERR_BUF_TOO_MANY)
        for arg, unicode_name in zip(node.positional_args, self.buffer_options):
            name = str(unicode_name)
            options[name] = arg
        # Fetch named arguments
        for item in node.keyword_args.key_value_pairs:
            name = str(item.key.value)
            if not name in self.buffer_options:
                raise PostParseError(item.key.pos,
                                     ERR_BUF_UNKNOWN % name)
            if name in options.keys():
                raise PostParseError(item.key.pos,
                                     ERR_BUF_DUP % key)
            options[name] = item.value

        provided = options.keys()
        # get dtype
        dtype = options.get("dtype")
        if dtype is None: raise PostParseError(node.pos, ERR_BUF_MISSING % 'dtype')
        node.dtype_node = dtype

        # get ndim
        if "ndim" in provided:
            ndimnode = options["ndim"]
            if not isinstance(ndimnode, IntNode):
                # Compile-time values (DEF) are currently resolved by the parser,
                # so nothing more to do here
                raise PostParseError(ndimnode.pos, ERR_BUF_INT % 'ndim')
            ndim_value = int(ndimnode.value)
            if ndim_value < 0:
                raise PostParseError(ndimnode.pos, ERR_BUF_NONNEG % 'ndim')
            node.ndim = int(ndimnode.value)
        else:
            node.ndim = 1
        
        # We're done with the parse tree args
        node.positional_args = None
        node.keyword_args = None
        return node

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

#                ass = SingleAssignmentNode(pos=node.pos,
#                    lhs=NameNode(node.pos, name=entry.name),
#                    rhs=IndexNode(node.pos,
#                        base=AttributeNode(node.pos,
#                            obj=NameNode(node.pos, name=bufaux.buffer_info_var.name),
#                            attribute=EncodedString("strides")),
#                        index=IntNode(node.pos, value=EncodedString(idx))))
#                print ass.dump()
    def visit_SingleAssignmentNode(self, node):
        self.visitchildren(node)
        bufaux = node.lhs.entry.buffer_aux
        if bufaux is not None:
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
#            stats += [node] # Do assignment after successful buffer acquisition
         #   print acq.dump()
            return stats
        else:
            return node

    buffer_access = TreeFragment(u"""
        (<unsigned char*>(BUF.buf + OFFSET))[0]
    """)
    def visit_IndexNode(self, node):
        if node.is_buffer_access:
            assert node.index is None
            assert node.indices is not None
            bufaux = node.base.entry.buffer_aux
            assert bufaux is not None
            to_sum = [ IntBinopNode(node.pos, operator='*', operand1=index,
                                    operand2=NameNode(node.pos, name=stride.name))
                for index, stride in zip(node.indices, bufaux.stridevars)]
            print to_sum

            indices = node.indices
            # reduce * on indices
            expr = to_sum[0]
            for next in to_sum[1:]:
                expr = IntBinopNode(node.pos, operator='+', operand1=expr, operand2=next)
            tmp= self.buffer_access.substitute({
                'BUF': NameNode(node.pos, name=bufaux.buffer_info_var.name),
                'OFFSET': expr
                })
            tmp.analyse_expressions(self.scope)
            return tmp.stats[0].expr
        else:
            return node

    def visit_CallNode(self, node):
###        print node.dump()
        return node
    
#    def visit_FuncDefNode(self, node):
#        print node.dump()
    

class WithTransform(CythonTransform):

    # EXCINFO is manually set to a variable that contains
    # the exc_info() tuple that can be generated by the enclosing except
    # statement.
    template_without_target = TreeFragment(u"""
        MGR = EXPR
        EXIT = MGR.__exit__
        MGR.__enter__()
        EXC = True
        try:
            try:
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, temps=[u'MGR', u'EXC', u"EXIT", u"SYS)"],
    pipeline=[NormalizeTree(None)])

    template_with_target = TreeFragment(u"""
        MGR = EXPR
        EXIT = MGR.__exit__
        VALUE = MGR.__enter__()
        EXC = True
        try:
            try:
                TARGET = VALUE
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, temps=[u'MGR', u'EXC', u"EXIT", u"VALUE", u"SYS"],
    pipeline=[NormalizeTree(None)])

    def visit_WithStatNode(self, node):
        excinfo_name = temp_name_handle('EXCINFO')
        excinfo_namenode = NameNode(pos=node.pos, name=excinfo_name)
        excinfo_target = NameNode(pos=node.pos, name=excinfo_name)
        if node.target is not None:
            result = self.template_with_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'TARGET' : node.target,
                u'EXCINFO' : excinfo_namenode
                }, pos = node.pos)
            # Set except excinfo target to EXCINFO
            result.stats[4].body.stats[0].except_clauses[0].excinfo_target = excinfo_target
        else:
            result = self.template_without_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'EXCINFO' : excinfo_namenode
                }, pos = node.pos)
            # Set except excinfo target to EXCINFO
            result.stats[4].body.stats[0].except_clauses[0].excinfo_target = excinfo_target
        
        return result.stats

class AnalyseDeclarationsTransform(CythonTransform):

    def __call__(self, root):
        self.env_stack = [root.scope]
        return super(AnalyseDeclarationsTransform, self).__call__(root)        
    
    def visit_ModuleNode(self, node):
        node.analyse_declarations(self.env_stack[-1])
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        lenv = node.create_local_scope(self.env_stack[-1])
        node.body.analyse_control_flow(lenv) # this will be totally refactored
        node.declare_arguments(lenv)
        node.body.analyse_declarations(lenv)
        self.env_stack.append(lenv)
        self.visitchildren(node)
        self.env_stack.pop()
        return node
        
class AnalyseExpressionsTransform(CythonTransform):
    def visit_ModuleNode(self, node):
        node.body.analyse_expressions(node.scope)
        self.visitchildren(node)
        return node
        
    def visit_FuncDefNode(self, node):
        node.body.analyse_expressions(node.local_scope)
        self.visitchildren(node)
        return node
        
class MarkClosureVisitor(CythonTransform):
    
    needs_closure = False
    
    def visit_FuncDefNode(self, node):
        self.needs_closure = False
        self.visitchildren(node)
        node.needs_closure = self.needs_closure
        self.needs_closure = True
        return node
        
    def visit_ClassDefNode(self, node):
        self.visitchildren(node)
        self.needs_closure = True
        return node
        
    def visit_YieldNode(self, node):
        self.needs_closure = True
        
class CreateClosureClasses(CythonTransform):
    # Output closure classes in module scope for all functions
    # that need it. 
    
    def visit_ModuleNode(self, node):
        self.module_scope = node.scope
        self.visitchildren(node)
        return node

    def create_class_from_scope(self, node, target_module_scope):
        as_name = temp_name_handle("closure")
        func_scope = node.local_scope

        entry = target_module_scope.declare_c_class(name = as_name,
            pos = node.pos, defining = True, implementing = True)
        class_scope = entry.type.scope
        for entry in func_scope.entries.values():
            class_scope.declare_var(pos=node.pos,
                                    name=entry.name,
                                    cname=entry.cname,
                                    type=entry.type,
                                    is_cdef=True)
            
    def visit_FuncDefNode(self, node):
        self.create_class_from_scope(node, self.module_scope)
        return node
        

