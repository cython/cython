# mode: run
# tag: pep492, asyncfor, await, gh2613

# Using C-globals in coroutines.


cdef object py_retval


async def test():
    """
    >>> t = test()
    >>> try: t.send(None)
    ... except StopIteration as ex:
    ...     print(ex.args[0] if ex.args else None)
    ... else: print("NOT STOPPED!")
    None
    """
    global py_retval
    py_retval = {'foo': 42}
