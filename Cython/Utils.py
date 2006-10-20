#
#   Pyrex -- Things that don't belong
#            anywhere else in particular
#

import os, sys

def replace_suffix(path, newsuf):
    base, _ = os.path.splitext(path)
    return base + newsuf

def open_new_file(path):
    #  Open and truncate existing file to
    #  preserve metadata on the Mac.
    return open(path, "w+")

