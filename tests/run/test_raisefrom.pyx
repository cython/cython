import unittest
# adapted from pyregr
class TestCause(unittest.TestCase):
    def test_invalid_cause(self):
        try:
            raise IndexError from 5
        except TypeError as e:
            self.assertTrue("exception cause" in str(e))
        else:
            self.fail("No exception raised")

    def test_class_cause(self):
        try:
            raise IndexError from KeyError
        except IndexError as e:
            self.assertTrue(isinstance(e.__cause__, KeyError))
        else:
            self.fail("No exception raised")

    def test_instance_cause(self):
        cause = KeyError()
        try:
            raise IndexError from cause
        except IndexError as e:
            self.assertTrue(e.__cause__ is cause)
        else:
            self.fail("No exception raised")

    def test_erroneous_cause(self):
        class MyException(Exception):
            def __init__(self):
                raise RuntimeError()

        try:
            raise IndexError from MyException
        except RuntimeError:
            pass
        else:
            self.fail("No exception raised")
