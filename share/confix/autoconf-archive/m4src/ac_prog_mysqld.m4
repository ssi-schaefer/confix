dnl @synopsis AC_PROG_MYSQLD
dnl
dnl Check for the program 'mysqld' let script continue if exists &
dnl works pops up error message if not.
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl 	MYSQLD = which mysqld
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2003-01-09
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_MYSQLD],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(MYSQLD, mysqld$EXEEXT, nocommand)
if test "$MYSQLD" = nocommand; then
	AC_MSG_ERROR([mysqld not found in $PATH])
fi;dnl
])
