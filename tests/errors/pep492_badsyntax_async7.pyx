# mode: error
# tag: pep492, async

async def foo():
    yield from []

_ERRORS = """
5:4: 'yield from' not supported here
5:4: 'yield' not allowed in async coroutines (use 'await')
"""
