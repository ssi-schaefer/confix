dnl @synopsis ACLTX_DVIPS_T_LETTER_LANDSCAPE
dnl
dnl check if dvips accept -t letter -t landscape
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_DVIPS_T_LETTER_LANDSCAPE],[
AC_REQUIRE([ACLTX_DVIPS_T_LETTER])
ACLTX_DVIPS_T(letter,dvips_t_letter_landscape,on)
if test $dvips_t_letter_landscape = "no";
then
    AC_MSG_ERROR([Unable to find the -t letter -t landscape option in dvips])
fi
])
