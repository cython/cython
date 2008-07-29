from Visitor import CythonTransform
from sets import Set as set

class AnchorTemps(CythonTransform):

    def init_scope(self, scope):
        scope.free_temp_entries = []

    def handle_node(self, node):
        if node.temps:
            for temp in node.temps:
                temp.cname = self.scope.allocate_temp(temp.type)
                self.temps_beneath_try.add(temp.cname)
            self.visitchildren(node)
            for temp in node.temps:
                self.scope.release_temp(temp.cname)
        else:
            self.visitchildren(node)

    def visit_Node(self, node):
        self.handle_node(node)
        return node

    def visit_ModuleNode(self, node):
        self.scope = node.scope
        self.temps_beneath_try = set()
        self.init_scope(self.scope)
        self.handle_node(node)
        return node

    def visit_FuncDefNode(self, node):
        pscope = self.scope
        pscope_temps = self.temps_beneath_try
        self.scope = node.local_scope
        self.init_scope(node.local_scope)
        self.handle_node(node)
        self.scope = pscope
        self.temps_beneath_try = pscope_temps
        return node

    def visit_TryExceptNode(self, node):
        old_tbt = self.temps_beneath_try
        self.temps_beneath_try = set()
        self.handle_node(node)
        entries = [ scope.cname_to_entry[cname] for
                    cname in self.temps_beneath_try]
        node.cleanup_list.extend(entries)
        return node
