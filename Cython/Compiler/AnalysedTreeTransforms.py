from Cython.Compiler.Visitor import VisitorTransform, CythonTransform, TreeVisitor
from Nodes import StatListNode, SingleAssignmentNode
from ExprNodes import (DictNode, DictItemNode, NameNode, UnicodeNode, NoneNode,
                      ExprNode, AttributeNode)
from PyrexTypes import py_object_type
from Builtin import dict_type
from StringEncoding import EncodedString
import Naming

class DoctestHackTransform(CythonTransform):
    # Handles doctesthack directive

    def visit_ModuleNode(self, node):
        if self.current_directives['doctesthack']:
            assert isinstance(node.body, StatListNode)
            pos = node.pos

            self.tests = []
            self.testspos = node.pos

            test_dict_entry = node.scope.declare_var(EncodedString(u'__test__'),
                                                     py_object_type,
                                                     pos,
                                                     visibility='public')
            create_test_dict_assignment = SingleAssignmentNode(pos,
                lhs=NameNode(pos, name=EncodedString(u'__test__'),
                             entry=test_dict_entry),
                rhs=DictNode(pos, key_value_pairs=self.tests))
            self.visitchildren(node)
            node.body.stats.append(create_test_dict_assignment)

            
        return node

    def add_test(self, testpos, name, funcname):
        pos = self.testspos
        keystr = u'%s (line %d)' % (name, testpos[1])
        key = UnicodeNode(pos, value=EncodedString(keystr))

        getfunc = AttributeNode(pos, obj=ModuleRefNode(pos),
                                attribute=funcname,
                                type=py_object_type,
                                is_py_attr=True,
                                is_temp=True)
        
        value = DocstringRefNode(pos, getfunc)
        self.tests.append(DictItemNode(pos, key=key, value=value))
    
    def visit_ClassDefNode(self, node):
        return node

    def visit_FuncDefNode(self, node):
        if node.doc:
            self.add_test(node.pos, node.entry.name, node.entry.name)
        return node


class ModuleRefNode(ExprNode):
    type = py_object_type
    is_temp = False
    subexprs = []
    
    def analyse_types(self, env):
        pass

    def calculate_result_code(self):
        return Naming.module_cname

    def generate_result_code(self, code):
        pass

class DocstringRefNode(ExprNode):
    # Extracts the docstring of the body element
    
    subexprs = ['body']
    type = py_object_type
    is_temp = True
    
    def __init__(self, pos, body):
        ExprNode.__init__(self, pos)
        assert body.type.is_pyobject
        self.body = body

    def analyse_types(self, env):
        pass

    def generate_result_code(self, code):
        code.putln('%s = __Pyx_GetAttrString(%s, "__doc__");' %
                   (self.result(), self.body.result()))
        code.put_gotref(self.result())
