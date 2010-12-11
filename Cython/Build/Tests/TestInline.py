from Cython.Shadow import inline

from Cython.TestUtils import CythonTest

class TestStripLiterals(CythonTest):

    def test_inline(self):
        self.assertEquals(inline("return 1+2"), 3)
