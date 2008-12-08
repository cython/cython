u"""
>>> try:
...     raise ValueError
... finally:
...     raise TypeError
Traceback (most recent call last):
TypeError
>>> finally_except()
Traceback (most recent call last):
TypeError

>>> def try_return_py():
...    try:
...        return 1
...    finally:
...        return 2
>>> try_return_py()
2
>>> try_return_cy()
2

>>> i=1
>>> for i in range(3):
...     try:
...         continue
...     finally:
...         i+=1
>>> i
3
>>> try_continue(3)
3
"""

def finally_except():
    try:
        raise ValueError
    finally:
        raise TypeError

def try_return_cy():
    try:
        return 1
    finally:
        return 2

def try_return_temp(a):
    b = a+2
    try:
        c = a+b
        return c
    finally:
        print b-a

def try_continue(a):
    i=1
    for i in range(a):
        try:
            continue
        finally:
            i+=1
    return i
