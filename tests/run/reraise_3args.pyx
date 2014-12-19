
import sys


class MyError(Exception):
    def __init__(self, name, var):
        self.name = name
        self.var = var


def reraise_explicitly():
    """
    >>> try: reraise_explicitly()
    ... except MyError: print("RAISED!")
    ... else: print("NOT RAISED!")
    RAISED!
    """
    try:
        raise MyError('Oh no!', 42)
    except MyError:
        tmp = sys.exc_info()

    raise tmp[0], tmp[1], tmp[2]
