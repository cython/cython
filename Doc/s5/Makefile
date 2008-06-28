
SLIDES=$(subst .txt,.html,$(wildcard *.txt))

all: slides

slides: $(SLIDES)

%.html: %.txt
	rst2s5 --current-slide --language=en $< $@

clean:
	rm -f *~ $(SLIDES)
