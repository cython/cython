__doc__ = u"""
  >>> s = Swallow("Brian", 42)
  Name: Brian
  Airspeed: 42
  Extra args: ()
  Extra keywords: []

  >>> s = Swallow("Brian", 42, "African")
  Name: Brian
  Airspeed: 42
  Extra args: ('African',)
  Extra keywords: []

  >>> s = Swallow("Brian", airspeed = 42)
  Name: Brian
  Airspeed: 42
  Extra args: ()
  Extra keywords: []

  >>> s = Swallow("Brian", airspeed = 42, species = "African", coconuts = 3)
  Name: Brian
  Airspeed: 42
  Extra args: ()
  Extra keywords: [('coconuts', 3), ('species', 'African')]

  >>> s = Swallow("Brian", 42, "African", coconuts = 3)
  Name: Brian
  Airspeed: 42
  Extra args: ('African',)
  Extra keywords: [('coconuts', 3)]
"""

cdef class Swallow:

    def __init__(self, name, airspeed, *args, **kwds):
        print u"Name:", name
        print u"Airspeed:", airspeed
        print u"Extra args:", args
        print u"Extra keywords:", sorted(kwds.items())
