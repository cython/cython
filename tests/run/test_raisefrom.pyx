
import sys
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

    def test_raise_from_none_sets_no_cause(self):
        try:
            raise IndexError from None
        except IndexError as e:
            self.assertFalse(e.__cause__)
            self.assertTrue(e.__suppress_context__)
        else:
            self.fail("No exception raised")

    def test_raise_from_none_covers_context(self):
        try:
            try:
                raise IndexError("INDEX")
            except IndexError as e:
                raise ValueError("VALUE") from None
            else:
                self.fail("No exception raised")
        except ValueError as e:
            self.assertFalse(e.__cause__)
            self.assertTrue(e.__context__)
            self.assertTrue(e.__suppress_context__)

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
