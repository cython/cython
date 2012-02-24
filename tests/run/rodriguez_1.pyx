__doc__ = u"""
    >>> b = B()
    >>> sorted(b.t.items())
    [(1, ((1, 2, 3),)), (2, (1, 2, 3))]
"""

class B:
    def __init__(self):
        self.t = {
            1 : (
                (1, 2, 3)
                ,
                )

            , 2 : ( 1, 2, 3)
            }
