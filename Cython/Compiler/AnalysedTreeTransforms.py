from Cython.Compiler.Visitor import VisitorTransform, ScopeTrackingTransform, TreeVisitor
from Nodes import StatListNode, SingleAssignmentNode, CFuncDefNode
from ExprNodes import DictNode, DictItemNode, NameNode, UnicodeNode, NoneNode, \
                      ExprNode, AttributeNode, ModuleRefNode, DocstringRefNode
from PyrexTypes import py_object_type
from Builtin import dict_type
from StringEncoding import EncodedString
import Naming

class AutoTestDictTransform(ScopeTrackingTransform):
    # Handles autotestdict directive

    blacklist = ['__cinit__', '__dealloc__', '__richcmp__', '__nonzero__']

    def visit_ModuleNode(self, node):
        self.scope_type = 'module'
        self.scope_node = node
        if self.current_directives['autotestdict']:
            assert isinstance(node.body, StatListNode)

            # First see if __test__ is already created
            if u'__test__' in node.scope.entries:
                # Do nothing
                return node
            
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

    def add_test(self, testpos, name, func_ref_node):
        # func_ref_node must evaluate to the function object containing
        # the docstring, BUT it should not be the function itself (which
        # would lead to a new *definition* of the function)
        pos = self.testspos
        keystr = u'%s (line %d)' % (name, testpos[1])
        key = UnicodeNode(pos, value=EncodedString(keystr))

        value = DocstringRefNode(pos, func_ref_node)
        self.tests.append(DictItemNode(pos, key=key, value=value))
    
    def visit_FuncDefNode(self, node):
        if node.doc:
            if isinstance(node, CFuncDefNode) and not node.py_func:
                # skip non-cpdef cdef functions
                return node
            
            pos = self.testspos
            if self.scope_type == 'module':
                parent = ModuleRefNode(pos)
                name = node.entry.name
            elif self.scope_type in ('pyclass', 'cclass'):
                if isinstance(node, CFuncDefNode):
                    name = node.py_func.name
                else:
                    name = node.name
                if self.scope_type == 'cclass' and name in self.blacklist:
                    return node
                mod = ModuleRefNode(pos)
                if self.scope_type == 'pyclass':
                    clsname = self.scope_node.name
                else:
                    clsname = self.scope_node.class_name
                parent = AttributeNode(pos, obj=mod,
                                       attribute=clsname,
                                       type=py_object_type,
                                       is_py_attr=True,
                                       is_temp=True)
                name = "%s.%s" % (clsname, node.entry.name)
            else:
                assert False
            getfunc = AttributeNode(pos, obj=parent,
                                    attribute=node.entry.name,
                                    type=py_object_type,
                                    is_py_attr=True,
                                    is_temp=True)
            self.add_test(node.pos, name, getfunc)
        return node

