# mode: compile
# tag: warnings

print(x, y)
x = 10

_WARNINGS = """
1:0: Assignment in pxd file will not be executed. Suggest declaring as const
"""
