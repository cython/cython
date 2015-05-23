# mode: error
# tag: pep492, async

async def foo():
    await await fut

_ERRORS = """
5:10: Expected an identifier or literal
"""
