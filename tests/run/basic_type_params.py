# mode: run
# tag: pure3.13, warnings

# This is just to check that our minimal implementation of typeparams
# produces usable functions and classes.  Beyond that, they don't do
# anything and aren't expected to do anything

import cython

type MyTypeVar[T] = list[T]

# Cython will produce an evaluateable variable for MyTypeVar
# (abeit set to None) and this pointless-looking assert is just to check that.
assert isinstance(MyTypeVar, object)

class C1[T]:
    """
    >>> C1()  # doctest: +ELLIPSIS
    <basic_type_params.C1 object at ...>
    """
    pass

class C2[T: int]:
    """
    >>> C2()  # doctest: +ELLIPSIS
    <basic_type_params.C2 object at ...>
    """
    pass

class C3[T=int]:
    """
    >>> C3()  # doctest: +ELLIPSIS
    <basic_type_params.C3 object at ...>
    """
    pass

class C4[*T]:
    """
    >>> C4()  # doctest: +ELLIPSIS
    <basic_type_params.C4 object at ...>
    """
    pass

class C5[**T]:
    """
    >>> C5()  # doctest: +ELLIPSIS
    <basic_type_params.C5 object at ...>
    """
    pass

class C6[T](list):
    """
    >>> C6()
    []
    """
    pass

@cython.cclass
class CC[T]:
    """
    >>> CC()  # doctest: +ELLIPSIS
    <basic_type_params.CC object at ...>
    """
    pass

def f1[T]():
    """
    >>> f1()
    hello from f1
    """
    print("hello from f1")

def f2[T: int]():
    """
    >>> f2()
    hello from f2
    """
    print("hello from f2")

def f3[T = int](x):
    """
    >>> f3(None)
    hello from f3
    """
    print("hello from f3")

def f4[*T]():
    """
    >>> f4()
    hello from f4
    """
    print("hello from f4")

def f5[**T](x, y):
    """
    >>> f5(1, 2)
    hello from f5
    """
    print("hello from f5")

@cython.cfunc
def cf[T](a):
    print("hello from cf")

def call_cf(a):
    """
    >>> call_cf(1)
    hello from cf
    """
    return cf(a)

@cython.ccall
def cpf[T]():
    """
    >>> cpf()
    hello from cpf
    """
    print("hello from cpf")

def genexpr_allowed_in_args[T](x=tuple(i for i in range(3))):
    """
    >>> genexpr_allowed_in_args()
    (0, 1, 2)
    """
    return x

type GenexprAllowedInTypeVar = tuple(x for x in (int,))

def genexpr_allowed_in_bound[T: tuple(x for x in (int,))](x: T):
    """
    >>> genexpr_allowed_in_bound(1)
    1
    """
    return x

def yield_allowed_in_lambda[T](x: (lambda: (yield)) = 1):
    """
    >>> yield_allowed_in_lambda()
    1
    """
    return x

def named_expression_allowed_in_default(x=(y := 1)):
    """
    >>> named_expression_allowed_in_default()
    1
    >>> y
    1
    """
    return x

def trailing_comma[T,](x: T) -> T:
    return x

class TrailingComma[T,]:
    pass

type TrailingTypeVarComma[T,] = list[T]

type TrailingTypeVarNewline = int; z = 1

_WARNINGS = """
10:0: Type aliases are currently ignored by Cython. This will be replaced with 'MyTypeVar = None'.
16:9: Type parameters are currently completely ignored by Cython.
23:9: Type parameters are currently completely ignored by Cython.
30:9: Type parameters are currently completely ignored by Cython.
37:10: Type parameters are currently completely ignored by Cython.
44:11: Type parameters are currently completely ignored by Cython.
51:9: Type parameters are currently completely ignored by Cython.
59:9: Type parameters are currently completely ignored by Cython. 'cclass' extension types are unlikely to use them meaningfully in future.
66:7: Type parameters are currently completely ignored by Cython.
73:7: Type parameters are currently completely ignored by Cython.
80:7: Type parameters are currently completely ignored by Cython.
87:8: Type parameters are currently completely ignored by Cython.
94:9: Type parameters are currently completely ignored by Cython.
102:7: Type parameters are currently completely ignored by Cython. 'cfunc' functions are unlikely to use them meaningfully in future.
113:8: Type parameters are currently completely ignored by Cython. 'ccall' functions are unlikely to use them meaningfully in future.
120:28: Type parameters are currently completely ignored by Cython.
127:0: Type aliases are currently ignored by Cython. This will be replaced with 'GenexprAllowedInTypeVar = None'.
129:29: Type parameters are currently completely ignored by Cython.
129:61: Unknown type declaration 'T' in annotation, ignoring
136:28: Type parameters are currently completely ignored by Cython.
136:35: Failed to convert lambda to string representation in annotation
136:35: Unknown type declaration in annotation, ignoring
152:19: Type parameters are currently completely ignored by Cython.
152:26: Unknown type declaration 'T' in annotation, ignoring
152:32: Unknown type declaration 'T' in annotation, ignoring
155:20: Type parameters are currently completely ignored by Cython.
158:0: Type aliases are currently ignored by Cython. This will be replaced with 'TrailingTypeVarComma = None'.
160:0: Type aliases are currently ignored by Cython. This will be replaced with 'TrailingTypeVarNewline = None'.

# Spurious
112:0: 'cpf' redeclared
"""
