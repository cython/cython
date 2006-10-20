#
#   Simple Apple-event driven Python interpreter
#

import os, sys, traceback
from cStringIO import StringIO
from MiniAEFrame import AEServer, MiniApplication

class PythonServer(AEServer, MiniApplication):
    
    def __init__(self):
        MiniApplication.__init__(self)
        AEServer.__init__(self)
        self.installaehandler('aevt', 'oapp', ignore)
        self.installaehandler('aevt', 'quit', quit)
        self.installaehandler('misc', 'dosc', doscript)


def ignore(**kwds):
    pass

def quit(**kwds):
    server._quit()

def doscript(args, **kwds):
    print "doscript:", repr(args) ###
    stat = 0
    output = ""
    errput = ""
    #print "Normalising args" ###
    if type(args) == type(""):
        args = [args]
    #print "Setting sys.argv" ###
    sys.argv = args
    #print "Finding script directory and module file" ###
    dir = os.path.dirname(args[0])
    dir = os.path.join(start_dir, dir)
    pyfile = os.path.basename(args[0])
    mod = os.path.splitext(pyfile)[0]
    #print "dir:", repr(dir) ###
    #print "mod:", repr(mod) ###
    os.chdir(dir)
    sys.path = start_path[:]
    sys.path[0] = dir
    #print "path:", sys.path ###
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        try:
            #sys.__stdout__.write("Path: %s\n" % sys.path) ###
            #sys.__stdout__.write("Importing: %s\n" % mod) ###
            try:
                __import__(mod)
            except KeyboardInterrupt:
                raise
            except SystemExit, exc:
                #sys.__stdout__.write("Caught a SystemExit\n") ###
                try:
                    stat = int(str(exc))
                except ValueError:
                    stat = 1
                #sys.__stdout__.write("stat = %s\n" % stat) ###
            except:
                traceback.print_exc()
                stat = 1
            #sys.__stdout__.write("Done the import\n") ###
        finally:
            output = sys.stdout.getvalue()
            #sys.__stdout__.write("Output:\n%s" % output) ###
            errput = sys.stderr.getvalue()
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stdout__
        pass
    return [stat, output, errput]

start_dir = os.getcwd()
start_path = sys.path[:]
server = PythonServer()
#print "Open for business"
try:
    server.mainloop()
except:
    traceback.print_exc()
    #sys.exit(1)
#print "Closing shop"
