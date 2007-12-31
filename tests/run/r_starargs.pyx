__doc__ = """
    >>> swallow("Brian", 42)
    Name: Brian
    Airspeed: 42
    Extra args: ()
    Extra keywords: {}

    >>> swallow("Brian", 42, "African")
    Name: Brian
    Airspeed: 42
    Extra args: ('African',)
    Extra keywords: {}

    >>> swallow("Brian", airspeed = 42)
    Name: Brian
    Airspeed: 42
    Extra args: ()
    Extra keywords: {}

    >>> swallow("Brian", airspeed = 42, species = "African", coconuts = 3)
    Name: Brian
    Airspeed: 42
    Extra args: ()
    Extra keywords: {'coconuts': 3, 'species': 'African'}

    >>> swallow("Brian", 42, "African", coconuts = 3)
    Name: Brian
    Airspeed: 42
    Extra args: ('African',)
    Extra keywords: {'coconuts': 3}
"""

def swallow(name, airspeed, *args, **kwds):
    print "Name:", name
    print "Airspeed:", airspeed
    print "Extra args:", args
    print "Extra keywords:", kwds

