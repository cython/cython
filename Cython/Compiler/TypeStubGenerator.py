from . import Version
from .Nodes import CNameDeclaratorNode
from .ExprNodes import CallNode, NameNode, ImportNode, TupleNode, AttributeNode
from ..CodeWriter import DeclarationWriter
from .Visitor import CythonTransform
from . import PyrexTypes
from ..Utils import open_new_file
import cython
import os
import sys

cython.declare(
    PyrexTypes=object,
    Naming=object,
    ExprNodes=object,
    Nodes=object,
    Options=object,
    UtilNodes=object,
    LetNode=object,
    LetRefNode=object,
    TreeFragment=object,
    EncodedString=object,
    error=object,
    warning=object,
    copy=object,
    _unicode=object,
)


# Inspired by and based around https://github.com/cython/cython/pull/3818
# with some less lazy changes to it and a few minor improvements and optimizations...

# Decided to revert to an older variant I had wrote of this code for the sake of
# maintainability - Vizonex


# TODO Save this implementation commented out if required....
if sys.version_info >= (3, 9):
    typing_module = "typing"
else:
    typing_module = "typing_extensions"


class PyiWriter(CythonTransform, DeclarationWriter):
    """Used By Cython to help Write stubfiles
    this comes in handy for ides like Pylance
    which suffer from having no code access to
    annotations from compiled python modules...
    """

    def __init__(self, context):
        super(PyiWriter, self).__init__(context=context)
        self.module_name = ""
        self.class_func_count = 0

        self.translation_table = {}
        """Used as an eternal resource for translating ctype declarations into python-types"""

        self.use_typing = False
        """if true we must import typing's generator typehint..."""

    def _visitchildren_indented(self, node):
        self.indent()
        self.visitchildren(node)
        self.dedent()

    def translate_pyrex_type(self, ctype):
        # TODO implement Pyrex to cython shadow typehints converter...

        if ctype.is_numeric or ctype.is_builtin_type:
            return ctype.py_type_name()

        if ctype is c_void_type:
            return "None"

        if isinstance(ctype, PyrexTypes.CIntType):
            return "int"

        elif isinstance(ctype, PyrexTypes.CFloatType):
            return "float"

        elif isinstance(ctype, PyrexTypes.PyObjectType):
            return ctype.py_type_name()

        return "object"

    # Instead of doing it into C, we're doing it backwards...
    def translate_base_type_to_py(self, base):

        # Try checking our table first...
        if self.translation_table.get(base.name):
            return self.translation_table[base.name]

        elif base.name == "object":
            return "object"

        elif base.name in ("unicode", "basestring"):
            return "str"

        elif not base.is_basic_c_type:
            # Likely that it's already a python object that's being handled...
            # except for basestring and unicode...
            return base.name

        elif base.name == "bint":
            return "bool"

        ctype = PyrexTypes.simple_c_type(base.signed, base.longness, base.name)  # type: ignore
        return self.translate_pyrex_type(ctype)

    def emptyline(self):
        self.result.putline("")

    def visit_ModuleNode(self, node):
        # We need to extract the name to write our pyi file down...
        if node.directives["write_stub_file"]:
            result = self.write(node, True)
            new_path = node.full_module_name.replace(".", "/")
            print("writing file %s.pyi ..." % node.full_module_name)
            with open_new_file(os.path.join(new_path + ".pyi")) as w:
                w.write("\n".join(result.lines))
                w.write("\n")
        return node

    def visit_StatListNode(self, node):
        self.visitchildren(node)
        return node

    def visit_CImportStatNode(self, node):
        return node

    def visit_FromCImportStatNode(self, node):
        return node

    def visit_CDefExternNode(self, node):
        self.visitchildren(node)
        return node

    def visit_CEnumDefNode(self, node):
        # TODO Figure out how to define an enum-class via typehints...

        # NOTE It seems that only public will make the enum accessible to python so
        # I'll just have it check if the enums will be public for now... - Vizonex
        if node.visibility == "public":
            # Enum's name is not in or visible in the final product because
            # it's not an enum class so do not indent here...
            # Also Leave visit_CEnumDefItemNode up to the previous
            # class's function...
            self.putline("# -- enum %s --" % node.name)
            self.visitchildren(node)
        return node

    # Used in our translation table to register return types variables from...
    def visit_CTypeDefNode(self, node):
        if isinstance(node.declarator, CNameDeclaratorNode):
            # Register a new type to use in our translation table...
            self.translation_table[
                node.declarator.name
            ] = self.translate_base_type_to_py(node.base_type)

    def visit_CStructOrUnionDefNode(self, node):
        # XXX : Currently, I don't know what to do here yet but ignoring
        # is triggering some problems currently...
        return node

    def visit_CVarDefNode(self, node):

        # if they aren't public or readonly then the variable inside of a class
        # or outside should be ignored by default...

        if node.visibility in ["readonly", "public"]:

            # TODO handle ctypedef nodes and give them a
            # new type-registry system to help translate
            # all incoming variables...

            py_name = self.translate_base_type_to_py(node.base_type)

            # Final check...
            if py_name is not None:
                # Write in all the objects listed on the defined line...
                for d in node.declarators:
                    self.putline("%s: %s" % (d.name, py_name))

        return node

    def visit_ImportNode(self, node):
        module_name = node.module_name.value

        if not node.name_list:
            self.putline("import %s" % module_name)
        else:
            all_imported_children = ", ".join(
                (arg.value for arg in node.name_list.args)
            )

            if node.level > 0:
                module_name = "%s%s" % ("." * node.level, module_name)

            self.putline("from %s import %s" % (module_name, all_imported_children))

        return node

    # Optimized original code by having there be one function to take
    # the place of two of them I could see what Scoder meant when
    # said the original pull request needed to be cleaned up...

    def write_class(self, node, class_name):
        self.endline()
        self.put("class %s" % class_name)
        if node.bases and node.bases.is_sequence_constructor and node.bases.args:
            self.put("(")
            self.put(",".join([name.name for name in node.bases.args]))
            self.endline("):")
        else:
            self.endline(":")
        self.class_func_count = 0
        self._visitchildren_indented(node)
        if self.class_func_count < 1:
            self.indent()
            self.putline("pass")
            self.dedent()
        self.class_func_count = 0
        self.emptyline()
        return node

    # I have tried to merege these before via visit_ClassDefNode but it causes the system to break so this
    # was the best I could do to minigate the problem - Vizonex
    def visit_CClassDefNode(self, node):
        return self.write_class(node, node.class_name)

    def visit_PyClassDefNode(self, node):
        return self.write_class(node, node.name)

    def visit_CFuncDefNode(self, node):
        # cdefs are for C only...
        if not node.overridable:
            return node

        func_args = []
        for arg in node.declarator.args:
            value = ""
            if not arg.declarator.name:
                value = arg.base_type.name
            elif hasattr(arg.base_type, "name"):
                value = "%s : %s" % (
                    arg.declarator.name,
                    self.translate_base_type_to_py(arg.base_type),
                )
            if arg.default is not None or arg.default_value is not None:
                value += " = ..."
            func_args.append(value)

        self.class_func_count += 1

        func_name = node.declared_name()
        self.startline()
        self.put("def %s(" % func_name)

        self.put(", ".join(func_args))

        # TODO Maybe Try passing docstrings in the future for vscode users' sake
        # or have it also be a compiler argument?...

        self.endline(") -> %s: ..." % self.translate_base_type_to_py(node.base_type))

        return node

  
    def visit_NameNode(self, node):
        self.put(node.name)

    def visit_AttributeNode(self, node):
        self.visit(node.obj)
        self.put(u".%s" % node.attribute)

    def write_decorator(self, decorator):
        attribte = decorator.as_cython_attribute()
        if not attribte:
            return 
        self.putline("@%s" % attribte)
        

    def annotation_Str(self, annotation):
        return (
            annotation.name
            if hasattr(annotation, "name") and annotation.is_name
            else annotation.string.unicode_value
        )

    def visit_DefNode(self, node):
        self.class_func_count += 1
        func_name = node.name

        # TODO Change how init is being handled...
        if func_name == "__cinit__":
            func_name = "__init__"

        def argument_str(arg):
            value = arg.declarator.name

            if arg.annotation is not None:
                value += ": %s" % self.annotation_Str(arg.annotation)

            elif hasattr(arg.base_type, "name") and arg.base_type.name is not None:
                value += ": %s" % self.translate_base_type_to_py(arg.base_type)

            if arg.default is not None or arg.default_value is not None:
                value += " = ..."

            return value

        # TODO See if "*," or "/," or an "Ellipsis"
        # can be passed through and accepted into all the stub
        # files with a regex to check it off as a unittest.

        async_name = (
            "async " if node.is_async_def or getattr(node, "is_coroutine", None) else ""
        )

        if node.decorators is not None:
            for decorator in node.decorators:
                self.write_decorator(decorator.decorator)

        self.startline("%sdef %s(" % (async_name, func_name))

        # TODO Maybe look into trying AutoDocTransforms?

        args_list = []

        # Ordinary arguments:
        args_list += (argument_str(arg) for arg in node.args)

        # extra positional and keyword arguments:
        star_arg = node.star_arg
        starstar_arg = node.starstar_arg

        npoargs = getattr(node, "num_posonly_args", 0)
        nkargs = getattr(node, "num_kwonly_args", 0)
        npargs = len(node.args) - nkargs - npoargs

        if star_arg is not None:

            args_list.insert(npargs + npoargs, "*%s" % star_arg.name)

        elif nkargs:
            args_list.insert(npargs + npoargs, "*")

        if npoargs:
            args_list.insert(npoargs, "/")

        if starstar_arg is not None:
            args_list.append("**%s" % starstar_arg.name)

        self.put(", ".join(args_list))

        retype = node.return_type_annotation

        if retype is not None:

            # This is a little bit different than the original pull request
            # since I wanted there to be better typehints given to all the
            # objects hence why I added "Generator" as a typehint & keyword...
            # TODO: Remove annotation_Str Function and replace it with something safer...
            annotation = self.annotation_Str(retype)
            if node.is_generator and not annotation.startswith("Generator"):
                # TODO figure out how the extract the other two required variables...
                # Also the function could be an Iterator but
                # hadn't added the "__iter__" function name-check just yet...
                self.use_typing = True
                self.put(") -> Generator[ %s, None, None]:..." % annotation)
            else:
                self.put(") -> %s: ..." % annotation)

        # TODO Add Return Type Recovery tool to resolve all missing annotations...
        else:
            self.put("): ...")
        self.endline()
        return node

    def visit_ExprNode(self, node):
        return node

    def visit_SingleAssignmentNode(self, node):
        if isinstance(node.rhs, ImportNode):
            self.visitchildren(node)
            return node

        name = node.lhs.name
        if node.lhs.annotation:
            # TODO Check if the annotation's values are existent...
            self.putline("%s : %s = ..." % (name, node.lhs.annotation.string.value))
        elif hasattr(node, "rhs"):
            self.putline("%s : %s" % (name, self.translate_pyrex_type(node.rhs.type)))
        else:
            self.putline(name)
        return node


    def visit_ExprStatNode(self, node):
        if isinstance(node.expr, NameNode):
            expr = node.expr
            name = expr.name  # type: ignore
            if expr.annotation:
                self.putline("%s: %s " % (name, self.annotation_Str(expr.annotation)))
            else:
                self.putline("%s " % name)
        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def putline_at(self, index, line):
        self.result.lines.insert(index, line)

    def write(self, root, _debug=False):
        # Top Notice will likely change once I've made a full on pull request...
        self.putline("# Python stub file generated by Cython %s" % Version.watermark)
        self.emptyline()

        self.visitchildren(root)
        if self.use_typing:
            # Inject Keyword Generator
            self.putline_at(1, "from typing import Generator")

        # added a new debugger in case needed for now...
        if _debug:
            print("# -- Pyi Result --")
            print("\n".join(self.result.lines))
            print("# -- End Of Pyi Result --")

        return self.result
