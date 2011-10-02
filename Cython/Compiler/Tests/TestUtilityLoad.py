import unittest

from Cython.Compiler import Code, UtilityCode


def strip_2tup(tup):
    return tup[0] and tup[0].strip(), tup[1] and tup[1].strip()

class TestUtilityLoader(unittest.TestCase):
    """
    Test loading UtilityCodes
    """

    expected = "test {{loader}} prototype", "test {{loader}} impl"
    expected_tempita = (expected[0].replace('{{loader}}', 'Loader'),
                        expected[1].replace('{{loader}}', 'Loader'))

    required = "I am a dependency proto", "I am a dependency impl"

    context = dict(loader='Loader')

    name = "TestUtilityLoader"
    filename = "TestUtilityLoader.c"
    cls = Code.UtilityCode

    def test_load_as_string(self):
        got = strip_2tup(self.cls.load_as_string(self.name))
        self.assertEquals(got, self.expected)

        got = strip_2tup(self.cls.load_as_string(self.name, self.filename))
        self.assertEquals(got, self.expected)

        got = strip_2tup(self.cls.load_as_string(self.name, context=self.context))
        self.assertEquals(got, self.expected_tempita)

    def test_load(self):
        utility = self.cls.load(self.name)
        got = strip_2tup((utility.proto, utility.impl))
        self.assertEquals(got, self.expected)

        # Not implemented yet
        #required, = utility.requires
        #self.assertEquals((required.proto, required.impl), self.required)

        utility = self.cls.load(self.name, from_file=self.filename)
        got = strip_2tup((utility.proto, utility.impl))
        self.assertEquals(got, self.expected)


class TestCythonUtilityLoader(TestUtilityLoader):
    """
    Test loading CythonUtilityCodes
    """

    # Just change the attributes and run the same tests
    expected = None, "test {{cy_loader}} impl"
    expected_tempita = None, "test CyLoader impl"

    required = None, "I am a Cython dependency impl"

    context = dict(cy_loader='CyLoader')

    name = "TestCyUtilityLoader"
    filename = "TestCyUtilityLoader.pyx"
    cls = UtilityCode.CythonUtilityCode

    # Small hack to pass our tests above
    cls.proto = None