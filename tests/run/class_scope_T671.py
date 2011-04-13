# mode:run
# tag: class, scope
# ticket: 671

MAIN = True

class OuterScopeLookup(object):
    """
    >>> OuterScopeLookup.MAIN
    True
    """
    MAIN = MAIN  # looked up in parent scope, assigned to class scope
