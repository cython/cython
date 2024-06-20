import cython

def func(foo: dict, bar: cython.int) -> tuple:
    foo["hello world"] = 3 + bar
    return foo, 5
