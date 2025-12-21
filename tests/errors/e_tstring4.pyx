# mode: error

# This is split into many sub-files because some errors terminate the parser

t'{x!}'
t'{x=!}'
t'{x!z}'        
t'{lambda:1}'       
t'{x:{;}}'
t'{1:d\n}'

_ERRORS = """
5:5: missing conversion character
6:6: missing conversion character
7:5: invalid conversion character 'z'
# TODO This message could probably be improved
8:9: Expected an identifier, found 'EOF'
8:9: Unrecognized character
"""
