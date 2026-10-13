import unittest
import asyncio

try:
    raise ExceptionGroup("Errors", [
        ValueError("invalid value"),
        TypeError("invalid type"),
    ])
except* ValueError as eg:
    VALUE_ERROR_COUNT = len(eg.exceptions)
    VALUE_ERROR_MSG = str(eg.exceptions[0])
except* TypeError as eg:
    TYPE_ERROR_COUNT = len(eg.exceptions)
    TYPE_ERROR_MSG = str(eg.exceptions[0])

async def async_f():
    try:
        raise ExceptionGroup("Errors", [
            ValueError("invalid value"),
            TypeError("invalid type"),
        ])
    except* ValueError as eg:
        value_error_count = len(eg.exceptions)
        value_error_msg = str(eg.exceptions[0])
    except* TypeError as eg:
        type_error_count = len(eg.exceptions)
        type_error_msg = str(eg.exceptions[0])
    return [
        value_error_count, value_error_msg,
        type_error_count, type_error_msg
    ]


def generator():
    try:
        raise ExceptionGroup("Errors", [
            ValueError("invalid value"),
            TypeError("invalid type"),
        ])
    except* ValueError as eg:
        value_error_count = len(eg.exceptions)
        value_error_msg = str(eg.exceptions[0])
    except* TypeError as eg:
        type_error_count = len(eg.exceptions)
        type_error_msg = str(eg.exceptions[0])

    for i in [
        value_error_count, value_error_msg,
        type_error_count, type_error_msg
    ]:
        yield i

async def async_generator():
    try:
        raise ExceptionGroup("Errors", [
            ValueError("invalid value"),
            TypeError("invalid type"),
        ])
    except* ValueError as eg:
        value_error_count = len(eg.exceptions)
        value_error_msg = str(eg.exceptions[0])
    except* TypeError as eg:
        type_error_count = len(eg.exceptions)
        type_error_msg = str(eg.exceptions[0])

    for i in [
        value_error_count, value_error_msg,
        type_error_count, type_error_msg
    ]:
        yield i


class MyClass:
    try:
        raise ExceptionGroup("Errors", [
            ValueError("invalid value"),
            TypeError("invalid type"),
        ])
    except* ValueError as eg:
        value_error_count = len(eg.exceptions)
        value_error_msg = str(eg.exceptions[0])
    except* TypeError as eg:
        type_error_count = len(eg.exceptions)
        type_error_msg = str(eg.exceptions[0])


def class_level_inside_function(errors: list[Exception]):
    class LocalClass:
        value_error_count = 0
        value_error_msg = None
        type_error_count = 0
        type_error_msg = None
        try:
            if errors:
                raise ExceptionGroup("Errors", errors)
        except* ValueError as eg:
            value_error_count = len(eg.exceptions)
            value_error_msg = str(eg.exceptions[0])
        except* TypeError as eg:
            type_error_count = len(eg.exceptions)
            type_error_msg = str(eg.exceptions[0])
    return LocalClass

class TestExceptStar(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()
        self.loop = None
        super().tearDown()

    def test_async_def(self):
        res = self.loop.run_until_complete(async_f())
        self.assertEqual(res, [1, "invalid value", 1, "invalid type"] )

    def test_generator(self):
        ret = list(generator())
        self.assertEqual(ret, [1, "invalid value", 1, "invalid type"])

    def test_async_generator(self):
        async def consume():
            return [x async for x in async_generator()]
        ret = self.loop.run_until_complete(consume())
        self.assertEqual(ret, [1, "invalid value", 1, "invalid type"])

    def test_module_level(self):
        self.assertEqual(VALUE_ERROR_COUNT, 1)
        self.assertEqual(VALUE_ERROR_MSG, "invalid value")
        self.assertEqual(TYPE_ERROR_COUNT, 1)
        self.assertEqual(TYPE_ERROR_MSG, "invalid type")

    def test_class_level(self):
        self.assertEqual(MyClass.value_error_count, 1)
        self.assertEqual(MyClass.value_error_msg, "invalid value")
        self.assertEqual(MyClass.type_error_count, 1)
        self.assertEqual(MyClass.type_error_msg, "invalid type")

    def test_class_level_inside_function(self):
        c = class_level_inside_function(
            [ValueError("invalid value"), TypeError("invalid type")]
        )
        self.assertEqual(c.value_error_count, 1)
        self.assertEqual(c.value_error_msg, "invalid value")
        self.assertEqual(c.type_error_count, 1)
        self.assertEqual(c.type_error_msg, "invalid type")

        c = class_level_inside_function([])
        self.assertEqual(c.value_error_count, 0)
        self.assertEqual(c.value_error_msg, None)
        self.assertEqual(c.type_error_count, 0)
        self.assertEqual(c.type_error_msg, None)


if __name__ == '__main__':
    unittest.main()
