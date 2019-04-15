# mode: run
# tag: posonly

# TODO: remove posonly tag before merge

import cython

# TODO: add the test below to an 'error' test
#def test_invalid_syntax_errors():
#    def f(a, b = 5, /, c): pass
#    def f(a = 5, b, /, c): pass
#    def f(a = 5, b, /): pass
#    def f(*args, /): pass
#    def f(*args, a, /): pass
#    def f(**kwargs, /): pass
#    def f(/, a = 1): pass
#    def f(/, a): pass
#    def f(/): pass
#    def f(*, a, /): pass
#    def f(*, /, a): pass
#    def f(a, /, a): pass
#    def f(a, /, *, a): pass
#    def f(a, b/2, c): pass

def test_optional_posonly_args1(a, b=10, /, c=100):
    """
    >>> test_optional_posonly_args1(1, 2, 3)
    6
    >>> test_optional_posonly_args1(1, 2, c=3)
    6
    >>> test_optional_posonly_args1(1, b=2, c=3)
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args1() got an unexpected keyword argument 'b'
    >>> test_optional_posonly_args1(1, 2)
    103
    >>> test_optional_posonly_args1(1, b=2)
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args1() got an unexpected keyword argument 'b'
    """
    return a + b + c

def test_optional_posonly_args2(a=1, b=10, /, c=100):
    """
    >>> test_optional_posonly_args2(1, 2, 3)
    6
    >>> test_optional_posonly_args2(1, 2, c=3)
    6
    >>> test_optional_posonly_args2(1, b=2, c=3)
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args2() got an unexpected keyword argument 'b'
    >>> test_optional_posonly_args2(1, 2)
    103
    >>> test_optional_posonly_args2(1, b=2)
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args2() got an unexpected keyword argument 'b'
    >>> test_optional_posonly_args2(1, c=2)
    13
    """
    return a + b + c

# TODO: remove the test below?  would need to hard-code the function with > 255 posonly args
#def test_syntax_for_many_positional_only():
#    # more than 255 positional only arguments, should compile ok
#    fundef = "def f(%s, /):\n  pass\n" % ', '.join('i%d' % i for i in range(300))
#    compile(fundef, "<test>", "single")

# TODO: remove the test below?  doesn't seem relevant to Cython implementation
#def test_pos_only_definition(self):
#    def f(a, b, c, /, d, e=1, *, f, g=2):
#        pass
#
#    self.assertEqual(2, f.__code__.co_argcount)  # 2 "standard args"
#    self.assertEqual(3, f.__code__.co_posonlyargcount)
#    self.assertEqual((1,), f.__defaults__)
#
#    def f(a, b, c=1, /, d=2, e=3, *, f, g=4):
#        pass
#
#    self.assertEqual(2, f.__code__.co_argcount)  # 2 "standard args"
#    self.assertEqual(3, f.__code__.co_posonlyargcount)
#    self.assertEqual((1, 2, 3), f.__defaults__)

def test_pos_only_call_via_unpacking(a, b, /):
    """
    >>> test_pos_only_call_via_unpacking(*[1,2])
    3
    """
    return a + b

def test_use_positional_as_keyword1(a, /):
    """
    >>> test_use_positional_as_keyword1(a=1)
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword1() takes no keyword arguments
    """
    pass

def test_use_positional_as_keyword2(a, /, b):
    """
    >>> test_use_positional_as_keyword2(a=1, b=2)
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword2() takes exactly 2 positional arguments (0 given)
    """
    pass

def test_use_positional_as_keyword3(a, b, /):
    """
    >>> test_use_positional_as_keyword3(a=1, b=2)
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword3() takes exactly 2 positional arguments (0 given)
    """
    pass

def test_positional_only_and_arg_invalid_calls(a, b, /, c):
    """
    >>> test_positional_only_and_arg_invalid_calls(1, 2)
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() takes exactly 3 positional arguments (2 given)
    >>> test_positional_only_and_arg_invalid_calls(1)
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() takes exactly 3 positional arguments (1 given)
    >>> test_positional_only_and_arg_invalid_calls(1,2,3,4)
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() takes exactly 3 positional arguments (4 given)
    """
    pass

def test_positional_only_and_optional_arg_invalid_calls(a, b, /, c=3):
    """
    >>> test_positional_only_and_optional_arg_invalid_calls(1, 2)
    >>> test_positional_only_and_optional_arg_invalid_calls(1)
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() takes at least 2 positional arguments (1 given)
    >>> test_positional_only_and_optional_arg_invalid_calls()
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() takes at least 2 positional arguments (0 given)
    >>> test_positional_only_and_optional_arg_invalid_calls(1, 2, 3, 4)
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() takes at most 3 positional arguments (4 given)
    """
    pass

def test_positional_only_invalid_calls(a, b, /):
    """
    >>> test_positional_only_invalid_calls(1, 2)
    >>> test_positional_only_invalid_calls(1)
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() takes exactly 2 positional arguments (1 given)
    >>> test_positional_only_invalid_calls()
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() takes exactly 2 positional arguments (0 given)
    >>> test_positional_only_invalid_calls(1, 2, 3)
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() takes exactly 2 positional arguments (3 given)
    """
    pass

def test_positional_only_with_optional_invalid_calls(a, b=2, /):
    """
    >>> test_positional_only_with_optional_invalid_calls(1)
    >>> test_positional_only_with_optional_invalid_calls()
    Traceback (most recent call last):
    TypeError: test_positional_only_with_optional_invalid_calls() takes at least 1 positional argument (0 given)
    >>> test_positional_only_with_optional_invalid_calls(1, 2, 3)
    Traceback (most recent call last):
    TypeError: test_positional_only_with_optional_invalid_calls() takes at most 2 positional arguments (3 given)
    """
    pass

def test_no_standard_args_usage(a, b, /, *, c):
    """
    >>> test_no_standard_args_usage(1, 2, c=3)
    >>> test_no_standard_args_usage(1, b=2, c=3)
    Traceback (most recent call last):
    TypeError: test_no_standard_args_usage() takes exactly 2 positional arguments (1 given)
    """
    pass

#def test_change_default_pos_only():
# TODO: probably remove this, since we have no __defaults__ in Cython?
#    """
#    >>> test_change_default_pos_only()
#    True
#    True
#    """
#    def f(a, b=2, /, c=3):
#        return a + b + c
#
#    print((2,3) == f.__defaults__)
#    f.__defaults__ = (1, 2, 3)
#    print(f(1, 2, 3) == 6)

def test_lambdas():
    """
    >>> test_lambdas()
    3
    3
    3
    3
    3
    """
    x = lambda a, /, b: a + b
    print(x(1,2))
    print(x(1,b=2))

    x = lambda a, /, b=2: a + b
    print(x(1))

    x = lambda a, b, /: a + b
    print(x(1, 2))

    x = lambda a, b, /, : a + b
    print(x(1, 2))


#TODO: need to implement this in the 'error' test
#def test_invalid_syntax_lambda(self):
#    lambda a, b = 5, /, c: None
#    lambda a = 5, b, /, c: None
#    lambda a = 5, b, /: None
#    lambda a, /, a: None
#    lambda a, /, *, a: None
#    lambda *args, /: None
#    lambda *args, a, /: None
#    lambda **kwargs, /: None
#    lambda /, a = 1: None
#    lambda /, a: None
#    lambda /: None
#    lambda *, a, /: None
#    lambda *, /, a: None

class Example:
    def f(self, a, b, /):
        return a, b

def test_posonly_methods():
    """
    >>> Example().f(1,2)
    (1, 2)
    >>> Example.f(Example(), 1, 2)
    (1, 2)
    >>> try:
    ...     Example.f(1,2)
    ... except TypeError:
    ...    print("Got type error")
    Got type error
    >>> Example().f(1, b=2)
    Traceback (most recent call last):
    TypeError: f() takes exactly 3 positional arguments (2 given)
    """
    pass

class X:
    def f(self, *, __a=42):
        return __a
def test_mangling():
    """
    >>> X().f()
    42
    """
    pass

def global_pos_only_f(a, b, /):
    pass

def test_module_function():
    """
    >>> global_pos_only_f()
    Traceback (most recent call last):
    TypeError: global_pos_only_f() takes exactly 2 positional arguments (0 given)
    """
    pass

def test_closures1(x,y):
    """
    >>> test_closures1(1,2)(3,4)
    10
    >>> test_closures1(1,2)(3)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (1 given)
    >>> test_closures1(1,2)(3,4,5)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (3 given)
    """
    def g(x2,/,y2):
        return x + y + x2 + y2
    return g

def test_closures2(x,/,y):
    """
    >>> test_closures2(1,2)(3,4)
    10
    """
    def g(x2,y2):
        return x + y + x2 + y2
    return g

def test_closures3(x,/,y):
    """
    >>> test_closures3(1,2)(3,4)
    10
    >>> test_closures3(1,2)(3)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (1 given)
    >>> test_closures3(1,2)(3,4,5)
    Traceback (most recent call last):
    TypeError: g() takes exactly 2 positional arguments (3 given)
    """
    def g(x2,/,y2):
        return x + y + x2 + y2
    return g

def test_same_keyword_as_positional_with_kwargs(something, /, **kwargs):
    """
    >>> test_same_keyword_as_positional_with_kwargs(42, something=42)
    (42, {'something': 42})
    >>> test_same_keyword_as_positional_with_kwargs(something=42)
    Traceback (most recent call last):
    TypeError: test_same_keyword_as_positional_with_kwargs() takes exactly 1 positional argument (0 given)
    >>> test_same_keyword_as_positional_with_kwargs(42)
    (42, {})
    """
    return (something, kwargs)
