dnl @synopsis AC_CHECK_MYSQL_DB
dnl
dnl Check if the specified MySQL database exists, if yes set your
dnl environment variable to that database name else unset your
dnl environment variable
dnl
dnl Example:
dnl
dnl     AC_CHECK_MYSQL_DB(DBNAME, [fishmarket])
dnl     if test x$DBNAME = xfishmarket; then
dnl         bla..bla..bla..
dnl     else
dnl         bla..bla..bla..
dnl     fi
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_CHECK_MYSQL_DB],[
AC_REQUIRE([AC_PROG_MYSQLSHOW])dnl
AC_MSG_CHECKING([for MySQL db $2])
if $MYSQLSHOW -u root -prootpass $2 > /dev/null 2>&1; then
        $1=$2
        AC_MSG_RESULT([yes])
else
        unset $1
        AC_MSG_RESULT([no])
fi;dnl
])
