from __future__ import absolute_import

import cython
cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, LetNode=object,
               LetRefNode=object, TreeFragment=object, EncodedString=object,
               error=object, warning=object, copy=object, _unicode=object)

from .Nodes import CFuncDefNode
from .ExprNodes import ImportNode

from . import Version

from .Visitor import TreeVisitor

class TypeStubGenerator(TreeVisitor):

    def __init__(self):
        super(TypeStubGenerator, self).__init__()
        self._indent = 0
        pass

    def visit_ModuleNode(self, node):

        self.visitchildren(node)

        print()

        return node

    def visit_ImportNode(self, node):

        module_name = node.module_name.value

        if node.name_list is None:
            self._print_indented("import %s" % module_name)
        else:
            names = (arg.value for arg in node.name_list.args)
            all_names = ", ".join(names)

            if node.level > 0:
                module_name = "%s%s" % ("."*node.level, module_name)

            self._print_indented("from %s import %s" % (module_name, all_names))

        return node

    def visit_SingleAssignmentNode(self, node):

        if not isinstance(node.rhs, ImportNode):
            return node

        module_name = node.rhs.module_name.value

        module_name_start = module_name

        pos = module_name.find('.')

        if pos != -1:
            module_name_start = module_name[:pos]

        imported_name = node.lhs.name

        if module_name_start == imported_name:
            self.visitchildren(node)
            return node

        self._print_indented("import %s as %s" % (module_name, imported_name))

        return node

    def visit_CClassDefNode(self, node):

        print("class %s:" % node.class_name)

        self._indent += 1

        self.visitchildren(node)

        self._indent -= 1

        print("")

        return node

    def _indent_str(self):
        return "  " * self._indent

    def _print_indented(self, *args, **kwds):
        print(self._indent_str(), end='')
        print(*args, **kwds)

    def visit_PyClassDefNode(self, node):

        self._print_indented("class %s" % node.name)

        self._indent += 1

        self.visitchildren(node)

        self._indent -= 1

        print()

        return node

        # return self.visit_scope(node, 'pyclass')

    def visit_CFuncDefNode(self, node):

        # cdef rather than cpdef => invisible
        if node.py_func is None:
            return node

        entry = node.entry

        if entry is None:
            self.print_DefNode(node.py_func)

        func_name = node.py_func.name
        func_type = entry.type

        py_args = node.py_func.args

        self._print_indented("def %s(" % func_name, end='')

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

        print(", ".join(arg_names), end='')

        print(") -> %s: ..." % type_name(func_type.return_type), end='')

        print()

        return node

    def print_DefNode(self, node):

        def annotation_str(annotation):
            value = annotation.string.value
            return value.decode('utf-8').strip()

        # arg: CArgDeclNode
        def argument_str(arg):
            value = arg.name
            if arg.annotation is not None:
                value += (": %s" % annotation_str(arg.annotation))

            if (arg.default is not None or
                arg.default_value is not None):
                value += " = ..."

            return value

        self._print_indented("def %s(" % node.name, end='')

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

        print(", ".join(args), end='')

        retype = node.return_type_annotation

        if retype is not None:
            print(") -> %s: ..." % annotation_str(retype), end='')
        else:
            print("): ...", end='')

        print()


    def visit_DefNode(self, node):

        self.print_DefNode(node)

        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def __call__(self, root):
        print("# Python stub file generated by Cython %s" % Version.watermark)
        print()
        return self._visit(root)
