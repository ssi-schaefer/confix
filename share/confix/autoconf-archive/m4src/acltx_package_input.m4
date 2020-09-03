dnl @synopsis ACLTX_PACKAGE_INPUT(PACKAGENAME,CLASSNAME,VARIABLETOSET)
dnl
dnl ...
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PACKAGE_INPUT],[
ACLTX_PACKAGE_LOCATION($1,$3_location)
if test "[$]$3_location" = "no" ; then
    AC_MSG_WARN([Unable to locate the $1.sty file])
    [ac_cv_latex_i_]translit($1,[-.],[__])[_]translit($2,[-],[_])="no";
else
if test "$[ac_cv_latex_class_]translit($2,[-],[_])" = "" ;
then
	ACLTX_CLASS($2,boretti_classesansparametre)
	export boretti_classesansparametre;
else
	boretti_classesansparametre=$[ac_cv_latex_class_]translit($2,[-],[_]) ;
	export boretti_classesansparemetre;
fi;
if test $boretti_classesansparametre = "no" ;
then
    AC_MSG_ERROR([Unable to find $2 class])
fi
AC_CACHE_CHECK([for usability of package $1 in class $2, using \\input instance of \\usepackage],[ac_cv_latex_i_]translit($1,[-.],[__])[_]translit($2,[-],[_]),[
_ACLTX_TEST([
\documentclass{$2}
\input $1
\begin{document}
\end{document}
],[ac_cv_latex_i_]translit($1,[-.],[__])[_]translit($2,[-],[_]))
])
fi
$3=$[ac_cv_latex_i_]translit($1,[-.],[__])[_]translit($2,[-],[_]); export $3;
AC_SUBST($3)
])
