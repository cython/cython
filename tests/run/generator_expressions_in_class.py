# mode: run
# tag: generators


class TestClass(object):
    """
    >>> TestClass.x
    [1, 2, 3]
    >>> list(TestClass.gen)
    []
    >>> TestClass.gen_result
    [2, 4, 6]
    >>> TestClass.test
    True
    >>> list(TestClass.gen3)
    [2, 4, 6, 8, 10, 12]
    """

    x = [1, 2, 3]

    gen = (i * 2 for i in x)

    test = all(i * 2 for i in x)

    gen_result = list(gen)

    nested_list = [[1, 2, 3], [4, 5, 6]]

    #gen2 = (i * 2 for i in x for x in nested_list)  # move to error test

    gen3 = (i * 2 for x in nested_list for i in x)
