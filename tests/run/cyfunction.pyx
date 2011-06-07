# cython: binding=True
# mode: run
# tag: cyfunction

def test_dict():
    """
    >>> test_dict.foo = 123
    >>> test_dict.__dict__
    {'foo': 123}
    """

def test_name():
    """
    >>> test_name.__name__
    'test_name'
    """

def test_reduce():
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(test_reduce))()
    'Hello, world!'
    """
    return 'Hello, world!'

def test_method(self):
    return self

class BindingTest:
    """
    >>> BindingTest.test_method = test_method
    >>> BindingTest.test_method() #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> BindingTest().test_method()
    <BindingTest instance>
    """
    def __repr__(self):
        return '<BindingTest instance>'
