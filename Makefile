PYTHON?=python

clean:
	@echo Cleaning Source
	@rm -fr build
	@rm -f *.pyc */*.pyc */*/*.pyc 
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@(cd Demos; $(MAKE) clean)

testclean:
	rm -fr BUILD

test:	testclean
	${PYTHON} runtests.py -vv

test3:	testclean
	${PYTHON} runtests.py --no-cleanup
	python3.0 runtests.py -vv --no-cython

s5:
	$(MAKE) -C Doc/s5 slides
