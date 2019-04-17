# cython: language_level=3
# mode: run
# tag: pep3135, pure3.0


class C(object):
    """
    >>> obj = C()
    >>> obj.method_1()
    2
    >>> obj.method_2()
    3
    >>> obj.method_3()
    ['__class__', 'self']
    """

    @classmethod
    def class_method(cls):
        return 2

    @staticmethod
    def static_method():
        return 3

    def method_1(self):
        return __class__.class_method()

    def method_2(self):
        return __class__.static_method()

    def method_3(self):
        __class__
        return sorted(list(locals().keys()))