# mode: error
# tag: pep492, async

async def foo():
    await

_ERRORS = """
5:9: Expected an identifier or literal
"""
