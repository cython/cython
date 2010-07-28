PYTHON?=python
REPO = http://hg.cython.org/cython-devel

all:    local 

local:
	${PYTHON} setup.py build_ext --inplace

.hg: REV := $(shell cat .hgrev)
.hg: TMPDIR := $(shell mktemp -d tmprepo.XXXXXX)
.hg: 
	hg clone --rev $(REV) $(REPO) $(TMPDIR)
	hg -R $(TMPDIR) update
	mv $(TMPDIR)/.hg .
	mv $(TMPDIR)/.hgignore .
	mv $(TMPDIR)/.hgtags .
	rm -rf $(TMPDIR)

repo: .hg


clean:
	@echo Cleaning Source
	@rm -fr build
	@rm -f *.py[co] */*.py[co] */*/*.py[co] */*/*/*.py[co]
	@rm -f *.so */*.so */*/*.so 
	@rm -f *.pyd */*.pyd */*/*.pyd 
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@rm -f Cython/Compiler/*.c
	@rm -f Cython/Plex/*.c
	@rm -f Cython/Runtime/refnanny.c
	@(cd Demos; $(MAKE) clean)

testclean:
	rm -fr BUILD

test:	testclean
	${PYTHON} runtests.py -vv

s5:
	$(MAKE) -C Doc/s5 slides
