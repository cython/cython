# mode: error

def test_non_existant():
    nonlocal no_such_name
    no_such_name = 1

def redef():
    x = 1
    def f():
        x = 2
        nonlocal x

global_name = 5

def ref_to_global():
    nonlocal global_name
    global_name = 6

def global_in_class_scope():
    class Test():
        nonlocal global_name
        global_name = 6

def redef_in_class_scope():
    x = 1
    class Test():
        x = 2
        nonlocal x


_ERRORS = u"""
 4:4: no binding for nonlocal 'no_such_name' found
10:8: Previous declaration is here
11:8: 'x' redeclared as nonlocal
16:4: no binding for nonlocal 'global_name' found
27:8: Previous declaration is here
28:8: 'x' redeclared as nonlocal
"""
