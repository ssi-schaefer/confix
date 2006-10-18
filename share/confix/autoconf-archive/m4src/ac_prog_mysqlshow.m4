dnl @synopsis AC_PROG_MYSQLSHOW
dnl
dnl Check for the program 'mysqlshow' let script continue if exists &
dnl works pops up error message if not.
dnl
dnl Testing of functionality is by invoking it with root password
dnl 'rootpass'. If it works, it should show all databases currently in
dnl system.
dnl
dnl Besides checking mysql, this macro also set these environment
dnl variables upon completion:
dnl
dnl     MYSQLSHOW = which mysqlshow
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_MYSQLSHOW],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(MYSQLSHOW, mysqlshow$EXEEXT, nocommand)
if test "$MYSQLSHOW" = nocommand; then
        AC_MSG_ERROR([mysqlshow not found in $PATH])
fi
AC_MSG_CHECKING([if mysqlshow works])
if $MYSQLSHOW -u root -prootpass > /dev/null; then
        AC_MSG_RESULT([yes])
else
        AC_MSG_NOTICE([Before installation, set MySQL root password to rootpass; restore your root password afterwards.])
        AC_MSG_ERROR([mysqlshow cannot run with root password = rootpass])
fi;dnl
])
