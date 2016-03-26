all:
	python setup.py build_ext --inplace

test:	all
	python run_primes.py 20
	python run_numeric_demo.py
	python run_spam.py
	cd callback; $(MAKE) test
	cd embed; $(MAKE) test
	#
	# longer running
	#python integrate_timing.py
	# also  run
	# python setup.py build_ext --inplace in
	#  benchmarks to build benchmarks
	# python setup.py build_ext --inplace in libraries then
	# python -c 'import call_mymath;print(call_mymath.call_sinc(1))'
	#
	# embed and freeze are working for python2 but not python3
	#
	#
clean:
	@echo Cleaning Demos
	@rm -f *.c *.o *.so *~ core
	@rm -rf build
	@cd callback; $(MAKE) clean
	@cd embed; $(MAKE) clean
