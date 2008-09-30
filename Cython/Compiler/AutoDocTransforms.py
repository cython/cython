from Cython.Compiler.Visitor import CythonTransform
from Cython.Compiler.Nodes import DefNode, CFuncDefNode
from Cython.Compiler.Errors import CompileError
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler import Options
from Cython.Compiler import PyrexTypes



class EmbedSignature(CythonTransform):

    def __init__(self, context):
        super(EmbedSignature, self).__init__(context)
        self.denv = None # XXX
        self.class_name = None

    def _fmt_arg_defv(self, arg):
        if not arg.default:
            return None
        try:
            denv = self.denv  # XXX
            ctval = arg.default.compile_time_value(self.denv)
            return '%s' % ctval
        except Exception:
            try:
                return arg.default.name # XXX
            except AttributeError:
                return '<???>'

    def _fmt_arg(self, arg):
        if arg.type is PyrexTypes.py_object_type or arg.is_self_arg:
            doc = arg.name
        else:
            doc = arg.type.declaration_code(arg.name, for_display=1)
        if arg.default:
            arg_defv = self._fmt_arg_defv(arg)
            if arg_defv:
                doc = doc + ('=%s' % arg_defv)
        return doc

    def _fmt_arglist(self, args,
                     npargs=0, pargs=None,
                     nkargs=0, kargs=None):
        arglist = []
        for arg in args:
            arg_doc = self._fmt_arg(arg)
            arglist.append(arg_doc)
        if pargs:
            arglist.insert(npargs, '*%s' % pargs.name)
        elif nkargs:
            arglist.insert(npargs, '*')
        if kargs:
            arglist.append('**%s' % kargs.name)
        return arglist

    def _fmt_ret_type(self, ret):
        if ret is PyrexTypes.py_object_type:
            return None
        else:
            return ret.declaration_code("", for_display=1)

    def _fmt_signature(self, cls_name, func_name, args,
                       npargs=0, pargs=None,
                       nkargs=0, kargs=None,
                       return_type=None):
        arglist = self._fmt_arglist(args,
                                    npargs, pargs,
                                    nkargs, kargs)
        arglist_doc = ', '.join(arglist)
        func_doc = '%s(%s)' % (func_name, arglist_doc)
        if cls_name:
            func_doc = '%s.%s' % (cls_name, func_doc)
        if return_type:
            ret_doc = self._fmt_ret_type(return_type)
            if ret_doc:
                func_doc = '%s -> %s' % (func_doc, ret_doc)
        return func_doc

    def _embed_signature(self, signature, node_doc):
        if node_doc:
            return signature + '\n' + node_doc
        else:
            return signature


    def __call__(self, node):
        if not Options.docstrings:
            return node
        else:
            return super(EmbedSignature, self).__call__(node)
        
    def visit_ClassDefNode(self, node):
        oldname = self.class_name
        try:
            # PyClassDefNode
            self.class_name = node.name
        except AttributeError:
            # CClassDefNode
            self.class_name = node.class_name
        self.visitchildren(node)
        self.class_name = oldname
        return node

    def visit_FuncDefNode(self, node):
        if not self.current_directives['embedsignature']:
            return node
        
        signature = None
        if type(node) is DefNode: # def FOO(...):
            if not node.entry.is_special:
                nkargs = getattr(node, 'num_kwonly_args', 0)
                npargs = len(node.args) - nkargs
                signature = self._fmt_signature(
                    self.class_name, node.name, node.args,
                    npargs, node.star_arg,
                    nkargs, node.starstar_arg,
                    return_type=None)
        elif type(node) is CFuncDefNode:
            if node.overridable: # cpdef FOO(...):
                signature = self._fmt_signature(
                    self.class_name, node.declarator.base.name,
                    node.declarator.args,
                    return_type=node.return_type)
        else: # should not fall here ...
            assert False
        if signature:
            new_doc  = self._embed_signature(signature, node.entry.doc)
            node.entry.doc = EncodedString(new_doc)
            if hasattr(node, 'py_func') and node.py_func is not None:
                node.py_func.entry.doc = EncodedString(new_doc)
        return node
