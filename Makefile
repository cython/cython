PYTHON?=python
REPO = git://github.com/cython/cython.git

all:    local 

local:
	${PYTHON} setup.py build_ext --inplace

.git: REV := $(shell cat .gitrev)
.git: TMPDIR := $(shell mktemp -d tmprepo.XXXXXX)
.git: 
	rm -rf $(TMPDIR)
	git clone $(REPO) $(TMPDIR)
	cd $(TMPDIR); git checkout -b working $(REV)
	mv $(TMPDIR)/.hgtags .
	mv $(TMPDIR)/.hgignore .
	mv $(TMPDIR)/.git .
	mv $(TMPDIR)/Doc/s5 Doc/s5
	rm -rf $(TMPDIR)

repo: .git


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
