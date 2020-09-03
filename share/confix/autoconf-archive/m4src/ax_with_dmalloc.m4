dnl @synopsis AX_WITH_DMALLOC
dnl
dnl @summary Enable/disable dmalloc library support.
dnl
dnl Let the user enable/disable support for the dmalloc library
dnl available from <http://www.dmalloc.org/>.
dnl
dnl The macro adds the command-line flag "--with-dmalloc". Furthermore,
dnl "-IPREFIX/include" will be added to "$CPPFLAGS", "-LPREFIX/lib" to
dnl "$LDFLAGS", and "-DDEBUG_DMALLOC" and "-DDMALLOC_FUNC_CHECK" to
dnl "$CPPFLAGS".
dnl
dnl To enable dmalloc support in your code, add the following snippet
dnl to your header files:
dnl
dnl   #ifdef DEBUG_DMALLOC
dnl   #  include <dmalloc.h>
dnl   #endif
dnl
dnl @category InstalledPackages
dnl @author Peter Simons <simons@cryp.to>
dnl @version 2006-01-15
dnl @license AllPermissive

AC_DEFUN([AX_WITH_DMALLOC], [
AC_MSG_CHECKING(whether to use the dmalloc library)
AC_ARG_WITH(dmalloc,
[  --with-dmalloc[=PREFIX]  Compile with dmalloc library],
if test "$withval" = "" -o "$withval" = "yes"; then
    ac_cv_dmalloc="/usr/local"
else
    ac_cv_dmalloc="$withval"
fi
AC_MSG_RESULT(yes)
CPPFLAGS="$CPPFLAGS -DDEBUG_DMALLOC -DDMALLOC_FUNC_CHECK -I$ac_cv_dmalloc/include"
LDFLAGS="$LDFLAGS -L$ac_cv_dmalloc/lib"
LIBS="$LIBS -ldmalloc"
,AC_MSG_RESULT(no))
])dnl
