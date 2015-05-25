# mode: error
# tag: pep492, async

async def foo():
    yield

_ERRORS = """
5:4: 'yield' not allowed in async coroutines (use 'await')
5:4: 'yield' not supported here
"""
