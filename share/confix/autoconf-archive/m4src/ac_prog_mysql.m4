dnl @synopsis AC_PROG_MYSQL
dnl
dnl Check for the program 'mysql' let script continue if exists & works
dnl pops up error message if not.
dnl
dnl Testing of functionality is by invoking it with root password
dnl 'rootpass' and a 'SELECT * FROM user' SQL statement. That SQL
dnl statement will select all user information from the 'user'
dnl privileges table, and should work on every proper MySQL server.
dnl
dnl Besides checking mysql, this macro also set these environment
dnl variables upon completion:
dnl
dnl     MYSQL = which mysql
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_MYSQL],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(MYSQL, mysql$EXEEXT, nocommand)
if test "$MYSQL" = nocommand; then
        AC_MSG_ERROR([mysql not found in $PATH])
fi
AC_MSG_CHECKING([if mysql works])
if echo 'SELECT * FROM user' | $MYSQL -u root -prootpass mysql > /dev/null; then
        AC_MSG_RESULT([yes])
else
        AC_MSG_NOTICE([Before installation, set MySQL root password to rootpass; restore your root password afterwards.])
        AC_MSG_ERROR([mysql cannot execute SELECT with root password = rootpass])
fi;dnl
])
