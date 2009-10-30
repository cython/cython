def swallow(name = None, airspeed = None, coconuts = None):
    """
    >>> swallow(name = "Brian")
    This swallow is called Brian
    >>> swallow(airspeed = 42)
    This swallow is flying at 42 furlongs per fortnight
    >>> swallow(coconuts = 3)
    This swallow is carrying 3 coconuts
    """
    if name is not None:
        print u"This swallow is called", name
    if airspeed is not None:
        print u"This swallow is flying at", airspeed, u"furlongs per fortnight"
    if coconuts is not None:
        print u"This swallow is carrying", coconuts, u"coconuts"
