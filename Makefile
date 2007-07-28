VERSION = 0.9.4.1

version:
	@echo "Setting version to $(VERSION)"
	@echo "version = '$(VERSION)'" > Pyrex/Compiler/Version.py

#check_contents:
#	@if [ ! -d Pyrex/Distutils ]; then \
#		echo Pyrex/Distutils missing; \
#		exit 1; \
#	fi

clean:
	@echo Cleaning Source
	@rm -f *.pyc */*.pyc */*/*.pyc 
	@rm -f *~ */*~ */*/*~
	@rm -f core */core
	@(cd Demos; $(MAKE) clean)
