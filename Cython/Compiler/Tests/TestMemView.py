from Cython.TestUtils import CythonTest
import Cython.Compiler.Errors as Errors
from Cython.Compiler.Nodes import *
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Buffer import *


class TestMemviewParsing(CythonTest):

    def parse(self, s):
        return self.should_not_fail(lambda: self.fragment(s)).root

    def not_parseable(self, expected_error, s):
        e = self.should_fail(lambda: self.fragment(s),  Errors.CompileError)
        self.assertEqual(expected_error, e.message_only)
    
    def test_default_1dim(self):
        self.parse(u"cdef int[:] x")
        self.parse(u"cdef short int[:] x")

    def test_default_ndim(self):
        self.parse(u"cdef int[:,:,:,:,:] x")
        self.parse(u"cdef unsigned long int[:,:,:,:,:] x")
        self.parse(u"cdef unsigned int[:,:,:,:,:] x")

    def test_zero_offset(self):
        self.parse(u"cdef long double[0:] x")
        self.parse(u"cdef int[0:] x")

    def test_zero_offset_ndim(self):
        self.parse(u"cdef int[0:,0:,0:,0:] x")

    def test_general_slice(self):
        self.parse(u'cdef float[::ptr, ::direct & contig, 0::full & strided] x')

    def test_non_slice_memview(self):
        self.not_parseable("An axis specification in memoryview declaration does not have a ':'.",
                u"cdef double[:foo, bar] x")
        self.not_parseable("An axis specification in memoryview declaration does not have a ':'.",
                u"cdef double[0:foo, bar] x")

    def test_basic(self):
        t = self.parse(u"cdef int[:] x")
        memv_node = t.stats[0].base_type
        self.assert_(isinstance(memv_node, MemoryViewTypeNode))

if __name__ == '__main__':
    import unittest
    unittest.main()
