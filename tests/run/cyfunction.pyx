# cython: binding=True
# mode: run
# tag: cyfunction

def test_dict():
    """
    >>> test_dict.foo = 123
    >>> test_dict.__dict__
    {'foo': 123}
    >>> test_dict.__dict__ = {'bar': 321}
    >>> test_dict.__dict__
    {'bar': 321}
    >>> test_dict.func_dict
    {'bar': 321}
    """

def test_name():
    """
    >>> test_name.__name__
    'test_name'
    >>> test_name.func_name
    'test_name'
    >>> test_name.__name__ = 123 #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: __name__ must be set to a ... object
    >>> test_name.__name__ = 'foo'
    >>> test_name.__name__
    'foo'
    """

def test_doc():
    """
    >>> del test_doc.__doc__
    >>> test_doc.__doc__
    >>> test_doc.__doc__ = 'docstring'
    >>> test_doc.__doc__
    'docstring'
    >>> test_doc.func_doc
    'docstring'
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
