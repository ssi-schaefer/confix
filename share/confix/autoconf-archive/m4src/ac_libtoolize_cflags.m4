dnl @synopsis AC_LIBTOOLIZE_CFLAGS(COMPILER-FLAGS-VAR)
dnl
dnl Change the contents of variable COMPILER-FLAGS-VAR so that they are
dnl Libtool friendly, ie. prefix each of them with `-Xcompiler' so that
dnl Libtool doesn't remove them.
dnl
dnl @category Misc
dnl @author Ludovic Courtès <ludo@chbouib.org>
dnl @version 2004-09-07
dnl @license AllPermissive

AC_DEFUN([AC_LIBTOOLIZE_CFLAGS],
  [ac_libtoolize_ldflags_temp=""
   for i in $$1
   do
     ac_libtoolize_ldflags_temp="$ac_libtoolize_ldflags_temp -Xcompiler $i"
   done
   $1="$ac_libtoolize_ldflags_temp"])dnl
