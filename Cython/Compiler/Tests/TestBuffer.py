from Cython.TestUtils import CythonTest
import Cython.Compiler.Errors as Errors
from Cython.Compiler.Nodes import *
from Cython.Compiler.ParseTreeTransforms import *


class TestBufferParsing(CythonTest):
    # First, we only test the raw parser, i.e.
    # the number and contents of arguments are NOT checked.
    # However "dtype"/the first positional argument is special-cased
    #  to parse a type argument rather than an expression

    def parse(self, s):
        return self.should_not_fail(lambda: self.fragment(s)).root

    def not_parseable(self, expected_error, s):
        e = self.should_fail(lambda: self.fragment(s),  Errors.CompileError)
        self.assertEqual(expected_error, e.message_only)
    
    def test_basic(self):
        t = self.parse(u"cdef object[float, 4, ndim=2, foo=foo] x")
        bufnode = t.stats[0].base_type
        self.assert_(isinstance(bufnode, CBufferAccessTypeNode))
        self.assertEqual(2, len(bufnode.positional_args))
#        print bufnode.dump()
        # should put more here...
        
    def test_type_fail(self):
        self.not_parseable("Expected: type",
                           u"cdef object[2] x")
    
    def test_type_pos(self):
        self.parse(u"cdef object[short unsigned int, 3] x")

    def test_type_keyword(self):
        self.parse(u"cdef object[foo=foo, dtype=short unsigned int] x")

    def test_notype_as_expr1(self):
        self.not_parseable("Expected: expression",
                           u"cdef object[foo2=short unsigned int] x")

    def test_notype_as_expr2(self):
        self.not_parseable("Expected: expression",
                           u"cdef object[int, short unsigned int] x")

    def test_pos_after_key(self):
        self.not_parseable("Non-keyword arg following keyword arg",
                           u"cdef object[foo=1, 2] x")

class TestBufferOptions(CythonTest):
    # Tests the full parsing of the options within the brackets

    def parse_opts(self, opts):
        s = u"cdef object[%s] x" % opts
        root = self.fragment(s, pipeline=[PostParse(self)]).root
        buftype = root.stats[0].base_type
        self.assert_(isinstance(buftype, CBufferAccessTypeNode))
        self.assert_(isinstance(buftype.base_type_node, CSimpleBaseTypeNode))
        self.assertEqual(u"object", buftype.base_type_node.name)
        return buftype

    def non_parse(self, expected_err, opts):
        e = self.should_fail(lambda: self.parse_opts(opts))
        self.assertEqual(expected_err, e.message_only)
        
    def test_basic(self):
        buf = self.parse_opts(u"unsigned short int, 3")
        self.assert_(isinstance(buf.dtype, CSimpleBaseTypeNode))
        self.assert_(buf.dtype.signed == 0 and buf.dtype.longness == -1)
        self.assertEqual(3, buf.ndim)

    def test_dict(self):
        buf = self.parse_opts(u"ndim=3, dtype=unsigned short int")
        self.assert_(isinstance(buf.dtype, CSimpleBaseTypeNode))
        self.assert_(buf.dtype.signed == 0 and buf.dtype.longness == -1)
        self.assertEqual(3, buf.ndim)
        
    def test_dtype(self):
        self.non_parse(ERR_BUF_MISSING % 'dtype', u"")
    
    def test_ndim(self):
        self.parse_opts(u"int, 2")
        self.non_parse(ERR_BUF_INT % 'ndim', u"int, 'a'")
        self.non_parse(ERR_BUF_NONNEG % 'ndim', u"int, -34")

    def test_use_DEF(self):
        t = self.fragment(u"""
        DEF ndim = 3
        cdef object[int, ndim] x
        cdef object[ndim=ndim, dtype=int] y
        """, pipeline=[PostParse(self)]).root
        self.assert_(t.stats[1].base_type.ndim == 3)
        self.assert_(t.stats[2].base_type.ndim == 3)

    # add exotic and impossible combinations as they come along
