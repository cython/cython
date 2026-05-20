"""Tests for the Cython code writer extension"""

from Cython.Compiler.TreeFragment import StringParseContext, parse_from_strings
from Cython.TestUtils import CythonTest


class TestCodeWriter(CythonTest):

    def parse_code(self, code):
        return parse_from_strings("test", code, context=StringParseContext("test"))

    def rewrite(self, code):
        node = self.parse_code(code)
        self.assertEqual(
            code.strip(), 
            self.codeToString(node), 
            "code failed to write correctly"
        ) 


    def test_cdef_enum(self):
        self.rewrite(
            (
                "cdef enum start_stop:\n" +
                "    START = 1\n" + 
                "    STOP = 2"
            )
        )
    
    def test_cpdef_enum(self):
        self.rewrite(
            (
                "cpdef enum start_stop:\n" +
                "    START = 1\n" + 
                "    STOP = 2"
            )
        )

    def test_nogil(self):
        # trigger visiting CFuncDeclaratorNode
        self.rewrite(
            (
                "cdef int func(int a, int b) nogil:\n"
                "    return a + b"
            )
        )

    def test_except_minus_one(self):
        self.rewrite(
            (
                "cdef int func(int a, int b) except -1:\n"
                "    return a + b"
            )
        )
    
    def test_noexcept(self):
        self.rewrite(
            (
                "cdef int func(int a, int b) noexcept:\n"
                "    return a + b"
            )
        )
    
    def test_noexcept_with_gil(self):
        self.rewrite(
            (
                "cdef int func(int a, int b) noexcept with gil:\n"
                "    return a + b"
            )
        )

    def test_except_plus(self):
        self.rewrite(
            (
                "cdef int func(a, int b) except +:\n"
                "    return a + b"
            )
        )
    
    def test_cpdef_nogil(self):
        self.rewrite(
            (
                "cpdef int func(int a, int b) nogil:\n"
                "    return a + b"
            )
        )
