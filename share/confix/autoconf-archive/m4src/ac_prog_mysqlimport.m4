dnl @synopsis AC_PROG_MYSQLIMPORT
dnl
dnl Check for the program 'mysqlimport', let script continue if exists,
dnl pops up error message if not.
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl     MYSQLIMPORT = which mysqlimport
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_MYSQLIMPORT],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(MYSQLIMPORT, mysqlimport$EXEEXT, nocommand)
if test "$MYSQLIMPORT" = nocommand; then
        AC_MSG_ERROR([mysqlimport not found in $PATH])
fi;dnl
])
