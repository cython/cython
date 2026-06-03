# mode: run
# tag: exceptions

import sys


__doc__ = u"""
>>> def test_py(outer_exc):
...   try:
...     raise AttributeError
...   except AttributeError:
...     print(sys.exc_info()[0] is AttributeError or sys.exc_info()[0])
...     try: raise KeyError
...     except:
...       print(sys.exc_info()[0] is KeyError or sys.exc_info()[0])
...       print(isinstance(sys.exc_info()[1].__context__, AttributeError)
...             or sys.exc_info()[1].__context__)
...     print((sys.exc_info()[0] is AttributeError) or
...           sys.exc_info()[0])
...   print((sys.exc_info()[0] is outer_exc) or
...         sys.exc_info()[0])

>>> print(sys.exc_info()[0]) # 0
None

>>> test_py(None)
True
True
True
True
True
>>> print(sys.exc_info()[0]) # test_py()
None

>>> test_c(None)
True
True
True
True
True
>>> print(sys.exc_info()[0]) # test_c()
None

>>> def test_py2():
...   try:
...     raise Exception
...   except Exception:
...     test_py(Exception)
...     print(sys.exc_info()[0] is Exception or sys.exc_info()[0])
...   print((sys.exc_info()[0] is None) or
...         sys.exc_info()[0])

>>> test_py2()
True
True
True
True
True
True
True
>>> print(sys.exc_info()[0]) # test_py2()
None

>>> test_c2()
True
True
True
True
True
True
True
>>> print(sys.exc_info()[0]) # test_c2()
None
"""


def test_c(outer_exc):
    try:
        raise AttributeError
    except AttributeError:
        print(sys.exc_info()[0] is AttributeError or sys.exc_info()[0])
        try: raise KeyError
        except:
            print(sys.exc_info()[0] is KeyError or sys.exc_info()[0])
            print(isinstance(sys.exc_info()[1].__context__, AttributeError)
                  or sys.exc_info()[1].__context__)
        print(sys.exc_info()[0] is AttributeError or sys.exc_info()[0])
    print(sys.exc_info()[0] is outer_exc or sys.exc_info()[0])


def test_c2():
    try:
        raise Exception
    except Exception:
        test_c(Exception)
        print(sys.exc_info()[0] is Exception or sys.exc_info()[0])
    print(sys.exc_info()[0] is None or sys.exc_info()[0])
