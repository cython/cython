all:
	python setup.py build_ext --inplace

test:	all
	python run_primes.py 20
	python run_numeric_demo.py
	python run_spam.py
	python integrate_timing.py
	cd callback; $(MAKE) test
	cd embed; $(MAKE) test

clean:
	@echo Cleaning Demos
	@rm -f *.c *.o *.so *~ core
	@rm -rf build
	@cd callback; $(MAKE) clean
	@cd embed; $(MAKE) clean
