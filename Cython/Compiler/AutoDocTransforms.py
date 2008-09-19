import re

from Cython.Compiler.Visitor import CythonTransform
from Cython.Compiler.Nodes import DefNode, CFuncDefNode
from Cython.Compiler.Errors import CompileError
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler import Options


class EmbedSignature(CythonTransform):

    SPECIAL_METHOD_RE = re.compile(r'__\w+__')

    def __init__(self, context):
        super(EmbedSignature, self).__init__(context)
        self.denv = None # XXX
        self.is_in_class = False
        self.class_name = None

    def _fmt_arg_type(self, arg):
        try:
            return arg.base_type.name
        except AttributeError:
            return ""

    def _fmt_arg_name(self, arg):
        try:
            return arg.declarator.name
        except AttributeError:
            return arg.declarator.base.name

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
        arg_type = self._fmt_arg_type(arg)
        arg_name = self._fmt_arg_name(arg)
        arg_defv = self._fmt_arg_defv(arg)
        doc = arg_name
        if arg_type:
            doc = ('%s ' % arg_type) + doc
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

    def _fmt_signature(self, cls_name, func_name, args,
                       npargs=0, pargs=None,
                       nkargs=0, kargs=None,
                       return_type=None):
        arglist = self._fmt_arglist(args,
                                    npargs, pargs,
                                    nkargs, kargs)
        arglist = ', '.join(arglist)
        func_doc = '%s(%s)' % (func_name, arglist)
        if cls_name:
            func_doc = ('%s.' % cls_name) + func_doc
        if return_type:
            func_doc = func_doc + ' -> %s' % return_type
        return func_doc

    def _embed_signature(self, signature, node_doc):
        if node_doc:
            return signature + '\n' + node_doc
        else:
            return signature

    def visit_ClassDefNode(self, node):
        oldincls = self.is_in_class
        oldname = self.class_name
        self.is_in_class = True
        try:
            # PyClassDefNode
            self.class_name = node.name
        except AttributeError:
            # CClassDefNode
            self.class_name = node.class_name
        self.visitchildren(node)
        self.is_in_class = oldincls
        self.class_name = oldname
        return node

    def visit_FuncDefNode(self, node):
        signature = None
        if type(node) is DefNode: # def FOO(...):
            special_method = (self.is_in_class and \
                              self.SPECIAL_METHOD_RE.match(node.name))
            if not special_method:
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
                    return_type=node.base_type.name)
        else: # should not fall here ...
            assert False
        if signature:
            if Options.docstrings and node.options['embedsignature']:
                new_doc  = self._embed_signature(signature, node.doc)
                node.doc = EncodedString(new_doc) # XXX
        return node
