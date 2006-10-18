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
	epydoc -o epydoc ../libconfix/*.py
epydoc-clean:
	-rm -rf epydoc

optmod.ps: optmod.dot
	dot -Tps -Gpage=8.27,11.7 -Gsize=8.27,11.7 -Gconcentrate=true -Gratio=fill -Gmargin=0 -Gcenter=true $< -o $@

optmod.gif: optmod.dot
	dot -Tgif -Gsize=8.27,11.7 -Gconcentrate=true -Gratio=fill -Gmargin=0 -Gcenter=true $< -o $@

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
