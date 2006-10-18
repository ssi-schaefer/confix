dnl @synopsis AC_PROG_CRONTAB
dnl
dnl Check for the program crontab, if exists let script continue, else
dnl pops an error message
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl     CRONTAB = which crontab
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_CRONTAB],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(CRONTAB, crontab$EXEEXT, nocommand)
if test "$CRONTAB" = nocommand; then
        AC_MSG_ERROR([crontab (needed for scheduled job) not found in $PATH])
fi;dnl
])
