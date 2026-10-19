# mode: error

# This is split into many sub-files because some errors terminate the parser

t'}'
t'{}'
t'{=x}'

_ERRORS = """
5:2: f-string or t-string: single '}' is not allowed
6:2: empty expression not allowed in t-string
7:3: Expected an identifier or literal
"""
