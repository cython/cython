# ticket: 536

__doc__ = """
>>> inner_result
['ENTER']
>>> result  # doctest: +ELLIPSIS
['ENTER', ...EXIT (<...ValueError...>,...ValueError..., <traceback object at ...)...]

>>> inner_result_no_exc
['ENTER']
>>> result_no_exc
['ENTER', 'EXIT (None, None, None)']
"""

class ContextManager(object):
    def __init__(self, result):
        self.result = result
    def __enter__(self):
        self.result.append("ENTER")
    def __exit__(self, *values):
        self.result.append("EXIT %r" % (values,))
        return True

result_no_exc = []

with ContextManager(result_no_exc) as c:
    inner_result_no_exc = result_no_exc[:]

result = []

with ContextManager(result) as c:
    inner_result = result[:]
    raise ValueError('TEST')
    
