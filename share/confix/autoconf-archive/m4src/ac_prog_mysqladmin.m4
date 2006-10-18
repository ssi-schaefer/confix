dnl @synopsis AC_PROG_MYSQLADMIN
dnl
dnl Check for the program 'mysqladmin' let script continue if exists &
dnl works pops up error message if not.
dnl
dnl Testing of functionality is by invoking it with root password
dnl 'rootpass' and a 'flush-privileges' command.
dnl
dnl Besides checking mysql, this macro also set these environment
dnl variables upon completion:
dnl
dnl 	MYSQLADMIN = which mysqladmin
dnl     MYSQL_DATADIR = directory containing mysql database
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2003-01-09
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_MYSQLADMIN],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(MYSQLADMIN, mysqladmin$EXEEXT, nocommand)
if test "$MYSQLADMIN" = nocommand; then
	AC_MSG_ERROR([mysqladmin not found in $PATH])
fi
AC_MSG_CHECKING([if mysqladmin works])
if $MYSQLADMIN -u root -prootpass flush-privileges; then
	AC_MSG_RESULT([yes])
else
	AC_MSG_NOTICE([Before installation, set MySQL root password to rootpass; restore your root password afterwards.])
	AC_MSG_ERROR([mysqladmin cannot run with root password = rootpass])
fi
DATADIR_PATTERN='^|[[[:blank:]]]*datadir[[[:blank:]]]*|[[[:blank:]]]*\([[^[:blank:]]][[^[:blank:]]]*\)[[[:blank:]]]*|'
MYSQL_DATADIR=`$MYSQLADMIN -u root -prootpass variables 2> /dev/null | grep $DATADIR_PATTERN | sed "s/$DATADIR_PATTERN/\1/"`;dnl
])
