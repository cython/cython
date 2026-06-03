# mode: run
# tag: cyfunction,call,python
# cython: binding=True

#######
# Test that Cython and Python functions can call each other in various signature combinations
# and check that the right calls use vectorcall (PyMethodCallNode).
#######

cimport cython

py_call_noargs = eval("lambda: 'noargs'")
py_call_onearg = eval("lambda arg: arg")
py_call_twoargs = eval("lambda arg, arg2: (arg, arg2)")
py_call_starargs = eval("lambda *args: args")
py_call_pos_and_starargs = eval("lambda arg, *args: (arg, args)")
py_call_starstarargs = eval("lambda **kw: sorted(kw.items())")
py_call_args_and_starstarargs = eval("lambda *args, **kw: (args, sorted(kw.items()))")


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_noargs():
    """
    >>> cy_call_noargs()
    'noargs'
    """
    return py_call_noargs()


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_onearg(f):
    """
    >>> cy_call_onearg(py_call_onearg)
    'onearg'
    >>> try: cy_call_onearg(py_call_noargs)
    ... except TypeError: pass
    ... else: print("FAILED!")
    >>> try: cy_call_onearg(py_call_twoargs)
    ... except TypeError: pass
    ... else: print("FAILED!")

    >>> class Class(object):
    ...     def method(self, arg): return arg

    >>> cy_call_onearg(Class().method)
    'onearg'
    """
    return f('onearg')


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_twoargs(f, arg):
    """
    >>> cy_call_twoargs(py_call_twoargs, 132)
    (132, 'twoargs')

    >>> class Class2(object):
    ...     def method(self, arg, arg2): return arg, arg2
    >>> cy_call_twoargs(Class2().method, 123)
    (123, 'twoargs')

    >>> class Class1(object):
    ...     def method(self, arg): return arg
    >>> cy_call_twoargs(Class1.method, Class1())
    'twoargs'
    """
    return f(arg, 'twoargs')


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_arg_and_kwarg(f, arg):
    """
    >>> cy_call_arg_and_kwarg(py_call_twoargs, 123)
    (123, 'twoargs')


    >>> class Class(object):
    ...     def method1(self, arg, arg2): return arg, arg2
    ...     def method2(self, arg): return arg
    >>> cy_call_arg_and_kwarg(Class().method1, 123)
    (123, 'twoargs')
    >>> cy_call_twoargs(Class.method2, Class())
    'twoargs'
    """
    return f(arg, arg2='twoargs')


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_two_kwargs(f, arg):
    """
    >>> cy_call_two_kwargs(py_call_twoargs, arg=132)
    (132, 'two-kwargs')
    >>> cy_call_two_kwargs(f=py_call_twoargs, arg=132)
    (132, 'two-kwargs')
    >>> cy_call_two_kwargs(arg=132, f=py_call_twoargs)
    (132, 'two-kwargs')

    >>> class Class(object):
    ...     def method(self, arg, arg2): return arg, arg2

    >>> cy_call_two_kwargs(Class().method, 123)
    (123, 'two-kwargs')
    """
    return f(arg2='two-kwargs', arg=arg)


@cython.test_fail_if_path_exists("//PyMethodCallNode")
def cy_call_starargs(*args):
    """
    >>> cy_call_starargs()
    ()
    >>> cy_call_starargs(1)
    (1,)
    >>> cy_call_starargs(1, 2)
    (1, 2)
    >>> cy_call_starargs(1, 2, 3)
    (1, 2, 3)
    """
    return py_call_starargs(*args)


@cython.test_fail_if_path_exists("//PyMethodCallNode")
def cy_call_pos_and_starargs(f, *args):
    """
    >>> cy_call_pos_and_starargs(py_call_onearg)
    'no-arg'
    >>> cy_call_pos_and_starargs(py_call_onearg, 123)
    123
    >>> cy_call_pos_and_starargs(py_call_twoargs, 123, 321)
    (123, 321)
    >>> cy_call_pos_and_starargs(py_call_starargs)
    ('no-arg',)
    >>> cy_call_pos_and_starargs(py_call_starargs, 123)
    (123,)
    >>> cy_call_pos_and_starargs(py_call_starargs, 123, 321)
    (123, 321)
    >>> cy_call_pos_and_starargs(py_call_pos_and_starargs)
    ('no-arg', ())
    >>> cy_call_pos_and_starargs(py_call_pos_and_starargs, 123)
    (123, ())
    >>> cy_call_pos_and_starargs(py_call_pos_and_starargs, 123, 321)
    (123, (321,))
    >>> cy_call_pos_and_starargs(py_call_pos_and_starargs, 123, 321, 234)
    (123, (321, 234))

    >>> class Class(object):
    ...     def method(self, arg, arg2): return arg, arg2

    >>> cy_call_pos_and_starargs(Class().method, 123, 321)
    (123, 321)
    >>> cy_call_pos_and_starargs(Class.method, Class(), 123, 321)
    (123, 321)
    """
    return f(args[0] if args else 'no-arg', *args[1:])


# Choice of whether to use PyMethodCallNode here is pretty arbitrary -
# vectorcall_dict or PyObject_Call are likely to be fairly similar cost.
# The test is for the current behaviour but it isn't a big issue if it changes.
@cython.test_fail_if_path_exists("//PyMethodCallNode")
def cy_call_starstarargs(**kw):
    """
    >>> kw = {}
    >>> cy_call_starstarargs(**kw)
    []
    >>> kw = {'a': 123}
    >>> cy_call_starstarargs(**kw)
    [('a', 123)]
    >>> kw = {'a': 123, 'b': 321}
    >>> cy_call_starstarargs(**kw)
    [('a', 123), ('b', 321)]
    """
    return py_call_starstarargs(**kw)


# Choice of whether to use PyMethodCallNode here is pretty arbitrary -
# vectorcall_dict or PyObject_Call are likely to be fairly similar cost.
# The test is for the current behaviour but it isn't a big issue if it changes.
@cython.test_fail_if_path_exists("//PyMethodCallNode")
def cy_call_kw_and_starstarargs(f=None, arg1=None, **kw):
    """
    >>> kw = {}
    >>> cy_call_kw_and_starstarargs(**kw)
    [('arg', None)]
    >>> try: cy_call_kw_and_starstarargs(py_call_noargs, **kw)
    ... except TypeError: pass
    >>> try: cy_call_kw_and_starstarargs(py_call_twoargs, **kw)
    ... except TypeError: pass
    ... else: print("FAILED!")
    >>> cy_call_kw_and_starstarargs(py_call_onearg, **kw)
    >>> cy_call_kw_and_starstarargs(f=py_call_onearg, **kw)
    >>> cy_call_kw_and_starstarargs(py_call_pos_and_starargs, **kw)
    (None, ())

    >>> kw = {'arg1': 123}
    >>> cy_call_kw_and_starstarargs(**kw)
    [('arg', 123)]
    >>> cy_call_kw_and_starstarargs(py_call_onearg, **kw)
    123
    >>> cy_call_kw_and_starstarargs(f=py_call_onearg, **kw)
    123
    >>> cy_call_kw_and_starstarargs(py_call_twoargs, arg2=321, **kw)
    (123, 321)
    >>> cy_call_kw_and_starstarargs(f=py_call_twoargs, arg2=321, **kw)
    (123, 321)
    >>> try: cy_call_kw_and_starstarargs(py_call_twoargs, **kw)
    ... except TypeError: pass
    ... else: print("FAILED!")
    >>> try: cy_call_kw_and_starstarargs(py_call_twoargs, arg2=321, other=234, **kw)
    ... except TypeError: pass
    ... else: print("FAILED!")
    >>> cy_call_kw_and_starstarargs(py_call_pos_and_starargs, **kw)
    (123, ())

    >>> try: cy_call_kw_and_starstarargs(arg=321, **kw)   # duplicate kw in Python call
    ... except TypeError: pass
    ... else: print("FAILED!")

    >>> kw = {'a': 123}
    >>> cy_call_kw_and_starstarargs(**kw)
    [('a', 123), ('arg', None)]
    >>> cy_call_kw_and_starstarargs(arg1=321, **kw)
    [('a', 123), ('arg', 321)]

    >>> kw = {'a': 123, 'b': 321}
    >>> cy_call_kw_and_starstarargs(**kw)
    [('a', 123), ('arg', None), ('b', 321)]
    >>> cy_call_kw_and_starstarargs(arg1=234, **kw)
    [('a', 123), ('arg', 234), ('b', 321)]

    >>> class Class2(object):
    ...     def method(self, arg, arg2): return arg, arg2

    >>> cy_call_kw_and_starstarargs(Class2().method, arg1=123, arg2=321)
    (123, 321)
    """
    return (f or py_call_starstarargs)(arg=arg1, **kw)


@cython.test_assert_path_exists("//PyMethodCallNode")
def cy_call_pos_and_starstarargs(f=None, arg1=None, **kw):
    """
    >>> cy_call_pos_and_starstarargs(arg=123)
    ((None,), [('arg', 123)])
    >>> cy_call_pos_and_starstarargs(arg1=123)
    ((123,), [])
    >>> cy_call_pos_and_starstarargs(arg=123, arg2=321)
    ((None,), [('arg', 123), ('arg2', 321)])
    >>> cy_call_pos_and_starstarargs(arg1=123, arg2=321)
    ((123,), [('arg2', 321)])

    >>> class Class2(object):
    ...     def method(self, arg, arg2=None): return arg, arg2

    >>> cy_call_pos_and_starstarargs(Class2().method, 123)
    (123, None)
    >>> cy_call_pos_and_starstarargs(Class2().method, 123, arg2=321)
    (123, 321)
    >>> cy_call_pos_and_starstarargs(Class2().method, arg1=123, arg2=321)
    (123, 321)
    >>> cy_call_pos_and_starstarargs(Class2.method, Class2(), arg=123)
    (123, None)
    >>> cy_call_pos_and_starstarargs(Class2.method, Class2(), arg=123, arg2=321)
    (123, 321)
    >>> cy_call_pos_and_starstarargs(Class2.method, arg1=Class2(), arg=123, arg2=321)
    (123, 321)
    """
    return (f or py_call_args_and_starstarargs)(arg1, **kw)
