# mode: error
# tag: pep492, async

async def foo():
    async def foo(): await list()

_ERRORS = """
# ???  - this fails in CPython, not sure why ...
"""
