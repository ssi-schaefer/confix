dnl @synopsis MS_PGSQL_PRIV_ROOT(DB, USER, [HOST], [PASSWORD], [ACTION_IF_FAILED], [ACTION_IF_OK])
dnl
dnl This macro checks wether the given PostgreSQL user has root
dnl privileges (can create and drop databases) It is recommended to
dnl first call MS_CHECK_PGSQL_DB, this makes it easier to locate the
dnl cause of error. The macro MS_PROG_PGCLIENT is required by this one.
dnl
dnl The variable $pgclient_root_call is set for later use in Makefiles,
dnl if you'd like to make use of this, you must do
dnl
dnl     AC_SUBST(pgclient_root_call)
dnl
dnl after having called MS_CHECK_PGSQL_PRIV_ROOT. You can then do
dnl something like the following in your Makefile.am:
dnl
dnl     @pgclient_root_call@ -f file.sql
dnl
dnl If you want the user to set the data, you should support something
dnl like these configure options:
dnl
dnl     AC_ARG_WITH(pgsql-host,
dnl             [  --with-pgsql-host=HOST               server is running on HOST @<:@local socket@:>@],
dnl             [pg_host=$withval], [pg_host=])
dnl
dnl     AC_ARG_WITH(pgsql-db,
dnl             [  --with-pgsql-db=DBNAME               use database DBNAME @<:@test@:>@],
dnl             [pg_db=$withval], [pg_db=test])
dnl
dnl     AC_ARG_WITH(pgsql-root-user,
dnl             [  --with-pgsql-root-user=USER          use user USER, must have root (all) privileges @<:@postgres@:>@],
dnl             [pg_root_user=$withval], [pg_root_user=postgres])
dnl
dnl     AC_ARG_WITH(pgsql-password,
dnl             [  --with-pgsql-password=PASSWORD       use password PASSWORD @<:@none@:>@],
dnl             [pg_password=$withval], [pg_password=""])
dnl
dnl You can then call the macro like this:
dnl
dnl     MS_CHECK_PGSQL_PRIV_ROOT([$pg_db], [$pg_root_user], [$pg_host], [$pg_password], [AC_MSG_ERROR([We need root privileges on database!])])
dnl
dnl @category InstalledPackages
dnl @author Moritz Sinn <moritz@freesources.org>
dnl @version 2002-09-25
dnl @license GPLWithACException

AC_DEFUN([MS_CHECK_PGSQL_PRIV_ROOT], [
AC_REQUIRE([MS_PROG_PGCLIENT])dnl
AC_REQUIRE([MS_CHECK_PGSQL_DB])dnl
AC_MSG_CHECKING([if PostgreSQL user $2 has root privileges])

pgclient_root_call="$pgclient"

if test "x$1" != "x"; then
        pgclient_root_call="$pgclient_root_call dbname=$1";
fi
if test "x$2" != "x"; then
        pgclient_root_call="$pgclient_root_call user=$2";
fi
if test "x$3" != "x"; then
        pgclient_root_call="$pgclient_root_call host=$3";
fi
if test "x$4" != "x"; then
        pgclient_root_call="$pgclient_root_call password=$4";
fi

testdb="test`date +%s`"
echo "CREATE DATABASE $testdb; DROP DATABASE $testdb;" | $pgclient_root_call  > /dev/null 2>&1
if test "x$?" = "x0"; then
        AC_MSG_RESULT([yes])
        $6
else
        AC_MSG_RESULT([no])
        $5
fi;
])dnl
