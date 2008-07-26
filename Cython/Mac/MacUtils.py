#
#   Pyrex -- Misc Mac-specific things
#

import os, MacOS, macfs

def open_new_file(path):
    # On the Mac, try to preserve Finder position
    # of previously existing file.
    fsspec = macfs.FSSpec(path)
    try:
        old_finfo = fsspec.GetFInfo()
    except MacOS.Error, e:
        #print "MacUtils.open_new_file:", e ###
        old_finfo = None
    try:
        os.unlink(path)
    except OSError:
        pass
    file = open(path, "w")
    new_finfo = fsspec.GetFInfo()
    if old_finfo:
        #print "MacUtils.open_new_file:", path ###
        #print "...old file info =", old_finfo.Creator, old_finfo.Type, old_finfo.Location ###
        #print "...new file info =", new_finfo.Creator, new_finfo.Type, new_finfo.Location ###
        new_finfo.Location = old_finfo.Location
        new_finfo.Flags = old_finfo.Flags
    # Make darn sure the type and creator are right. There seems
    # to be a bug in MacPython 2.2 that screws them up sometimes.
    new_finfo.Creator = "R*ch"
    new_finfo.Type = "TEXT"
    fsspec.SetFInfo(new_finfo)
    return file

