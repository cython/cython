# mode: error
# tag: pep492, async

async def foo():
    def foo(a:await list()):
        pass

_ERRORS = """
5:14: 'await' not supported here
5:14: 'await' not supported here
"""
