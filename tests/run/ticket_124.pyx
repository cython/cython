__doc__ = u"""
>>> spam(dict(test=2))
False
"""
def spam(dict d):
    for elm in d:
        return False
    return True
