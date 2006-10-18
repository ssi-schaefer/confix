dnl @synopsis MS_PROG_PGCLIENT()
dnl
dnl This macro searches for a program called 'pgclient'. If found the
dnl variable $pgclient is set to its path. Else it is set to 0. An
dnl option is added to the configure script for setting an search path
dnl instead of $PATH ($pgclient_dir). If pgclient is necessary for
dnl installing your program, you can do something like the following to
dnl stop configure with an error if pgclient wasn't found:
dnl
dnl       if test "x$pgclient" = "x0"; then AC_MSG_ERROR([We need that to setup the database!]); fi
dnl
dnl pgclient can be found at http://pgclient.freesources.org
dnl
dnl @category InstalledPackages
dnl @author Moritz Sinn <moritz@freesources.org>
dnl @version 2002-10-07
dnl @license GPLWithACException

AC_DEFUN([MS_PROG_PGCLIENT], [
AC_ARG_WITH(pgclient, [  --with-pgclient=DIR                    where to find pgclient (default: $PATH)], [pgclient_dir=$withval], [pgclient_dir=$PATH])
AC_PATH_PROG([pgclient], [pgclient], [0], $pgclient_dir)
])dnl
