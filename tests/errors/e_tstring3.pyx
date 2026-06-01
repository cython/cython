# mode: error

# This is split into many sub-files because some errors terminate the parser

t'{:x}'
t'{x;y}'
t'{x=y}'
t'{x!s!}'
t'{x!s:'

_ERRORS = """
5:2: empty expression not allowed in t-string
6:4: Unexpected characters after t-string expression: ;
7:5: Unexpected characters after t-string expression: y
8:6: Unexpected characters after t-string expression: !
# TODO This message could probably be improved
9:7: Expected '}', found 'END_FT_STRING'
"""
