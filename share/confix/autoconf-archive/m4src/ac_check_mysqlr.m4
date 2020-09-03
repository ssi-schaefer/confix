dnl @synopsis AC_CHECK_MYSQLR
dnl
dnl First check if mysqlconfig exists. It fails if mysqlconfig is not
dnl in path. Then it checks for the libraries and replaces
dnl -lmysqlclient statement with -lmysqlclient_r statement, to enable
dnl threaded client library.
dnl
dnl The following are exported environment variables:
dnl
dnl   MYSQL_LIBS
dnl   MYSQL_CFLAGS
dnl
dnl @category InstalledPackages
dnl @author Can Bican <bican@yahoo.com>
dnl @version 2003-05-21
dnl @license AllPermissive

AC_DEFUN([AC_CHECK_MYSQLR],[
AC_PATH_PROG(mysqlconfig,mysql_config)
if test [ -z "$mysqlconfig" ]
then
    AC_MSG_ERROR([mysql_config executable not found])
else
    AC_MSG_CHECKING(mysql libraries)
    MYSQL_LIBS=`${mysqlconfig} --libs | sed -e \
    's/-lmysqlclient /-lmysqlclient_r /' -e 's/-lmysqlclient$/-lmysqlclient_r/'`
    AC_MSG_RESULT($MYSQL_LIBS)
    AC_MSG_CHECKING(mysql includes)
    MYSQL_CFLAGS=`${mysqlconfig} --cflags`
    AC_MSG_RESULT($MYSQL_CFLAGS)
fi
])
