# mode: error
# tag: pep492, async

async def foo():
    [i async for i in els]

_ERRORS = """
5:7: Expected ']', found 'async'
"""
