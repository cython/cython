from __future__ import with_statement

__doc__ = u"""
>>> no_as()
enter
hello
exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
>>> basic()
enter
value
exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
>>> with_exception(None)
enter
value
exit <type 'type'> <class 'withstat.MyException'> <type 'traceback'>
outer except
>>> with_exception(True)
enter
value
exit <type 'type'> <class 'withstat.MyException'> <type 'traceback'>
>>> multitarget()
enter
1 2 3 4 5
exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
>>> tupletarget()
enter
(1, 2, (3, (4, 5)))
exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
>>> typed()
enter
10
exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
"""

class MyException(Exception):
    pass

class ContextManager:
    def __init__(self, value, exit_ret = None):
        self.value = value
        self.exit_ret = exit_ret

    def __exit__(self, a, b, tb):
        print "exit", type(a), type(b), type(tb)
        return self.exit_ret
        
    def __enter__(self):
        print "enter"
        return self.value

def no_as():
    with ContextManager("value"):
        print "hello"
        
def basic():
    with ContextManager("value") as x:
        print x

def with_exception(exit_ret):
    try:
        with ContextManager("value", exit_ret=exit_ret) as value:
            print value
            raise MyException()
    except:
        print "outer except"

def multitarget():
    with ContextManager((1, 2, (3, (4, 5)))) as (a, b, (c, (d, e))):
        print a, b, c, d, e

def tupletarget():
    with ContextManager((1, 2, (3, (4, 5)))) as t:
        print t

def typed():
    cdef unsigned char i
    c = ContextManager(255)
    with c as i:
        i += 11
        print i
