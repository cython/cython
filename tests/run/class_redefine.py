class set:
    def __init__(self, x):
        self.x = x

SET = {1}

class set:
    def __init__(self, x):
        self.X = x

def test_class_redef(x):
    """
    >>> SET.x
    [1]
    >>> test_class_redef(2).X
    [2]
    """
    return {x}
