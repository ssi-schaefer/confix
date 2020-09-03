dnl @synopsis AC_PROG_SCP
dnl
dnl Check for the program 'scp', let script continue if exists, pops up
dnl error message if not.
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl     SCP = which scp
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_SCP],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(SCP, scp$EXEEXT, nocommand)
if test "$SCP" = nocommand; then
        AC_MSG_ERROR([scp not found in $PATH])
fi;dnl
])
