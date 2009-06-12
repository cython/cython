import os, sys
from fparser import api
from fparser import block_statements
from Visitor import PrintTree, KindResolutionVisitor, \
        AutoConfigGenerator, FortranWrapperGenerator, \
        CHeaderGenerator

def wrap(filename, directory, workdir):
    print >>sys.stderr, "wrapping %s from %s in %s" % (filename, directory, workdir)
    block = api.parse(os.path.join(directory, filename), analyze=True)
    KindResolutionVisitor()(block)
    AutoConfigGenerator()(block, open('%s_autoconf.f95'%filename.split('.')[0],'w'))
    FortranWrapperGenerator()(block, open('%s_wrapper.f95'%filename.split('.')[0],'w'))
    CHeaderGenerator()(block, open('%s_wrapper.h'%filename.split('.')[0],'w'))

