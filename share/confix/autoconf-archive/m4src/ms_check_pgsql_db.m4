dnl @synopsis MS_CHECK_PGSQL_DB([DB], [USER], [HOST], [PASSWORD], [ACTION_IF_FAILED], [ACTION_IF_OK])
dnl
dnl This macro checks wether we can connect to a PostgreSQL server with
dnl the given data. The macro MS_PROG_PGCLIENT is required by this one.
dnl The variable $pgclient_call is set for later use in Makefiles, if
dnl you'd like to make use of this, you must do
dnl
dnl     AC_SUBST(pgclient_call)
dnl
dnl after having called MS_CHECK_PGSQL_DB. You can then do something
dnl like the following in your Makefile.am:
dnl
dnl     @pgclient_call@ -f file.sql
dnl
dnl If you want the user to set the data, you should support something
dnl like these configure options:
dnl
dnl     AC_ARG_WITH(pgsql-host,
dnl             [  --with-pgsql-host=HOST               server is running on HOST @<:@local socket@:>@],
dnl             [pg_host=$withval], [pg_host=])
dnl
dnl     AC_ARG_WITH(pgsql-db,
dnl             [  --with-pgsql-db=DATABASE             use DATABASE @<:@tarantoola@:>@],
dnl             [pg_db=$withval], [pg_db=tarantoola])
dnl
dnl     AC_ARG_WITH(pgsql-user,
dnl             [  --with-pgsql-user=USER               use USER @<:@postgres@:>@],
dnl             [pg_user=$withval], [pg_user=postgres])
dnl
dnl     AC_ARG_WITH(pgsql-password,
dnl             [  --with-pgsql-password=PASSWORD       use PASSWORD @<:@none@:>@],
dnl             [pg_password=$withval], [pg_password=""])
dnl
dnl You can then call the macro like this:
dnl
dnl     MS_CHECK_PGSQL_DB([$pg_db], [$pg_user], [$pg_host], [$pg_password], [AC_MSG_ERROR([We need a database connection!])])
dnl
dnl @category InstalledPackages
dnl @author Moritz Sinn <moritz@freesources.org>
dnl @version 2002-09-25
dnl @license GPLWithACException

AC_DEFUN([MS_CHECK_PGSQL_DB], [
AC_REQUIRE([MS_PROG_PGCLIENT])
AC_MSG_CHECKING([for PostgreSQL db $1 (user: $2, host: $3)])

pgclient_call="$pgclient"

if test "x$1" != "x"; then
        pgclient_call="$pgclient_call dbname=$1";
fi
if test "x$2" != "x"; then
        pgclient_call="$pgclient_call user=$2";
fi
if test "x$3" != "x"; then
        pgclient_call="$pgclient_call host=$3";
fi
if test "x$4" != "x"; then
        pgclient_call="$pgclient_call password=$4";
fi

$pgclient_call -c 'SELECT 1' > /dev/null 2>&1
if test "x$?" = "x0"; then
        AC_MSG_RESULT([yes])
        $6
else
        AC_MSG_RESULT([no])
        $5
fi;
])dnl
