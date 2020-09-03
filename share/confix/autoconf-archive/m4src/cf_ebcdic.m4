dnl @synopsis CF_EBCDIC
dnl
dnl If the target character set is EBCDIC, defines variables
dnl cf_cv_ebcdic, EBCDIC, and NOT_ASCII.
dnl
dnl I originally wrote this and submitted it to the Lynx distribution.
dnl Editorial revisions by Tom Dickey, et. al.
dnl
dnl @category Misc
dnl @author Paul Gilmartin <pg@sweng.stortek.com>
dnl @version 2000-07-19
dnl @license GPLWithACException

dnl Check whether character set is EBCDIC.
AC_DEFUN([CF_EBCDIC],[
AC_MSG_CHECKING(if character set is EBCDIC)
AC_CACHE_VAL(cf_cv_ebcdic,[
        AC_TRY_COMPILE([ ],
[ /* TryCompile function for CharSet.
   Treat any failure as ASCII for compatibility with existing art.
   Use compile-time rather than run-time tests for cross-compiler
   tolerance.  */
#if '0'!=240
make an error "Character set is not EBCDIC"
#endif ],
[ # TryCompile action if true
cf_cv_ebcdic=yes ],
[ # TryCompile action if false
cf_cv_ebcdic=no])
# end of TryCompile ])
# end of CacheVal CvEbcdic
AC_MSG_RESULT($cf_cv_ebcdic)
case "$cf_cv_ebcdic" in  #(vi
    yes) AC_DEFINE(EBCDIC)
         AC_DEFINE(NOT_ASCII);; #(vi
    *)   ;;
esac
])dnl
