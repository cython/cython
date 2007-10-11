# July 2002, Graham Fawcett

#

# this hack was inspired by the way Thomas Heller got py2exe

# to appear as a distutil command

#

# we replace distutils.command.build_ext with our own version

# and keep the old one under the module name _build_ext,

# so that *our* build_ext can make use of it.



from build_ext import build_ext



