# mode: error
# tag: werror, unreachable, control-flow

def try_finally():
    try:
        return
    finally:
        return
    print 'oops'

def try_return():
    try:
        return
    except:
        return
    print 'oops'

def for_return(a):
    for i in a:
        return
    else:
        return
    print 'oops'

def while_return(a):
    while a:
        return
    else:
        return
    print 'oops'

def forfrom_return(a):
    for i from 0 <= i <= a:
        return
    else:
        return
    print 'oops'

_ERRORS = """
9:4: Unreachable code
16:4: Unreachable code
23:4: Unreachable code
30:4: Unreachable code
37:4: Unreachable code
"""
