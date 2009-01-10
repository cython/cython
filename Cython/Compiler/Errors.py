#
#   Pyrex - Errors
#

import sys
from Cython.Utils import open_new_file


class PyrexError(Exception):
    pass

class PyrexWarning(Exception):
    pass


def context(position):
    source = position[0]
    assert not (isinstance(source, unicode) or isinstance(source, str)), (
        "Please replace filename strings with Scanning.FileSourceDescriptor instances %r" % source)
    try:
        F = list(source.get_lines())
    except UnicodeDecodeError:
        # file has an encoding problem
        s = "[unprintable code]\n"
    else:
        s =''.join(F[max(0, position[1]-6):position[1]])
        s = '...\n' + s + ' '*(position[2]-1) + '^\n'
    s = '-'*60 + '\n' + s + '-'*60 + '\n'
    return s
    
class CompileError(PyrexError):
    
    def __init__(self, position = None, message = ""):
        self.position = position
        self.message_only = message
        self.reported = False
    # Deprecated and withdrawn in 2.6:
    #   self.message = message
        if position:
            pos_str = "%s:%d:%d: " % (position[0].get_description(), position[1], position[2])
            cont = context(position)
        else:
            pos_str = ""
            cont = ''
        Exception.__init__(self, '\nError converting Pyrex file to C:\n' + cont + '\n' + pos_str + message )

class CompileWarning(PyrexWarning):
    
    def __init__(self, position = None, message = ""):
        self.position = position
    # Deprecated and withdrawn in 2.6:
    #   self.message = message
        if position:
            pos_str = "%s:%d:%d: " % (position[0].get_description(), position[1], position[2])
        else:
            pos_str = ""
        Exception.__init__(self, pos_str + message)


class InternalError(Exception):
    # If this is ever raised, there is a bug in the compiler.
    
    def __init__(self, message):
        Exception.__init__(self, "Internal compiler error: %s"
            % message)


class CompilerCrash(CompileError):
    # raised when an unexpected exception occurs in a transform
    def __init__(self, pos, context, message, cause, stacktrace=None):
        if message:
            message = u'\n' + message
        else:
            message = u'\n'
        if context:
            message = "Compiler crash in " + context + message
        if stacktrace:
            import traceback
            message += (
                u'\n\nCompiler crash traceback from this point on:\n' +
                u''.join(traceback.format_tb(stacktrace)))
        if cause:
            if not stacktrace:
                message += u'\n'
            message += u'%s: %s' % (cause.__class__.__name__, cause)
        CompileError.__init__(self, pos, message)


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

def report_error(err):
    if error_stack:
        error_stack[-1].append(err)
    else:
        global num_errors
        # See Main.py for why dual reporting occurs. Quick fix for now.
        if err.reported: return
        err.reported = True
        line = "%s\n" % err
        if listing_file:
            listing_file.write(line)
        if echo_file:
            echo_file.write(line)
        num_errors = num_errors + 1

def error(position, message):
    #print "Errors.error:", repr(position), repr(message) ###
    err = CompileError(position, message)
    #if position is not None: raise Exception(err) # debug
    report_error(err)
    return err

LEVEL=1 # warn about all errors level 1 or higher

def warning(position, message, level=0):
    if level < LEVEL:
        return
    warn = CompileWarning(position, message)
    line = "warning: %s\n" % warn
    if listing_file:
        listing_file.write(line)
    if echo_file:
        echo_file.write(line)
    return warn

# These functions can be used to momentarily suppress errors. 

error_stack = []

def hold_errors():
    error_stack.append([])

def release_errors(ignore=False):
    held_errors = error_stack.pop()
    if not ignore:
        for err in held_errors:
            report_error(err)

def held_errors():
    return error_stack[-1]
