PYTHON?=python

clean:
	@echo Cleaning Source
	@rm -f *.pyc */*.pyc */*/*.pyc 
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@(cd Demos; $(MAKE) clean)

testclean:
	rm -fr BUILD

test:	testclean
	${PYTHON} runtests.py

test3:	testclean
	${PYTHON} runtests.py --no-cleanup
	python3.0 runtests.py --no-cython
