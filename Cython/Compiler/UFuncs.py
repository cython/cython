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
    import pdb; pdb.set_trace()
    error(pos, "Type '%s' cannot be used as a ufunc argument" % type_)

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
    """
    Finds the CFuncDefNode in the tree

    The assumption is that there's only one CFuncDefNode
    """
    found_node = None

    def visit_Node(self, node):
        if self.found_node:
            return
        else:
            self.visitchildren(node)

    def visit_CFuncDefNode(self, node):
        self.found_node = node

    def __call__(self, tree):
        self.visit(tree)
        return self.found_node



class NameFinderVisitor(TreeVisitor):
    """
    Finds the names of all the NameNodes in the tree
    """
    def __init__(self):
        super(NameFinderVisitor, self).__init__()
        self.names = set()

    def visit_Node(self, node):
        self.visitchildren(node)

    def visit_NameNode(self, node):
        self.names.add(node.name)

    def __call__(self, tree):
        self.visit(tree)
        return self.names


class UFuncPyObjectTargetNode(ExprNodes.ExprNode):
    """
    Takes ownership of a pyobject and assigns it to the output
    char* in a ufunc. This node exists because it's quite difficult
    to do the right casts in Cython

    target   NameNode
    """
    subexprs = ["target"]
    is_temp = False

    def analyse_target_declaration(self, env):
        self.target.analyse_target_declaration(env)

    def analyse_types(self, env):
        assert False, "Should only be used as a target"
        return self

    def analyse_target_types(self, env):
        self.target = self.target.analyse_types(env)
        assert self.target.is_name
        assert (self.target.type.is_ptr and self.target.type.base_type.is_int and
                    self.target.type.base_type.rank == 0)
        assert self.type.is_pyobject
        return self

    def generate_assignment_code(self, rhs, code, overloaded_assignment=False,
                                 exception_check=None, exception_value=None):
        code.putln("*((PyObject**)%s) = %s;" % (self.target.result(), rhs.result()))
        code.put_giveref(rhs.result(), rhs.type)
        code.putln("%s = 0;" % rhs.result())
        rhs.free_temps(code)



class ReplaceReturnsTransform(VisitorTransform):
    """
    Replace the return statement in a function with an assignment

    The user defines a Cython ufunc with a single short function. To convert it
    into a real ufunc Cython inserts that function into a loop, and the return
    statement should be converted to an assignment
    """
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
                cast_node = UFuncPyObjectTargetNode(node.pos, target=name_node, type=out_type)
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
                stats = [ Nodes.SingleAssignmentNode(
                    node.pos,
                    lhs=nn, rhs=arg) for nn, arg in zip(write_nodes, node.value.args) ])


class _ArgumentInfo(object):
    """
    Everything related to defining an input/output argument for a ufunc

    name  - str - name in the generated code
    arg_name  - str or None - only defined for "in" arguments
    type  - PyrexType
    type_constant  - str such as "NPY_INT8" representing numpy dtype constants
    """
    def __init__(self, name, type, type_constant, arg_name=None):
        self.name = name
        self.arg_name = arg_name
        self.type = type
        self.type_constant = type_constant


class UFuncConversion(object):
    def __init__(self, node):
        self.node = node
        self.global_scope = node.local_scope.global_scope()

        names = NameFinderVisitor()(node.ufunc_body)
        self.name_handler = _UniquePyNameHandler(set(node.local_scope.entries.keys()).union(names))

        self.in_definitions = self.get_in_type_info()
        self.out_definitions = self.get_out_type_info()

        cname = node.entry.cname

        self.step_names = [
            self.name_handler.get_unique_py_name("step%s" % n)
            for n in range(len(self.in_definitions)+len(self.out_definitions))
        ]

    def get_in_type_info(self):
        definitions = []
        for n, arg in enumerate(self.node.args):
            in_name = self.name_handler.get_unique_py_name("in%s" % n)
            type_const = _get_type_constant(self.node.pos, arg.type)
            definitions.append(_ArgumentInfo(in_name, arg.type, type_const, arg.name))
        return definitions

    def get_out_type_info(self):
        if self.node.return_type.is_ctuple:
            components = self.node.return_type.components
        else:
            components = [ self.node.return_type ]
        definitions = []
        for n, type in enumerate(components):
            out_name = self.name_handler.get_unique_py_name("out%s" % n)
            definitions.append(_ArgumentInfo(out_name, type, _get_type_constant(self.node.pos, type)))
        return definitions

    def generate_cy_utility_code(self):
        in_names, arg_types, arg_names = zip(*[
            (a.name, a.type, a.arg_name) for a in self.in_definitions
        ])
        out_names, out_types = zip(*[
            (a.name, a.type) for a in self.out_definitions
        ])

        context = dict(func_cname=self.node.entry.cname,
                   args=self.name_handler.get_unique_py_name("args"),
                   dimensions=self.name_handler.get_unique_py_name("dimensions"),
                   steps=self.name_handler.get_unique_py_name("steps"),
                   data=self.name_handler.get_unique_py_name("data"),
                   i=self.name_handler.get_unique_py_name("i"),
                   n=self.name_handler.get_unique_py_name("n"),
                   in_names=in_names, step_names=self.step_names,
                   arg_names=arg_names, arg_types=arg_types,
                   out_names=out_names, out_types=out_types)

        code = CythonUtilityCode.load("UFuncDefinition", "UFuncs.pyx", context=context,
                                      outer_module_scope=self.global_scope)

        original_body = self.node.ufunc_body
        return_replacer = ReplaceReturnsTransform(out_names, out_types)
        original_body = return_replacer(original_body)

        def pipeline_modifier_function(pipeline):
            subs_trans = lambda root: TreeFragment.TemplateTransform()(
                root, {'UFUNC_BODY': original_body}, [], None)
            pipeline.insert(0, subs_trans)
            # TODO - if we need a bit of help to pick up @cython.locals or similar
            # from the original function, this is the place to do it
        tree = code.get_tree(entries_only=True, modify_pipeline_callback=pipeline_modifier_function)
        return tree

    def generate_ufunc_initialization(self, func_cnames):
        #def initialize_constants(pos, func_name, docstr, global_scope, func_cnames, in_type_constants, out_type_constants):
        ufunc_funcs_name = self.global_scope.next_id(Naming.pyrex_prefix + "funcs")
        ufunc_types_name = self.global_scope.next_id(Naming.pyrex_prefix + "types")
        ufunc_data_name = self.global_scope.next_id(Naming.pyrex_prefix + "data")
        in_type_constants = [ d.type_constant for d in self.in_definitions ]
        out_type_constants = [ d.type_constant for d in self.out_definitions ]

        context = dict(
            ufunc_funcs_name = ufunc_funcs_name,
            func_cnames = func_cnames,
            ufunc_types_name = ufunc_types_name,
            type_constants = in_type_constants+out_type_constants,
            ufunc_data_name = ufunc_data_name,
        )
        self.global_scope.use_utility_code(
            TempitaUtilityCode.load("UFuncConsts", "UFuncs_C.c",
                                        context=context))

        pos = self.node.pos
        func_name = self.node.entry.name
        docstr = self.node.doc
        args_to_func = '%s(), %s, %s(), 1, %s, %s, PyUFunc_None, "%s", %s, 0' % (
            ufunc_funcs_name,
            ufunc_data_name,
            ufunc_types_name,
            len(in_type_constants),
            len(out_type_constants),
            func_name, docstr.as_c_string_literal() if docstr else "NULL")

        call_node = ExprNodes.PythonCapiCallNode(
            pos,
            function_name="PyUFunc_FromFuncAndData",
            # use a dummy type because it's honestly too fiddly
            func_type=PyrexTypes.CFuncType(
                PyrexTypes.py_object_type, [
                    PyrexTypes.CFuncTypeArg("dummy", PyrexTypes.c_void_ptr_type, None)]),
                args=[ExprNodes.ConstNode(pos, type=PyrexTypes.c_void_ptr_type, value=args_to_func)])
        del self.global_scope.entries[func_name]  # because we've overridden it
        lhs_entry = self.global_scope.declare_var(func_name, PyrexTypes.py_object_type, pos)
        assgn_node = Nodes.SingleAssignmentNode(
            pos,
            lhs=ExprNodes.NameNode(pos, name=func_name, type=PyrexTypes.py_object_type, entry=lhs_entry),
            rhs=call_node)
        return assgn_node

    def use_generic_utility_code(self):
        # use the invariant C utility code
        self.global_scope.use_utility_code(
            UtilityCode.load_cached("UFuncsInit", "UFuncs_C.c"))
        self.global_scope.use_utility_code(
                    UtilityCode.load_cached("NumpyImportUFunc", "NumpyImportArray.c"))

    def get_generated_stats(self):
        tree = self.generate_cy_utility_code()
        ufunc_node = FindCFuncDefNode()(tree)

        capi_func = self.generate_ufunc_initialization([ufunc_node.entry.cname])

        return [ufunc_node, capi_func]


def convert_to_ufunc(node):
    if not isinstance(node, Nodes.CFuncDefNode):
        error(node.pos, "Only C functions can be converted to a ufunc")
        return node
    if node.local_scope.parent_scope.is_c_class_scope:
        error(node.pos, "Methods cannot currently be converted to a ufunc")
        return node

    converter = UFuncConversion(node)
    converter.use_generic_utility_code()
    return converter.get_generated_stats()


def protect_node_body(node):
    # stash the body out of the way so that it doesn't get transformed
    # allowing us to use it "fresh" later
    node.ufunc_body = node.body
    node.body = Nodes.StatListNode(node.body.pos, stats=[])
