# mode: compile
# tag: pep492, await

# Need to include all utility code !

async def sleep(x):
    pass


async def call():
    await sleep(1)
    yield
