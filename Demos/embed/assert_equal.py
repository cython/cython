import sys
if open(sys.argv[1]).read() != open(sys.argv[2]).read():
    print "Files differ"
    sys.exit(1)
else:
    print "Files identical"
