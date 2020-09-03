dnl @synopsis ACLTX_DVIPS_T(PAPERSIZE,VARIABLETOSET,[LANDSCAPE])
dnl
dnl check if dvips accept the PAPERSIZE option with optional LANDSCAPE
dnl and set VARIABLETOSET to yes or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_DVIPS_T],[
AC_REQUIRE([ACLTX_DEFAULT_CLASS])
AC_REQUIRE([ACLTX_PROG_DVIPS])
if test "$3" = "on" ;
then
_ac_latex_dvips_local=" -t landscape" ; export _ac_latex_dvips_local ;
else
_ac_latex_dvips_local=" " ; export _ac_latex_dvips_local ;
fi
AC_CACHE_CHECK([for option $dvips -t $1 $_ac_latex_dvips_local],[ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_]),[
_ACLTX_TEST([\documentclass{$defaultclass}
\begin{document}
Test
\end{document}],[],no)
cd conftest.dir/.acltx
[ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_])="no"; export [ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_]);
$dvips -o conftest.ps texput.dvi -t $1 $_ac_latex_dvips_local 2>error 1>/dev/null
cat error | grep "dvips: no match for papersize" 1>/dev/null 2>&1 || [ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_])="yes"; export [ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_])
cd ..
cd ..
echo "$as_me:$LINENO: executing $dvips -o conftest.ps texput.dvi -t $1 $_ac_latex_dvips_local" >&5
sed 's/^/| /' conftest.dir/.acltx/error >&5
rm -rf conftest.dir/.acltx
])
$2=$[ac_cv_dvips_t_]translit($1,[-],[_])[_]translit($3,[-],[_]); export $2;
AC_SUBST($2)
])
