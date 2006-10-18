dnl @synopsis AC_VERY_NICE
dnl
dnl A macro to check the options of nice, in order to have a VERY_NICE
dnl variable which runs a program at the lowest priority VERY_NICE is
dnl undefined if we don't find the proper options, so you can safely
dnl use:
dnl
dnl   @VERY_NICE@ mycommand
dnl
dnl in a shell script.
dnl
dnl The VERY_NICE variable includes the placeholder NICE_VALUE that you
dnl have to instantiate at run-time. If you give a argument to
dnl AC_VERY_NICE, it will be used as an argument of nice for testing
dnl and included in VERY_NICE instead of the above placeholder.
dnl
dnl @category Misc
dnl @author Stephane Bortzmeyer <bortzmeyer@pasteur.fr>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([AC_VERY_NICE],[
if test "x$1" != "x"; then
  NICE_VALUE=$1
else
  NICE_VALUE=20
fi
AC_CHECK_PROGS(TEST_NICE, date)
AC_CHECK_PROGS(NICE, nice, )
AC_MSG_CHECKING(syntax of nice)
if test "x$NICE" != "x"; then
     if  ( $NICE -n $NICE_VALUE $TEST_NICE > /dev/null 2>&1 ) ;  then
        VERY_NICE="$NICE -n $NICE_VALUE"
     else
      if  ( $NICE -$NICE_VALUE $TEST_NICE > /dev/null 2>&1 ) ;  then
        VERY_NICE="$NICE -$NICE_VALUE"
      fi
     fi
fi
if test "x$1" = "x"; then
  VERY_NICE=`echo $VERY_NICE | sed "s/$NICE_VALUE/NICE_VALUE/"`
fi
AC_MSG_RESULT($VERY_NICE)
AC_SUBST(VERY_NICE)
])
