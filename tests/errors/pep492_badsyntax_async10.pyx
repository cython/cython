# mode: error
# tag: pep492, async

async def genexpr(it):
    return (await x for x in it)


async def listcomp(it):
    return [await x for x in it]


async def setcomp(it):
    return {await x for x in it}


async def dictcomp(it):
    return {await x:x+1 for x in it}


# NOTE: CPython doesn't allow comprehensions either


_ERRORS = """
5:12: 'await' not allowed in generators (use 'yield')
5:12: 'await' not supported here
"""
