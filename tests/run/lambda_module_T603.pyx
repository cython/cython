# mode: run
# tag: lambda
# ticket: t603

# Module scope lambda functions

__doc__ = """
>>> pow2(16)
256
>>> with_closure(0)
0
>>> typed_lambda(1)(2)
3
>>> typed_lambda(1.5)(1.5)
2
>>> cdef_const_lambda()
123
>>> const_lambda()
321
"""

pow2 = lambda x: x * x
with_closure = lambda x:(lambda: x)()
typed_lambda = lambda int x : (lambda int y: x + y)

cdef int xxx = 123
cdef_const_lambda = lambda: xxx

yyy = 321
const_lambda = lambda: yyy
