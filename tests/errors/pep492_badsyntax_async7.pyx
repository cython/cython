# mode: error
# tag: pep492, async

async def foo():
    yield from []

_ERRORS = """
5:4: 'yield from' not supported here
"""
