import os, sys
from fparser import api
from fparser import block_statements
from Visitor import PrintTree, KindResolutionVisitor, \
        AutoConfigGenerator, FortranWrapperGenerator, \
        CHeaderGenerator, PxdGenerator, CyHeaderGenerator, \
        CyImplGenerator

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
                 CyHeaderGenerator(projectname),
                 CyImplGenerator(projectname)
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

    # write out the makefile
    gen_makefile(projectname, filenames, directory, projdir)

def gen_makefile(projname, src_files, src_dir, out_dir):
    import sys
    PYTHON = '/usr/bin/python2.6'
    PY_INC = '-I/usr/include/python2.6'
    CYTHON = '/home/ksmith/GSoC/gsoc-kurt/cython.py'
    SRCDIR = src_dir
    if len(src_files) != 1:
        raise RuntimeError("not set-up for multiple fortran source files, yet.")
    SRCFILE = src_files[0]
    FORTSRCBASE, FORTSRCEXT = os.path.splitext(SRCFILE)
    PROJECTNAME = projname
    fh = open(os.path.join(out_dir, 'Makefile'), 'w')
    fh.write(makefile_template % locals())

    fh.close()

makefile_template = '''
PYTHON=%(PYTHON)s
PY_INC=%(PY_INC)s
CYTHON=%(CYTHON)s

SRCDIR =%(SRCDIR)s

FORTSRCBASE = %(FORTSRCBASE)s
FORTSRCEXT = %(FORTSRCEXT)s

CONFIG = config
GENCONFIG = genconfig
PROJNAME = %(PROJECTNAME)s
FORTSOURCE = $(FORTSRCBASE)$(FORTSRCEXT)
FORTWRAP = $(PROJNAME)_fortran

FC = gfortran
FFLAGS = -g -Wall -fPIC
CFLAGS = -pthread -fno-strict-aliasing -g -fwrapv -Wall -Wstrict-prototypes -fPIC
LFLAGS = -pthread -shared -Wl,-Bsymbolic-functions -lgfortran
CC = gcc


#------------------------------------------------------------------------------
all: $(PROJNAME).so

%%.c : %%.pyx $(CONFIG).h
	@$(PYTHON) $(CYTHON) $<

$(FORTSRCBASE).o : $(SRCDIR)/$(FORTSOURCE)
	@$(FC) $(FFLAGS) -c $< -o $@

$(CONFIG).h : $(GENCONFIG).f95
	@$(FC) $< -o $(GENCONFIG)
	@./$(GENCONFIG)
	@rm $(GENCONFIG)

$(CONFIG).f95 : $(GENCONFIG).f95
	@$(FC) $< -o $(GENCONFIG)
	@./$(GENCONFIG)
	@rm $(GENCONFIG)

$(CONFIG).o : $(CONFIG).f95
	@$(FC) $(FFLAGS) -c $< -o $@

$(FORTWRAP).o : $(FORTWRAP).f95 $(CONFIG).o
	@$(FC) $(FFLAGS) -c $< -o $@

$(PROJNAME).o : $(PROJNAME).c
	@$(CC) $(CFLAGS) $(PY_INC) -c $< -o $@

$(PROJNAME).so : $(PROJNAME).o $(FORTWRAP).o $(FORTSRCBASE).o $(PROJNAME).o
	@$(CC) $(LFLAGS) $? -o $@

clean:
	@rm *.o *.so *.c *.mod
'''
