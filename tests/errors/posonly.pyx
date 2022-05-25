# mode: error
# tag: posonly

def f(a, b = 5, /, c):
    pass

def f(a = 5, b, /, c):
    pass

def f(a = 5, b, /):
    pass

def f(a, /, a):
    pass

def f(a, /, *, a):
    pass

#def f(a, b/2, c): #D
#    pass

#def f(*args, /): #D
#    pass

#def f(*args, a, /):
#    pass

#def f(**kwargs, /):
#    pass

#def f(/, a = 1): # D
#    pass

#def f(/, a):
#    pass

#def f(/):
#    pass

#def f(*, a, /):
#    pass

#def f(*, /, a):
#    pass

#def f(a, /, c, /):
#    pass

#def f(a, /, c, /, d):
#    pass

#def f(a, /, c, /, d, *, e):
#    pass

#def f(a, *, c, /, d, e):
#    pass

def test_invalid_syntax_lambda(self):
    lambda a, b = 5, /, c: None
    lambda a = 5, b, /, c: None
    lambda a = 5, b, /: None
    lambda a, /, a: None
    lambda a, /, *, a: None
#    lambda *args, /: None
#    lambda *args, a, /: None
#    lambda **kwargs, /: None
#    lambda /, a = 1: None
#    lambda /, a: None
#    lambda /: None
#    lambda *, a, /: None
#    lambda *, /, a: None

async def f(a, b = 5, /, c):
    pass

#def test_multiple_seps(a,/,b,/):
#    pass

_ERRORS = u"""
4:19: Non-default argument following default argument
7:13: Non-default argument following default argument
7:19: Non-default argument following default argument
10:13: Non-default argument following default argument
13:6: Previous declaration is here
13:12: 'a' redeclared
16:6: Previous declaration is here
16:15: 'a' redeclared
59:24: Non-default argument following default argument
60:18: Non-default argument following default argument
60:24: Non-default argument following default argument
61:18: Non-default argument following default argument
62:11: Previous declaration is here
62:17: 'a' redeclared
63:11: Previous declaration is here
63:20: 'a' redeclared
73:25: Non-default argument following default argument
"""





