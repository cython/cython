VERSION = 0.9.6

version:
	@echo "Setting version to $(VERSION)"
	@echo "version = '$(VERSION)'" > Cython/Compiler/Version.py

clean:
	@echo Cleaning Source
	@rm -f *.pyc */*.pyc */*/*.pyc 
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@(cd Demos; $(MAKE) clean)
