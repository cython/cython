# mode: run

import cython

# Unsuitable for the Limited API because it involves inheriting from (opaque) builins.

@cython.cclass
class MyDict(dict):
    pass

# Note that list is defined as an extern extension type in the pxd file
@cython.cclass
class MyList(list):
    pass

def test_match_dict(x):
    """
    >>> test_match_dict(None)
    no match
    >>> test_match_dict({})
    case dict: {}
    >>> test_match_dict(MyDict())
    case mydict: {}
    """
    match x:
        case MyDict(value):
            print(f"case mydict: {value}")
        case dict(value):
            print(f"case dict: {value}")
        case _:
            print("no match")

def test_match_list(x):
    """
    >>> test_match_list(None)
    no match
    >>> test_match_list([])
    case list: []
    >>> test_match_list(MyList())
    case mylist: []
    """
    match x:
        case MyList(value):
            print(f"case mylist: {value}")
        case list(value):  # noting that it's an extern extension type
            print(f"case list: {value}")
        case _:
            print("no match")
