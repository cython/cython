# mode: error
# tag: werror

def simple_return():
    return
    print 'Where am I?'

def simple_loops(*args):
    for i in args:
        continue
        print 'Never be here'

    while True:
        break
        print 'Never be here'

def conditional(a, b):
    if a:
        return 1
    elif b:
        return 2
    else:
        return 3
    print 'oops'

def try_except():
    try:
        raise TypeError
    except ValueError:
        pass
    else:
        print 'unreachable'


_ERRORS = """
6:4: Unreachable code
11:8: Unreachable code
15:8: Unreachable code
24:4: Unreachable code
32:8: Unreachable code
"""
