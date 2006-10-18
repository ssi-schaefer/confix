dnl @synopsis ACLTX_DVIPS_T_A4_LANDSCAPE
dnl
dnl check if dvips accept -t a4 -t landscape
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_DVIPS_T_A4_LANDSCAPE],[
AC_REQUIRE([ACLTX_DVIPS_T_A4])
ACLTX_DVIPS_T(a4,dvips_t_a4_landscape,on)
if test $dvips_t_a4_landscape = "no";
then
    AC_MSG_ERROR([Unable to find the -t a4 -t landscape option in dvips])
fi
])
