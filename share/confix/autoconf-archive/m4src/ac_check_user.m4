dnl @synopsis AC_CHECK_USER
dnl
dnl Check if the specified UNIX user exists, if yes set your
dnl environment variable to that username else unset your environment
dnl variable
dnl
dnl Example:
dnl
dnl     AC_CHECK_USER(USER, [gleensalmon])
dnl     if test x$USER = xgleensalmon; then
dnl         bla..bla..bla..
dnl     else
dnl         bla..bla..bla..
dnl     fi
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl     USER_HOME = home directory of user, written in /etc/passwd
dnl
dnl @category Misc
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-04-11
dnl @license GPLWithACException

AC_DEFUN([AC_CHECK_USER],[
AC_MSG_CHECKING([for user $2])
if grep ^$2: /etc/passwd > /dev/null; then
        $1=$2
        USER_HOME=`grep ^$2: /etc/passwd | sed "s/^\([[^:]]*:\)\{5\}\([[^:]]*\):[[^:]]*$/\2/"`
        AC_MSG_RESULT([yes])
else
        unset $1
        unset USER_HOME
        AC_MSG_RESULT([no])
fi;dnl
])
