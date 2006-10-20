#
#   Pyrex - Errors
#

import sys
from Pyrex.Utils import open_new_file


class PyrexError(Exception):
    pass


class CompileError(PyrexError):
    
    def __init__(self, position = None, message = ""):
        self.position = position
        self.message = message
        if position:
            pos_str = "%s:%d:%d: " % position
        else:
            pos_str = ""
        Exception.__init__(self, pos_str + message)


class InternalError(Exception):
    # If this is ever raised, there is a bug in the compiler.
    
    def __init__(self, message):
        Exception.__init__(self, "Internal compiler error: %s"
            % message)
            

listing_file = None
num_errors = 0
echo_file = None

def open_listing_file(path, echo_to_stderr = 1):
    # Begin a new error listing. If path is None, no file
    # is opened, the error counter is just reset.
    global listing_file, num_errors, echo_file
    if path is not None:
        listing_file = open_new_file(path)
    else:
        listing_file = None
    if echo_to_stderr:
        echo_file = sys.stderr
    else:
        echo_file = None
    num_errors = 0

def close_listing_file():
    global listing_file
    if listing_file:
        listing_file.close()
        listing_file = None

def error(position, message):
    #print "Errors.error:", repr(position), repr(message) ###
    global num_errors
    err = CompileError(position, message)
    line = "%s\n" % err
    if listing_file:
        listing_file.write(line)
    if echo_file:
        echo_file.write(line)
    num_errors = num_errors + 1
    return err
