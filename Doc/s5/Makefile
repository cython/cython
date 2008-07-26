
SLIDES=$(subst .txt,.html,$(wildcard *.txt))
SOURCES=$(subst .py,.c,$(subst .pyx,.c,$(wildcard */*.py */*.pyx)))

slides: $(SLIDES) $(SOURCES)

%.html: %.txt
	rst2s5 --current-slide --language=en $< $@

%.c: %.py
	cython --annotate $<

%.c: %.pyx
	cython --annotate $<

clean:
	rm -f *~ $(SLIDES) $(SOURCES) $(subst .c,.html,$(SOURCES))
