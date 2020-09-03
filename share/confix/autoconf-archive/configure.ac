dnl Configure the Autoconf Macro Archive
dnl
dnl Copyright (c) 2006 by Peter Simons <simons@cryp.to>.
dnl Licensed under the terms of the GNU General Public License.

AC_INIT([autoconf-archive], [2006-08-20], [simons@cryp.to])
AM_INIT_AUTOMAKE([foreign dist-bzip2])
AC_CONFIG_SRCDIR([m4src/ac_cxx_explicit.m4])

AC_MSG_CHECKING([for available Autoconf macros])
M4SOURCE=""
for n in $srcdir/m4src/*.m4 ; do
  M4SOURCE="$M4SOURCE $n"
done
AC_SUBST([M4SOURCE])
AC_MSG_RESULT([done])

AC_MSG_CHECKING([for available documentation])
HTMLDOC=""
for n in $srcdir/htmldoc/*.html $srcdir/htmldoc/*.css ; do
  HTMLDOC="$HTMLDOC $n"
done
AC_SUBST([HTMLDOC])
AC_MSG_RESULT([done])

AM_CONDITIONAL([MAINTAINER], [test -e $srcdir/tools/genarchive.hs])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
