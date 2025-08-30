# cython: always_allow_keywords=True
# mode: run
# tag: posonly, pure3.8

import cython
import pickle

def test_optional_posonly_args1(a, b=10, /, c=100):
    """
    >>> test_optional_posonly_args1(1, 2, 3)
    6
    >>> test_optional_posonly_args1(1, 2, c=3)
    6
    >>> test_optional_posonly_args1(1, b=2, c=3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args1() got ... keyword argument... 'b'
    >>> test_optional_posonly_args1(1, 2)
    103
    >>> test_optional_posonly_args1(1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args1() got ... keyword argument... 'b'
    """
    return a + b + c

def test_optional_posonly_args2(a=1, b=10, /, c=100):
    """
    >>> test_optional_posonly_args2(1, 2, 3)
    6
    >>> test_optional_posonly_args2(1, 2, c=3)
    6
    >>> test_optional_posonly_args2(1, b=2, c=3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args2() got ... keyword argument... 'b'
    >>> test_optional_posonly_args2(1, 2)
    103
    >>> test_optional_posonly_args2(1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_optional_posonly_args2() got ... keyword argument... 'b'
    >>> test_optional_posonly_args2(1, c=2)
    13
    """
    return a + b + c

# TODO: this causes a line that is too long for old versions of Clang
#def many_args(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,
#              a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,a38,a39,a40,
#              a41,a42,a43,a44,a45,a46,a47,a48,a49,a50,a51,a52,a53,a54,a55,a56,a57,a58,a59,
#              a60,a61,a62,a63,a64,a65,a66,a67,a68,a69,a70,a71,a72,a73,a74,a75,a76,a77,a78,
#              a79,a80,a81,a82,a83,a84,a85,a86,a87,a88,a89,a90,a91,a92,a93,a94,a95,a96,a97,
#              a98,a99,a100,a101,a102,a103,a104,a105,a106,a107,a108,a109,a110,a111,a112,
#              a113,a114,a115,a116,a117,a118,a119,a120,a121,a122,a123,a124,a125,a126,a127,
#              a128,a129,a130,a131,a132,a133,a134,a135,a136,a137,a138,a139,a140,a141,a142,
#              a143,a144,a145,a146,a147,a148,a149,a150,a151,a152,a153,a154,a155,a156,a157,
#              a158,a159,a160,a161,a162,a163,a164,a165,a166,a167,a168,a169,a170,a171,a172,
#              a173,a174,a175,a176,a177,a178,a179,a180,a181,a182,a183,a184,a185,a186,a187,
#              a188,a189,a190,a191,a192,a193,a194,a195,a196,a197,a198,a199,a200,a201,a202,
#              a203,a204,a205,a206,a207,a208,a209,a210,a211,a212,a213,a214,a215,a216,a217,
#              a218,a219,a220,a221,a222,a223,a224,a225,a226,a227,a228,a229,a230,a231,a232,
#              a233,a234,a235,a236,a237,a238,a239,a240,a241,a242,a243,a244,a245,a246,a247,
#              a248,a249,a250,a251,a252,a253,a254,a255,a256,a257,a258,a259,a260,a261,a262,
#              a263,a264,a265,a266,a267,a268,a269,a270,a271,a272,a273,a274,a275,a276,a277,
#              a278,a279,a280,a281,a282,a283,a284,a285,a286,a287,a288,a289,a290,a291,a292,
#              a293,a294,a295,a296,a297,a298,a299,/,b,c=42,*,d):
#    """
#    >>> many_args(*range(299),b=1,c=2,d=3)
#    (298, 1, 2, 3)
#    >>> many_args(*range(299),b=1,d=3)
#    (298, 1, 42, 3)
#    >>> many_args(*range(300),d=3)
#    (298, 299, 42, 3)
#    """
#    return (a299, b, c, d)

#TODO: update this test for Python 3.8 final
@cython.binding(True)
def func_introspection1(a, b, c, /, d, e=1, *, f, g=2):
    """
    >>> assert func_introspection2.__code__.co_argcount == 5, func_introspection2.__code__.co_argcount
    >>> func_introspection1.__defaults__
    (1,)
    """

@cython.binding(True)
def func_introspection2(a, b, c=1, /, d=2, e=3, *, f, g=4):
    """
    >>> assert func_introspection2.__code__.co_argcount == 5, func_introspection2.__code__.co_argcount
    >>> func_introspection2.__defaults__
    (1, 2, 3)
    """

def test_pos_only_call_via_unpacking(a, b, /):
    """
    >>> test_pos_only_call_via_unpacking(*[1,2])
    3
    """
    return a + b

def test_use_positional_as_keyword1(a, /):
    """
    >>> test_use_positional_as_keyword1(1)
    >>> test_use_positional_as_keyword1(a=1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword1() ... keyword argument...
    """

def test_use_positional_as_keyword2(a, /, b):
    """
    >>> test_use_positional_as_keyword2(1, 2)
    >>> test_use_positional_as_keyword2(1, b=2)
    >>> test_use_positional_as_keyword2(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword2() ... positional...argument...
    """

def test_use_positional_as_keyword3(a, b, /):
    """
    >>> test_use_positional_as_keyword3(1, 2)
    >>> test_use_positional_as_keyword3(a=1, b=2) # doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_use_positional_as_keyword3() got ... keyword argument...
    """

def test_positional_only_and_arg_invalid_calls(a, b, /, c):
    """
    >>> test_positional_only_and_arg_invalid_calls(1, 2, 3)
    >>> test_positional_only_and_arg_invalid_calls(1, 2, c=3)
    >>> test_positional_only_and_arg_invalid_calls(1, 2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() ... positional argument...
    >>> test_positional_only_and_arg_invalid_calls(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() ... positional arguments...
    >>> test_positional_only_and_arg_invalid_calls(1,2,3,4)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_arg_invalid_calls() takes ... positional arguments ...4 ...given...
    """

def test_positional_only_and_optional_arg_invalid_calls(a, b, /, c=3):
    """
    >>> test_positional_only_and_optional_arg_invalid_calls(1, 2)
    >>> test_positional_only_and_optional_arg_invalid_calls(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() ... positional argument...
    >>> test_positional_only_and_optional_arg_invalid_calls()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() ... positional arguments...
    >>> test_positional_only_and_optional_arg_invalid_calls(1, 2, 3, 4)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_optional_arg_invalid_calls() takes ... positional arguments ...4 ...given...
    """

def test_positional_only_and_kwonlyargs_invalid_calls(a, b, /, c, *, d, e):
    """
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2, 3, d=1, e=2)
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2, 3, e=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() ... keyword-only argument...d...
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() ... keyword-only argument...d...
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() ... positional argument...
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() ... positional arguments...
    >>> test_positional_only_and_kwonlyargs_invalid_calls()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() ... positional arguments...
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2, 3, 4, 5, 6, d=7, e=8)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() takes ... positional arguments ...
    >>> test_positional_only_and_kwonlyargs_invalid_calls(1, 2, 3, d=1, e=4, f=56)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_and_kwonlyargs_invalid_calls() got an unexpected keyword argument 'f'
    """

def test_positional_only_invalid_calls(a, b, /):
    """
    >>> test_positional_only_invalid_calls(1, 2)
    >>> test_positional_only_invalid_calls(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() ... positional argument...
    >>> test_positional_only_invalid_calls()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() ... positional arguments...
    >>> test_positional_only_invalid_calls(1, 2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_invalid_calls() takes ... positional arguments ...3 ...given...
    """

def test_positional_only_with_optional_invalid_calls(a, b=2, /):
    """
    >>> test_positional_only_with_optional_invalid_calls(1)
    >>> test_positional_only_with_optional_invalid_calls()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_with_optional_invalid_calls() ... positional argument...
    >>> test_positional_only_with_optional_invalid_calls(1, 2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_positional_only_with_optional_invalid_calls() takes ... positional arguments ...3 ...given...
    """

def test_no_standard_args_usage(a, b, /, *, c):
    """
    >>> test_no_standard_args_usage(1, 2, c=3)
    >>> test_no_standard_args_usage(1, b=2, c=3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_no_standard_args_usage() ... positional... argument...
    """

#def test_change_default_pos_only():
# TODO: probably remove this, since  __defaults__ is not writable in Cython?
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

class TestPosonlyMethods(object):
    """
    >>> TestPosonlyMethods().f(1,2)
    (1, 2)
    >>> TestPosonlyMethods.f(TestPosonlyMethods(), 1, 2)
    (1, 2)
    >>> try:
    ...     TestPosonlyMethods.f(1,2)
    ... except TypeError:
    ...    print("Got type error")
    Got type error
    >>> TestPosonlyMethods().f(1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...f() got ... keyword argument... 'b'
    """
    def f(self, a, b, /):
        return a, b

class TestMangling(object):
    """
    >>> TestMangling().f()
    42
    >>> TestMangling().f2()
    42

    #>>> TestMangling().f3()
    #(42, 43)
    #>>> TestMangling().f4()
    #(42, 43, 44)

    >>> TestMangling().f2(1)
    1

    #>>> TestMangling().f3(1, _TestMangling__b=2)
    #(1, 2)
    #>>> TestMangling().f4(1, _TestMangling__b=2, _TestMangling__c=3)
    #(1, 2, 3)
    """
    def f(self, *, __a=42):
        return __a

    def f2(self, __a=42, /):
        return __a

# FIXME: https://github.com/cython/cython/issues/1382
#    def f3(self, __a=42, /, __b=43):
#        return (__a, __b)

#    def f4(self, __a=42, /, __b=43, *, __c=44):
#        return (__a, __b, __c)

def test_module_function(a, b, /):
    """
    >>> test_module_function(1, 2)
    >>> test_module_function()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_module_function() ... positional arguments...
    """

def test_closures1(x,y):
    """
    >>> test_closures1(1,2)(3,4)
    10
    >>> test_closures1(1,2)(3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...g() ... positional argument...
    >>> test_closures1(1,2)(3,4,5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...g() ... positional argument...
    """
    def g(x2, /, y2):
        return x + y + x2 + y2
    return g

def test_closures2(x, /, y):
    """
    >>> test_closures2(1,2)(3,4)
    10
    """
    def g(x2,y2):
        return x + y + x2 + y2
    return g


def test_closures3(x, /, y):
    """
    >>> test_closures3(1,2)(3,4)
    10
    >>> test_closures3(1,2)(3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...g() ... positional argument...
    >>> test_closures3(1,2)(3,4,5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...g() ... positional argument...
    """
    def g(x2, /, y2):
        return x + y + x2 + y2
    return g


def test_same_keyword_as_positional_with_kwargs(something, /, **kwargs):
    """
    >>> test_same_keyword_as_positional_with_kwargs(42, something=42)
    (42, {'something': 42})
    >>> test_same_keyword_as_positional_with_kwargs(something=42)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_same_keyword_as_positional_with_kwargs() ... positional argument...
    >>> test_same_keyword_as_positional_with_kwargs(42)
    (42, {})
    """
    return (something, kwargs)

def test_serialization1(a, b, /):
    """
    >>> pickled_posonly = pickle.dumps(test_serialization1)
    >>> unpickled_posonly = pickle.loads(pickled_posonly)
    >>> unpickled_posonly(1, 2)
    (1, 2)
    >>> unpickled_posonly(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_serialization1() got ... keyword argument...
    """
    return (a, b)

def test_serialization2(a, /, b):
    """
    >>> pickled_optional = pickle.dumps(test_serialization2)
    >>> unpickled_optional = pickle.loads(pickled_optional)
    >>> unpickled_optional(1, 2)
    (1, 2)
    >>> unpickled_optional(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_serialization2() ... positional... argument...
    """
    return (a, b)

def test_serialization3(a=1, /, b=2):
    """
    >>> pickled_defaults = pickle.dumps(test_serialization3)
    >>> unpickled_defaults = pickle.loads(pickled_defaults)
    >>> unpickled_defaults(1, 2)
    (1, 2)
    >>> unpickled_defaults(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_serialization3() got ... keyword argument... 'a'
    """
    return (a, b)


async def test_async(a=1, /, b=2):
    """
    >>> test_async(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_async() got ... keyword argument... 'a'
    """
    return a, b


def test_async_call(*args, **kwargs):
    """
    >>> test_async_call(1, 2)
    >>> test_async_call(1, b=2)
    >>> test_async_call(1)
    >>> test_async_call()
    """
    try:
        coro = test_async(*args, **kwargs)
        coro.send(None)
    except StopIteration as e:
        result = e.value
    assert result == (1, 2), result


def test_generator(a=1, /, b=2):
    """
    >>> test_generator(a=1, b=2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: test_generator() got ... keyword argument... 'a'
    >>> gen = test_generator(1, 2)
    >>> next(gen)
    (1, 2)
    >>> gen = test_generator(1, b=2)
    >>> next(gen)
    (1, 2)
    >>> gen = test_generator(1)
    >>> next(gen)
    (1, 2)
    >>> gen = test_generator()
    >>> next(gen)
    (1, 2)
    """
    yield a, b

def f_call_1_0_0(a,/):
    """
    >>> f_call_1_0_0(1)
    (1,)
    """
    return (a,)

def f_call_1_1_0(a, /, b):
    """
    >>> f_call_1_1_0(1,2)
    (1, 2)
    """
    return (a,b)

def f_call_1_1_1(a, /, b, *, c):
    """
    >>> f_call_1_1_1(1,2,c=3)
    (1, 2, 3)
    """
    return (a,b,c)

def f_call_1_1_1_star(a, /, b, *args, c):
    """
    >>> f_call_1_1_1_star(1,2,c=3)
    (1, 2, (), 3)
    >>> f_call_1_1_1_star(1,2,3,4,5,6,7,8,c=9)
    (1, 2, (3, 4, 5, 6, 7, 8), 9)
    """
    return (a,b,args,c)

def f_call_1_1_1_kwds(a, /, b, *, c, **kwds):
    """
    >>> f_call_1_1_1_kwds(1,2,c=3)
    (1, 2, 3, {})
    >>> f_call_1_1_1_kwds(1,2,c=3,d=4,e=5) == (1, 2, 3, {'d': 4, 'e': 5})
    True
    """
    return (a,b,c,kwds)

def f_call_1_1_1_star_kwds(a, /, b, *args, c, **kwds):
    """
    >>> f_call_1_1_1_star_kwds(1,2,c=3,d=4,e=5) == (1, 2, (), 3, {'d': 4, 'e': 5})
    True
    >>> f_call_1_1_1_star_kwds(1,2,3,4,c=5,d=6,e=7) == (1, 2, (3, 4), 5, {'d': 6, 'e': 7})
    True
    """
    return (a,b,args,c,kwds)

def f_call_one_optional_kwd(a, /, *, b=2):
    """
    >>> f_call_one_optional_kwd(1)
    (1, 2)
    >>> f_call_one_optional_kwd(1, b=3)
    (1, 3)
    """
    return (a,b)

def f_call_posonly_stararg(a, /, *args):
    """
    >>> f_call_posonly_stararg(1)
    (1, ())
    >>> f_call_posonly_stararg(1, 2, 3, 4)
    (1, (2, 3, 4))
    """
    return (a,args)

def f_call_posonly_kwarg(a, /, **kw):
    """
    >>> f_call_posonly_kwarg(1)
    (1, {})
    >>> all_args = f_call_posonly_kwarg(1, b=2, c=3, d=4)
    >>> all_args == (1, {'b': 2, 'c': 3, 'd': 4}) or all_args
    True
    """
    return (a,kw)

def f_call_posonly_stararg_kwarg(a, /, *args, **kw):
    """
    >>> f_call_posonly_stararg_kwarg(1)
    (1, (), {})
    >>> f_call_posonly_stararg_kwarg(1, 2)
    (1, (2,), {})
    >>> all_args = f_call_posonly_stararg_kwarg(1, b=3, c=4)
    >>> all_args == (1, (), {'b': 3, 'c': 4}) or all_args
    True
    >>> all_args = f_call_posonly_stararg_kwarg(1, 2, b=3, c=4)
    >>> all_args == (1, (2,), {'b': 3, 'c': 4}) or all_args
    True
    """
    return (a,args,kw)

def test_empty_kwargs(a, b, /):
    """
    >>> test_empty_kwargs(1, 2)
    (1, 2)
    >>> test_empty_kwargs(1, 2, **{})
    (1, 2)
    >>> test_empty_kwargs(1, 2, **{'c': 3})
    Traceback (most recent call last):
    TypeError: test_empty_kwargs() got an unexpected keyword argument 'c'
    """
    return (a,b)


@cython.cclass
class TestExtensionClass:
    """
    >>> t = TestExtensionClass()
    >>> t.f(1,2)
    (1, 2, 3)
    >>> t.f(1,2,4)
    (1, 2, 4)
    >>> t.f(1, 2, c=4)
    (1, 2, 4)
    >>> t.f(1, 2, 5, c=6)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...f() got multiple values for ...argument 'c'
    """
    def f(self, a, b, /, c=3):
        return (a,b,c)
