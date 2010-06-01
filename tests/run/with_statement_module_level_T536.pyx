
__doc__ = """
>>> inner_result
['ENTER']
>>> result
['ENTER', 'EXIT (None, None, None)']
"""

result = []

class ContextManager(object):
    def __enter__(self):
        result.append("ENTER")
    def __exit__(self, *values):
        result.append("EXIT %r" % (values,))

with ContextManager() as c:
    inner_result = result[:]
