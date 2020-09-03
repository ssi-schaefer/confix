dnl @synopsis ACLTX_DVIPS_O_STDOUT
dnl
dnl Check if dvips accept -o-
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_DVIPS_O_STDOUT],[
AC_REQUIRE([ACLTX_DEFAULT_CLASS])
AC_REQUIRE([ACLTX_PROG_DVIPS])
AC_CACHE_CHECK([for option -o- in dvips],ac_cv_dvips_o_stdout,[
_ACLTX_TEST([\documentclass{$defaultclass}
\begin{document}
Test
\end{document}],[],no)
cd conftest.dir/.acltx
ac_cv_dvips_o_stdout="no"; export ac_cv_dvips_o_stdout;
$dvips -o- texput.dvi   1>/dev/null 2>&1 && ac_cv_dvips_o_stdout="yes"; export ac_cv_dvips_o_stdout
cd ..
cd ..
echo "$as_me:$LINENO: executing $dvips -o- texput.dvi" >&5
rm -rf conftest.dir/.acltx
])
DVIPS_O_STDOUT=$ac_cv_dvips_o_stdout; export DVIPS_O_STDOUT;
if test $DVIPS_O_STDOUT = "no" ;
then
    AC_MSG_ERROR(Unable to find the option -o- in dvips)
fi
AC_SUBST(DVIPS_O_STDOUT)
])
