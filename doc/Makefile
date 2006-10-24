BASEDOC = confix
EPS = prov-req.eps
PNG = prov-req.png

all: ps html
clean: dvi-clean ps-clean html-clean pdf-clean

dvi: $(BASEDOC).dvi
dvi-clean:
	-rm -f $(BASEDOC).dvi $(BASEDOC).log

ps: $(BASEDOC).ps 
ps-clean:
	-rm -f $(BASEDOC).ps

pdf: $(BASEDOC).pdf
pdf-clean:
	-rm -f $(BASEDOC).pdf

html: $(BASEDOC).html
html-clean:
	-rm -f $(BASEDOC).html

epydoc:
	epydoc --verbose --graph=all --docformat=restructuredtext -o epydoc ../libconfix/core ../libconfix/plugins ../libconfix/frontends
epydoc-clean:
	-rm -rf epydoc

$(BASEDOC).dvi: $(BASEDOC).texi $(EPS)
	texi2dvi --clean --texinfo=@setcontentsaftertitlepage --output=$@ $<

$(BASEDOC).pdf: $(BASEDOC).texi $(EPDF)
	texi2dvi --pdf --clean --texinfo=@setcontentsaftertitlepage --output=$@ $<

$(BASEDOC).ps: $(BASEDOC).dvi
	dvips -o $@ $<

$(BASEDOC).html: $(BASEDOC).texi $(PNG)
	makeinfo --number-sections --no-split --html $<

$(EPS): %.eps: %.fig
	fig2dev -L eps $< $@

$(EPDF): %.pdf: %.fig
	fig2dev -L pdf $< $@

$(PNG): %.png: %.fig
	fig2dev -L png $< $@

sf: sourceforge

sourceforge: all
	find .|												\
	grep -v \\.\$$|											\
	grep -v CVS|											\
	grep -v presentation|										\
	grep -v installation|										\
	tar -z -c -v -f - -T - |									\
	ssh `whoami`@shell.sourceforge.net '(cd /home/groups/c/co/confix/htdocs&&tar zxf -)'
