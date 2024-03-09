from unittest import TestCase

from Cython.Compiler.Code import UtilityCode

class TestUtilityCode(TestCase):
    def test_equality(self):
        c1 = UtilityCode.load("NumpyImportUFunc", "NumpyImportArray.c")
        c2 = UtilityCode.load("NumpyImportArray", "NumpyImportArray.c")
        c3 = UtilityCode.load("pyunicode_strlen", "StringTools.c")
        c4 = UtilityCode.load("pyunicode_from_unicode", "StringTools.c")
        c5 = UtilityCode.load("IncludeStringH", "StringTools.c")
        c6 = UtilityCode.load("IncludeCppStringH", "StringTools.c")

        codes = [c1, c2, c3, c4, c5, c6]
        for m in range(len(codes)):
            for n in range(len(codes)):
                if n == m:
                    continue
                self.assertNotEqual(codes[m], codes[n])
