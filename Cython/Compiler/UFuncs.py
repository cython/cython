from . import Nodes
from . import ExprNodes
from .Errors import error
from . import PyrexTypes
from .UtilityCode import CythonUtilityCode
from .Code import TempitaUtilityCode, UtilityCode
from .Visitor import PrintTree, TreeVisitor, VisitorTransform
from . import TreeFragment
from . import Pipeline
from . import ParseTreeTransforms
from . import Naming

numpy_int_types = ["NPY_BYTE", "NPY_INT8", "NPY_SHORT", "NPY_INT16", "NPY_INT",
                        "NPY_INT32", "NPY_LONG", "NPY_LONGLONG", "NPY_INT64"]
numpy_uint_types = [ tp.replace("NPY_", "NPY_U") for tp in numpy_int_types ]
# note: half float type is deliberately omitted
numpy_numeric_types = numpy_int_types + numpy_uint_types + [
    "NPY_FLOAT", "NPY_FLOAT32", "NPY_DOUBLE", "NPY_FLOAT64", "NPY_LONGDOUBLE",
]

def _get_type_constant(pos, type_):
    # 'is' checks don't seem to work for complex types
    if type_ == PyrexTypes.c_float_complex_type:
        return "NPY_CFLOAT"
    elif type_ == PyrexTypes.c_double_complex_type:
        return "NPY_CDOUBLE"
    elif type_ == PyrexTypes.c_longdouble_complex_type:
        return "NPY_CLONGDOUBLE"
    elif type_.is_numeric:
        postfix = str(type_).upper().replace(" ", "")
        typename = "NPY_%s" % postfix
        if typename in numpy_numeric_types:
            return typename
    elif type_.is_pyobject:
        return "NPY_OBJECT"
    # TODO possible NPY_BOOL to bint but it needs a cast?
    # TODO NPY_DATETIME, NPY_TIMEDELTA, NPY_STRING, NPY_UNICODE and maybe NPY_VOID might be handleable
    error(pos, "Type '%s' cannot be used as a ufunc argument" % type_)

def _get_in_type_constants(node):
    return [ _get_type_constant(node.pos, arg.type) for arg in node.args ]

def _get_out_type_info(node):
    if node.return_type.is_ctuple:
        return [ _get_type_constant(node.pos, c) for c in node.return_type.components ], node.return_type.components
    else:
        return [ _get_type_constant(node.pos, node.return_type) ],  [ node.return_type ]

class _UniquePyNameHandler(object):
    def __init__(self, existing_names):
        self.existing_names = existing_names
        self.extra_names = set()

    def get_unique_py_name(self, name):
        while name in self.existing_names or name in self.extra_names:
            name += "_"
        self.extra_names.add(name)
        return name

class FindCFuncDefNode(TreeVisitor):
    found_node = None

    def visit_Node(self, node):
        if self.found_node:
            return
        else:
            self.visitchildren(node)

    def visit_CFuncDefNode(self, node):
        self.found_node = node


class NameFinderVisitor(TreeVisitor):
    visit_Node = TreeVisitor.recurse_to_children

    def __init__(self):
        super(NameFinderVisitor, TreeVisitor).__init__()
        self.names = set()

    def visit_NameNode(self, node):
        self.names.add(node.name)


class ReplaceReturnsTransform(VisitorTransform):
    def __init__(self, out_names, out_types):
        super(ReplaceReturnsTransform, self).__init__()
        self.out_names = out_names
        self.out_types = out_types

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def visit_ReturnStatNode(self, node):
        if len(self.out_names) == 0:
            return None
        write_nodes = []
        for out_name, out_type in zip(self.out_names, self.out_types):
            name_node = ExprNodes.NameNode(node.pos, name=out_name)
            if not out_type.is_pyobject:
                cast_node = ExprNodes.TypecastNode(node.pos, operand=name_node,
                                                type=PyrexTypes.c_ptr_type(out_type))
                index_node = ExprNodes.IndexNode(node.pos, base=cast_node,
                                                 index=ExprNodes.IntNode(node.pos, value="0"))
                write_nodes.append(index_node)
            else:
                cast_node = ExprNodes.TypecastNode(node.pos, operand=name_node, type=out_type)
                write_nodes.append(cast_node)
        if (len(write_nodes) == 1 or not node.value.is_sequence_constructor or
                node.value.mult_factor or len(node.value.args) != len(write_nodes)):
            lhs = write_nodes[0] if len(write_nodes)==1 else ExprNodes.TupleNode(
                node.pos, args=write_nodes)
            return Nodes.SingleAssignmentNode(
                node.pos,
                lhs=lhs,
                rhs=node.value)
        elif node.value:
            return Nodes.ParallelAssignmentNode(
                node.pos,
                assignments = [ Nodes.SingleAssignmentNode(
                    node.pos,
                    lhs=nn, rhs=arg) for nn, arg in zip(write_nodes, node.value.args) ])


def convert_to_ufunc(node):
    if not isinstance(node, Nodes.CFuncDefNode):
        error(node.pos, "Only C functions can be converted to a ufunc")
        return node
    if node.local_scope.parent_scope.is_c_class_scope:
        error(node.pos, "Methods cannot currently be converted to a ufunc")
        return node

    global_scope = node.local_scope.global_scope()

    in_type_constants = _get_in_type_constants(node)
    out_type_constants, out_types = _get_out_type_info(node)

    cname = node.entry.cname

    name_finder = NameFinderVisitor()
    name_finder(node.ufunc_body)
    name_handler = _UniquePyNameHandler(set(node.local_scope.keys()) + name_finder.names)

    in_names = []
    arg_names = []
    arg_types = []
    for n, arg in enumerate(node.args):
        in_names.append(name_handler.get_unique_py_name("in%s" % n))
        arg_names.append(arg.name)
        arg_types.append(arg.type)
    out_names = []
    for n in range(len(out_types)):
        out_names.append(name_handler.get_unique_py_name("out%s" % n))

    step_names = [ name_handler.get_unique_py_name("step%s" % n)
                   for n in range(len(in_type_constants)+len(out_type_constants)) ]

    context = dict(func_cname=cname,
                   args=name_handler.get_unique_py_name("args"),
                   dimensions=name_handler.get_unique_py_name("dimensions"),
                   steps=name_handler.get_unique_py_name("steps"),
                   data=name_handler.get_unique_py_name("data"),
                   i=name_handler.get_unique_py_name("i"),
                   n=name_handler.get_unique_py_name("n"),
                   in_names=in_names, step_names=step_names,
                   arg_names=arg_names, arg_types=arg_types,
                   out_names=out_names, out_types=out_types)

    code = CythonUtilityCode.load("UFuncDefinition", "UFuncs.pyx", context=context,
                                  outer_module_scope=global_scope)
    original_body = node.ufunc_body
    return_replacer = ReplaceReturnsTransform(out_names, out_types)
    original_body = return_replacer(original_body)

    def pipeline_modifier_function(pipeline):
        subs_trans = lambda root: TreeFragment.TemplateTransform()(
            root, {'UFUNC_BODY': original_body}, [], None)
        pipeline.insert(0, subs_trans)
        # TODO - if we need a bit of help to pick up @cython.locals or similar
        # from the original function, this is the place to do it
    tree = code.get_tree(entries_only=True, modify_pipeline_callback=pipeline_modifier_function)

    PrintTree()(tree)

    cfunc_finder = FindCFuncDefNode()
    cfunc_finder.visit(tree)

    global_scope.use_utility_code(
        UtilityCode.load_cached("UFuncsInit", "UFuncs_C.c"))

    original_node = node
    node = cfunc_finder.found_node

    capi_func = initialize_constants(
        original_node.pos, original_node.entry.name,
        global_scope, [node.entry.cname],
        in_type_constants, out_type_constants)

    return [node, AddImportUFuncNode(node.pos), capi_func]

class AddImportUFuncNode(Nodes.Node):
    child_attrs = []
    def analyse_expressions(self, env):
        return self

    def generate_function_definitions(self, env, code):
        return

    def generate_execution_code(self, code):
        code.globalstate.use_utility_code(
                    UtilityCode.load_cached("NumpyImportUFunc", "NumpyImportArray.c")
            )

def protect_node_body(node):
    # stash the body out of the way so that it doesn't get transformed
    # allowing us to use it "fresh" later
    node.ufunc_body = node.body
    node.body = Nodes.StatListNode(node.body.pos, stats=[])

def initialize_constants(pos, func_name, global_scope, func_cnames, in_type_constants, out_type_constants):
    ufunc_funcs = global_scope.next_id(Naming.pyrex_prefix + "funcs")
    ufunc_types = global_scope.next_id(Naming.pyrex_prefix + "types")
    ufunc_data = global_scope.next_id(Naming.pyrex_prefix + "data")
    context = dict(
        ufunc_funcs_name = ufunc_funcs,
        func_cnames = func_cnames,
        ufunc_types_name = ufunc_types,
        type_constants = in_type_constants+out_type_constants,
        ufunc_data_name = ufunc_data,
    )
    global_scope.use_utility_code(
        TempitaUtilityCode.load("UFuncConsts", "UFuncs_C.c",
                                       context=context))

    args_to_func = '%s, %s, %s, 1, %s, %s, PyUFunc_None, "%s", NULL, 0' % (
        ufunc_funcs,
        ufunc_data,
        ufunc_types,
        len(in_type_constants),
        len(out_type_constants),
        func_name,)

    call_node = ExprNodes.PythonCapiCallNode(
        pos,
        function_name="PyUFunc_FromFuncAndData",
        # use a dummy type because it's honestly too fiddly
        func_type=PyrexTypes.CFuncType(
            PyrexTypes.py_object_type, [
                PyrexTypes.CFuncTypeArg("dummy", PyrexTypes.c_void_ptr_type, None)]),
            args=[ExprNodes.ConstNode(pos, type=PyrexTypes.c_void_ptr_type, value=args_to_func)])
    del global_scope.entries[func_name]  # because we've overridden it
    lhs_entry = global_scope.declare_var(func_name, PyrexTypes.py_object_type, pos)
    assgn_node = Nodes.SingleAssignmentNode(
        pos,
        lhs=ExprNodes.NameNode(pos, name=func_name, type=PyrexTypes.py_object_type, entry=lhs_entry),
        rhs=call_node)
    return assgn_node

