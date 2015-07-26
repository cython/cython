all:
	python Setup.py build_ext --inplace

test:   all
	python run_mt_cheeses.py

clean:
	@echo Cleaning Demos/mt_callback
	@rm -f mt_cheeses.c mt_cheeses.h *.o *.so *~ core
	@rm -rf build

