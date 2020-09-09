from __future__ import absolute_import

import cython
cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, LetNode=object,
               LetRefNode=object, TreeFragment=object, EncodedString=object,
               error=object, warning=object, copy=object, _unicode=object)

from .Nodes import CFuncDefNode
from .ExprNodes import AttributeNode, CallNode, ImportNode, NameNode

from . import Version

from .Visitor import TreeVisitor
from Cython.CodeWriter import IndentationWriter

class TypeStubGenerator(TreeVisitor, IndentationWriter):

    class Context:
        name = ""
        empty = True

        def __init__(self, name):
            self.name = name

    def __init__(self, result=None):
        TreeVisitor.__init__(self)
        IndentationWriter.__init__(self, result)

        self.context = []

    def visit_ModuleNode(self, node):

        self.context.append(self.Context(node.full_module_name))

        self.visitchildren(node)

        return node

    def _visit_indented(self, node):
        self.indent()
        self.visitchildren(node)
        self.dedent()

    @property
    def currentContext(self):
        return self.context[-1]

    def atModuleRoot(self):
        return len(self.context) == 1

    def visit_ImportNode(self, node):

        module_name = node.module_name.value

        self.currentContext.empty = False

        if node.name_list is None:
            self.putline("import %s" % module_name)
        else:
            names = (arg.value for arg in node.name_list.args)
            all_names = ", ".join(names)

            if node.level > 0:
                complete_level = "." * node.level
                module_name = "%s%s" % (complete_level, module_name)

            self.putline("from %s import %s" % (module_name, all_names))

        return node

    def visit_SingleAssignmentNode(self, node):

        if not isinstance(node.rhs, ImportNode):
            return node

        module_name = node.rhs.module_name.value

        self.currentContext.empty = False

        module_name_start = module_name

        pos = module_name.find('.')

        if pos != -1:
            module_name_start = module_name[:pos]

        imported_name = node.lhs.name

        if module_name_start == imported_name:
            self.visitchildren(node)
            return node

        self.putline("import %s as %s" % (module_name, imported_name))

        return node

    def visit_CClassDefNode(self, node):

        self.putline("class %s:" % node.class_name)

        self.context.append(self.Context(node.class_name))

        self._visit_indented(node)

        assert self.currentContext.name == node.class_name

        if self.currentContext.empty:
            with self.indented():
                self.putline("pass")

        self.context.pop()

        self.emptyline()

        return node

    def visit_PyClassDefNode(self, node):

        self.putline("class %s" % node.name)

        self.context.append(self.Context(node.name))

        self._visit_indented(node)

        assert self.currentContext.name == node.class_name

        if self.currentContext.empty:
            with self.indented():
                self.putline("pass")

        self.context.pop()

        self.emptyline()

        return node

    def visit_CFuncDefNode(self, node):

        # cdef rather than cpdef => invisible
        if node.py_func is None:
            return node

        self.currentContext.empty = False

        func_name = node.py_func.name
        func_type = node.type

        py_args = node.py_func.args

        self.startline()

        self.put("def %s(" % func_name)

        def type_name(ctype):

            if arg.type is not None:
                if hasattr(arg.type, 'name'):
                    return arg.type.name

            py_name = func_type.return_type.py_type_name()

            if "(int, long)" in py_name:
                return "int"
            return py_name

        arg_names = []

        for (arg, py_arg) in zip(func_type.args, py_args):

            arg_name = ""

            if arg.name == "self":
                arg_name = arg.name
            else:
                arg_name = "%s: %s" % (arg.name, type_name(arg))

            if (py_arg.default is not None or
                py_arg.default_value is not None):
                arg_name += " = ..."

            arg_names.append(arg_name)

        self.put(", ".join(arg_names))

        self.endline(") -> %s: ..." % type_name(func_type.return_type))

        return node

    def print_Decorator(self, decorator):

        # Not implemented and afaik not required..
        if isinstance(decorator, CallNode):
            return

        self.startline("@")

        if isinstance(decorator, NameNode):
            self.put("%s" % decorator.name)
        else:
            assert isinstance(decorator, AttributeNode)
            self.put("%s.%s" % (decorator.obj.name, decorator.attribute))

        self.emptyline()

    def annotation_Str(self, annotation):
        value = annotation.string.value
        return value.decode('utf-8').strip()

    def print_DefNode(self, node):

        self.currentContext.empty = False

        # arg: CArgDeclNode
        def argument_str(arg):
            value = arg.declarator.name
            if arg.annotation is not None:
                value += (": %s" % self.annotation_Str(arg.annotation))

            if (arg.default is not None or
                arg.default_value is not None):
                value += " = ..."

            return value

        async_name = "async " if (node.is_async_def or
                                  node.is_asyncgen or
                                  node.is_coroutine) else ""

        if node.decorators is not None:
            for decorator in node.decorators:
                self.print_Decorator(decorator.decorator)

        self.startline("%sdef %s(" % (async_name, node.name))

        args = []

        # Ordinary arguments:
        args += (argument_str(arg) for arg in node.args)

        # Star(star) arguments:
        star_arg = node.star_arg
        starstar_arg = node.starstar_arg

        if star_arg is not None:
            args.append("*%s" % star_arg.name)

        if starstar_arg is not None:
            args.append("**%s" % starstar_arg.name)

        self.put(", ".join(args))

        retype = node.return_type_annotation

        if retype is not None:
            self.put(") -> %s: ..." % self.annotation_Str(retype))
        else:
            self.put("): ...")

        self.endline()

    def visit_ExprStatNode(self, node):
        if not self.atModuleRoot():
            return node

    def visit_SingleAssignmentNode(self, node):

        if not self.atModuleRoot():
            return node

        name = node.lhs.name

        if node.lhs.annotation:
            annotation = node.lhs.annotation.string.value
            self.putline("%s: %s = ..." % (name, annotation))
        else:
            self.putline("%s = ..." % name)

    def visit_ExprStatNode(self, node):

        if not self.atModuleRoot():
            return node

        if isinstance(node.expr, NameNode):

            node = node.expr

            name = node.name

            if node.annotation:
                annotation = self.annotation_Str(node.annotation)
                self.putline("%s: %s" % (name, annotation))
            else:
                self.putline("%s" % (name))

    def visit_DefNode(self, node):

        self.print_DefNode(node)

        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def __call__(self, root):
        self.putline("# Python stub file generated by Cython %s" % Version.watermark)
        self.emptyline()

        node = self._visit(root)

        # print(self.result)

        return node
