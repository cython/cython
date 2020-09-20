PACKAGENAME=Cython
PYTHON?=python
TESTOPTS?=
REPO = git://github.com/cython/cython.git
VERSION?=$(shell sed -ne 's|^__version__\s*=\s*"\([^"]*\)".*|\1|p' Cython/Shadow.py)
PARALLEL?=$(shell ${PYTHON} -c 'import sys; print("-j5" if sys.version_info >= (3,5) else "")' || true)

MANYLINUX_IMAGE_X86_64=quay.io/pypa/manylinux2010_x86_64
MANYLINUX_IMAGE_686=quay.io/pypa/manylinux2010_i686

all:    local

local:
	${PYTHON} setup.py build_ext --inplace $(PARALLEL)

plocal:
	${PYTHON} setup.py build_ext --inplace --cython-profile $(PARALLEL)

sdist: dist/$(PACKAGENAME)-$(VERSION).tar.gz

dist/$(PACKAGENAME)-$(VERSION).tar.gz:
	$(PYTHON) setup.py sdist

pywheel: dist/$(PACKAGENAME)-$(VERSION)-py2.py3-none-any.whl

dist/$(PACKAGENAME)-$(VERSION)-py2.py3-none-any.whl:
	${PYTHON} setup.py bdist_wheel --no-cython-compile --universal
	[ -f "$@" ]  # check that we generated the expected universal wheel

TMPDIR = .repo_tmp
.git: .gitrev
	rm -rf $(TMPDIR)
	git clone -n $(REPO) $(TMPDIR)
	cd $(TMPDIR) && git reset -q "$(shell cat .gitrev)"
	mv $(TMPDIR)/.git .
	rm -rf $(TMPDIR)
	git ls-files -d | xargs git checkout --

# Create a git repo from an unpacked source directory.
repo: .git


clean:
	@echo Cleaning Source
	@rm -fr build
	@rm -f *.py[co] */*.py[co] */*/*.py[co] */*/*/*.py[co]
	@rm -f *.so */*.so */*/*.so
	@rm -f *.pyd */*.pyd */*/*.pyd
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@rm -f Cython/*.c
	@rm -f Cython/Compiler/*.c
	@rm -f Cython/Plex/*.c
	@rm -f Cython/Tempita/*.c
	@rm -f Cython/Runtime/refnanny.c
	@(cd Demos; $(MAKE) clean)

testclean:
	rm -fr BUILD TEST_TMP

test:	testclean
	${PYTHON} runtests.py -vv ${TESTOPTS}

checks:
	${PYTHON} runtests.py -vv --no-unit --no-doctest --no-file --no-pyregr --no-examples

s5:
	$(MAKE) -C Doc/s5 slides

wheel_manylinux: wheel_manylinux64 wheel_manylinux32

wheel_manylinux32 wheel_manylinux64: dist/$(PACKAGENAME)-$(VERSION).tar.gz
	echo "Building wheels for $(PACKAGENAME) $(VERSION)"
	mkdir -p wheelhouse_$(subst wheel_,,$@)
	time docker run --rm -t \
		-v $(shell pwd):/io \
		-e CFLAGS="-O3 -g0 -mtune=generic -pipe -fPIC" \
		-e LDFLAGS="$(LDFLAGS) -fPIC" \
		-e WHEELHOUSE=wheelhouse_$(subst wheel_,,$@) \
		$(if $(patsubst %32,,$@),$(MANYLINUX_IMAGE_X86_64),$(MANYLINUX_IMAGE_686)) \
		bash -c 'for PYBIN in /opt/python/*/bin; do \
		    $$PYBIN/python -V; \
		    { $$PYBIN/pip wheel -w /io/$$WHEELHOUSE /io/$< & } ; \
		    done; wait; \
		    for whl in /io/$$WHEELHOUSE/$(PACKAGENAME)-$(VERSION)-*-linux_*.whl; do auditwheel repair $$whl -w /io/$$WHEELHOUSE; done'
