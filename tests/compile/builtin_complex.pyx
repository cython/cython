# mode: compile
# tag: gh6860

# Make sure we generate the C complex type declarations
# even if the user code does not reference the type explicitly.

def c(x, y):
    return complex(x) / complex(y)
