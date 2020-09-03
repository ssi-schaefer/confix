dnl @synopsis ACX_CHECK_PATHNAME_STYLE_DOS
dnl
dnl Check if host OS uses DOS-style pathnames. This includes the use of
dnl drive letters and backslashes. Under DOS, Windows, and OS/2,
dnl defines HAVE_PATHNAME_STYLE_DOS and PATH_SEPARATOR to ';'.
dnl Otherwise, defines PATH_SEPARATOR to ':'.
dnl
dnl This macro depends on the AC_CANONICAL_HOST.
dnl
dnl Use for enabling code to handle drive letters, backslashes in
dnl filenames and semicolons in the PATH.
dnl
dnl @category Misc
dnl @author Mark Elbrecht <snowball3@bigfoot.com>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([ACX_CHECK_PATHNAME_STYLE_DOS],
[AC_MSG_CHECKING(for Windows and DOS and OS/2 style pathnames)
AC_CACHE_VAL(acx_cv_pathname_style_dos,
[AC_REQUIRE([AC_CANONICAL_HOST])

acx_cv_pathname_style_dos="no"
case ${host_os} in
  *djgpp | *mingw32* | *emx*) acx_cv_pathname_style_dos="yes" ;;
esac
])
AC_MSG_RESULT($acx_cv_pathname_style_dos)
if test "$acx_cv_pathname_style_dos" = "yes"; then
  AC_DEFINE(HAVE_PATHNAME_STYLE_DOS,,[defined if running on a system with dos style paths])
  AC_DEFINE(PATH_SEPARATOR, ';')
else
  AC_DEFINE(PATH_SEPARATOR, ':')
fi
])
