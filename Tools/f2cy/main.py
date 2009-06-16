import os, sys
from fparser import api
from fparser import block_statements
from Visitor import PrintTree, KindResolutionVisitor, \
        AutoConfigGenerator, FortranWrapperGenerator, \
        CHeaderGenerator, PxdGenerator, CyHeaderGenerator

def setup_project(projectname, src_dir, outdir):
    fq_projdir = os.path.join(outdir, projectname)
    if os.path.isdir(fq_projdir):
        #XXX: make this more nuanced in the future.
        raise RuntimeError("Error, project directory %s already exists." % fq_projdir)
    os.mkdir(fq_projdir)
    return fq_projdir


def wrap(filenames, directory, outdir, projectname):

    projectname = projectname.lower().strip()

    projdir = setup_project(projectname, directory, outdir)

    print >>sys.stderr, "wrapping %s from %s in %s" % (filenames, directory, projdir)

    pipeline = [ KindResolutionVisitor(),
                 AutoConfigGenerator(projectname),
                 FortranWrapperGenerator(projectname),
                 CHeaderGenerator(projectname),
                 PxdGenerator(projectname),
                 CyHeaderGenerator(projectname)
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
        full_path = os.path.join(projdir, out_fname)
        fh = open(full_path, 'w')
        stage.copyto(fh)
        fh.close()
