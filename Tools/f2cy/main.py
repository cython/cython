import os, sys
from fparser import api
from fparser import block_statements
from Visitor import PrintTree, KindResolutionVisitor, \
        AutoConfigGenerator, FortranWrapperGenerator, \
        CHeaderGenerator

def wrap(filenames, directory, outdir, projectname):
    print >>sys.stderr, "wrapping %s from %s in %s" % (filenames, directory, outdir)
    projectname = projectname.lower().strip()
    pipeline = [ KindResolutionVisitor(),
                 AutoConfigGenerator(projectname),
                 FortranWrapperGenerator(projectname),
                 CHeaderGenerator(projectname)
               ]

    for fname in filenames:
        block = api.parse(os.path.join(directory, fname), analyze=True)
        for stage in pipeline:
            stage(block) # assumes no transformations to the parse tree.

    # write out the files.
    for stage in pipeline:
        if not stage.is_generator:
            continue
        out_fname = stage.make_fname(projectname)
        full_path = os.path.join(outdir, out_fname)
        fh = open(full_path, 'w')
        stage.copyto(fh)
        fh.close()
