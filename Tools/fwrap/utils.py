import sys
import re

LEVEL = 0

def warning(message, position=None, level=0, stream=sys.stderr):
    if level < LEVEL:
        return
    # for now, echo on stream
    stream.write("warning: %s\n" % message)
    stream.flush()

mangle_prefix = 'fwrap_'
valid_name = re.compile(r'[a-z]\w+$',re.I).match

CY_IMPORT_ALIAS = "__wf"
