# mode: compile
# tag: gh6865

# This used to lead to C compile errors due to an unfortunate ordering
# of the '.proto' sections of the Coroutine.c and Profile.c utility code.

async def main():
    await main()
