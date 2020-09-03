# Build the Autoconf Macro Archive

SGMLNORMALIZE	= osgmlnorm --dtd
TIDY            = tidy -quiet --indent yes --indent-spaces 1	\
			--write-back yes --tidy-mark no     	\
			-wrap 80 --hide-comments yes

CLEANFILES	= $(DIST_ARCHIVES) dist/macros-by-category.inc
DISTCLEANFILES	= tools/genarchive tools/htmlredirect
MAINTAINERCLEANFILES = missing install-sh configure Makefile.in aclocal.m4

.PHONY:		generate redate publish

generate:	clean htmldoc/index.html htmldoc/ac-archive.css htmldoc/notfound.html
	@echo Generating Archive ...
	@$(MAKE) -s MAKEFLAGS= -C tools genarchive
	@tools/genarchive $(M4SOURCE)
	@$(SGMLNORMALIZE) dist/macros-by-category.html >htmldoc/macros-by-category.html

	@echo Pretty-printing HTML files ...
	@for n in `find htmldoc -name '*.html'`; do $(TIDY) $$n; done

	@echo Reconfigure Build System
	@./config.status --recheck

redate:
	@redate configure.ac README

publish:	dist
	cp $(distdir).tar.bz2 htmldoc/
	rsync -va htmldoc/ \
	  /usr/local/apache/htdocs/cryp.to/autoconf-archive/

htmldoc/index.html:	README
	lhs2html README
	@mv README.html $@
	@-$(TIDY) $@

htmldoc/%:	dist/%
	cp -p $< $@
