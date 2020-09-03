dnl @synopsis AX_EXTRA_DIST
dnl
dnl Allow support for custom dist targets.
dnl
dnl To add custom dist targets, you must create a dist-<TYPE> target
dnl within your Makefile.am, where <TYPE> is the name of the dist and
dnl then add <TYPE> to EXTRA_SRC_DISTS or EXTRA_BIN_DISTS. For example:
dnl
dnl    dist-foobar:
dnl    	<rules for making the foobar dist>
dnl
dnl    EXTRA_BIN_DISTS += foobar
dnl
dnl You can then build all the src dist targets by running:
dnl
dnl    make dist-src
dnl
dnl You can build all the binary dist targets by running:
dnl
dnl    make dist-bin
dnl
dnl and you can build both the src and dist targets by running:
dnl
dnl    make all-dist
dnl
dnl @category Automake
dnl @author Tom Howard <tomhoward@users.sf.net>
dnl @version 2005-01-14
dnl @license AllPermissive

AC_DEFUN([AX_EXTRA_DIST],
[
AC_MSG_NOTICE([adding custom dist support])
AM_CONDITIONAL(USING_AX_EXTRA_DIST, [true])
AX_ADD_AM_MACRO([[
EXTRA_SRC_DISTS =
EXTRA_BIN_DISTS =
dist-src-extra:
	@echo \"Making custom src targets...\"
	@cd \$(top_builddir); \\
	list='\$(EXTRA_SRC_DISTS)'; \\
	for dist in \$\$list; do \\
	    \$(MAKE) \$(AM_MAKEFLAGS) dist-\$\$dist; \\
	done

dist-src: dist-all dist-src-extra


dist-bin:
	@echo \"Making custom binary targets...\"
	@cd \$(top_builddir); \\
	list='\$(EXTRA_BIN_DISTS)'; \\
	for dist in \$\$list; do \\
	    \$(MAKE) \$(AM_MAKEFLAGS) dist-\$\$dist; \\
	done

all-dist dist2 dist-all2: dist-src dist-bin

all-dist-check dist2-check dist-all-check: dist-check dist-src-extra dist-bin
]])
])# AX_EXTRA_DIST
